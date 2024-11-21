import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
const pinia = createPinia()
const VITE_KAKAO_KEY = import.meta.env['VITE_API_KEY_KAKAO_JS']

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)


app.mount('#app')

window.Kakao.init(VITE_KAKAO_KEY);