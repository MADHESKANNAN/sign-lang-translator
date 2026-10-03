# SignSpeak - Complete Package
Design: navy (#0a1030) + cyan (#68ebff) + violet (#c55fff), matches your S logo

| Folder | What | How to get it |
|---|---|---|
| 1_web_pwa_app | Website + PWA (+ Android + Windows wrapper) | steps A, B, C, D |
| 2_python_desktop | Python desktop software | steps E, F |

## A. Website (free, 2 minutes)
app.netlify.com/drop -> drag the 1_web_pwa_app folder -> you get an https link. Camera + mic work there.

## B. PWA (install on phone / PC)
Open the Netlify link in Chrome/Edge -> Install button (top right) or browser menu > Install app.
First load needs internet; AI models are cached for offline after that.

## C. Android app / Play Store
Easiest: pwabuilder.com -> paste your Netlify link -> Package for stores -> Android -> download .aab + signing key (keep safe).
Play Console (one-time $25) -> Create app -> upload .aab -> screenshots + privacy policy (camera processed on device only).
Test first: install the downloaded .apk on your phone.
Alternative (Android Studio + Node): put web files in a folder named www, then
  npm i @capacitor/core @capacitor/cli @capacitor/android
  npx cap init  (use capacitor.config.json)  ;  npx cap add android  ;  npx cap open android

## D. Windows software from web version
Easiest: Chrome/Edge > open Netlify link > Install = desktop app (mic works).
Real .exe: install Node.js, in 1_web_pwa_app run:  npm install  then  npm run build  -> dist\ (mic does not work in Electron).

## E. Python desktop - run
Install Python 3.11 (tick Add to PATH). In 2_python_desktop:
  pip install -r requirements.txt
  python main.py
## F. Python desktop - make .exe
Double-click build_exe.bat -> dist\SignSpeak\SignSpeak.exe

Your own logo: replace icon-192.png / icon-512.png (square PNG) in 1_web_pwa_app.
