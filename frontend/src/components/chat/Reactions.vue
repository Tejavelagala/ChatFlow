<template>
  <div v-if="reactions && Object.keys(reactions).length > 0" class="reaction-display">
    <span
      v-for="(count, emoji) in reactions"
      :key="emoji"
      class="reaction-badge"
      @click="$emit('react', emoji)"
    >
      {{ emoji }}
      <span class="reaction-count">{{ count }}</span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'Reactions',
  props: {
    reactions: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['react']
}
</script>

<style scoped>
.reaction-display {
  display: flex;
  gap: 4px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.reaction-badge {
  background: rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.12);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  transition: all 0.2s ease;
}

.reaction-badge:hover {
  background: rgba(0, 0, 0, 0.12);
  border-color: rgba(0, 0, 0, 0.2);
}

.reaction-count {
  font-size: 11px;
  font-weight: 500;
  opacity: 0.7;
}
</style>
