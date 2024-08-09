import { defineConfig } from 'vite'
// import { resolve } from 'path'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/static/",
  build: {
    manifest: 'manifest.json',
    outDir: './assets_output',
    rollupOptions: {
      input: {
        main: '/src/main.tsx',
      }
    }
  }
})
