import websockets
import asyncio
from pvrecorder import PvRecorder
import json

async def websocket_stream_connection(uri: str):
    async with websockets.connect(uri) as websocket:
        recorder = PvRecorder(device_index=0, frame_length=512)
        try:
            recorder.start()

            frames_per_chunk = int((5000000 / 1000) * 16000)
            audio_frames = []

            while True:

                while len(audio_frames) * 512 < frames_per_chunk:
                    frame = recorder.read()
                    audio_frames.extend(frame)

                
                data = {
                    "binary" : audio_frames
                }
                await websocket.send(json.dumps(data))
                
        except KeyboardInterrupt:
            recorder.stop()

        finally:
            recorder.delete()


if __name__ == '__main__':
    uri = "ws://localhost:8000"
    asyncio.run(websocket_stream_connection(uri=uri)) 
