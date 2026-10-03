import threading, tempfile, os, uuid

def speak(text, lang="en"):
    threading.Thread(target=_speak, args=(text, lang), daemon=True).start()

def _speak(text, lang):
    try:
        if lang == "ta":                      # Tamil voice (needs internet)
            from gtts import gTTS
            import pygame
            f = os.path.join(tempfile.gettempdir(), f"ss_{uuid.uuid4().hex}.mp3")
            gTTS(text, lang="ta").save(f)
            pygame.mixer.init(); pygame.mixer.music.load(f); pygame.mixer.music.play()
        else:                                 # English voice (offline)
            import pyttsx3
            e = pyttsx3.init(); e.say(text); e.runAndWait()
    except Exception as ex:
        print("speak error:", ex)

def listen(lang, callback):
    """Mic -> text in a thread. callback(text, error)"""
    def run():
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as src:
                r.adjust_for_ambient_noise(src, 0.5)
                audio = r.listen(src, timeout=6, phrase_time_limit=12)
            callback(r.recognize_google(audio, language="ta-IN" if lang == "ta" else "en-US"), None)
        except Exception as ex:
            callback(None, str(ex) or "Could not understand")
    threading.Thread(target=run, daemon=True).start()
