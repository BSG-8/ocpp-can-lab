from infra.scenario_base import ScenarioHooks

class BaselineScenario(ScenarioHooks):
    """
    Baseline (normal behavior) scenario.
    This scenario does NOT modify anything.
    All hooks call the parent class which returns data unchanged.
    """

    pass  # No changes needed; inherits everything from ScenarioHooks
