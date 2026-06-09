<template>
  <div class="empty-state">
    <div class="empty-icon">{{ icon }}</div>
    <h3>{{ title }}</h3>
    <p>{{ message }}</p>
    <button v-if="actionText" @click="$emit('action')" class="action-btn">
      {{ actionText }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    icon: {
      type: String,
      default: '📭'
    },
    title: {
      type: String,
      default: 'Nothing here yet'
    },
    message: {
      type: String,
      default: 'Get started by creating something new'
    },
    actionText: {
      type: String,
      default: ''
    }
  },
  emits: ['action']
}
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.8;
}

.empty-state h3 {
  color: var(--text-primary);
  margin-bottom: 10px;
  font-size: var(--font-size-section-title);
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 30px;
  font-size: var(--font-size-body);
}

.action-btn {
  border: none;
  background: var(--accent-gradient);
  color: var(--text-inverse);
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.action-btn:hover {
  filter: brightness(1.03);
  transform: translateY(-2px);
}
</style>
