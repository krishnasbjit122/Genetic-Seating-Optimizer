from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Get absolute path for current dir (backend)
backend_dir = os.path.dirname(os.path.abspath(__file__))
# Add it to sys.path to find models and engine
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Import directly using sys.path
from models import Student, RoomConfig, GARequest, GAResult, SeatingSeat
from ga_engine import GeneticAlgorithm
from typing import List

app = FastAPI(title="Exam Seating Arrangement GA")

# Enable CORS (optional if on same origin, but useful for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.post("/generate-seating", response_model=GAResult)
async def generate_seating(request: GARequest):
    if not request.students:
        raise HTTPException(status_code=400, detail="No student data provided")
    
    engine = GeneticAlgorithm(
        students=request.students,
        room_config=request.room_config,
        pop_size=request.population_size,
        mutation_rate=request.mutation_rate,
        max_generations=request.generations
    )
    
    seating_plan, fitness_history, clashes = engine.run()
    
    return GAResult(
        seating_plan=seating_plan,
        fitness_history=fitness_history,
        best_fitness=fitness_history[-1],
        generation_count=len(fitness_history),
        clashes=clashes,
        room_config=request.room_config
    )

# --- Static File Serving ---
project_root = os.path.dirname(backend_dir)
dist_path = os.path.join(project_root, "frontend", "dist")

if os.path.exists(dist_path):
    # This catch-all serves assets or index.html
    @app.get("/{full_path:path}")
    async def serve_static(full_path: str):
        # 1. Search for existing file in dist root
        file_path = os.path.normpath(os.path.join(dist_path, full_path))
        
        # Security check to stay inside dist folder
        if not file_path.startswith(os.path.abspath(dist_path)):
            return FileResponse(os.path.join(dist_path, "index.html"))

        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # 2. Redirect everything else to index.html (SPA routing)
        return FileResponse(os.path.join(dist_path, "index.html"))

else:
    @app.get("/")
    async def root():
        return {
            "status": "ready",
            "info": "Frontend dist folder not found. Please run 'npm run build' in frontend folder."
        }

if __name__ == "__main__":
    import uvicorn
    # Important: when running with uvicorn directly, we don't need -m
    uvicorn.run(app, host="0.0.0.0", port=8000)
