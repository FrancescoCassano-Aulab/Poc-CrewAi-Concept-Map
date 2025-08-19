// vite.config.js (ESM)
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => [
            'concept-map-associator',
            'concept-map-widget',
          ].includes(tag),
        },
      },
    }),
  ],
})
