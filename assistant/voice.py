import whisper
import pyaudio
import wave
import tempfile

model = whisper.load_model("base")  # You can also use "tiny", "small", "medium", "large"

def listen_to_voice() -> str:
    print("🎙️ [Voice Mode] Listening with Whisper...")

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5  # You can increase for longer input
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    print("🟢 Recording...")
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("🛑 Done recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(temp_wav.name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Transcribe with Whisper
    result = model.transcribe(temp_wav.name)
    print(f"[Whisper] You said: {result['text']}")
    return result["text"].strip()