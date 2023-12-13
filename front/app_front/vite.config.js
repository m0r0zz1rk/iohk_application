import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // treat all tags with ui5- as custom elements
          isCustomElement: tag => tag.includes('ui5-')
        }
      }
    })
  ]
})
