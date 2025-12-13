"""
Ghost Charge Attack Simulation - Backend
=========================================
EV şarj istasyonlarına yönelik "Hayalet Şarj" saldırısını simüle eder.

Mimari:
- FastAPI (Port 8000): Web UI + WebSocket
- CSMS (Port 9000): OCPP 1.6 WebSocket Server
- Virtual Meter: Fiziksel sayaç simülasyonu
- Charge Point: CSMS'e bağlanan istemci
"""

import asyncio
import uvicorn
import json
import logging
import websockets
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call, call_result
from ocpp.v16.enums import Action, RegistrationStatus, ChargePointStatus

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GhostCharge")

# ============================================================================
# KONFİGÜRASYON
# ============================================================================
CSMS_HOST = "127.0.0.1"
CSMS_PORT = 9000
WEB_PORT = 8000
CP_ID = "CP_001"

# ============================================================================
# GLOBAL STATE
# ============================================================================
class SimulationState:
    """Simülasyon durumu"""
    def __init__(self):
        self.is_running = False
        self.attack_mode = False
        self.physical_energy_kwh = 0.0
        self.reported_energy_kwh = 0.0
        self.energy_rate = 0.5  # kWh per second (simülasyon hızı)
        self.cp_connected = False
        
    def reset(self):
        self.physical_energy_kwh = 0.0
        self.reported_energy_kwh = 0.0

state = SimulationState()

# WebSocket connections
ui_websocket: Optional[WebSocket] = None
meter_to_cp_queue: asyncio.Queue = None
cp_instance = None  # Global CP instance

# ============================================================================
# UI İLETİŞİM FONKSİYONLARI
# ============================================================================
async def send_ui_log(source: str, message: str, log_type: str = "info"):
    """UI'a log mesajı gönder"""
    if ui_websocket:
        try:
            payload = {
                "type": "log",
                "source": source,
                "message": message,
                "log_type": log_type,
                "timestamp": datetime.now().isoformat()
            }
            await ui_websocket.send_text(json.dumps(payload))
        except Exception:
            pass
    logger.info(f"[{source}] {message}")

async def send_ui_data(data_type: str, value: float, extra: dict = None):
    """UI'a veri gönder"""
    if ui_websocket:
        try:
            payload = {
                "type": "data",
                "data_type": data_type,
                "value": value,
                "attack_mode": state.attack_mode,
                "timestamp": datetime.now().isoformat()
            }
            if extra:
                payload.update(extra)
            await ui_websocket.send_text(json.dumps(payload))
        except Exception:
            pass

async def send_ui_state():
    """UI'a durum bilgisi gönder"""
    if ui_websocket:
        try:
            payload = {
                "type": "state",
                "is_running": state.is_running,
                "attack_mode": state.attack_mode,
                "physical_energy": state.physical_energy_kwh,
                "reported_energy": state.reported_energy_kwh,
                "cp_connected": state.cp_connected
            }
            await ui_websocket.send_text(json.dumps(payload))
        except Exception:
            pass

# ============================================================================
# VİRTUAL METER (Fiziksel Sayaç Simülasyonu)
# ============================================================================
async def virtual_meter_loop():
    """Sanal elektrik sayacı - fiziksel tüketimi simüle eder"""
    global meter_to_cp_queue, cp_instance
    
    await send_ui_log("METER", "Sanal sayaç başlatıldı, komut bekleniyor...", "info")
    
    while True:
        if state.is_running:
            # Enerji üret
            state.physical_energy_kwh += state.energy_rate
            
            await send_ui_log(
                "METER", 
                f"⚡ Fiziksel tüketim: {state.physical_energy_kwh:.2f} kWh",
                "meter"
            )
            await send_ui_data("physical", state.physical_energy_kwh)
            
            # CP'ye gönder (eğer bağlıysa)
            if cp_instance and state.cp_connected:
                try:
                    await cp_instance.send_meter_value(state.physical_energy_kwh)
                except Exception as e:
                    logger.error(f"Meter send error: {e}")
            
            await asyncio.sleep(1.0)
        else:
            await asyncio.sleep(0.1)

# ============================================================================
# CSMS (Central System Management System) - PORT 9000
# ============================================================================
class SimulatedCSMS(cp):
    """OCPP 1.6 uyumlu CSMS simülasyonu"""
    
    @on(Action.boot_notification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        await send_ui_log(
            "CSMS",
            f"🖥️ CP bağlandı: {charge_point_vendor} - {charge_point_model}",
            "csms"
        )
        return call_result.BootNotification(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.heartbeat)
    async def on_heartbeat(self, **kwargs):
        return call_result.Heartbeat(current_time=datetime.utcnow().isoformat())

    @on(Action.status_notification)
    async def on_status_notification(self, connector_id, error_code, status, **kwargs):
        await send_ui_log("CSMS", f"📊 Status: Connector {connector_id} -> {status}", "csms")
        return call_result.StatusNotification()

    @on(Action.start_transaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        await send_ui_log("CSMS", f"🔌 Transaction başlatıldı: {id_tag}", "csms")
        return call_result.StartTransaction(
            transaction_id=1,
            id_tag_info={"status": "Accepted"}
        )

    @on(Action.stop_transaction)
    async def on_stop_transaction(self, meter_stop, timestamp, transaction_id, **kwargs):
        await send_ui_log("CSMS", f"🛑 Transaction durduruldu: {meter_stop} Wh", "csms")
        return call_result.StopTransaction(
            id_tag_info={"status": "Accepted"}
        )

    @on(Action.meter_values)
    async def on_meter_values(self, connector_id, meter_value, **kwargs):
        """Metre değerlerini al ve işle"""
        try:
            # OCPP mesajından değeri çıkar
            if isinstance(meter_value[0], dict):
                if 'sampled_value' in meter_value[0]:
                    val = meter_value[0]['sampled_value'][0]
                else:
                    val = meter_value[0]['sampledValue'][0]
                energy_wh = float(val.get('value', val.get('Value', 0)))
            else:
                energy_wh = float(meter_value[0].sampled_value[0].value)
            
            energy_kwh = energy_wh / 1000.0
            state.reported_energy_kwh = energy_kwh
            
            # Saldırı tespiti
            if state.attack_mode and state.physical_energy_kwh > 0:
                diff = state.physical_energy_kwh - energy_kwh
                await send_ui_log(
                    "CSMS",
                    f"💰 FATURA: {energy_kwh:.2f} kWh (Gerçek: {state.physical_energy_kwh:.2f} kWh, Kayıp: {diff:.2f} kWh)",
                    "attack"
                )
            else:
                await send_ui_log(
                    "CSMS",
                    f"💰 Raporlanan tüketim: {energy_kwh:.2f} kWh",
                    "csms"
                )
            
            await send_ui_data("reported", energy_kwh)
            
        except Exception as e:
            logger.error(f"CSMS MeterValues parse error: {e}")
        
        return call_result.MeterValues()

async def csms_connection_handler(websocket):
    """CSMS WebSocket bağlantı işleyici"""
    try:
        # Websockets version compatibility
        if hasattr(websocket, 'path'):
            path = websocket.path
        elif hasattr(websocket, 'request'):
            path = websocket.request.path
        else:
            path = "/CP_001"
        charge_point_id = path.strip('/')
        
        await send_ui_log("CSMS", f"📡 Bağlantı isteği: {charge_point_id}", "csms")
        
        csms_instance = SimulatedCSMS(charge_point_id, websocket)
        await csms_instance.start()
        
    except ConnectionClosed:
        await send_ui_log("CSMS", "❌ CP bağlantısı koptu", "error")
    except Exception as e:
        logger.error(f"CSMS connection error: {e}")

async def run_csms_server():
    """CSMS WebSocket sunucusunu başlat"""
    await send_ui_log("CSMS", f"🖥️ CSMS sunucusu başlatılıyor (Port {CSMS_PORT})...", "system")
    
    server = await websockets.serve(
        csms_connection_handler,
        CSMS_HOST,
        CSMS_PORT,
        subprotocols=["ocpp1.6"]
    )
    
    await send_ui_log("CSMS", f"✅ CSMS aktif: ws://{CSMS_HOST}:{CSMS_PORT}", "system")
    
    await server.wait_closed()

# ============================================================================
# CHARGE POINT (Şarj İstasyonu İstemcisi)
# ============================================================================
class SimulatedChargePoint(cp):
    """OCPP 1.6 uyumlu Charge Point simülasyonu"""
    
    def __init__(self, id, connection):
        super().__init__(id, connection)
        self.transaction_id = 1
        
    async def send_boot_notification(self):
        """Boot notification gönder"""
        await send_ui_log("CP", "📤 BootNotification gönderiliyor...", "cp")
        
        request = call.BootNotification(
            charge_point_model="GhostSim-2000",
            charge_point_vendor="SecurityLab"
        )
        response = await self.call(request)
        
        if response.status == RegistrationStatus.accepted:
            await send_ui_log("CP", "✅ CSMS tarafından kabul edildi", "cp")
            state.cp_connected = True
        else:
            await send_ui_log("CP", "❌ CSMS tarafından reddedildi", "error")

    async def send_meter_value(self, energy_kwh: float):
        """CSMS'e metre değeri gönder"""
        reported_kwh = energy_kwh
        
        # SALDIRI MODU
        if state.attack_mode:
            reported_kwh = 0.01  # Sahte değer
            await send_ui_log(
                "CP",
                f"🔴 SALDIRI! Gerçek: {energy_kwh:.2f} kWh → Sahte: {reported_kwh} kWh",
                "attack"
            )
        else:
            await send_ui_log(
                "CP",
                f"📊 MeterValue: {energy_kwh:.2f} kWh gönderiliyor",
                "cp"
            )
        
        energy_wh = int(reported_kwh * 1000)
        
        request = call.MeterValues(
            connector_id=1,
            transaction_id=self.transaction_id,
            meter_value=[{
                "timestamp": datetime.utcnow().isoformat(),
                "sampled_value": [{
                    "value": str(energy_wh),
                    "unit": "Wh",
                    "measurand": "Energy.Active.Import.Register"
                }]
            }]
        )
        
        try:
            await self.call(request)
        except Exception as e:
            logger.error(f"MeterValue send error: {e}")

async def run_charge_point():
    """Charge Point istemcisini çalıştır"""
    global cp_instance
    
    # CSMS'in başlamasını bekle
    await asyncio.sleep(2)
    
    while True:  # Reconnect loop
        await send_ui_log("CP", f"🔌 CSMS'e bağlanılıyor (ws://{CSMS_HOST}:{CSMS_PORT})...", "cp")
        
        try:
            async with websockets.connect(
                f"ws://{CSMS_HOST}:{CSMS_PORT}/{CP_ID}",
                subprotocols=["ocpp1.6"]
            ) as ws:
                cp_instance = SimulatedChargePoint(CP_ID, ws)
                
                # Boot notification'ı ayrı task olarak başlat
                async def boot_and_run():
                    await asyncio.sleep(0.5)  # start() biraz önce başlasın
                    await cp_instance.send_boot_notification()
                
                # Paralel çalıştır - start() mesaj routing için şart!
                await asyncio.gather(
                    cp_instance.start(),  # OCPP mesaj routing
                    boot_and_run()        # Boot notification gönder
                )
                
        except ConnectionRefusedError:
            await send_ui_log("CP", "❌ CSMS'e bağlanılamadı! Yeniden deneniyor...", "error")
            state.cp_connected = False
        except ConnectionClosed:
            await send_ui_log("CP", "⚠️ CSMS bağlantısı kapandı. Yeniden bağlanılıyor...", "error")
            state.cp_connected = False
        except Exception as e:
            logger.error(f"CP client error: {e}")
            await send_ui_log("CP", f"❌ Hata: {e}", "error")
            state.cp_connected = False
        
        cp_instance = None
        await asyncio.sleep(3)  # Reconnect delay

# ============================================================================
# FASTAPI UYGULAMASI
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama yaşam döngüsü"""
    global meter_to_cp_queue
    
    logger.info("=" * 50)
    logger.info("Ghost Charge Simulation Starting...")
    logger.info("=" * 50)
    
    # Queue oluştur
    meter_to_cp_queue = asyncio.Queue()
    
    # Background task'ları başlat
    tasks = [
        asyncio.create_task(run_csms_server()),
        asyncio.create_task(run_charge_point()),
        asyncio.create_task(virtual_meter_loop())
    ]
    
    yield
    
    # Cleanup
    logger.info("Shutting down...")
    for task in tasks:
        task.cancel()

app = FastAPI(
    title="Ghost Charge Simulation",
    description="EV Charging Station Attack Simulation",
    lifespan=lifespan
)

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Ana sayfa"""
    html_path = Path(__file__).parent / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """UI WebSocket endpoint"""
    global ui_websocket
    
    await websocket.accept()
    ui_websocket = websocket
    
    logger.info("UI WebSocket connected")
    
    # Başlangıç durumu gönder
    await send_ui_log("SYSTEM", "✅ Backend'e bağlandı", "system")
    await send_ui_log("SYSTEM", f"📡 CSMS: ws://{CSMS_HOST}:{CSMS_PORT}", "system")
    await send_ui_log("SYSTEM", f"🔌 CP ID: {CP_ID}", "system")
    await send_ui_state()
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "START":
                if not state.is_running:
                    state.reset()
                    state.is_running = True
                    await send_ui_log("SYSTEM", "▶️ Simülasyon BAŞLATILDI", "system")
                    await send_ui_state()
                    
            elif data == "STOP":
                if state.is_running:
                    state.is_running = False
                    await send_ui_log("SYSTEM", "⏹️ Simülasyon DURDURULDU", "system")
                    await send_ui_state()
                    
            elif data == "TOGGLE_ATTACK":
                state.attack_mode = not state.attack_mode
                status = "🔴 AKTİF" if state.attack_mode else "🟢 KAPALI"
                await send_ui_log("SYSTEM", f"⚠️ Saldırı Modu: {status}", "attack" if state.attack_mode else "system")
                await send_ui_state()
                
            elif data == "GET_STATE":
                await send_ui_state()
                
    except Exception as e:
        logger.warning(f"UI WebSocket error: {e}")
    finally:
        ui_websocket = None
        logger.info("UI WebSocket disconnected")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    print("\n" + "=" * 60)
    print("👻 GHOST CHARGE ATTACK SIMULATION")
    print("=" * 60)
    print(f"🌐 Web UI: http://127.0.0.1:{WEB_PORT}")
    print(f"🖥️ CSMS: ws://127.0.0.1:{CSMS_PORT}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=WEB_PORT,
        reload=False,
        log_level="warning"
    )
