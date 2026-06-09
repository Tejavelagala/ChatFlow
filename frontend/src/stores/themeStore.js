import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    darkMode: localStorage.getItem('darkMode') === 'true'
  }),

  getters: {
    isDarkMode: (state) => state.darkMode,
    themeClass: (state) => state.darkMode ? 'dark' : 'light'
  },

  actions: {
    toggleTheme() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
    },

    setDarkMode(value) {
      this.darkMode = value
      localStorage.setItem('darkMode', value)
    }
  }
})
