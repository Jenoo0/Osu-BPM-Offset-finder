import streamlit as st
import librosa
import numpy as np
import tempfile
import os
import plotly.graph_objects as go
import soundfile as sf
import base64

# 1. Website-Konfiguration
st.set_page_config(
    page_title="osu! BPM & Offset Finder",
    page_icon="🎵",
    layout="centered"
)

# 2. Styling (Edler Dark-Mode + Custom Fonts + Full-Logo Pulsar)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap');
    
    .main {
        background-color: #0f111a;
        color: #e6e6fa;
    }
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Comfortaa', sans-serif;
    }
    h1 {
        color: #ff66aa;
        text-align: center;
        text-shadow: 0 0 10px rgba(255, 102, 170, 0.5);
        font-family: 'Comfortaa', sans-serif;
        font-weight: 700;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #ff66aa;
        font-weight: bold;
    }
    code {
        color: #ff66aa !important;
        background-color: #1a1c28 !important;
    }

    /* --- ANIMATION & OPTIMIERUNG FÜR DEN FULL-LOGO PULSAR --- */
    @keyframes pulse-glow {
        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(255, 102, 170, 0.8);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 25px rgba(255, 102, 170, 0);
        }
        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(255, 102, 170, 0);
        }
    }

    .pulsar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 40px 0;
    }

    .pulsar-logo-frame {
        border-radius: 50%;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse-glow 1.5s infinite ease-in-out;
        box-shadow: 0 0 20px rgba(255, 102, 170, 0.5);
    }

    .pulsar-logo-frame img {
        display: block;
        width: 100%;
        height: auto;
        max-width: 150px;
    }

    .pulsar-text {
        margin-top: 25px;
        color: #ff66aa;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(255, 102, 170, 0.3);
    }
    
    audio {
        filter: invert(1) hue-rotate(180deg);
        width: 100%;
        height: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 osu! BPM & Offset Finder")
st.write("Lade deine .mp3-Datei hoch, um die perfekte BPM, Offsets und eine interaktive Waveform zu erhalten.")

# 3. File Uploader
uploaded_file = st.file_uploader("Wähle eine MP3-Datei aus", type=["mp3"])

if uploaded_file is not None:
    # Platzhalter für den Ladebildschirm
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        st.markdown("""
            <div class="pulsar-container">
                <div class="pulsar-logo-frame">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/1/1e/Osu%21_Logo_2016.svg" />
                </div>
                <div class="pulsar-text">Analysiere Audio und synchronisiere Waveform...</div>
            </div>
        """, unsafe_allow_html=True)

    # Temporäre Dateien vorbereiten
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    temp_intro_path = temp_path + "_intro.wav"
    temp_peak_path = temp_path + "_peak.wav"

    try:
        # Song laden
        y, sr = librosa.load(temp_path, sr=None)
        
        # BPM und Beats berechnen
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, start_bpm=150.0)

        if hasattr(tempo, "__len__"):
            bpm = tempo[0]
        else:
            bpm = tempo

        if bpm < 100:
            bpm = bpm * 2

        rounded_bpm = round(bpm)
        beat_times = librosa.frames_to_time(beat_frames[:4], sr=sr)

        # Audio-Ausschnitte erstellen
        y_intro = y[:int(sr * 10)]
        sf.write(temp_intro_path, y_intro, sr)

        # Peak finden
        hop_length = 512
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        window_size = int((10 * sr) / hop_length)
        
        if len(rms) > window_size:
            moving_avg = np.convolve(rms, np.ones(window_size)/window_size, mode='valid')
            best_start_frame = np.argmax(moving_avg)
            start_sample = best_start_frame * hop_length
            end_sample = start_sample + (10 * sr)
            y_peak = y[start_sample:end_sample]
        else:
            y_peak = y
            start_sample = 0
            
        sf.write(temp_peak_path, y_peak, sr)
        peak_start_time_sec = start_sample / sr

        # Beide Ausschnitte für die Player in Base64 konvertieren
        with open(temp_intro_path, "rb") as f:
            intro_audio_bytes = f.read()
        intro_audio_base64 = base64.b64encode(intro_audio_bytes).decode('utf-8')

        with open(temp_peak_path, "rb") as f:
            peak_audio_bytes = f.read()
        peak_audio_base64 = base64.b64encode(peak_audio_bytes).decode('utf-8')

        # Pulsar löschen
        loading_placeholder.empty()

        # --- ERGEBNISSE ANZEIGEN ---
        st.success("Analyse erfolgreich abgeschlossen!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Errechnete BPM", value=f"{bpm:.2f}")
        with col2:
            st.metric(label="osu! BPM (Gerundet)", value=f"{rounded_bpm}")

        # --- NATIVE STREAMLIT PLOTLY WAVEFORM ---
        st.write("### 📊 Interaktive Waveform (Erste 10 Sekunden)")
        
        duration_sec = 10
        y_10s = y[:int(sr * duration_sec)]
        times_10s = np.linspace(0, duration_sec, len(y_10s))

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=times_10s, 
            y=y_10s, 
            mode='lines',
            name='Audio-Welle',
            line=dict(color='#3a3f58', width=1),
            hoverinfo='skip'
        ))

        all_beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beats_in_10s = [b for b in all_beat_times if b <= duration_sec]

        for idx, beat_t in enumerate(beats_in_10s):
            fig.add_vline(
                x=beat_t, 
                line_width=2, 
                line_dash="dash", 
                line_color="#ff66aa",
                annotation_text=f"B{idx+1}",
                annotation_position="top"
            )

        # Der weiße Playhead
        fig.add_vline(
            x=0, 
            line_width=2.5, 
            line_color="#ffffff",
            name="playhead"
        )

        fig.update_layout(
            plot_bgcolor='#0f111a',
            paper_bgcolor='#0f111a',
            font=dict(color='#e6e6fa', family="Comfortaa"),
            xaxis=dict(title="Zeit (Sekunden)", showgrid=False, tickformat=".2f", range=[0, 10]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
            height=300,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True, key="my_plotly_chart")

        # --- DIE AUDIO-PLAYER ---
        st.write("### 🎧 Audio-Gegenprobe")
        
        minutes = int(peak_start_time_sec // 60)
        seconds = int(peak_start_time_sec % 60)
        
        # Beide Player nebeneinander, mit gedrosselter Frame-Rate fürs Zeichnen
        html_players = f"""
        <div style="display: flex; gap: 20px; justify-content: space-between; width: 100%;">
            <div style="flex: 1;">
                <p style="color: #e6e6fa; font-family: 'Comfortaa', sans-serif; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                    ⏱️ Die ersten 10 Sekunden (mit Live-Playhead):
                </p>
                <audio id="sync-audio-player" controls style="width: 100%; filter: invert(1) hue-rotate(180deg);">
                    <source src="data:audio/wav;base64,{intro_audio_base64}" type="audio/wav">
                </audio>
            </div>
            <div style="flex: 1;">
                <p style="color: #e6e6fa; font-family: 'Comfortaa', sans-serif; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                    🔥 Der Peak des Songs (ab {minutes:02d}:{seconds:02d}):
                </p>
                <audio id="peak-audio-player" controls style="width: 100%; filter: invert(1) hue-rotate(180deg);">
                    <source src="data:audio/wav;base64,{peak_audio_base64}" type="audio/wav">
                </audio>
            </div>
        </div>

        <script>
        const parentDoc = window.parent.document;
        let animationFrameId = null;

        function updatePlayhead() {{
            const audio = document.getElementById('sync-audio-player');
            const chartDiv = parentDoc.querySelector('[data-testid="stPlotlyChart"] div.js-plotly-plot');
            
            if (chartDiv && audio) {{
                // FPS-Begrenzung einrichten (60 FPS sind super smooth und schonen die CPU extrem)
                const fpsLimit = 60;
                const interval = 1000 / fpsLimit;
                let lastUpdateTime = 0;
                
                function renderLoop(timestamp) {{
                    if (!audio.paused && !audio.ended) {{
                        if (!lastUpdateTime) lastUpdateTime = timestamp;
                        const elapsed = timestamp - lastUpdateTime;

                        // Nur updaten, wenn genug Zeit vergangen ist
                        if (elapsed >= interval) {{
                            const currentTime = audio.currentTime;
                            const numShapes = chartDiv.layout.shapes ? chartDiv.layout.shapes.length : 0;
                            if (numShapes > 0) {{
                                const update = {{
                                    [`shapes[${{numShapes - 1}}].x0`]: currentTime,
                                    [`shapes[${{numShapes - 1}}].x1`]: currentTime
                                }};
                                window.parent.Plotly.relayout(chartDiv, update);
                            }}
                            lastUpdateTime = timestamp - (elapsed % interval);
                        }}
                    }}
                    animationFrameId = requestAnimationFrame(renderLoop);
                }}

                audio.addEventListener('play', () => {{
                    cancelAnimationFrame(animationFrameId);
                    lastUpdateTime = 0;
                    renderLoop(performance.now());
                }});

                audio.addEventListener('pause', () => {{
                    cancelAnimationFrame(animationFrameId);
                }});

                audio.addEventListener('seeked', () => {{
                    const currentTime = audio.currentTime;
                    const numShapes = chartDiv.layout.shapes ? chartDiv.layout.shapes.length : 0;
                    if (numShapes > 0) {{
                        const update = {{
                            [`shapes[${{numShapes - 1}}].x0`]: currentTime,
                            [`shapes[${{numShapes - 1}}].x1`]: currentTime
                        }};
                        window.parent.Plotly.relayout(chartDiv, update);
                    }}
                }});

                audio.addEventListener('ended', () => {{
                    cancelAnimationFrame(animationFrameId);
                    const numShapes = chartDiv.layout.shapes ? chartDiv.layout.shapes.length : 0;
                    if (numShapes > 0) {{
                        const update = {{
                            [`shapes[${{numShapes - 1}}].x0`]: 10.0,
                            [`shapes[${{numShapes - 1}}].x1`]: 10.0
                        }};
                        window.parent.Plotly.relayout(chartDiv, update);
                    }}
                }});
                
            }} else {{
                setTimeout(updatePlayhead, 500);
            }}
        }}
        updatePlayhead();
        </script>
        """
        st.components.v1.html(html_players, height=130)

        # --- OFFSETS ---
        st.write("### ⏱️ Mögliche Offsets (in Millisekunden):")
        st.write("Klicke rechts in den Boxen auf das Symbol, um den Wert direkt zu kopieren:")
        
        cols = st.columns(4)
        for i, time in enumerate(beat_times):
            offset_ms = int(time * 1000)
            with cols[i]:
                st.write(f"**Beat {i+1}**")
                st.code(f"{offset_ms}", language="text")

        # Hinweis-Text
        st.warning("""
        ⚠️ **Wichtiger Hinweis zum Offset:** Da MP3-Dateien minimale Verzögerungen am Anfang haben können und Musikstücke oft natürliche Rhythmus-Schwankungen besitzen, kann die automatische Analyse leicht abweichen.
        """)

    except Exception as e:
        loading_placeholder.empty()
        st.error(f"Fehler bei der Analyse: {e}")
    finally:
        for p in [temp_path, temp_intro_path, temp_peak_path]:
            if os.path.exists(p):
                os.remove(p)