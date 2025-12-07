from infra.scenario_base import ScenarioHooks

class Scenario(ScenarioHooks):
    """
    Base template for creating a scenario.
    
    HOW TO USE:
    - Override only the hooks you need.
    - Do NOT modify pipeline.py or ocpp_client.py.
    - Return modified data when needed.
    - Return None from pre_can() to DROP a CAN frame.
    """

    def pre_ocpp(self, action, payload):
        # Example:
        # payload["chargePointVendor"] = "HackedVendor"
        return action, payload

    def post_ocpp(self, action, payload, reply):
        # Example:
        # print("Received:", reply)
        return reply

    def pre_can(self, can_frame):
        # Example:
        # can_frame["data"] = [0xFF] * len(can_frame["data"])
        return can_frame

    def post_can(self, can_frame):
        # Example:
        # print("CAN sent:", can_frame)
        pass
