# ============================================
# ThaléOS Voice Engine - Speech to Text
# ============================================
import speech_recognition as sr

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"🗣️ Heard: {command}")
        return command
    except:
        return None

if __name__ == "__main__":
    listen_command()
