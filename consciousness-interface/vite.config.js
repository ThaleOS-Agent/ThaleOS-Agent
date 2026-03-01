import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// Base path: /ThaleOS-Agent/ on GitHub Pages, / everywhere else
const base = process.env.GITHUB_PAGES === 'true' ? '/ThaleOS-Agent/' : '/'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base,
  
  // Tauri expects a fixed port for development
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      // Tell Vite to ignore watching src-tauri
      ignored: ['**/src-tauri/**'],
    },
  },
  
  // Resolve aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@store': path.resolve(__dirname, './src/store'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  
  // Build configuration
  build: {
    // Tauri uses Chromium on Windows and WebKit on macOS and Linux
    target: process.env.TAURI_PLATFORM == 'windows' ? 'chrome105' : 'safari13',
    // Don't minify for debug builds
    minify: !process.env.TAURI_DEBUG ? 'esbuild' : false,
    // Produce sourcemaps for debug builds
    sourcemap: !!process.env.TAURI_DEBUG,
  },
  
  // Environment variables
  envPrefix: ['VITE_', 'TAURI_'],
  
  // Optimizations
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
  },
})
