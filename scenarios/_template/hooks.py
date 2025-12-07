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
        # self.log(f"pre_ocpp called for action={action}")
        return action, payload

    def post_ocpp(self, action, payload, reply):
        # Example:
        # self.log(f"post_ocpp reply={reply}")
        return reply

    def pre_can(self, can_frame):
        # Example:
        # self.log(f"Modifying CAN frame: {can_frame}")
        return can_frame

    def post_can(self, can_frame):
        # Example:
        # self.log(f"CAN frame sent: {can_frame}")
        pass
