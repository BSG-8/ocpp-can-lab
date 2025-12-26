import time
from infra.scenario_base import ScenarioHooks

class Scenario(ScenarioHooks):
    """
    Scenario 11: MCU DoS (CAN Bus-Off Attack)
    
    Demonstrates a compromised MCU flooding the CAN bus with high-priority (ID 0x000)
    messages to cause a specific denial of service condition.
    """

    def __init__(self):
        super().__init__()
        self.attack_active = False
        self.start_time = time.time()
        self.flood_count = 0
        self.MAX_FLOOD = 500  # Number of flood messages to inject per legitimate message

    def pre_ocpp(self, action, payload):
        # Trigger attack after a delay or specific action (e.g., StartTransaction)
        if hasattr(self, 'start_time') and (time.time() - self.start_time > 5):
            if not self.attack_active:
                self.attack_active = True
                self.log("⚠️ Attack Triggered: Starting CAN Bus Flood!")
        
        return action, payload

    def pre_can(self, can_frame):
        """
        In this scenario, legitimate CAN frames are either dropped or
        drowned out by the flood of high-priority messages.
        """
        if self.attack_active:
            # Simulate flooding by logging massive activity and potentially blocking real traffic
            # In a real CAN interface, we would execute: can_bus.send(id=0x000, ...) repeatedly.
            
            # 1. Flood Simulation (Log Noise)
            self.flood_count += 1
            if self.flood_count % 50 == 0: # Log every 50th batch to avoid crashing terminal
                self.log(f"💥 FLOODING BUS: Injecting 0x000 frames... (Batch {self.flood_count})")
            
            # 2. Drop legitimate traffic to simulate "Bus-Off" or collision
            # Returning None drops the legitimate frame from the pipeline.
            # self.log(f"🛑 Dropped legitimate frame ID: {hex(can_frame.get('id', 0))}")
            return int(can_frame.get('id', 0)) == 0x000 # Only allow attack frames if we were generating them here

            # To make it more visual, we can inject a Fake Frame instead of just dropping
            # But the 'pre_can' hook is a filter for the *current* frame.
            # We will transform the legitimate frame into a generic high-priority attack frame
            
            can_frame['id'] = 0x000
            can_frame['data'] = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            return can_frame

        return can_frame

    def post_ocpp(self, action, payload, reply):
        return reply

    def post_can(self, can_frame):
        pass
