import pyttsx3
import speech_recognition as sr

def listen_to_voice() -> str:
    """Captures mic input and returns text using SpeechRecognition."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Voice Mode] Listening...")
        r.pause_threshold = 1 # seconds of non-speaking audio before a phrase is considered complete
        r.adjust_for_ambient_noise(source, duration=1) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"[Voice Mode] You said: {text}")
        return text
    except sr.UnknownValueError:
        print("[Voice Mode] Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"[Voice Mode] Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(text: str):
    """Uses pyttsx3 to read responses aloud."""
    print(f"\n[Voice Mode] Speaking: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Voice Mode] Error speaking: {e} (pyttsx3 might not be fully configured or available)")
        print("Please ensure you have a compatible text-to-speech engine installed on your system.")


