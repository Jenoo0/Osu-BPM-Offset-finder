import librosa

# 1. Name deiner Musikdatei (muss im selben Ordner liegen!)
audio_file = "test.mp3"  # <-- Hier den genauen Namen deiner Datei eintragen!

print("Lade Song und analysiere... (Das kann ein paar Sekunden dauern)")

# 2. Song laden (sr=None lädt die Original-Abtastrate für bessere Qualität)
y, sr = librosa.load(audio_file, sr=None)

# 3. BPM und Beat-Zeitpunkte berechnen
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Das Tempo ist oft ein Array, wir holen uns den ersten Wert als Zahl
if hasattr(tempo, "__len__"):
    bpm = tempo[0]
else:
    bpm = tempo

# 4. Den allerersten erkannten Beat in Millisekunden umrechnen
first_beat_time = librosa.frames_to_time(beat_frames[0], sr=sr)
offset_ms = first_beat_time * 1000

# 5. Ergebnis im Terminal ausgeben
print("\n--- ANALYSE FERTIG ---")
print(f"Empfohlene BPM: {bpm:.2f}")
print(f"Empfohlenes Offset: {offset_ms:.0f} ms")
print("----------------------")