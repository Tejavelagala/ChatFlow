<template>
  <div v-if="show" class="confirm-overlay" @click.self="$emit('cancel')">
    <div class="confirm-dialog">
      <div class="confirm-icon" :class="type">
        {{ icons[type] }}
      </div>
      <h3>{{ title }}</h3>
      <p>{{ message }}</p>
      <div class="confirm-actions">
        <button class="btn btn-secondary" @click="$emit('cancel')">
          {{ cancelText }}
        </button>
        <button class="btn" :class="`btn-${type}`" @click="$emit('confirm')">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    show: Boolean,
    title: {
      type: String,
      default: 'Confirm Action'
    },
    message: {
      type: String,
      default: 'Are you sure?'
    },
    type: {
      type: String,
      default: 'danger',
      validator: (v) => ['danger', 'warning', 'info'].includes(v)
    },
    confirmText: {
      type: String,
      default: 'Confirm'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    }
  },
  data() {
    return {
      icons: {
        danger: '⚠️',
        warning: '⚡',
        info: 'ℹ️'
      }
    }
  },
  emits: ['confirm', 'cancel']
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 5000;
  animation: fadeIn 0.2s ease;
}

.confirm-dialog {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  box-shadow: var(--shadow-xl);
  animation: slideUp 0.3s ease;
  text-align: center;
}

.confirm-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.confirm-icon.danger {
  color: var(--danger);
}

.confirm-icon.warning {
  color: var(--warning);
}

.confirm-icon.info {
  color: var(--info);
}

.confirm-dialog h3 {
  color: var(--text-primary);
  font-size: var(--font-size-section-title);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.confirm-dialog p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  font-size: var(--font-size-body);
}

.confirm-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
