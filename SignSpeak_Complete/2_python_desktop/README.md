# SignSpeak (Python desktop app)

## Setup (Windows)
1. Install Python 3.11 from python.org. TICK "Add python.exe to PATH". Restart Command Prompt.
2. In this folder:  pip install -r requirements.txt
   (If PyAudio fails:  pip install pipwin  then  pipwin install pyaudio)
3. Run:  python main.py      (or double-click run.bat)

## Use
- Live: show sign for 1 sec -> typed in Notepad. Speak / Mic / Undo / Save buttons.
- Teach: add your own hand sign or face expression (record 2.5 sec, repeat from other angles).
- Library: list, delete, sensitivity, export/import. Your data: data/custom_signs.json
- Tamil voice output + Mic need internet. English voice works offline.

## Make .exe
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --collect-all mediapipe --collect-all customtkinter main.py
(Play Store needs the web/PWA version, not Python.)
