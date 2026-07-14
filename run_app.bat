@echo off
start /min cmd /c "streamlit run app.py --server.headless true"
timeout /t 3 >nul
start chrome --app=http://localhost:8501
exit