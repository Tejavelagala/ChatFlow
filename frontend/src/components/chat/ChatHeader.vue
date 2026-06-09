<template>
  <div class="chat-header">
    <div class="connection-status" :class="connectionStatus">
      <span v-if="connectionStatus === 'connected'">🟢 Connected</span>
      <span v-else-if="connectionStatus === 'connecting'">🟡 Connecting...</span>
      <span v-else>🔴 Disconnected</span>
    </div>

    <div>
      <h4>{{ roomName || 'Room Chat' }}</h4>
      <input
        :value="searchQuery"
        @input="$emit('update-search', $event.target.value)"
        type="text"
        placeholder="Search messages..."
        class="message-search"
      />
    </div>

    <div class="d-flex gap-2">
      <button class="btn btn-dark btn-sm" @click="$emit('toggle-theme')">
        {{ darkMode ? '☀' : '🌙' }}
      </button>
      <button class="profile-btn" @click="$emit('show-profile')">
        👤
      </button>
      <button class="btn btn-secondary btn-sm" @click="$emit('open-settings')">
        ⚙️
      </button>
      <button class="btn btn-danger btn-sm" @click="$emit('logout')">
        Logout
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatHeader',
  props: {
    roomName: String,
    darkMode: Boolean,
    searchQuery: String,
    connectionStatus: String
  },
  emits: ['toggle-theme', 'update-search', 'show-profile', 'open-settings', 'logout']
}
</script>

<style scoped>
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%);
  backdrop-filter: blur(20px);
  border-bottom: 2px solid transparent;
  border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: var(--shadow-sm);
}

.connection-status {
  font-size: var(--font-size-body-sm);
  margin-top: 0.25rem;
  font-weight: 600;
  padding: 0.375rem 0.75rem;
  border-radius: 1.25rem;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  box-shadow: var(--shadow-sm);
}

.connection-status.connected {
  color: white;
  background: linear-gradient(135deg, #43b581 0%, #3ba370 100%);
  animation: pulse 2s ease-in-out infinite;
}

.connection-status.connecting {
  color: white;
  background: linear-gradient(135deg, #faa61a 0%, #f59e0b 100%);
  animation: pulse 1s ease-in-out infinite;
}

.connection-status.disconnected {
  color: white;
  background: linear-gradient(135deg, #f04747 0%, #dc2626 100%);
}

.message-search {
  margin-top: 0.75rem;
  width: 280px;
  max-width: 100%;
  padding: 0.625rem 1rem;
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  background: var(--surface-secondary);
  color: var(--text-primary);
  outline: none;
  font-size: var(--font-size-body-sm);
  transition: all 0.2s ease;
}

.message-search:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px var(--primary-light), var(--shadow-md);
  background: var(--surface-hover);
}

.message-search::placeholder {
  color: var(--text-muted);
}

.profile-btn {
  border: none;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.125rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
}

.profile-btn:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: scale(1.1) rotate(5deg);
  box-shadow: var(--shadow-lg);
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.02);
  }
}
</style>