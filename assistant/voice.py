import whisper
import pyaudio
import numpy as np
import webrtcvad
import struct

model = whisper.load_model("base")

def listen_to_voice(rate=16000, chunk_duration_ms=30, vad_aggressiveness=2):
    vad = webrtcvad.Vad(vad_aggressiveness)
    chunk_size = int(rate * chunk_duration_ms / 1000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                    input=True, frames_per_buffer=chunk_size)

    print("🎙️ [Voice Mode] Listening...")

    frames = bytearray()
    silence_threshold = 20
    silence_count = 0
    triggered = False

    try:
        while True:
            audio_chunk = stream.read(chunk_size)
            is_speech = vad.is_speech(audio_chunk, rate)

            if is_speech:
                triggered = True
                silence_count = 0
                frames.extend(audio_chunk)
            elif triggered:
                silence_count += 1
                if silence_count > silence_threshold:
                    print("🛑 [VAD] End of speech.")
                    break

        # Convert raw bytes to float32 numpy array for whisper
        audio_np = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        result = model.transcribe(audio_np)
        text = result["text"].strip()
        print(f"[Whisper] You said: {text}")
        return text

    except Exception as e:
        print(f"[Whisper Error] {e}")
        return ""

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()