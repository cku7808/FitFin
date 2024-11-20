import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueGeolocation from 'vue-geolocation-api'

import App from './App.vue'
import router from './router'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
const pinia = createPinia()
// const geolocation = VueGeolocation()

pinia.use(piniaPluginPersistedstate)
// app.use(createPinia())
app.use(pinia)
app.use(router)
// app.use(geolocation)

app.mount('#app')
window.Kakao.init("242327ad0274c1e85ab4064278373781");