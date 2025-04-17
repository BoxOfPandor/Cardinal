import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Allow access from Docker
    port: 3000       // Optional: Change the dev server port
  },
  build: {
    outDir: 'dist', // Output directory for production build
  },
})