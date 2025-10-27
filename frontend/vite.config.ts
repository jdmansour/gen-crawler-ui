import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), svgr()],
  base: "/static/",
  resolve: {
    alias: {
      'assets': '/src/assets'
    }
  },
  server: {
    origin: 'http://localhost:5173'
  },
  build: {
    manifest: 'manifest.json',
    outDir: './assets_output',
    rollupOptions: {
      input: {
        demo: '/src/demo.tsx',
        wlo_spa: '/src/wlo_spa.tsx',
        main: '/src/main.tsx',
        css: '/src/index.css'
      }
    }
  }
})
