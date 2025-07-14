import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr'

export default defineConfig({
  plugins: [
    react(),
    svgr({
      svgrOptions: {
        icon: true,
      },
    })
  ],
  build: {
    outDir: 'Pages/static/js/react',
    rollupOptions: {
      input: {
        bodyGraph: './frontend/src/components/FuturisticBodyGraph.jsx'
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    },
    lib: {
      entry: './frontend/src/components/FuturisticBodyGraph.jsx',
      name: 'FuturisticBodyGraph',
      fileName: 'body-graph',
      formats: ['umd']
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
      }
    }
  },
  define: {
    'process.env.NODE_ENV': '"production"'
  }
})