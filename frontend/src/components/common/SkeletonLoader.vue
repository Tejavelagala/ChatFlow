<template>
  <div class="skeleton-loader" :class="variant">
    <div v-if="variant === 'message'" class="skeleton-message">
      <div class="skeleton-avatar"></div>
      <div class="skeleton-content">
        <div class="skeleton-line short"></div>
        <div class="skeleton-line"></div>
      </div>
    </div>
    
    <div v-else-if="variant === 'room'" class="skeleton-room">
      <div class="skeleton-line"></div>
      <div class="skeleton-line short"></div>
    </div>
    
    <div v-else class="skeleton-default">
      <div class="skeleton-line"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line short"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'message', 'room'].includes(v)
    }
  }
}
</script>

<style scoped>
.skeleton-loader {
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-message {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
}

.skeleton-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--border);
}

.skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.skeleton-room {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.skeleton-line {
  height: 1rem;
  background: var(--border);
  border-radius: var(--radius);
}

.skeleton-line.short {
  width: 60%;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
