"""
FastAPI Bridge Server per integrare Vue.js con CrewAI
Riceve timestamp da frontend e lancia elaborazione CrewAI
"""

import os
import subprocess
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

# Modelli di input/output per l'API
class ConceptMapRequest(BaseModel):
    timestamp: str  # Formato "HH:MM:SS" 
    video_id: str   # ID del video Wistia
    
class ConceptMapResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    error_details: Optional[str] = None

# Inizializzazione FastAPI
app = FastAPI(
    title="CrewAI Concept Map Generator",
    description="API Bridge tra Vue.js e CrewAI per generazione mappe concettuali",
    version="1.0.0"
)

# Configurazione CORS per permettere chiamate da Vue.js (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "CrewAI API Bridge is running", "status": "OK"}

@app.post("/generate-concept-map", response_model=ConceptMapResponse)
async def generate_concept_map(request: ConceptMapRequest):
    """
    Endpoint principale per generare mappe concettuali
    
    - Riceve timestamp e video_id dal frontend Vue.js
    - Lancia script CrewAI main.py con timestamp come parametro
    - Restituisce success/error status
    """
    
    try:
        print(f"📨 Richiesta ricevuta: timestamp={request.timestamp}, video_id={request.video_id}")
        
        # Validazione basic del formato timestamp (HH:MM:SS)
        if not _is_valid_timestamp(request.timestamp):
            raise HTTPException(
                status_code=400, 
                detail=f"Formato timestamp non valido: {request.timestamp}. Usa HH:MM:SS"
            )
        
        # Path del script CrewAI main.py (stesso directory di questo file)
        script_path = Path(__file__).parent / "main.py"
        
        if not script_path.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Script CrewAI non trovato: {script_path}"
            )
        
        # Costruzione comando per eseguire CrewAI con timestamp
        # Formato: python main.py 00:01:30
        cmd = [sys.executable, str(script_path), request.timestamp]
        
        print(f"🚀 Esecuzione comando: {' '.join(cmd)}")
        print("📺 Output CrewAI in tempo reale:")
        print("=" * 50)
        
        # Esecuzione script CrewAI con subprocess.Popen per output real-time
        # stdout=PIPE per catturare output, stderr=STDOUT per unire stderr con stdout
        # text=True per output come stringa, bufsize=1 per line buffering
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Unisce stderr con stdout
            text=True,
            bufsize=1,  # Line buffering per output immediato
            cwd=str(script_path.parent)
        )
        
        # Buffer per raccogliere tutto l'output (per API response)
        full_output = []
        
        # Stream e stampa output in tempo reale
        try:
            # Leggi output line by line mentre il processo è running
            while True:
                line = process.stdout.readline()
                if not line:
                    # Se non ci sono più linee, controlla se processo è finito
                    if process.poll() is not None:
                        break
                    continue
                
                # Rimuovi newline finale per clean printing
                clean_line = line.rstrip()
                if clean_line:  # Solo se la linea non è vuota
                    print(f"[CrewAI] {clean_line}")  # Prefisso per identificare output CrewAI
                    full_output.append(line)
            
            # Aspetta che il processo finisca e ottieni return code
            return_code = process.wait(timeout=300)  # 5 minuti timeout
            
        except subprocess.TimeoutExpired:
            print("⏰ Timeout raggiunto, terminando processo CrewAI...")
            process.terminate()
            process.wait()
            raise subprocess.TimeoutExpired(cmd, 300)
        
        print("=" * 50)
        print(f"🏁 CrewAI processo terminato con exit code: {return_code}")
        
        # Crea oggetto result compatibile con il codice esistente
        class MockResult:
            def __init__(self, returncode, stdout, stderr=""):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr
        
        result = MockResult(
            returncode=return_code,
            stdout="".join(full_output),
            stderr=""
        )
        
        # Check se processo terminato con successo
        if result.returncode == 0:
            # Successo: cerca il file JSON generato
            expected_filename = f"mappa_concettuale_{request.timestamp.replace(':', '-')}.json"
            json_file_path = script_path.parent / expected_filename
            
            if json_file_path.exists():
                print(f"✅ Mappa concettuale generata con successo: {expected_filename}")
                return ConceptMapResponse(
                    success=True,
                    message=f"Mappa concettuale generata fino al timestamp {request.timestamp}",
                    filename=expected_filename
                )
            else:
                # Script completato ma file non trovato
                print(f"⚠️ Script completato ma file non trovato: {expected_filename}")
                return ConceptMapResponse(
                    success=False,
                    message="Script completato ma file JSON non generato",
                    error_details=result.stdout + result.stderr
                )
        else:
            # Errore durante esecuzione script
            error_msg = f"CrewAI script fallito (exit code: {result.returncode})"
            print(f"❌ {error_msg}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            
            return ConceptMapResponse(
                success=False,
                message=error_msg,
                error_details=f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )
            
    except subprocess.TimeoutExpired:
        error_msg = "Timeout: CrewAI script ha superato i 5 minuti di elaborazione"
        print(f"⏰ {error_msg}")
        return ConceptMapResponse(
            success=False,
            message=error_msg,
            error_details="Processo interrotto per timeout (>5 minuti)"
        )
        
    except Exception as e:
        error_msg = f"Errore interno del server: {str(e)}"
        print(f"💥 {error_msg}")
        return ConceptMapResponse(
            success=False,
            message=error_msg,
            error_details=str(e)
        )

def _is_valid_timestamp(timestamp: str) -> bool:
    """
    Validazione formato timestamp HH:MM:SS
    Accetta anche MM:SS (verrà gestito da CrewAI)
    """
    import re
    # Pattern per HH:MM:SS o MM:SS  
    pattern = r'^(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})$'
    return bool(re.match(pattern, timestamp))

# Endpoint di utilità per debug
@app.get("/status")
def get_status():
    """Status endpoint per debug"""
    script_path = Path(__file__).parent / "main.py"
    return {
        "api_server": "running",
        "crewai_script_exists": script_path.exists(),
        "working_directory": str(Path(__file__).parent),
        "openai_api_key_set": bool(os.getenv("OPENAI_API_KEY"))
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🌟 Avvio FastAPI Server per CrewAI Bridge")
    print("📍 Endpoint disponibili:")
    print("   - GET  /          (health check)")
    print("   - POST /generate-concept-map  (main endpoint)")
    print("   - GET  /status    (debug info)")
    print("🔗 Server URL: http://localhost:8000")
    print("📖 Docs URL:  http://localhost:8000/docs")
    print("\n⚠️  Assicurati che OPENAI_API_KEY sia impostata come variabile d'ambiente!")
    
    # Avvio server su porta 8000
    uvicorn.run(
        "api_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-reload durante sviluppo
        log_level="info"
    )