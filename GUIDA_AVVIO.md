# 🚀 GUIDA COMPLETA AVVIO POC CrewAI + Vue.js

## ⚠️ PREREQUISITI
- Python 3.8+ installato
- Node.js 16+ installato  
- OpenAI API Key valida
- File `crew-ai-summarizer/transcript.srt` presente

---

## 📁 STEP 1: Setup Backend Python

### 1.1 Naviga nella cartella backend
```bash
cd crew-ai-summarizer/
```

### 1.2 Crea Virtual Environment
```bash
# Crea venv
python -m venv venv

# Verifica che sia creato
ls -la venv/
```

### 1.3 Attiva Virtual Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows (se usi Windows)
# venv\Scripts\activate
```

**✅ Verifica attivazione:** Il prompt dovrebbe mostrare `(venv)` all'inizio

### 1.4 Aggiorna pip (importante!)
```bash
pip install --upgrade pip
```

### 1.5 Installa dipendenze (risoluzione automatica conflitti)
```bash
pip install -r requirements.txt
```

**Se hai ancora errori di conflitto, prova l'installazione manuale:**
```bash
pip install fastapi uvicorn python-multipart
pip install crewai
```

### 1.6 Configura OpenAI API Key
```bash
# Esporta la tua API Key (SOSTITUISCI con quella vera!)
export OPENAI_API_KEY="sk-proj-your-actual-openai-api-key-here"

# Verifica che sia impostata
echo $OPENAI_API_KEY
```

### 1.7 Test Backend (Opzionale)
```bash
# Test diretto CrewAI
python main.py 00:01:30

# Dovrebbe creare mappa_concettuale_00-01-30.json
ls -la *.json
```

---

## 🌐 STEP 2: Avvio FastAPI Server

### 2.1 Avvia server (dalla cartella crew-ai-summarizer/)
```bash
python api_server.py
```

**✅ Output atteso:**
```
🌟 Avvio FastAPI Server per CrewAI Bridge
📍 Endpoint disponibili:
   - GET  /          (health check)
   - POST /generate-concept-map  (main endpoint)  
   - GET  /status    (debug info)
🔗 Server URL: http://localhost:8000
📖 Docs URL:  http://localhost:8000/docs

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2.2 Test API (nuovo terminale)
```bash
# Test health check
curl http://localhost:8000

# Test status
curl http://localhost:8000/status
```

**⚠️ IMPORTANTE: Lascia questo terminale aperto con FastAPI running!**

**🎉 NOVITÀ: Ora vedrai l'output di CrewAI in tempo reale in questo terminale quando viene chiamato dall'API!**

---

## 🖥️ STEP 3: Setup Frontend Vue.js

### 3.1 Apri NUOVO terminale
```bash
# Torna alla root del progetto (fuori da crew-ai-summarizer/)
cd ..
pwd
# Dovrebbe mostrare: /home/aldodecillis/wa/01_Aulab/00_Proof_Of_Concepts/Poc-CrewAi-Concept-Map
```

### 3.2 Installa dipendenze Vue.js
```bash
npm install
```

### 3.3 Avvia Vue.js Development Server
```bash
npm run dev
```

**✅ Output atteso:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## 🧪 STEP 4: Test Flusso Completo

### 4.1 Apri Browser
```bash
# Vai a:
http://localhost:5173
```

### 4.2 Apri Developer Tools
- **Chrome/Firefox:** F12 → Console tab
- **Safari:** Cmd+Opt+I → Console tab

### 4.3 Test del Flow
1. **▶️ Play Video** → Il video Wistia dovrebbe partire
2. **⏸️ Pausa Video** → Ferma il video a ~1:30 o quando vuoi
3. **📱 Click Button** → Premi **"Riassumi fino a XX:XX:XX"**
4. **👀 Monitora Console** → Dovresti vedere:

**✅ Console Output Atteso:**
```javascript
📅 Generazione mappa concettuale CrewAI per timestamp: 00:01:30
🤖 Chiamata CrewAI per timestamp: 00:01:30
✅ CrewAI completato con successo!
📄 File generato: mappa_concettuale_00-01-30.json
💬 Messaggio: Mappa concettuale generata fino al timestamp 00:01:30
```

### 4.4 Verifica Output
```bash
# Controlla che il file JSON sia stato creato
ls -la crew-ai-summarizer/*.json

# Visualizza contenuto (opzionale)
cat crew-ai-summarizer/mappa_concettuale_*-*-*.json
```

---

## 🔧 TROUBLESHOOTING

### ❌ Errore: "ModuleNotFoundError: crewai"
```bash
# Assicurati che venv sia attivato
source crew-ai-summarizer/venv/bin/activate
pip install crewai
```

### ❌ Errore: "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
echo $OPENAI_API_KEY  # verifica
```

### ❌ Errore: "Connection refused localhost:8000"
- FastAPI server non è running
- Riavvia: `python crew-ai-summarizer/api_server.py`

### ❌ Errore: "transcript.srt not found"
```bash
# Verifica che il file esista
ls -la crew-ai-summarizer/transcript.srt

# Se non c'è, copialo dalla cartella public/transcriptions/
cp public/transcriptions/glkoqys695.srt crew-ai-summarizer/transcript.srt
```

### ❌ CORS Errors nel browser
- Verifica che Vue.js usi porta 5173
- Se usi porta diversa, modifica `api_server.py` → `allow_origins`

---

## 📋 CHECKLIST FINALE
- [ ] Virtual environment attivato `(venv)`
- [ ] OPENAI_API_KEY configurata
- [ ] FastAPI server running su `:8000`
- [ ] Vue.js running su `:5173`
- [ ] File `transcript.srt` presente
- [ ] Browser DevTools aperto su Console
- [ ] Test click button completato con successo
- [ ] File JSON generato e visibile

---

## 🎯 STATO TERMINALI FINALI

**Terminale 1 - FastAPI:**
```bash
(venv) user@machine:~/Poc-CrewAi-Concept-Map/crew-ai-summarizer$ python api_server.py
INFO:     Uvicorn running on http://127.0.0.1:8000

# Quando fai click sul button Vue.js, vedrai qui:
📺 Output CrewAI in tempo reale:
==================================================
[CrewAI] 🎬 CrewAI Transcript Analyzer
[CrewAI] ==================================================
[CrewAI] 📁 Caricamento file SRT: transcript.srt
[CrewAI] ✅ File caricato correttamente (15432 caratteri)
[CrewAI] 🤖 Inizializzazione CrewAI...
[CrewAI] 🚀 Avvio analisi del transcript...
[CrewAI] [Specialista di Analisi del Contenuto] Starting task...
[CrewAI] [Esperto di Estrazione] Starting task...
[CrewAI] ✅ Mappa concettuale salvata in: mappa_concettuale_00-01-30.json
==================================================
🏁 CrewAI processo terminato con exit code: 0
```

**Terminale 2 - Vue.js:**
```bash
user@machine:~/Poc-CrewAi-Concept-Map$ npm run dev  
Local:   http://localhost:5173/
```

**Browser:** Console con log di successo CrewAI ✅

Il POC è ora completamente funzionante! 🚀