<template>
  <div class="error-state">
    <div class="error-icon">⚠️</div>
    <h3>{{ title }}</h3>
    <p>{{ message }}</p>
    <button v-if="showRetry" @click="$emit('retry')" class="retry-btn">
      Retry
    </button>
  </div>
</template>

<script>
export default {
  name: 'ErrorState',
  props: {
    title: {
      type: String,
      default: 'Something went wrong'
    },
    message: {
      type: String,
      default: 'Please try again later'
    },
    showRetry: {
      type: Boolean,
      default: true
    }
  },
  emits: ['retry']
}
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #ef4444;
  margin-bottom: 10px;
  font-size: var(--font-size-section-title);
}

.error-state p {
  color: #666;
  margin-bottom: 25px;
  font-size: var(--font-size-body);
}

.retry-btn {
  border: none;
  background: #667eea;
  color: white;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #5a67d8;
  transform: translateY(-2px);
}
</style>
