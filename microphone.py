from pvrecorder import PvRecorder
import wave
import struct
from datetime import datetime

def realtime_microphone():
    recorder = PvRecorder(device_index=0, frame_length=512)

    audio = []
    try:
        recorder.start()
        while True:
            frame = recorder.read()
            audio.extend(frame)
            
    except KeyboardInterrupt:
        recorder.stop()
        with wave.open(f"{datetime.now()}.wav", 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))

    finally:
        recorder.delete()