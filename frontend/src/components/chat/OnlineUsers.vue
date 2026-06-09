<template>
  <div class="online-users-section">
    <div class="section-header">
      <span class="header-icon">🟢</span>
      <h6>Online Now</h6>
      <span class="count-badge">{{ onlineUsers.length }}</span>
    </div>
    <div class="users-list">
      <div
        v-for="(user, index) in onlineUsers"
        :key="index"
        class="online-user"
      >
        <div class="user-avatar online">
          {{ user.charAt(0).toUpperCase() }}
        </div>
        <span class="user-name">{{ user }}</span>
        <span class="status-dot online"></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OnlineUsers',
  props: {
    onlineUsers: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.online-users-section {
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, rgba(67, 181, 129, 0.18) 0%, rgba(67, 181, 129, 0.08) 100%);
  border-radius: var(--radius-lg);
  margin-bottom: 0.875rem;
  border: 1.5px solid rgba(67, 181, 129, 0.25);
  box-shadow: 0 2px 8px rgba(67, 181, 129, 0.15);
}

.header-icon {
  font-size: 1.125rem;
  animation: pulse 2.5s ease-in-out infinite;
  filter: drop-shadow(0 0 4px rgba(67, 181, 129, 0.5));
}

.section-header h6 {
  flex: 1;
  margin: 0;
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--brand-success);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.count-badge {
  background: linear-gradient(135deg, #43b581 0%, #3ba370 100%);
  color: white;
  padding: 0.25rem 0.625rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  box-shadow: 0 2px 6px rgba(67, 181, 129, 0.35);
  min-width: 1.5rem;
  text-align: center;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.online-user {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.75rem 0.875rem;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.online-user:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(67, 181, 129, 0.4);
  transform: translateX(6px);
  box-shadow: 0 4px 12px rgba(67, 181, 129, 0.2);
}

.user-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #43b581 0%, #3ba370 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9375rem;
  flex-shrink: 0;
  position: relative;
  box-shadow: 0 4px 12px rgba(67, 181, 129, 0.4);
  transition: all 0.2s ease;
}

.user-avatar::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  background: #43b581;
  border: 2px solid var(--bg-secondary);
  border-radius: 50%;
  box-shadow: 0 0 0 1px rgba(67, 181, 129, 0.3);
}

.user-name {
  flex: 1;
  font-weight: 700;
  font-size: 0.9375rem;
  color: #1a1a2e;
  letter-spacing: 0.01em;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #43b581;
  box-shadow: 0 0 4px rgba(67, 181, 129, 0.5);
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.75;
    transform: scale(1.15);
  }
}
</style>