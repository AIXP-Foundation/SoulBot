import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/dev-ui/',
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/health': 'http://localhost:8000',
      '/version': 'http://localhost:8000',
      '/list-apps': 'http://localhost:8000',
      '/cli-info': 'http://localhost:8000',
      '/apps': 'http://localhost:8000',
      '/run_sse': 'http://localhost:8000',
      '/run': 'http://localhost:8000',
      '/schedule': 'http://localhost:8000',
      '/aiap-store': 'http://localhost:8000',
    },
  },
  build: {
    outDir: resolve(__dirname, '../src/soulbot/server/static'),
    emptyOutDir: true,
  },
})
