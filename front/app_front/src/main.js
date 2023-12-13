import { createApp } from 'vue'
import store from './modules/store'
import router from './modules/router'
import App from './App.vue'
import VueTheMask from 'vue-the-mask'
import './ui5/index.js'

createApp(App)
    .use(store)
    .use(router)
    .use(VueTheMask)
    .mount('#app')