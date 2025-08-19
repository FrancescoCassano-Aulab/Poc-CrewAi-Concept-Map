"""
CrewAI Transcript Analyzer
Genera mappe concettuali strutturate in JSON da file SRT di video transcript
"""

import re
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from crewai import Agent, Crew, Task, Process

# Configurazione API Keys - DEVONO essere impostate come variabili d'ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Inserisci la tua OpenAI API key

class SRTProcessor:
    """Utility class per processare file SRT e gestire timestamp"""
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> timedelta:
        """Converte timestamp formato HH:MM:SS in timedelta"""
        try:
            # Supporta formati: HH:MM:SS o MM:SS
            parts = timestamp_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return timedelta(hours=hours, minutes=minutes, seconds=seconds)
            elif len(parts) == 2:
                minutes, seconds = map(int, parts)
                return timedelta(minutes=minutes, seconds=seconds)
            else:
                raise ValueError("Formato timestamp non valido")
        except Exception as e:
            raise ValueError(f"Errore nel parsing del timestamp '{timestamp_str}': {e}")
    
    @staticmethod
    def srt_timestamp_to_timedelta(srt_time: str) -> timedelta:
        """Converte timestamp SRT (HH:MM:SS,mmm) in timedelta"""
        # Rimuove i millisecondi e converte
        time_part = srt_time.split(',')[0]
        hours, minutes, seconds = map(int, time_part.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    @staticmethod
    def extract_text_until_timestamp(srt_content: str, target_timestamp: str) -> str:
        """
        Estrae il testo dal file SRT fino al timestamp specificato
        
        Args:
            srt_content: Contenuto del file SRT
            target_timestamp: Timestamp limite formato HH:MM:SS
            
        Returns:
            Testo estratto fino al timestamp specificato
        """
        target_time = SRTProcessor.parse_timestamp(target_timestamp)
        
        # Pattern per parsing SRT: numero subtitle, timestamp, testo
        srt_pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\d+\n|\n*$)'
        
        extracted_text = []
        matches = re.findall(srt_pattern, srt_content, re.DOTALL)
        
        for match in matches:
            subtitle_num, start_time, end_time, text = match
            
            # Converte il timestamp di inizio
            start_timedelta = SRTProcessor.srt_timestamp_to_timedelta(start_time)
            
            # Se il subtitle inizia dopo il timestamp target, ferma l'estrazione
            if start_timedelta > target_time:
                break
                
            # Pulisce il testo e aggiunge alla lista
            clean_text = re.sub(r'\n+', ' ', text.strip())
            if clean_text:
                extracted_text.append(clean_text)
        
        return ' '.join(extracted_text)


class TranscriptAnalyzerCrew:
    """Crew principale per l'analisi di transcript e generazione mappe concettuali"""
    
    def __init__(self, llm_model="gpt-5-nano"):
        """
        Inizializza la crew con il modello LLM specificato
        
        Args:
            llm_model: Modello LLM da utilizzare (default: "gpt-5-nano")
        """
        self.llm_model = llm_model
        print(f"🤖 Configurazione LLM: {llm_model}")
    
    def content_analyst(self) -> Agent:
        """
        Analista del Contenuto: identifica il tema centrale e la struttura del transcript
        """
        return Agent(
            role="Specialista di Analisi del Contenuto Educativo",
            goal="Identificare il tema centrale, gli argomenti principali e la struttura logica del transcript video per costruire la base della mappa concettuale",
            backstory="""Sei un esperto analista di contenuti educativi con oltre 15 anni di esperienza 
            nell'analisi di materiali didattici e transcript video. Hai una particolare competenza 
            nell'identificare strutture logiche, temi centrali e nel riconoscere come i concetti 
            si collegano tra loro. La tua specialità è estrarre l'essenza di contenuti complessi 
            e organizzarli in modo che siano facilmente comprensibili.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_model
        )

    def concept_extractor(self) -> Agent:
        """
        Estrattore di Concetti: identifica concetti principali e secondari con le loro relazioni
        """
        return Agent(
            role="Esperto di Estrazione e Categorizzazione Concettuale",
            goal="Estrarre sistematicamente tutti i concetti chiave dal transcript, categorizzarli per importanza e identificare le relazioni gerarchiche tra di essi",
            backstory="""Con un background in psicologia cognitiva e scienze dell'informazione, 
            hai sviluppato metodologie avanzate per l'estrazione automatica di concetti da testi 
            complessi. Hai lavorato con università e centri di ricerca per creare sistemi di 
            mappatura concettuale che massimizzano la comprensione e la ritenzione. La tua 
            expertise include l'analisi semantica e l'identificazione di relazioni concettuali.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_model
        )

    def structure_architect(self) -> Agent:
        """
        Architetto della Struttura: organizza i concetti in una gerarchia logica
        """
        return Agent(
            role="Architetto di Strutture Cognitive e Mappe Mentali",
            goal="Organizzare i concetti estratti in una struttura gerarchica ottimale, definendo relazioni padre-figlio e garantendo una navigazione logica e intuitiva",
            backstory="""Specialista in design dell'informazione e architetture cognitive, hai 
            creato sistemi di organizzazione della conoscenza per piattaforme educative leader 
            nel settore. La tua esperienza include la progettazione di mappe concettuali per 
            apprendimento adattivo e la strutturazione di contenuti complessi in formati 
            facilmente navigabili e comprensibili.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_model
        )

    def json_formatter(self) -> Agent:
        """
        Formattatore JSON: converte la struttura concettuale nel formato JSON richiesto
        """
        return Agent(
            role="Specialista di Formattazione Dati e Strutture JSON",
            goal="Convertire la mappa concettuale in un formato JSON perfettamente strutturato e conforme alle specifiche richieste, garantendo integrità e usabilità dei dati",
            backstory="""Esperto in data engineering e formattazione di strutture dati complesse, 
            hai anni di esperienza nella conversione di informazioni concettuali in formati 
            machine-readable. Ti specializzi nella creazione di JSON strutturati per applicazioni 
            educative e sistemi di gestione della conoscenza, garantendo sempre conformità agli 
            standard e facilità di parsing.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_model
        )

    def analyze_content_structure(self) -> Task:
        """
        Task 1: Analizza la struttura generale del contenuto del transcript
        """
        return Task(
            description="""
            Analizza il transcript fornito per identificare:
            
            1. **Tema Centrale**: Qual è l'argomento principale unificante del contenuto?
            2. **Contesto e Ambito**: In quale campo disciplinare si colloca il contenuto?
            3. **Struttura Narrativa**: Come è organizzato il contenuto (introduzione, sviluppo, conclusioni)?
            4. **Livello di Complessità**: Valuta la difficoltà e profondità degli argomenti trattati
            5. **Obiettivi Educativi**: Quali sembrano essere gli obiettivi formativi del video?
            
            **Processo di analisi:**
            - Leggi tutto il transcript identificando il filo conduttore principale
            - Individua i punti di transizione tra argomenti diversi
            - Determina il focus centrale che dovrebbe essere al vertice della mappa concettuale
            - Valuta l'approccio didattico utilizzato (teorico, pratico, esempi, ecc.)
            - Identifica il pubblico target implicito
            
            **IMPORTANTE**: 
            
            Analizza ESCLUSIVAMENTE il transcript fornito. Non inventare o aggiungere contenuti non presenti nel testo.
            Il JSON deve riflettere fedelmente solo i concetti effettivamente discussi nel transcript.
            
            TRANSCRIPT DA ANALIZZARE:
            {transcript}
            
            Basati SOLO su questo contenuto per creare la mappa concettuale.
            """,
            expected_output="""
            Un report di analisi strutturato contenente:
            
            ```
            ANALISI STRUTTURA CONTENUTO
            ============================
            
            TEMA CENTRALE: [Titolo conciso del tema principale]
            
            DESCRIZIONE: [Descrizione dettagliata del tema centrale in 100-150 parole]
            
            AMBITO DISCIPLINARE: [Campo di studio/settore]
            
            LIVELLO COMPLESSITÀ: [Principiante/Intermedio/Avanzato]
            
            STRUTTURA NARRATIVA:
            - Introduzione: [Contenuto introduttivo]
            - Sviluppo: [Argomenti principali sviluppati]
            - Conclusioni: [Elementi conclusivi o riassuntivi]
            
            OBIETTIVI EDUCATIVI:
            1. [Primo obiettivo identificato]
            2. [Secondo obiettivo identificato]
            3. [Terzo obiettivo identificato]
            
            NOTE AGGIUNTIVE: [Osservazioni rilevanti per la mappatura concettuale]
            ```
            
            **Requisiti di qualità:**
            - Descrizione del tema centrale tra 100-150 parole
            - Analisi accurata del livello di complessità
            - Identificazione di almeno 3 obiettivi educativi chiari
            - Struttura narrativa ben definita
            """,
            agent=self.content_analyst()
        )

    def extract_key_concepts(self) -> Task:
        """
        Task 2: Estrae tutti i concetti chiave e li categorizza
        """
        return Task(
            description="""
            Basandoti sull'analisi della struttura del contenuto, estrai sistematicamente tutti i concetti chiave dal transcript.
            
            **Attività da svolgere:**
            
            1. **Identificazione Concetti Primari**: Trova i 3-7 concetti più importanti che costituiscono i pilastri del contenuto
            2. **Identificazione Concetti Secondari**: Per ogni concetto primario, identifica i sotto-concetti collegati
            3. **Categorizzazione per Importanza**: Assegna priorità (Alta/Media/Bassa) a ogni concetto
            4. **Analisi Relazioni**: Identifica come i concetti si collegano tra loro
            5. **Ricerca Link di Approfondimento**: Se possibile, trova link Wikipedia pertinenti per i concetti principali
            
            **IMPORTANTE**: 
            
            Estrai concetti ESCLUSIVAMENTE dal transcript fornito:
            {transcript}
            
            Non aggiungere concetti esterni o da altre fonti. Lavora solo con il contenuto effettivamente presente.
            
            **Processo di categorizzazione:**
            - Concetti Primari: Argomenti centrali che costituiscono l'ossatura del contenuto
            - Concetti Secondari: Dettagli, esempi, applicazioni che supportano i primari
            - Concetti di Contesto: Informazioni di background necessarie per la comprensione
            """,
            expected_output="""
            Un inventario completo dei concetti strutturato come segue:
            
            ```
            INVENTARIO CONCETTI ESTRATTI
            ============================
            
            CONCETTI PRIMARI (Alta Priorità):
            1. [Nome Concetto]
               - Descrizione: [Spiegazione del concetto in 50-80 parole]
               - Link Wikipedia: [URL se trovato, altrimenti "Non disponibile"]
               - Presente nel transcript: [Citazione breve dal testo]
            
            2. [Nome Concetto]
               - Descrizione: [Spiegazione del concetto]
               - Link Wikipedia: [URL se disponibile]
               - Presente nel transcript: [Citazione breve]
            
            [...continua per tutti i concetti primari]
            
            CONCETTI SECONDARI (Media Priorità):
            [Struttura simile ai primari, raggruppati per area tematica]
            
            CONCETTI DI CONTESTO (Bassa Priorità):
            [Concetti di supporto e background]
            
            RELAZIONI IDENTIFICATE:
            - [Concetto A] → collegato a → [Concetto B] (tipo relazione)
            - [Concetto C] → parte di → [Concetto A]
            
            STATISTICHE:
            - Totale concetti primari: [numero]
            - Totale concetti secondari: [numero]
            - Totale concetti di contesto: [numero]
            ```
            
            **Requisiti di qualità:**
            - Tra 3-7 concetti primari per mantenere chiarezza
            - Ogni descrizione tra 50-80 parole
            - Link Wikipedia validi quando disponibili
            - Citazioni precise dal transcript per ogni concetto
            - Relazioni chiaramente definite tra concetti
            """,
            agent=self.concept_extractor(),
            context=[self.analyze_content_structure()]
        )

    def build_concept_hierarchy(self) -> Task:
        """
        Task 3: Costruisce la gerarchia concettuale ottimale
        """
        return Task(
            description="""
            Organizza tutti i concetti estratti in una struttura gerarchica logica e navigabile che servirà da base per la mappa concettuale JSON.
            
            **Obiettivi della strutturazione:**
            
            1. **Gerarchia Logica**: Crea una struttura ad albero con massimo 3-4 livelli di profondità
            2. **Relazioni Padre-Figlio**: Definisci chiaramente quali concetti sono sotto-categorie di altri
            3. **Bilanciamento**: Evita rami troppo sbilanciati (alcuni con molti figli, altri senza)
            4. **Navigabilità**: Assicurati che la struttura sia intuitiva per l'utente finale
            5. **Completezza**: Tutti i concetti estratti devono trovare posto nella gerarchia
            
            **Processo di strutturazione:**
            - Identifica il concetto radice (tema centrale)
            - Posiziona i concetti primari come figli diretti della radice
            - Organizza i concetti secondari sotto i primari appropriati
            - Colloca i concetti di contesto dove più logicamente appartengono
            - Verifica che non ci siano nodi orfani o collegamenti illogici
            
            **IMPORTANTE**: 
            
            Organizza SOLO i concetti estratti dal transcript:
            {transcript}
            
            Non aggiungere o inventare concetti. Mantieni fedeltà assoluta al contenuto originale.
            """,
            expected_output="""
            Una mappa gerarchica strutturata dettagliata:
            
            ```
            STRUTTURA GERARCHICA CONCETTUALE
            ================================
            
            LIVELLO 0 (RADICE):
            └── [TEMA CENTRALE]
                Descrizione: [Descrizione completa]
                Link: [URL Wikipedia se disponibile]
            
            LIVELLO 1 (CONCETTI PRIMARI):
            ├── [CONCETTO PRIMARIO 1]
            │   Descrizione: [Descrizione]
            │   Link: [URL se disponibile]
            │   
            ├── [CONCETTO PRIMARIO 2]
            │   Descrizione: [Descrizione]
            │   Link: [URL se disponibile]
            │   
            └── [CONCETTO PRIMARIO N]
                Descrizione: [Descrizione]
                Link: [URL se disponibile]
            
            LIVELLO 2 (CONCETTI SECONDARI):
            [CONCETTO PRIMARIO 1]
            ├── [SOTTO-CONCETTO 1.1]
            │   Descrizione: [Descrizione]
            │   Link: [URL se disponibile]
            │   
            ├── [SOTTO-CONCETTO 1.2]
            │   Descrizione: [Descrizione]
            │   
            └── [SOTTO-CONCETTO 1.N]
                Descrizione: [Descrizione]
            
            [Continua per tutti i rami...]
            
            LIVELLO 3-4 (DETTAGLI SPECIFICI):
            [Struttura dettagliata dei livelli più profondi]
            
            VALIDAZIONE STRUTTURA:
            - Profondità massima: [numero] livelli
            - Numero totale nodi: [numero]
            - Distribuzione per livello: Livello 1: [X], Livello 2: [Y], ecc.
            - Nodi con più figli: [lista nodi con numero figli]
            - Nodi foglia: [numero]
            
            NOTE ARCHITETTURALI:
            [Spiegazioni delle scelte strutturali e eventuali compromessi]
            ```
            
            **Requisiti di qualità:**
            - Massimo 3-4 livelli di profondità
            - Struttura bilanciata e logica
            - Ogni nodo con descrizione appropriata
            - Collegamenti gerarchici chiari e motivati
            - Validazione completa della struttura
            """,
            agent=self.structure_architect(),
            context=[self.analyze_content_structure(), self.extract_key_concepts()]
        )

    def generate_json_map(self) -> Task:
        """
        Task 4: Genera il JSON finale conforme alle specifiche richieste
        """
        return Task(
            description="""
            Converti la struttura gerarchica concettuale nel formato JSON finale richiesto, rispettando rigorosamente le specifiche fornite.
            
            **Specifiche formato JSON richiesto:**
            
            Struttura ricorsiva con i seguenti campi:
            - `title` (string, obbligatorio): Titolo del concetto
            - `description` (string, opzionale): Descrizione estesa del concetto  
            - `image` (string URL, opzionale): URL immagine rappresentativa
            - `link` (string URL, opzionale): Link per approfondimenti
            - `children` (array, obbligatorio): Lista sotto-concetti (sempre presente, anche se vuota)
            
            **Processo di conversione:**
            
            1. **Mappatura Strutturale**: Converti ogni nodo della gerarchia in un oggetto JSON
            2. **Compilazione Campi**: Riempi tutti i campi disponibili per ogni nodo
            3. **Gestione Link**: Includi i link Wikipedia trovati nel campo `link`
            4. **Gestione Immagini**: Lascia vuoto il campo `image` per ora (sviluppo futuro)
            5. **Validazione Ricorsiva**: Assicurati che ogni `children` sia presente
            6. **Test JSON**: Verifica che il JSON sia valido e parsabile
            
            **Regole di conversione:**
            - Ogni livello della gerarchia diventa un nodo JSON
            - I sotto-concetti diventano elementi dell'array `children`
            - Le descrizioni devono essere concise ma informative (max 200 caratteri)
            - I titoli devono essere brevi e descrittivi (max 50 caratteri)
            - Tutti gli URL devono essere completi e validi
            
            **TRANSCRIPT ORIGINALE DA CONVERTIRE:**
            {transcript}
            
            **IMPORTANTE**: Il JSON finale deve riflettere ESATTAMENTE i concetti presenti nel transcript sopra.
            Non aggiungere, modificare o inventare contenuti non presenti nel testo originale.
            """,
            expected_output="""
            Un JSON valido e completamente strutturato nel formato richiesto:
            
            ```json
            {
              "title": "[Tema Centrale - max 50 caratteri]",
              "description": "[Descrizione completa del tema centrale - max 200 caratteri]",
              "image": "",
              "link": "[URL Wikipedia se disponibile]",
              "children": [
                {
                  "title": "[Concetto Primario 1]",
                  "description": "[Descrizione concetto primario]",
                  "image": "",
                  "link": "[URL se disponibile]",
                  "children": [
                    {
                      "title": "[Sotto-concetto 1.1]",
                      "description": "[Descrizione sotto-concetto]",
                      "image": "",
                      "link": "",
                      "children": []
                    },
                    {
                      "title": "[Sotto-concetto 1.2]", 
                      "description": "[Descrizione]",
                      "image": "",
                      "link": "",
                      "children": [
                        {
                          "title": "[Dettaglio specifico]",
                          "description": "[Descrizione dettaglio]",
                          "image": "",
                          "link": "",
                          "children": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "title": "[Concetto Primario 2]",
                  "description": "[Descrizione]",
                  "image": "",
                  "link": "",
                  "children": []
                }
              ]
            }
            ```
            
            **Validazione finale:**
            - JSON sintatticamente valido ✓
            - Tutti i campi obbligatori presenti ✓  
            - Campo `children` sempre presente ✓
            - URL validi quando presenti ✓
            - Lunghezza titoli e descrizioni rispettata ✓
            - Struttura ricorsiva corretta ✓
            
            **IMPORTANTE**: Il JSON deve essere restituito come blocco di codice valido, pronto per il parsing e l'uso immediato.
            """,
            agent=self.json_formatter(),
            context=[self.analyze_content_structure(), self.extract_key_concepts(), self.build_concept_hierarchy()]
        )

    def create_crew(self) -> Crew:
        """Crea e configura la crew principale"""
        return Crew(
            agents=[
                self.content_analyst(),
                self.concept_extractor(), 
                self.structure_architect(),
                self.json_formatter()
            ],
            tasks=[
                self.analyze_content_structure(),
                self.extract_key_concepts(),
                self.build_concept_hierarchy(), 
                self.generate_json_map()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,  # Abilita memoria per coerenza tra task
            max_rpm=30    # Limite richieste per minuto
        )


def analyze_json_structure(json_obj: dict, level: int = 0) -> dict:
    """
    Analizza la struttura di un JSON per fornire statistiche
    
    Args:
        json_obj: Oggetto JSON da analizzare
        level: Livello di profondità corrente
        
    Returns:
        Dizionario con statistiche della struttura
    """
    stats = {
        'total_nodes': 1,
        'max_depth': level,
        'nodes_with_children': 0
    }
    
    if 'children' in json_obj and json_obj['children']:
        stats['nodes_with_children'] = 1
        
        for child in json_obj['children']:
            child_stats = analyze_json_structure(child, level + 1)
            stats['total_nodes'] += child_stats['total_nodes']
            stats['max_depth'] = max(stats['max_depth'], child_stats['max_depth'])
            stats['nodes_with_children'] += child_stats['nodes_with_children']
    
    return stats


def load_srt_file(file_path: str) -> str:
    """
    Carica il contenuto di un file SRT
    
    Args:
        file_path: Percorso al file SRT
        
    Returns:
        Contenuto del file come stringa
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File SRT non trovato: {file_path}")
    except Exception as e:
        raise Exception(f"Errore nella lettura del file SRT: {e}")


def main():
    """
    Funzione principale per l'esecuzione dell'analisi transcript
    
    UTILIZZO:
    - Metodo 1 (nuovo): python main.py [timestamp] 
      Esempio: python main.py 00:01:30
    - Metodo 2 (legacy): python main.py (usa timestamp hardcoded)
    
    Il risultato JSON sarà stampato e salvato come file.
    """
    
    # ============================================================================
    # CONFIGURAZIONE INPUT - Automatica da argv o valori default
    # ============================================================================
    
    # Percorso al file SRT del transcript  
    srt_file_path = "transcript.srt"
    
    # Timestamp: da argv[1] se presente, altrimenti usa default per test
    if len(sys.argv) > 1:
        target_timestamp = sys.argv[1]  # Timestamp passato da API FastAPI
        print(f"📥 Timestamp ricevuto da parametro: {target_timestamp}")
    else:
        target_timestamp = "00:01:30"  # Default per test manuali
        print(f"⚙️  Usando timestamp di default: {target_timestamp}")
    
    # ============================================================================
    
    print("🎬 CrewAI Transcript Analyzer")
    print("=" * 50)
    
    try:
        # 1. Carica il file SRT
        print(f"📁 Caricamento file SRT: {srt_file_path}")
        srt_content = load_srt_file(srt_file_path)
        print(f"✅ File caricato correttamente ({len(srt_content)} caratteri)")
        
        # 2. Estrai il testo fino al timestamp specificato
        print(f"⏰ Estrazione testo fino al timestamp: {target_timestamp}")
        processor = SRTProcessor()
        extracted_text = processor.extract_text_until_timestamp(srt_content, target_timestamp)
        
        if not extracted_text:
            print("⚠️  Nessun testo estratto. Verifica il timestamp o il formato del file SRT.")
            return
            
        print(f"✅ Testo estratto correttamente ({len(extracted_text)} caratteri)")
        print(f"📝 Anteprima: {extracted_text[:200]}...")
        
        # 3. Inizializza e avvia la crew
        print("\n🤖 Inizializzazione CrewAI...")
        
        # CONFIGURAZIONE MODELLO LLM
        # Modifica qui per cambiare il modello utilizzato:
        # - "gpt-4o-mini" (consigliato: veloce ed economico)
        # - "gpt-4o" (più potente ma costoso) 
        # - "gpt-4-turbo"
        # - "gpt-3.5-turbo" (più economico ma meno preciso)
        llm_model = "gpt-4o-mini"  # MODIFICA: Cambia il modello qui se necessario
        
        analyzer = TranscriptAnalyzerCrew(llm_model=llm_model)
        crew = analyzer.create_crew()
        
        print("🚀 Avvio analisi del transcript...")
        print("⏳ Questo processo può richiedere alcuni minuti...\n")
        
        # 4. Esegui l'analisi
        result = crew.kickoff(inputs={
            "transcript": extracted_text,
            "target_timestamp": target_timestamp,
            "original_file": srt_file_path
        })
        
        # 5. Estrai e valida il JSON risultante
        print("\n" + "=" * 50)
        print("🎯 RISULTATO FINALE - MAPPA CONCETTUALE JSON")
        print("=" * 50)
        
        # Il risultato dovrebbe contenere il JSON nel task finale
        final_output = str(result)
        
        # Cerca il JSON nel risultato con pattern migliorato
        try:
            # Pattern per estrarre JSON completo tra ```json e ```
            json_code_pattern = r'```json\s*(.*?)\s*```'
            json_matches = re.findall(json_code_pattern, final_output, re.DOTALL)
            
            if json_matches:
                # Prendi l'ultimo JSON (quello finale)
                json_result = json_matches[-1].strip()
                
                # Valida il JSON
                parsed_json = json.loads(json_result)
                
                # Verifica che il JSON abbia la struttura corretta
                if 'title' in parsed_json and 'children' in parsed_json:
                    # Stampa il JSON formattato
                    print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                    
                    # Salva il risultato in un file
                    output_file = f"mappa_concettuale_{target_timestamp.replace(':', '-')}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(parsed_json, f, indent=2, ensure_ascii=False)
                    
                    print(f"\n💾 Mappa concettuale salvata in: {output_file}")
                    
                    # Mostra statistiche della mappa
                    stats = analyze_json_structure(parsed_json)
                    print(f"\n📊 Statistiche mappa concettuale:")
                    print(f"   - Nodi totali: {stats['total_nodes']}")
                    print(f"   - Livelli profondità: {stats['max_depth']}")
                    print(f"   - Nodi con children: {stats['nodes_with_children']}")
                    
                else:
                    raise ValueError("JSON non conforme alla struttura richiesta")
                    
            else:
                # Fallback: cerca JSON senza delimitatori di codice
                print("⚠️  Ricerca JSON senza delimitatori...")
                
                # Pattern per JSON completo
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_matches = re.findall(json_pattern, final_output, re.DOTALL)
                
                if json_matches:
                    # Cerca il JSON più complesso (probabilmente quello giusto)
                    best_json = max(json_matches, key=lambda x: x.count('"title"'))
                    
                    try:
                        parsed_json = json.loads(best_json)
                        if 'title' in parsed_json and 'children' in parsed_json:
                            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                            
                            output_file = f"mappa_concettuale_{target_timestamp.replace(':', '-')}.json"
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(parsed_json, f, indent=2, ensure_ascii=False)
                            
                            print(f"\n💾 Mappa concettuale salvata in: {output_file}")
                        else:
                            raise ValueError("JSON struttura non valida")
                    except:
                        raise ValueError("Nessun JSON valido trovato")
                else:
                    raise ValueError("Nessun JSON trovato nel risultato")
                
        except json.JSONDecodeError as e:
            print(f"❌ Errore nel parsing JSON: {e}")
            print("\n🔍 Debug: Output completo della crew:")
            print("-" * 50)
            print(final_output)
            print("-" * 50)
            
        except ValueError as e:
            print(f"❌ {e}")
            print("\n🔍 Debug: Output completo della crew:")
            print("-" * 50)
            print(final_output)
            print("-" * 50)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Assicurati che il file SRT esista e il percorso sia corretto")
        
    except ValueError as e:
        print(f"❌ Errore nel formato timestamp: {e}")
        print("💡 Usa il formato HH:MM:SS o MM:SS (es: '00:01:30' o '1:30')")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        print("💡 Verifica la configurazione di CrewAI e le API keys")

if __name__ == "__main__":
    main()