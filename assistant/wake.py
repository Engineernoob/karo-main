import pvporcupine
import pyaudio
import struct
import os

class WakeWordListener:
    def __init__(self, access_key: str, keyword_paths: list[str]):
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.access_key = access_key
        self.keyword_paths = keyword_paths

    def start(self, callback):
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=self.keyword_paths
            )

            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            print("\n[Wake Word] Listening for \"Hey Karo\"...")
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    print("[Wake Word] Wake word detected!")
                    callback()

        except Exception as e:
            print(f"[Wake Word] Error: {e}")
            print("Please ensure you have a valid Picovoice AccessKey and the correct keyword file paths.")
            print("You can get a free AccessKey from the Picovoice Console: https://console.picovoice.ai/")
            print("For testing purposes, you can temporarily disable wake word and use --voice flag directly.")

        finally:
            self.stop()

    def stop(self):
        if self.porcupine is not None:
            self.porcupine.delete()
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.pa is not None:
            self.pa.terminate()

# Placeholder for keyword path - replace with your actual .ppn file path
# KEYWORD_PATH = os.path.join(os.path.dirname(__file__), "hey-karo_en_mac_v2_1_0.ppn")
# ACCESS_KEY = "YOUR_PICOVOICE_ACCESS_KEY"

# Example usage (for testing, will be integrated into app.py)
# if __name__ == "__main__":
#     def on_wake_word():
#         print("Wake word callback triggered!")
#
#     if os.path.exists(KEYWORD_PATH) and ACCESS_KEY != "YOUR_PICOVOICE_ACCESS_KEY":
#         listener = WakeWordListener(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])
#         listener.start(on_wake_word)
#     else:
#         print("Wake word not configured. Please set ACCESS_KEY and KEYWORD_PATH in assistant/wake.py")