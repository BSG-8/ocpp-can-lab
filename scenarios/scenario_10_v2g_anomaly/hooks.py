from infra.scenario_base import ScenarioHooks

class Scenario09(ScenarioHooks):
    def __init__(self):
        self.attack_active = True

    def pre_ocpp(self, action, payload):
        # self: Pipeline instance
        if self.attack_active and payload.get('direction') == 'Import':
            self.log("V2G Deşarj Anomalisi: Import -> Export manipülasyonu (10kW)")
            payload['direction'] = 'Export'
            payload['power_w'] = 10000
            payload['label'] = 'anomaly'
        return action, payload

    def post_ocpp(self, action, payload, reply):
        # self.log("post_ocpp çağrıldı")
        return reply

    def pre_can(self, can_frame):
        # self.log("pre_can çağrıldı")
        return can_frame

    def post_can(self, can_frame):
        # self.log("post_can çağrıldı")
        pass
