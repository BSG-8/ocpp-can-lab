"""
Mapping functions that translate OCPP actions into CAN frames.

This is the NORMAL (non-anomalous) behavior.

Later, anomaly scenarios will modify, block, or tamper with these mappings.
"""

def ocpp_to_can(action, payload):
    """
    Convert an OCPP action into a CAN frame dictionary structure.

    Returns:
        {
            "id": arbitration_id,
            "data": [bytes...]
        }
    """
    if action == "MeterValues":
        # Example encoding:
        # energyWh -> 2 bytes
        # powerW   -> 2 bytes
        energy = payload.get("energyWh", 0)
        power = payload.get("powerW", 0)

        can_id = 0x200  # Example CAN ID for MeterValues

        data = [
            (energy >> 8) & 0xFF,
            energy & 0xFF,
            (power >> 8) & 0xFF,
            power & 0xFF
        ]

        return {"id": can_id, "data": data}

    if action == "Heartbeat":
        # Heartbeat → small diagnostic CAN frame
        return {"id": 0x100, "data": [0x01]}

    if action == "BootNotification":
        # Boot → system ready message
        return {"id": 0x101, "data": [0xAA]}

    # No mapping defined
    return None
