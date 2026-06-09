<template>
  <div v-if="typingUser" class="typing-indicator">
    <div class="typing-avatar">
      {{ typingUser.charAt(0).toUpperCase() }}
    </div>
    <div class="typing-content">
      <span class="typing-text">{{ typingUser }} is typing</span>
      <div class="typing-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TypingIndicator',
  props: {
    typingUser: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  animation: fadeIn 0.3s ease;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.05), transparent);
  border-radius: var(--radius-md);
  margin: 0 1rem;
}

.typing-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8125rem;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

.typing-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.typing-text {
  font-weight: 600;
  color: var(--text-primary);
}

.typing-dots {
  display: flex;
  gap: 0.375rem;
  align-items: center;
  padding: 0.375rem 0.625rem;
  background: var(--surface-secondary);
  border-radius: 999px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.typing-dots .dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: var(--radius-round);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  animation: typingBounce 1.4s infinite ease-in-out;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.typing-dots .dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dots .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-0.5rem) scale(1.1);
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>