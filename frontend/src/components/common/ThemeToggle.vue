<template>
  <button 
    @click="toggleTheme" 
    class="navbar-btn"
    :title="isDarkMode ? 'Light mode' : 'Dark mode'"
  >
    {{ isDarkMode ? '☀️' : '🌙' }}
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/themeStore'

const themeStore = useThemeStore()
const isDarkMode = computed(() => themeStore.isDarkMode)

const toggleTheme = () => {
  themeStore.toggleTheme()
}
</script>

<style scoped>
.navbar-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  font-size: 1.25rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-btn:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
}
</style>
