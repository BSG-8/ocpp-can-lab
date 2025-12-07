"""
Base scenario hook definitions.

Scenarios can override these methods to:
- modify OCPP action/payload before sending
- inspect/modify OCPP response
- modify CAN frame before sending
- observe CAN frame after sending
"""


from infra.logger import LOGGER




class ScenarioHooks:

    def log(self, message: str):
        """
        Convenience helper for scenarios.
        Writes a free-form message into scenario_log.jsonl.
        """
        LOGGER.log_scenario(message)






    def pre_ocpp(self, action, payload):
        """
        Called BEFORE sending OCPP to CSMS.
        You can modify action/payload here.
        """
        return action, payload

    def post_ocpp(self, action, payload, reply):
        """
        Called AFTER receiving CSMS reply.
        You can modify/log the reply here.
        """
        return reply

    def pre_can(self, can_frame):
        """
        Called BEFORE sending CAN frame.
        You can modify or drop (return None) the frame.
        """
        return can_frame

    def post_can(self, can_frame):
        """
        Called AFTER sending CAN frame.
        You can log or trigger extra behavior here.
        """
        pass
