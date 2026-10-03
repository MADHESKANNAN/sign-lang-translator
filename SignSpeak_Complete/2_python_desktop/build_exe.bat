@echo off
python -m pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --name SignSpeak --icon icon.ico --add-data "assets;assets" --add-data "icon.ico;." --collect-all mediapipe --collect-all customtkinter main.py
echo Done. Open dist\SignSpeak\SignSpeak.exe
pause
