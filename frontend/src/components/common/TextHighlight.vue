<template>
  <span v-html="highlightedText"></span>
</template>

<script>
export default {
  name: 'TextHighlight',
  props: {
    text: {
      type: String,
      required: true
    },
    query: {
      type: String,
      default: ''
    }
  },
  computed: {
    highlightedText() {
      if (!this.query || !this.text) return this.text
      
      const regex = new RegExp(`(${this.escapeRegex(this.query)})`, 'gi')
      return this.text.replace(regex, '<mark class="highlight">$1</mark>')
    }
  },
  methods: {
    escapeRegex(str) {
      return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    }
  }
}
</script>

<style scoped>
:deep(.highlight) {
  background: var(--primary);
  color: var(--text-inverse);
  padding: 0.125rem 0.25rem;
  border-radius: 3px;
  font-weight: 600;
}
</style>
