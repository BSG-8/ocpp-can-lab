import can
import threading
import time

CHANNEL = "vcan0"
BUSTYPE = "socketcan"

def receiver():
    bus = can.interface.Bus(channel=CHANNEL, bustype=BUSTYPE)
    print("[RX] Listening on vcan0...")
    for msg in bus:
        print("[RX]", msg)

def sender():
    time.sleep(1)  # allow receiver to start
    bus = can.interface.Bus(channel=CHANNEL, bustype=BUSTYPE)
    msg = can.Message(arbitration_id=0x123, data=[1, 2, 3], is_extended_id=False)
    bus.send(msg)
    print("[TX] Sent:", msg)

if __name__ == "__main__":
    rx_thread = threading.Thread(target=receiver, daemon=True)
    rx_thread.start()

    sender()

    time.sleep(2)
    print("[TEST] Finished.")
