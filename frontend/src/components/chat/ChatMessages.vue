<template>
  <div class="chat-messages" @scroll="$emit('scroll', $event)">
    <!-- LOADING SKELETON -->
    <div v-if="loadingMessages" class="loading-skeleton">
      <SkeletonLoader v-for="i in 5" :key="i" variant="message" />
    </div>

    <!-- PINNED MESSAGES -->
    <PinnedMessages
      :pinnedMessages="pinnedMessages"
      :isRoomOwner="isRoomOwner"
      @unpin="$emit('unpin-message', $event)"
    />

    <!-- EMPTY STATE -->
    <div v-if="messages.length === 0 && !loadingMessages" class="empty-state">
      <div class="empty-icon">💬</div>
      <h3 class="empty-title">Welcome to {{ roomName || 'the chat' }}</h3>
      <p class="empty-text">Start the conversation by sending a message.</p>
    </div>

    <!-- NO SEARCH RESULTS -->
    <div v-if="filteredMessages.length === 0 && searchQuery && messages.length > 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3 class="empty-title">No messages found</h3>
      <p class="empty-text">Try searching with different keywords.</p>
    </div>

    <!-- MESSAGES -->
    <MessageBubble
      v-for="(msg, index) in filteredMessages"
      :key="index"
      :message="msg"
      :username="username"
      :searchQuery="searchQuery"
      :showReactionPicker="selectedMessageId === msg.message_id"
      :isEditing="editingMessageId === msg.message_id"
      :editedMessage="editedMessage"
      :canPin="isRoomOwner"
      @select-message="$emit('select-message', $event)"
      @react="$emit('react-message', $event, arguments[1])"
      @edit="$emit('start-editing', $event)"
      @delete="$emit('delete-message', $event)"
      @reply="$emit('reply-message', $event)"
      @pin="$emit('pin-message', $event)"
      @update-edit="$emit('update-edit', $event)"
      @save-edit="$emit('save-edit', $event)"
    />
  </div>
</template>

<script>
import MessageBubble from './MessageBubble.vue'
import PinnedMessages from './PinnedMessages.vue'
import SkeletonLoader from '../common/SkeletonLoader.vue'

export default {
  name: 'ChatMessages',
  components: {
    MessageBubble,
    PinnedMessages,
    SkeletonLoader
  },
  props: {
    messages: {
      type: Array,
      default: () => []
    },
    filteredMessages: {
      type: Array,
      default: () => []
    },
    searchQuery: {
      type: String,
      default: ''
    },
    loadingMessages: {
      type: Boolean,
      default: false
    },
    pinnedMessages: {
      type: Array,
      default: () => []
    },
    isRoomOwner: {
      type: Boolean,
      default: false
    },
    username: {
      type: String,
      required: true
    },
    selectedMessageId: {
      type: [String, Number],
      default: null
    },
    editingMessageId: {
      type: [String, Number],
      default: null
    },
    editedMessage: {
      type: String,
      default: ''
    },
    roomName: {
      type: String,
      default: ''
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        this.$el.scrollTop = this.$el.scrollHeight
      })
    }
  },
  emits: [
    'scroll',
    'unpin-message',
    'select-message',
    'react-message',
    'start-editing',
    'delete-message',
    'reply-message',
    'pin-message',
    'update-edit',
    'save-edit'
  ]
}
</script>

<style scoped>
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 1.25rem;
  scroll-behavior: smooth;
  background: var(--bg-primary);
}

.loading-skeleton {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.loading-indicator {
  color: var(--text-secondary);
  font-size: 0.875rem;
  padding: 0.75rem;
  text-align: center;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.empty-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  padding: 3rem 2rem;
  animation: fadeIn 0.4s ease;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.01em;
}

.empty-text {
  font-size: 0.9375rem;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

@keyframes fadeIn {
  from { 
    opacity: 0;
    transform: translateY(1.5rem);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-messages::-webkit-scrollbar {
  width: 10px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 5px;
  border: 2px solid var(--bg-primary);
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--interactive-hover);
}
</style>