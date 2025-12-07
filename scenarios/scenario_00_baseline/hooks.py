from infra.scenario_base import ScenarioHooks

class BaselineScenario(ScenarioHooks):
    """
    Baseline (normal behavior) scenario.
    This scenario does NOT modify traffic, only logs a start message.
    """

    def pre_ocpp(self, action, payload):
        # Log once at the beginning (first call)
        self.log(f"[baseline] pre_ocpp called for action={action}")
        return action, payload
