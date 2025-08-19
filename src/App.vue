<template>
  <div class="p-6 bg-slate-100 min-h-screen">
    <h1 class="text-2xl font-bold text-slate-700 mb-4">Lezione Demo</h1>

    <!-- Video Wistia -->
    <div class="mb-6">
      <script src="https://fast.wistia.com/embed/medias/VIDEO_ID.js" async></script>
      <script src="https://fast.wistia.com/assets/external/E-v1.js" async></script>
      <div class="wistia_responsive_padding" style="padding:56.25% 0 0 0;position:relative;">
        <div class="wistia_responsive_wrapper" style="height:100%;left:0;position:absolute;top:0;width:100%;">
          <div class="wistia_embed wistia_async_VIDEO_ID seo=false videoFoam=true" style="height:100%;position:relative;width:100%">&nbsp;</div>
        </div>
      </div>
    </div>

    <!-- Web Components -->
    <concept-map-associator id="mapAssociator"></concept-map-associator>
    <button
      id="createMapBtn"
      class="bg-green-600 text-white px-4 py-2 mt-4 rounded hover:bg-green-700"
    >
      ➕ Crea nuova mappa
    </button>
    <div id="map-container" class="map-section mt-4"></div>
  </div>
</template>

<script setup>
// qui per ora non serve logica: usi index.js esterno per orchestrazione
</script>

<style>
.map-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  flex-direction: column;
  padding-bottom: 10px;
}
</style>
