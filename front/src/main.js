import {getCookie} from './additional/functions/cookie.js'
import './additional/init.js'
import { createApp} from 'vue'
import './additional/init.js'
import store from './modules/store'
import router from './modules/router'
import App from './App.vue'
import VueTheMask from 'vue-the-mask'
import './ui5/index.js'

createApp(App)
    .use(store)
    .use(router)
    .use(getCookie)
    .use(VueTheMask)
    .mount('#app')