<template>
  <transition name="success-fade">
    <div v-if="show" class="success-feedback" :class="variant">
      <span class="success-icon">{{ icon }}</span>
      <span class="success-text">{{ text }}</span>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'SuccessFeedback',
  props: {
    show: Boolean,
    text: {
      type: String,
      default: 'Saved'
    },
    icon: {
      type: String,
      default: '✓'
    },
    variant: {
      type: String,
      default: 'success',
      validator: (v) => ['success', 'info', 'warning'].includes(v)
    }
  }
}
</script>

<style scoped>
.success-feedback {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--success-bg);
  color: var(--success);
  border-radius: var(--radius-md);
  font-size: var(--font-size-body-sm);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.success-feedback.info {
  background: var(--info-bg);
  color: var(--info);
}

.success-feedback.warning {
  background: var(--warning-bg);
  color: var(--warning);
}

.success-icon {
  font-size: 1rem;
  animation: checkmark 0.4s ease;
}

.success-text {
  animation: fadeInText 0.3s ease 0.1s both;
}

.success-fade-enter-active,
.success-fade-leave-active {
  transition: all 0.3s ease;
}

.success-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.9);
}

.success-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.9);
}

@keyframes checkmark {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fadeInText {
  from {
    opacity: 0;
    transform: translateX(-5px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
