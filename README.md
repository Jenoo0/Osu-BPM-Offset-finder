# 🎵 osu! BPM & Offset Finder

[![osu! Tool](https://img.shields.io/badge/osu!-Community_Tool-ff66aa?style=for-the-badge&logo=osu)](https://osu.ppy.sh/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Ein elegantes, schnelles und interaktives Desktop-Tool für die osu!-Mapping-Community, um die perfekte **BPM** und den optimalen **Start-Offset** für jeden Song zu finden. Kein lästiges Raten mehr im Editor!

---

## ✨ Features

* **⚡ Präzise BPM-Analyse:** Berechnet die exakte BPM deines Songs (und rundet sie direkt für das osu!-Grid).
* **⏱️ Automatische Offset-Vorschläge:** Zeigt dir die ersten 4 logischen Beat-Offsets in Millisekunden an – bereit zum Kopieren.
* **📊 Interaktive Waveform:** Visualisiert die ersten 10 Sekunden des Songs inklusive eingezeichneter Beat-Linien und einem **Live-Playhead**, der sich flüssig mit der Musik bewegt.
* **🎧 Audio-Gegenprobe:**
  * Hör dir das Intro (die ersten 10 Sek.) synchron mit der Waveform an.
  * Springe direkt zum lautesten Teil (**Peak**) des Songs, um das Timing bei schnellen Kicks/Beats zu überprüfen.
* **🎨 Edles Design:** Moderner Dark-Mode im typischen osu!-Style inklusive Comfortaa-Schriftart und einem pulsierenden Lade-Logo.

---

## 🚀 Download & Installation (Für Mapper)

Du musst kein Python installiert haben, um das Tool zu nutzen! 

1. Geh rechts auf **[Releases](https://github.com/Jenoo0/Osu-BPM-Offset-finder/releases)**.
2. Lade dir die neueste `osu-bpm-finder.zip` herunter.
3. Entpacke die ZIP-Datei an einem beliebigen Ort auf deinem PC.
4. Starte die **`main.exe`** (oder `osu_BPM_Finder.exe`). 
5. *Viel Spaß beim Mappen!*

---

## 💻 Für Entwickler (Lokales Setup)

Falls du das Tool selbst anpassen oder lokal über das Terminal starten willst:

### 1. Repository klonen
```bash
git clone [https://github.com/Jenoo0/Osu-BPM-Offset-finder.git](https://github.com/Jenoo0/Osu-BPM-Offset-finder.git)
cd Osu-BPM-Offset-finder