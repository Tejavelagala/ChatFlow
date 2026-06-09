import { onMounted, onUnmounted } from 'vue'

export function useKeyboardShortcuts(shortcuts) {
  const handleKeyDown = (event) => {
    const key = event.key.toLowerCase()
    const ctrl = event.ctrlKey || event.metaKey
    const shift = event.shiftKey
    const alt = event.altKey

    for (const shortcut of shortcuts) {
      const matches = 
        shortcut.key === key &&
        !!shortcut.ctrl === ctrl &&
        !!shortcut.shift === shift &&
        !!shortcut.alt === alt

      if (matches) {
        event.preventDefault()
        shortcut.handler()
        break
      }
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
  })
}
