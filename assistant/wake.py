# assistant/wake.py
import os
import wave
import pyaudio
import json
from vosk import Model, KaldiRecognizer

class WakeWordListener:
    """
    Listens continuously for the phrase “hey karo” via Vosk.
    No monthly limits, runs fully offline.
    """
    def __init__(self, callback, model_path="/Volumes/My Passport for Mac/karo-main/vosk-models/vosk-model-small-en-us-0.15"):
        if not os.path.isdir(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}. "
                "Download from https://alphacephei.com/vosk/models and unpack."
            )
        self.callback = callback
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000, '["hey karo"]')

    def start(self):
        """Begin listening in a blocking loop. Call callback() when wake-word is heard."""
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)
        stream.start_stream()
        print("[Wake Word] Listening for “hey karo”… (via Vosk)")

        try:
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if self.rec.AcceptWaveform(data):
                    res = json.loads(self.rec.Result())
                    if res.get("text", "") == "hey karo":
                        print("[Wake Word] Detected “hey karo”!")
                        self.callback()
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()