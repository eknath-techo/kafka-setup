import asyncio
from webrtc_server import setup_webrtc_and_run

async def main():
    ip_address = "192.168.30.40"
    port = 9999
    camera_id = 2  # Change this to the appropriate camera ID
    await setup_webrtc_and_run(ip_address, port, camera_id)

if __name__ == "__main__":
    asyncio.run(main())
