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
                  class="bg-white text-slate-700 border border-slate-200 rounded-lg px-3 py-[6px] text-[13px] font-semibold hover:bg-slate-50"
                  type="button"
                  @click="buildSummaryToNow"
                  title="Genera riassunto (trascrizione SRT) fino al timestamp corrente"
                >
                  Riassumi fino a {{ currentHHMMSS }}
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
  
          <!-- RIASSUNTO -->
          <section v-if="summary.visible" class="bg-white border border-slate-100 rounded-[10px] p-[14px]">
            <div class="flex justify-between items-center">
              <h3 class="font-bold text-slate-700 mb-2 mt-0">
                Riassunto 0 → {{ summary.hhmmss }}
              </h3>
              <button
                class="bg-white text-slate-700 border border-slate-200 rounded-lg px-3 py-[6px] text-[13px] font-semibold hover:bg-slate-50"
                @click="copySummary"
              >
                Copia
              </button>
            </div>
  
            <div class="space-y-3">
              <!-- Bullet dinamici (estratti dalla trascrizione) -->
              <div v-if="summary.bullets.length">
                <h4 class="text-[14px] font-semibold text-slate-700">Punti chiave</h4>
                <ul class="list-disc pl-5 space-y-1 text-sm text-slate-700">
                  <li v-for="(b, i) in summary.bullets" :key="i">{{ b }}</li>
                </ul>
              </div>
  
              <!-- Appunti utente -->
              <div v-if="summary.notes.length">
                <h4 class="text-[14px] font-semibold text-slate-700">Appunti (utente)</h4>
                <ul class="list-disc pl-5 space-y-1 text-sm text-slate-700">
                  <li v-for="n in summary.notes" :key="n.id">
                    <span class="text-slate-500 mr-2">{{ n.hhmmss }}</span>{{ n.text }}
                  </li>
                </ul>
              </div>
  
              <!-- Sintesi -->
              <p v-if="summary.paragraph" class="text-sm text-slate-700">
                {{ summary.paragraph }}
              </p>
            </div>
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
  
  /** URL trascrizione SRT (servita da /public) */
  const transcriptUrl = '/transcriptions/glkoqys695.srt' // <-- cambia se diverso
  
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
  function hhmmssToSeconds(hms: string) {
    const [h, m, s] = hms.split(':').map(n => parseInt(n || '0', 10))
    return (h * 3600) + (m * 60) + (s || 0)
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
  
  /** ========= Trascrizione: SRT (con fallback VTT) ========= */
  type Cue = { start: number; end: number; text: string }
  const cues = ref<Cue[]>([])
  const transcriptLoaded = ref(false)
  
  /** "HH:MM:SS,mmm" o "HH:MM:SS.mmm" → seconds */
  function tToSec(t: string) {
    const [h, m, s] = t.replace(',', '.').split(':').map(Number)
    return (h || 0) * 3600 + (m || 0) * 60 + (s || 0)
  }
  
  /** Parser VTT minimale (per sicurezza, nel caso avessi un VTT in futuro) */
  function parseVtt(text: string): Cue[] {
    const lines = text.replace(/\r/g, '').split('\n')
    const out: Cue[] = []
    let i = 0
    while (i < lines.length) {
      const line = lines[i].trim()
      if (!line || /^WEBVTT/i.test(line) || /^\d+$/.test(line)) { i++; continue }
      const m = line.match(/^(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})/)
      if (m) {
        const start = tToSec(m[1])
        const end   = tToSec(m[2])
        i++
        const buf: string[] = []
        while (i < lines.length && lines[i].trim() !== '') { buf.push(lines[i].trim()); i++ }
        out.push({ start, end, text: buf.join(' ') })
      } else {
        i++
      }
    }
    return out
  }
  
  /** Parser SRT (numero → time → testo → riga vuota) */
  function parseSrt(text: string): Cue[] {
    const blocks = text.replace(/\r/g, '').split(/\n\s*\n/) // blocchi separati da riga vuota
    const out: Cue[] = []
    for (const block of blocks) {
      const lines = block.split('\n').map(l => l.trim()).filter(Boolean)
      if (!lines.length) continue
      // riga tempo può essere la 1 o 2 (perché la 0 è spesso l'indice)
      let timeLine = ''
      if (/^\d+$/.test(lines[0]) && lines[1] && /-->/i.test(lines[1])) timeLine = lines[1]
      else if (/-->/i.test(lines[0])) timeLine = lines[0]
      else continue
  
      const m = timeLine.match(/^(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})/)
      if (!m) continue
      const start = tToSec(m[1])
      const end   = tToSec(m[2])
  
      // testo: tutte le righe che non sono l’indice o la riga del tempo
      const textLines = lines.filter((l, idx) => {
        if (idx === 0 && /^\d+$/.test(l)) return false
        if (l === timeLine) return false
        return true
      })
      const textNorm = textLines.join(' ')
        .replace(/<[^>]+>/g, '') // rimuovi eventuali tag
        .replace(/\s+/g, ' ')
        .trim()
  
      if (textNorm) out.push({ start, end, text: textNorm })
    }
    return out
  }
  
  /** Loader generico: auto-detect VTT/SRT (usa SRT nel tuo caso) */
  async function loadTranscript() {
    try {
      const res = await fetch(transcriptUrl, { cache: 'no-store' })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const text = await res.text()
      const isVtt = /^\s*WEBVTT/i.test(text)
      const parsed = isVtt ? parseVtt(text) : parseSrt(text)
      cues.value = parsed
      transcriptLoaded.value = true
    } catch (err) {
      console.error('Transcript load error:', err)
      showToast('Trascrizione non disponibile', 'error')
    }
  }
  
  /** Testo trascrizione dall’inizio fino a "sec" */
  function transcriptUpTo(sec: number) {
    if (!cues.value.length) return ''
    return cues.value
      .filter(c => c.start <= sec)
      .map(c => c.text)
      .join(' ')
  }
  
  /** Split in frasi basico */
  function splitSentences(txt: string) {
    return txt
      .replace(/\s+/g, ' ')
      .split(/(?<=[\.\!\?])\s+/)
      .map(s => s.trim())
      .filter(Boolean)
  }
  
  /** Stopword IT minime (espandibile) */
  const STOP = new Set([
    'a','ad','al','allo','ai','agli','alla','alle','con','col','coi','da','dal','dallo','dai','dagli','dalla','dalle',
    'di','del','dello','dei','degli','della','delle','in','nel','nello','nei','negli','nella','nelle',
    'su','sul','sullo','sui','sugli','sulla','sulle','per','tra','fra','il','lo','la','i','gli','le',
    'un','uno','una','e','o','ed','ma','non','più','meno','anche','come','che','dei','dell','dallo',
    'mi','ti','ci','vi','si','se','quindi','poi','solo','tutto','tutta','tutti','tutte','dai','degli'
  ])
  
  /** Estrae max N frasi “salienti” come bullet (TF molto semplice) */
  function buildBulletsFromText(txt: string, maxBullets = 6) {
    const sentences = splitSentences(txt)
    const freq = new Map<string, number>()
  
    for (const s of sentences) {
      for (const raw of s.toLowerCase().split(/[^a-zàèéìòóùA-ZÀÈÉÌÒÓÙ0-9]+/)) {
        const w = raw.trim()
        if (!w || STOP.has(w) || w.length < 3) continue
        freq.set(w, (freq.get(w) || 0) + 1)
      }
    }
  
    const keywords = [...freq.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([w]) => w)
  
    const picked: string[] = []
    const seen = new Set<string>()
    for (const s of sentences) {
      if (picked.length >= maxBullets) break
      const low = s.toLowerCase()
      if (keywords.some(k => low.includes(k)) && !seen.has(s)) {
        picked.push(s)
        seen.add(s)
      }
    }
  
    if (picked.length < Math.min(maxBullets, sentences.length)) {
      for (let i = Math.max(0, sentences.length - maxBullets); i < sentences.length; i++) {
        const s = sentences[i]
        if (!seen.has(s)) picked.push(s)
        if (picked.length >= maxBullets) break
      }
    }
  
    return picked
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
  
  /** ========= Riassunto dinamico (SRT) ========= */
  const summary = reactive<{
    visible: boolean
    hhmmss: string
    bullets: string[]
    notes: Note[]
    paragraph: string
  }>({
    visible: false,
    hhmmss: '00:00:00',
    bullets: [],
    notes: [],
    paragraph: '',
  })
  
  function buildSummaryToNow() {
    const ts = snapshotNow()
    const now = currentSeconds.value
  
    if (!transcriptLoaded.value || !cues.value.length) {
      summary.visible = true
      summary.hhmmss = ts
      summary.bullets = []
      summary.notes = notes.value.filter(n => n.seconds <= now)
      summary.paragraph = `Fino a ${ts} la trascrizione non è disponibile.`
      showToast('Trascrizione non disponibile', 'error')
      return
    }
  
    const text = transcriptUpTo(now)
    const bullets = buildBulletsFromText(text, 6)
  
    summary.visible = true
    summary.hhmmss = ts
    summary.bullets = bullets
    summary.notes = notes.value.filter(n => n.seconds <= now)
    summary.paragraph = bullets.length
      ? `Fino a ${ts} si sono trattati i seguenti punti chiave: ${bullets.slice(0,3).join(' · ')}.`
      : `Fino a ${ts} non sono emerse frasi salienti.`
  
    showToast('Riassunto dinamico generato')
  }
  
  async function copySummary() {
    const bulletsTxt = summary.bullets.map(b => `• ${b}`).join('\n')
    const notesTxt = summary.notes.map(n => `• [${n.hhmmss}] ${n.text}`).join('\n')
    const finalText =
  `Riassunto 0 → ${summary.hhmmss}
  
  Punti chiave:
  ${bulletsTxt || '—'}
  
  Appunti:
  ${notesTxt || '—'}
  
  Sintesi:
  ${summary.paragraph || '—'}
  `
    try {
      await navigator.clipboard.writeText(finalText)
      showToast('Riassunto copiato')
    } catch {
      showToast('Impossibile copiare', 'error')
    }
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
  
  /** Mount */
  onMounted(async () => {
    await initWistiaPlayer()
    await loadTranscript() // <-- carica l'SRT
  
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
  </style>
  