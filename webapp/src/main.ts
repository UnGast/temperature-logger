import { createApp } from 'vue'
import App from './App.vue'
import store from './store'

const app = createApp(App)
app.use(store)
app.mount("#app")

store.dispatch('restoreSettings').then(() => {
  return store.dispatch("connect")
}).catch((error) => {
  console.error("error during initial autoconnect", error)
})