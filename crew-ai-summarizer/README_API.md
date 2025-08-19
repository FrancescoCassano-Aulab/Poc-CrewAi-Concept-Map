# Guida per Test del Flusso CrewAI + Vue.js

## 🚀 Setup Iniziale

### 1. Setup Python Environment
```bash
cd crew-ai-summarizer/

# Crea virtual environment
python -m venv venv

# Attiva venv
source venv/bin/activate  # Linux/Mac
# OPPURE
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Configura Variabili d'Ambiente
```bash
# Esporta OpenAI API Key (OBBLIGATORIA)
export OPENAI_API_KEY="sk-your-actual-openai-api-key-here"

# Verifica che sia impostata
echo $OPENAI_API_KEY
```

### 3. Test Backend Isolato (Opzionale)
```bash
# Test diretto CrewAI con timestamp
python main.py 00:01:30

# Dovrebbe creare: mappa_concettuale_00-01-30.json
```

## 🌐 Avvio Servizi

### 1. Avvia FastAPI Server
```bash
cd crew-ai-summarizer/
python api_server.py
```
**Output atteso:**
```
🌟 Avvio FastAPI Server per CrewAI Bridge
📍 Endpoint disponibili:
   - GET  /          (health check)
   - POST /generate-concept-map  (main endpoint)
   - GET  /status    (debug info)  
🔗 Server URL: http://localhost:8000
📖 Docs URL:  http://localhost:8000/docs
```

### 2. Avvia Vue.js Frontend (Terminal separato)
```bash
# Dalla root del progetto
npm run dev
```

## 🧪 Test del Flusso Completo

### 1. Apri Browser
- Vai a: `http://localhost:5173` (o porta indicata da Vite)

### 2. Test Flow
1. **Play Video** → Il video Wistia dovrebbe partire
2. **Pausa a Timestamp** → Ferma il video al momento desiderato (es. 00:01:30)
3. **Click Button** → Premi "Riassumi fino a XX:XX:XX"
4. **Verifica Console** → Apri DevTools e controlla console per log CrewAI

**Console Output Atteso:**
```javascript
📅 Generazione mappa concettuale CrewAI per timestamp: 00:01:30
🤖 Chiamata CrewAI per timestamp: 00:01:30
✅ CrewAI completato con successo!
📄 File generato: mappa_concettuale_00-01-30.json
💬 Messaggio: Mappa concettuale generata fino al timestamp 00:01:30
```

### 3. Verifica Output
- **File JSON**: Controllare che sia stato creato `crew-ai-summarizer/mappa_concettuale_XX-XX-XX.json`
- **Console Browser**: Log di successo senza errori
- **Console FastAPI**: Log delle richieste ricevute ed elaborate

## 🛠️ Troubleshooting

### Errore: API Key Mancante
```bash
export OPENAI_API_KEY="your-key-here"
```

### Errore: FastAPI Non Risponde
- Verificare che sia running su `http://localhost:8000`
- Testare health check: `curl http://localhost:8000`

### Errore: CORS
- Il server FastAPI è configurato per accettare chiamate da `localhost:5173`
- Se usi porta diversa, modifica `api_server.py` → `allow_origins`

### Errore: File SRT Non Trovato
- Assicurarsi che `crew-ai-summarizer/transcript.srt` esista
- Oppure modificare `srt_file_path` in `main.py`

## 📋 Checklist Test
- [ ] FastAPI server running su `:8000`
- [ ] Vue.js app running su `:5173`  
- [ ] OPENAI_API_KEY configurata
- [ ] File transcript.srt presente
- [ ] Browser DevTools aperto
- [ ] Click su "Riassumi fino a XX:XX:XX"
- [ ] File JSON generato con successo
- [ ] Console browser senza errori

## 🎯 Risultato Atteso
**Success Flow:**
```
Vue Button Click → FastAPI API (/generate-concept-map) → python main.py {timestamp} → JSON file creato
```

Il file JSON generato conterrà la mappa concettuale strutturata secondo il formato CrewAI esistente.