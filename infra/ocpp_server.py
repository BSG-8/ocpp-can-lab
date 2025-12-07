import asyncio
import websockets

CSMS_HOST = "localhost"
CSMS_PORT = 9000


async def handle_client(websocket):
    print(f"[CSMS] New connection from {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"[CSMS] Received: {message}")
            await websocket.send('{"status": "Accepted"}')
    except websockets.ConnectionClosed:
        print("[CSMS] Connection closed")


async def main():
    print(f"[CSMS] Starting server on ws://{CSMS_HOST}:{CSMS_PORT}")
    async with websockets.serve(handle_client, CSMS_HOST, CSMS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
