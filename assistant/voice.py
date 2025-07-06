import whisper
import pyaudio
import webrtcvad
import wave
import collections
import tempfile
import numpy as np

model = whisper.load_model("base")

def record_with_vad(rate=16000, chunk_duration_ms=30, padding_duration_ms=300, vad_aggressiveness=2):
    vad = webrtcvad.Vad(vad_aggressiveness)
    chunk_size = int(rate * chunk_duration_ms / 1000)
    padding_chunks = int(padding_duration_ms / chunk_duration_ms)
    num_padding = padding_chunks
    ring_buffer = collections.deque(maxlen=padding_chunks)
    triggered = False

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                    input=True, frames_per_buffer=chunk_size)

    frames = []

    print("🎙️ [Voice Mode] Say something...")

    while True:
        chunk = stream.read(chunk_size)
        is_speech = vad.is_speech(chunk, rate)
        ring_buffer.append((chunk, is_speech))

        if not triggered:
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.9 * padding_chunks:
                triggered = True
                print("🟢 [VAD] Start speaking...")
                frames.extend([f for f, _ in ring_buffer])
                ring_buffer.clear()
        else:
            frames.append(chunk)
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > 0.9 * padding_chunks:
                print("🛑 [VAD] End of speech.")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save to WAV
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf = wave.open(temp_file.name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return temp_file.name

def listen_to_voice():
    try:
        audio_path = record_with_vad()
        result = model.transcribe(audio_path)
        text = result['text'].strip()
        print(f"[Whisper] You said: {text}")
        return text
    except Exception as e:
        print(f"[Whisper Error] {e}")
        return ""