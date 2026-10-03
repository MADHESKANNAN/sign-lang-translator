# SignSpeak - build guide

## 1. PWA (phone + PC)  -> needs HTTPS (camera + service worker)
1. Go to https://app.netlify.com/drop and drag this whole `signspeak` folder.
2. Open the https link in Chrome. Click "Install" (or menu > Install app).
3. First run needs internet (AI models cache for offline use).

## 2. Windows software (.exe)
Option A (easiest): open the Netlify link in Chrome/Edge > Install. It becomes a desktop app (voice typing works).
Option B (real .exe): install Node.js (nodejs.org), then in this folder:
  npm install
  npm start          (test)
  npm run build      (creates dist\SignSpeak Setup.exe)
Note: voice typing (mic) doesn't work in Electron; hand/face/notepad/speak work.

## 3. Google Play Store
1. Host on Netlify (step 1) -> you get https://yourname.netlify.app
2. Go to https://www.pwabuilder.com , paste the link, Package for stores > Android.
3. Download the generated .aab + signing key (KEEP the key safe).
4. Play Console (https://play.google.com/console, one-time $25) > Create app > upload .aab.
5. Add screenshots, description, privacy policy (say: camera used on-device only, no data uploaded).
