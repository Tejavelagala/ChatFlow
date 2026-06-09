import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import Toast from'vue-toastification'
import 'vue-toastification/dist/index.css'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
import VueVirtualScroller from 'vue-virtual-scroller'
import { useThemeStore } from './stores/themeStore'

// U1 Design System Foundation
import './assets/theme.css'
import './assets/components.css'

// Initialize theme before mounting
const darkMode = localStorage.getItem('darkMode') === 'true'
if (darkMode) {
  document.documentElement.classList.add('dark')
}

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueVirtualScroller)
app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
})

app.mount('#app')

// Watch for theme changes
const themeStore = useThemeStore()
themeStore.$subscribe((mutation, state) => {
  if (state.darkMode) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})