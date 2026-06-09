<template>
  <div v-if="show" class="notification-center">
    <div class="notification-header">
      <h3>🔔 Notifications</h3>
      <button @click="$emit('close')" class="close-btn" aria-label="Close notifications">✕</button>
    </div>
    <div class="notification-list">
      <div v-if="notifications.length === 0" class="empty-notifications">
        <span class="empty-icon">🔕</span>
        <p>No notifications yet</p>
      </div>
      <div v-else v-for="notif in notifications" :key="notif.id" class="notification-item" :class="notif.type">
        <div class="notif-icon">{{ notif.icon }}</div>
        <div class="notif-content">
          <p class="notif-title">{{ notif.title }}</p>
          <p class="notif-message">{{ notif.message }}</p>
          <span class="notif-time">{{ notif.time }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationCenter',
  props: {
    show: Boolean,
    notifications: {
      type: Array,
      default: () => []
    }
  },
  emits: ['close']
}
</script>

<style scoped>
.notification-center {
  position: fixed;
  top: 70px;
  right: 20px;
  width: 360px;
  max-height: 500px;
  background: var(--surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  z-index: 3000;
  animation: slideIn 0.3s ease;
  display: flex;
  flex-direction: column;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-primary);
}

.notification-header h3 {
  margin: 0;
  font-size: var(--font-size-card-title);
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: var(--font-size-card-title);
  padding: 0.25rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.notification-list {
  overflow-y: auto;
  max-height: 440px;
}

.empty-notifications {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-primary);
  transition: all 0.2s ease;
  cursor: pointer;
}

.notification-item:hover {
  background: var(--bg-hover);
}

.notification-item:last-child {
  border-bottom: none;
}

.notif-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-title {
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
  font-size: var(--font-size-body-sm);
}

.notif-message {
  color: var(--text-secondary);
  margin: 0 0 0.5rem 0;
  font-size: var(--font-size-body-sm);
  line-height: 1.4;
}

.notif-time {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 480px) {
  .notification-center {
    right: 10px;
    left: 10px;
    width: auto;
  }
}
</style>
