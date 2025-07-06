import whisper
import pyaudio
import numpy as np
import webrtcvad
import struct
import simpleaudio as sa
import sounddevice as sd
from TTS.api import TTS

# Load Whisper model once
model = whisper.load_model("base")

# Load Coqui TTS model once
try:
    tts_model = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
except Exception as e:
    print(f"[Voice] ❌ Error loading TTS model: {e}")
    tts_model = None

# Global for interrupting playback
_current_stream = None

def listen_to_voice(rate=16000, chunk_duration_ms=30, vad_aggressiveness=2):
    """Capture voice input with VAD and transcribe using Whisper."""
    global _current_stream
    # Stop any ongoing playback when user starts speaking
    if _current_stream:
        _current_stream.abort()
        _current_stream = None

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

def speak(text: str):
    """Convert text to speech using Coqui TTS and stream audio."""
    global _current_stream
    print(f"🗣️ [Voice] Karo says: {text}")
    if not tts_model:
        print("[Voice] TTS model unavailable.")
        return

    try:
        # Get numpy waveform from Coqui
        wav = tts_model.tts(text=text)
        sr = tts_model.synthesizer.output_sample_rate

        # Stop previous stream if active
        if _current_stream:
            _current_stream.abort()

        # Callback to feed chunks
        pointer = 0
        def callback(outdata, frames, time, status):
            nonlocal pointer
            chunk = wav[pointer:pointer+frames]
            if len(chunk) < frames:
                outdata[:len(chunk),0] = chunk
                raise sd.CallbackStop()
            outdata[:,0] = chunk
            pointer += frames

        # Open output stream
        _current_stream = sd.OutputStream(samplerate=sr, channels=1, callback=callback)
        with _current_stream:
            sd.sleep(int(len(wav)/sr*1000) + 100)  # wait until done

    except Exception as e:
        print(f"[Voice] ❌ Error during streaming speak: {e}")