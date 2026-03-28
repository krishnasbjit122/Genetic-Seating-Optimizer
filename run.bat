@echo off
setlocal

echo 🧬 Starting Seating Arrangement Project (Unified Server)...
echo.

:: Check for node_modules in frontend
if not exist "frontend\node_modules" (
    echo [1/4] Installing frontend dependencies (npm install)...
    cd frontend && npm install && cd ..
)

echo [2/4] Installing backend dependencies (pip install)...
pip install -r backend\requirements.txt

echo [3/4] Building frontend assets (minified bundle)...
cd frontend && npm run build && cd ..

echo [4/4] Launching Unified Server (FastAPI)...
echo.
echo ==================================================
echo URL: http://localhost:8000
echo ==================================================
echo.

:: Run backend
cd backend
python main.py

pause
