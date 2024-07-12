import asyncio
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling
from av import VideoFrame

import fractions

class CustomVideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0

    async def recv(self):
        self.frame_count += 1
        print(f"Sending frame {self.frame_count}")
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read frame from camera")
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = self.frame_count
        video_frame.time_base = fractions.Fraction(1, 30)  # Use fractions for time_base
        return video_frame

async def run(pc, signaling):
    await signaling.connect()

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"Data channel established: {channel.label}")  # Print data channel establishment

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "connected":
            print("WebRTC connection established successfully")

    video_sender = CustomVideoStreamTrack()
    pc.addTrack(video_sender) # Add video track to peer connection

    offer = await pc.createOffer() # Create offer for session description
    await pc.setLocalDescription(offer) # Set local description
    await signaling.send(pc.localDescription)  # Send local description to remote peer

    while True:
        obj = await signaling.receive()   # Receive object from signaling server
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)  # Set remote description
            print("Remote description set")
        elif obj is None:
            print("Signaling ended")
            break

    # print("Keeping connection open and sending frames for 30 seconds...")
    # for i in range(30):
    #     await asyncio.sleep(1)
    #     try:
    #         frame = await video_sender.recv()
    #         if frame:
    #             print(f"Sent frame {i+1}")
    #         else:
    #             print(f"Failed to send frame {i+1}")
    #     except Exception as e:
    #         print(f"Error sending frame: {str(e)}")

    print("Closing connection")

async def main():
    signaling = TcpSocketSignaling("192.168.30.40", 9999)
    pc = RTCPeerConnection()
    
    try:
        await run(pc, signaling)
    finally:
        print("Closing peer connection")
        await pc.close()

if __name__ == "__main__":
    asyncio.run(main())