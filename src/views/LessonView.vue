<template>
    <main class="min-h-screen bg-slate-50 text-slate-800 p-6 font-sans">
      <div class="grid grid-cols-1 gap-4 lg:[grid-template-columns:7fr_3fr]">
        <!-- COLONNA SINISTRA -->
        <section class="flex flex-col gap-4">
          <h2 class="text-[18px] font-bold text-slate-700 m-0">Energia</h2>
  
          <!-- VIDEO -->
          <section class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <h3 class="font-bold text-slate-700 mb-2 mt-0">Video lezione</h3>
            <div class="border border-slate-200 rounded-lg overflow-hidden bg-slate-200">
              <div class="wistia_responsive_padding" style="padding:56.25% 0 0 0; position:relative;">
                <div class="wistia_responsive_wrapper" style="height:100%; left:0; position:absolute; top:0; width:100%;">
                  <iframe
                    :src="`https://fast.wistia.net/embed/iframe/${wistiaId}?videoFoam=true`"
                    allowfullscreen
                    frameborder="0"
                    class="wistia_embed"
                    title="Lezione"
                    style="width:100%;height:100%;border-radius:8px;"
                  ></iframe>
                </div>
              </div>
            </div>
          </section>
  
          <!-- APPUNTI -->
          <section class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <h3 class="font-bold text-slate-700 mb-2 mt-0">Scrivi un appunto</h3>
            <textarea
              v-model="noteDraft"
              class="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm resize-y"
              rows="4"
              placeholder="Scrivi qui i tuoi appunti…"
            ></textarea>
            <div class="flex justify-between items-center gap-[10px] mt-2">
              <span class="text-[12px] bg-slate-100 text-slate-600 px-2 py-1 rounded-md">ts: {{ currentHHMMSS }}</span>
              <div class="flex gap-[10px]">
                <button
                  class="bg-white text-slate-700 border border-slate-200 rounded-lg px-[10px] py-[6px] text-[13px] font-semibold hover:bg-slate-50"
                  type="button"
                  @click="noteDraft = ''"
                >Annulla</button>
                <button
                  class="bg-primary text-white rounded-lg px-[10px] py-[6px] text-[13px] font-semibold hover:bg-primary-dark disabled:opacity-50"
                  type="button"
                  @click="saveNote"
                  :disabled="!noteDraft.trim()"
                >Salva (con timestamp)</button>
              </div>
            </div>
  
            <!-- Appunti salvati -->
            <ul v-if="notes.length" class="mt-3 space-y-2">
              <li v-for="n in notes" :key="n.id" class="text-sm text-slate-700">
                <span class="font-semibold text-slate-600 mr-2">{{ n.hhmmss }}</span> {{ n.text }}
              </li>
            </ul>
          </section>
  
          <!-- MAPPE + RIASSUNTO -->
          <section class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <div class="flex justify-between items-center gap-3 flex-wrap">
              <h3 class="font-bold text-slate-700 mb-2 mt-0">Mappe concettuali</h3>
              <div class="flex items-center gap-2">
                <span class="text-[12px] bg-slate-100 text-slate-600 px-2 py-1 rounded-md" title="Timestamp corrente/ultimo pausa">
                  ts: {{ currentHHMMSS }}
                </span>
  
                <button
                  class="bg-white text-slate-700 border border-slate-200 rounded-lg px-3 py-[6px] text-[13px] font-semibold hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  type="button"
                  @click="buildSummaryToNow"
                  :disabled="isGeneratingMap"
                  title="Genera mappa concettuale fino al timestamp corrente"
                >
                  <div v-if="isGeneratingMap" class="spinner"></div>
                  <span v-if="isGeneratingMap">Generando...</span>
                  <span v-else>Genera mappa fino a {{ currentHHMMSS }}</span>
                </button>
  
                <button
                  class="bg-primary text-white rounded-lg px-3 py-[6px] text-[13px] font-semibold hover:bg-primary-dark"
                  type="button"
                  @click="handleCreateMap"
                >
                  Crea mappa a {{ currentHHMMSS }}
                </button>
  
                <button
                  class="bg-white text-slate-700 border border-slate-200 rounded-lg px-3 py-[6px] text-[13px] font-semibold hover:bg-slate-50"
                  type="button"
                  @click="getMaps"
                >
                  Ricarica
                </button>
              </div>
            </div>
  
            <!-- associator invisibile -->
            <concept-map-associator id="mapAssociator" ref="associatorRef" />
  
            <!-- contenitore mappe -->
            <div id="map-container" class="flex flex-col gap-3 mt-2" ref="containerRef"></div>
          </section>
  
        </section>
  
        <!-- COLONNA DESTRA -->
        <aside class="flex flex-col gap-4">
          <section class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <div class="flex gap-[10px]">
              <div class="w-[46px] h-[46px] rounded-full grid place-items-center bg-primary text-white font-extrabold">50%</div>
              <div>
                <div class="font-bold text-slate-700">Titolo corso</div>
                <div class="text-[13px] text-slate-500">Corso di Fisica – Modulo Energia</div>
              </div>
            </div>
          </section>
  
          <section class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <h3 class="font-bold text-slate-700 mb-2 mt-0">Contenuti del corso</h3>
            <details open class="border-t border-slate-100 pt-2 mt-2">
              <summary class="cursor-pointer font-semibold text-slate-700 list-none">Titolo Modulo</summary>
              <ul class="mt-2 pl-4 text-slate-700 space-y-[6px]">
                <li>Lezione 1</li>
                <li>Lezione 2</li>
                <li>Lezione 3</li>
              </ul>
            </details>
            <details class="border-t border-slate-100 pt-2 mt-2">
              <summary class="cursor-pointer font-semibold text-slate-700 list-none">Titolo Modulo</summary>
            </details>
            <details class="border-t border-slate-100 pt-2 mt-2">
              <summary class="cursor-pointer font-semibold text-slate-700 list-none">Titolo Modulo</summary>
            </details>
          </section>
        </aside>
      </div>
  
      <!-- TOAST -->
      <div
        v-show="toast.visible"
        id="toast-message"
        class="fixed right-4 bottom-4 text-white px-3 py-2 rounded-lg shadow-[0_10px_24px_rgba(0,0,0,0.12)]"
        :class="toast.type === 'success' ? 'bg-secondary' : 'bg-red-500'"
        role="status"
        aria-live="polite"
      >
        {{ toast.message }}
      </div>
    </main>
  </template>
  
  <script setup lang="ts">
  import { onMounted, onBeforeUnmount, ref, reactive, computed } from 'vue'
  
  /** ID del video Wistia */
  const wistiaId = 'glkoqys695'
  
  /** Refs DOM */
  const associatorRef = ref<HTMLElement | null>(null)
  const containerRef = ref<HTMLElement | null>(null)
  
  /** Toast */
  const toast = reactive({ visible: false, message: '', type: 'success' as 'success' | 'error' })
  function showToast(message: string, type: 'success' | 'error' = 'success') {
    toast.message = message
    toast.type = type
    toast.visible = true
    setTimeout(() => (toast.visible = false), 2000)
  }

  /** Loading state per generazione mappa concettuale */
  const isGeneratingMap = ref(false)
  
  /** ========= Wistia ========= */
  const player = ref<any>(null)          // istanza del player Wistia
  const currentSeconds = ref<number>(0)  // posizione corrente/ultima pausa in secondi
  
  function secondsToHHMMSS(s: number) {
    const total = Math.max(0, Math.floor(s || 0))
    const h = String(Math.floor(total / 3600)).padStart(2, '0')
    const m = String(Math.floor((total % 3600) / 60)).padStart(2, '0')
    const sec = String(total % 60).padStart(2, '0')
    return `${h}:${m}:${sec}`
  }
  const currentHHMMSS = computed(() => secondsToHHMMSS(currentSeconds.value))
  
  /** Legge il tempo istantaneo dal player, aggiorna currentSeconds e ritorna HH:MM:SS */
  function snapshotNow(): string {
    if (!player.value?.time) return currentHHMMSS.value
    const t = Number(player.value.time()) || 0
    currentSeconds.value = t
    return secondsToHHMMSS(t)
  }
  
  /** Carica E-v1.js se non presente */
  function loadWistiaScript(): Promise<void> {
    return new Promise((resolve, reject) => {
      if ((window as any)._wq && (window as any).Wistia) return resolve()
      const s = document.createElement('script')
      s.src = 'https://fast.wistia.com/assets/external/E-v1.js'
      s.async = true
      s.onload = () => resolve()
      s.onerror = () => reject(new Error('Wistia E-v1 load error'))
      document.head.appendChild(s)
    })
  }
  
  /** Inizializza player e listener */
  async function initWistiaPlayer() {
    await loadWistiaScript()
    ;(window as any)._wq = (window as any)._wq || []
    ;(window as any)._wq.push({
      id: wistiaId,
      onReady: (video: any) => {
        player.value = video
        // snapshot iniziale
        try { currentSeconds.value = Number(video.time()) || 0 } catch {}
        // aggiorna alla pausa (timestamp "esatto")
        video.bind('pause', () => {
          try { currentSeconds.value = Number(video.time()) || 0 } catch {}
        })
        // opzionale: aggiornamento "live" (se disponibile)
        try { video.bind?.('timechange', (t: number) => { currentSeconds.value = Number(t) || currentSeconds.value }) } catch {}
      },
    })
  }

  /** ========= Appunti ========= */
  type Note = { id: string; text: string; seconds: number; hhmmss: string }
  const noteDraft = ref('')
  const notes = ref<Note[]>([])
  
  function saveNote() {
    const ts = snapshotNow()
    if (!noteDraft.value.trim()) return
    notes.value.push({
      id: cryptoRandomId(),
      text: noteDraft.value.trim(),
      seconds: currentSeconds.value,
      hhmmss: ts,
    })
    noteDraft.value = ''
    showToast('Appunto salvato')
  }
  
  function cryptoRandomId() {
    // @ts-ignore
    if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID()
    return `${Date.now().toString(36)}${Math.random().toString(36).slice(2)}`
  }
  

  /** ========= CrewAI Integration ========= */

  async function generateConceptMapFromSummary(timestamp: string) {
    /**
     * Nuova funzione che chiama l'API CrewAI e ritorna il JSON
     * per creare direttamente una mappa concettuale
     */
    if (isGeneratingMap.value) {
      showToast('Generazione già in corso...', 'error')
      return
    }

    isGeneratingMap.value = true
    
    try {
      console.log(`🤖 Generazione mappa concettuale per timestamp: ${timestamp}`)
      
      const response = await fetch('http://localhost:8000/generate-concept-map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          timestamp: timestamp,
          video_id: wistiaId
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`)
      }
      
      const result = await response.json()
      
      console.log(result);
      
      if (result.success && result.concept_map_data) {
        console.log(`✅ Dati mappa concettuale ricevuti direttamente!`)
        console.log(`📄 Dati mappa:`, result.concept_map_data)
        
        // Chiama handleCreateMap con i dati della mappa ricevuti direttamente
        handleCreateMapWithData(result.concept_map_data, timestamp)
        showToast('Mappa concettuale generata!')
        
      } else {
        console.error(`❌ Errore generazione mappa: ${result.message}`)
        showToast('Errore nella generazione della mappa', 'error')
      }
      
    } catch (error) {
      console.error('💥 Errore chiamata API:', error)
      showToast('Errore di connessione API', 'error')
    } finally {
      isGeneratingMap.value = false
    }
  }

  function buildSummaryToNow() {
    /**
     * NUOVA IMPLEMENTAZIONE: Genera mappa concettuale direttamente
     * invece di salvare un file JSON
     */
    const ts = snapshotNow()
    
    console.log(`📅 Generazione mappa concettuale per timestamp: ${ts}`)
    
    // Chiama la nuova funzione che ritorna JSON e crea la mappa
    generateConceptMapFromSummary(ts)
  }
  
  /** ========= Mappe ========= */
  function createDeleteButton(mapId: string, onDelete: (id: string) => void) {
    const btn = document.createElement('button')
    btn.textContent = 'Elimina'
    btn.className = 'bg-red-500 text-white rounded-lg px-[10px] py-[6px] text-[13px] font-semibold hover:bg-red-700'
    btn.addEventListener('click', () => onDelete(mapId))
    return btn
  }
  
  function renderMaps(mapsID: string[]) {
    const container = containerRef.value!
    while (container.firstChild) container.removeChild(container.firstChild)
  
    mapsID.forEach((id) => {
      const row = document.createElement('div')
      row.className =
        'grid grid-cols-1 lg:[grid-template-columns:1.2fr_1fr_auto] gap-[10px] items-center bg-slate-50 border border-slate-100 rounded-lg p-[10px]'
  
      const meta = document.createElement('div')
      meta.className = 'flex flex-col gap-[2px]'
      meta.innerHTML =
        `<div class="font-bold text-slate-700">Mappa</div>` +
        `<div class="text-[13px] text-slate-500">Fisica • L03 • ${currentHHMMSS.value}</div>`
  
      const widget = document.createElement('concept-map-widget')
      widget.setAttribute('map-id', id)
      const metaApi = document.querySelector('meta[name="api-base-url"]') as HTMLMetaElement | null
      const apiBaseUrl = (window as any).API_CONCEPT_MAP_BASE_URL || metaApi?.content || 'http://localhost:10000'
      if (apiBaseUrl) widget.setAttribute('api-base-url', apiBaseUrl)
  
      const del = createDeleteButton(id, (mapId) => {
        associatorRef.value?.dispatchEvent(
          new CustomEvent('deleteMap', {
            detail: {
              mapId,
              callback: () => {
                row.remove()
                showToast('Mappa eliminata')
              },
            },
            bubbles: true,
            composed: true,
          }),
        )
      })
  
      row.append(meta, widget, del)
      container.appendChild(row)
    })
  }
  
  function getMaps() {
    associatorRef.value?.dispatchEvent(
      new CustomEvent('getMaps', {
        detail: { callback: renderMaps },
        bubbles: true,
        composed: true,
      }),
    )
  }
  
  function handleCreateMap() {
    const ts = snapshotNow()
    associatorRef.value?.dispatchEvent(
      new CustomEvent('createMap', {
        detail: {
          name: 'Nuova Mappa Interattiva',
          association_type: 'lesson',
          teaching_subject: 'Fisica Generale',
          lesson_identifier: 'L03_Energia',
          paragraph_identifier: 'P2_Trasformazioni',
          timestamp: ts,
          callback: () => getMaps(),
        },
        bubbles: true,
        composed: true,
      }),
    )
  }

  function handleCreateMapWithData(map_data: any, timestamp: string) {
    /**
     * Nuova funzione che crea una mappa concettuale con dati specifici
     * ricevuti dall'API CrewAI
     */
    associatorRef.value?.dispatchEvent(
      new CustomEvent('createMap', {
        detail: {
          name: 'Mappa Concettuale Generata',
          association_type: 'lesson',
          teaching_subject: 'Fisica Generale',
          lesson_identifier: 'L03_Energia',
          paragraph_identifier: 'P2_Trasformazioni',
          timestamp: timestamp,
          map_data: map_data, 
          callback: () => getMaps(),
        },
        bubbles: true,
        composed: true,
      }),
    )
  }
  
  /** Mount */
  onMounted(async () => {
    await initWistiaPlayer()
  
    const metaApi = document.querySelector('meta[name="api-base-url"]') as HTMLMetaElement | null
    const apiBaseUrl = (window as any).API_CONCEPT_MAP_BASE_URL || metaApi?.content || 'http://localhost:10000'
    if (apiBaseUrl && associatorRef.value) associatorRef.value.setAttribute('api-base-url', apiBaseUrl)
  
    getMaps()
  })
  
  onBeforeUnmount(() => {
    try { player.value?.unbind?.('pause') } catch {}
  })
  </script>
  
  <style>
  /* Palette opzionale (coerente col tuo Tailwind) */
  :root{
    --primary:#cf1d56;
    --primary-dark:#861f41;
    --secondary:#005D68;
  
    --slate-25:#f8fafc; --slate-50:#f1f5f9; --slate-100:#e2e8f0; --slate-200:#cbd5e1;
    --slate-300:#94a3b8; --slate-500:#64748b; --slate-700:#334155; --slate-800:#1f2937;
    --red:#ef4444; --red-700:#dc2626;
  }

  /* Spinner animato */
  .spinner {
    width: 12px;
    height: 12px;
    border: 2px solid #e5e7eb;
    border-top: 2px solid #6b7280;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>
  