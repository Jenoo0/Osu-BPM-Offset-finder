<p align="center">
  <img src="https://i.imgur.com/JEqQZKC.png" alt="osu! BPM & Offset Finder Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/osu!-Community%20Tool-ff66aa.svg" alt="osu! Community Tool">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB.svg" alt="Python 3.9+">
  <a href="https://github.com/Jenoo0/osu-bpm-finder/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT">
  </a>
</p>

An elegant, fast, and interactive desktop tool for the osu! mapping community to find the perfect BPM and optimal starting offsets for any song. No more tedious guessing in the editor!

---

## ✨ Features

* ⚡ **Precise BPM Analysis:** Calculates the exact BPM of your song (and automatically rounds it to the official osu! grid).
* 🔮 **Automatic Offset Suggestions:** Shows you the first 4 logical beat offsets in milliseconds—ready to be copied.
* 📊 **Interactive Waveform:** Visualizes the first 10 seconds of the song, including marked beat lines and a **live playhead** that moves smoothly synced to the music.
* 🎧 **Audio Double-Check:**
  * Listen to the intro (first 10 seconds) perfectly synced with the waveform.
  * Jump directly to the loudest part (**Peak**) of the song to quickly verify the timing during fast kicks/beats.
* 🎨 **Sleek Design:** Modern dark-mode interface in the signature osu! style, featuring the Comfortaa font and a pulsing loading logo.

---

## 🚀 Download & Installation (For Mappers)

You don't need Python installed to run this tool!

1. Go to the **Releases** section on the right side of this page.
2. Download the latest `osu-bpm-finder.zip`.
3. Extract the ZIP file to any folder on your PC.
4. Double-click the **`osu_BPM_Finder.exe`** inside the folder to start the app!

> ⚠️ **Note on Antivirus Alerts:** Since this is an unsigned, self-compiled executable, Windows Defender or your antivirus program (like Norton) might flag it as suspicious or perform a background scan on your first launch. This is a common false positive. You can safely allow or trust the file to run.

---

## 🛠️ For Developers (Local Setup)

If you want to run or modify the code yourself:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Jenoo0/osu-bpm-finder.git](https://github.com/Jenoo0/osu-bpm-finder.git)
   cd osu-bpm-finder