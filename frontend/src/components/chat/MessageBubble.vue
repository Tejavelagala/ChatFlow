<template>
  <div class="message-wrapper" :class="{ own: message.username === username }">
    <!-- AVATAR (for other users) -->
    <div v-if="message.username !== username" class="message-avatar">
      <div class="avatar-circle" :title="message.username">
        {{ message.username.charAt(0).toUpperCase() }}
      </div>
    </div>

    <div class="message-content">
      <!-- USERNAME & TIMESTAMP (for other users) -->
      <div v-if="message.username !== username" class="message-meta">
        <span class="message-username">{{ message.username }}</span>
        <span class="message-timestamp">{{ formatTimestamp(message.created_at) }}</span>
      </div>

      <!-- MESSAGE BUBBLE -->
      <div 
        class="message-bubble" 
        :class="{ selected: showReactionPicker }"
        @click="$emit('select-message', message.message_id)"
      >
        <!-- REPLY PREVIEW -->
        <div v-if="message.reply_to_data" class="reply-preview">
          <div class="reply-line"></div>
          <div class="reply-content">
            <span class="reply-username">{{ message.reply_to_data.username }}</span>
            <p class="reply-text">{{ message.reply_to_data.message }}</p>
          </div>
        </div>

        <!-- MESSAGE ACTIONS -->
        <div v-if="message.username === username" class="message-actions">
          <button class="action-btn" @click.stop="$emit('edit', message)" title="Edit">✏️</button>
          <button class="action-btn" @click.stop="$emit('delete', message.message_id)" title="Delete">🗑</button>
          <button class="action-btn" @click.stop="$emit('reply', message)" title="Reply">↩️</button>
          <button v-if="canPin" class="action-btn" @click.stop="$emit('pin', message.message_id)" title="Pin">📌</button>
        </div>

        <!-- EDIT MODE -->
        <div v-if="isEditing" class="edit-mode">
          <input
            :value="editedMessage"
            @input="$emit('update-edit', $event.target.value)"
            @keyup.enter="$emit('save-edit', message.message_id)"
            class="edit-input"
            placeholder="Edit message..."
          />
          <button class="save-btn" @click.stop="$emit('save-edit', message.message_id)">Save</button>
        </div>

        <!-- MESSAGE TEXT -->
        <div v-else-if="message.message" class="message-text">
          <TextHighlight :text="message.message" :query="searchQuery" />
        </div>

        <!-- IMAGE -->
        <img v-if="message.image" :src="message.image" loading="lazy" class="message-image" alt="Shared image" />

        <!-- AUDIO -->
        <audio v-if="message.audio" controls class="message-audio">
          <source :src="message.audio" type="audio/webm" />
        </audio>

        <!-- FILE -->
        <FilePreview
          v-if="message.file"
          :fileName="message.file_name"
          :fileSize="message.file_size"
          :fileType="message.file_type"
          :fileUrl="message.file_url"
        />

        <!-- TIMESTAMP (for own messages) -->
        <div v-if="message.username === username" class="message-time">
          {{ formatTime(message.created_at) }}
          <span v-if="message.status" class="message-status">
            <span v-if="message.status === 'sent'" class="status-icon">✓</span>
            <span v-if="message.status === 'delivered'" class="status-icon">✓✓</span>
            <span v-if="message.status === 'seen'" class="status-icon status-seen">✓✓</span>
          </span>
        </div>
      </div>

      <!-- REACTIONS -->
      <div v-if="message.reactions && Object.keys(message.reactions).length > 0" class="reactions-container">
        <button
          v-for="(count, emoji) in message.reactions"
          :key="emoji"
          class="reaction-pill"
          @click.stop="$emit('react', message.message_id, emoji)"
        >
          <span class="reaction-emoji">{{ emoji }}</span>
          <span class="reaction-count">{{ count }}</span>
        </button>
      </div>

      <!-- REACTION PICKER -->
      <div v-if="showReactionPicker" class="reaction-picker">
        <button
          v-for="emoji in reactionEmojis"
          :key="emoji"
          class="picker-emoji"
          @click.stop="$emit('react', message.message_id, emoji)"
        >
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import FilePreview from './FilePreview.vue'
import TextHighlight from '../common/TextHighlight.vue'

export default {
  name: 'MessageBubble',
  components: {
    FilePreview,
    TextHighlight
  },
  props: {
    message: {
      type: Object,
      required: true
    },
    username: {
      type: String,
      required: true
    },
    searchQuery: {
      type: String,
      default: ''
    },
    showReactionPicker: {
      type: Boolean,
      default: false
    },
    isEditing: {
      type: Boolean,
      default: false
    },
    editedMessage: {
      type: String,
      default: ''
    },
    canPin: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      reactionEmojis: ['👍', '❤️', '😂', '😮', '😢', '🔥', '😍', '🤔', '🙏', '🎉', '🔔', '💯']
    }
  },
  methods: {
    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
      
      const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      
      if (messageDate.getTime() === today.getTime()) {
        return `Today • ${time}`
      } else if (messageDate.getTime() === today.getTime() - 86400000) {
        return `Yesterday • ${time}`
      } else {
        return `${date.toLocaleDateString()} • ${time}`
      }
    }
  },
  emits: ['select-message', 'react', 'edit', 'delete', 'reply', 'pin', 'update-edit', 'save-edit']
}
</script>

<style scoped>
.message-wrapper {
  display: flex;
  gap: 0.875rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem 0.75rem;
  transition: background-color 0.2s ease;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: var(--radius-md);
}

.message-wrapper:hover {
  background: var(--message-hover);
}

.message-wrapper.own {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  width: 2.5rem;
  padding-top: 0.25rem;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
  position: relative;
  overflow: hidden;
}

.avatar-circle::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.15), transparent);
  transform: rotate(45deg);
  transition: all 0.5s ease;
}

.avatar-circle:hover {
  transform: scale(1.08) rotate(-5deg);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.avatar-circle:hover::before {
  left: 100%;
}

.message-content {
  flex: 1;
  min-width: 0;
  max-width: 70%;
}

.message-wrapper.own .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-meta {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
  padding: 0 0.25rem;
}

.message-username {
  font-weight: 700;
  font-size: 0.9375rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.01em;
}

.message-timestamp {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  font-weight: 500;
}

.message-bubble {
  position: relative;
  padding: 0.75rem 1rem;
  border-radius: 18px;
  background: var(--message-bg-other);
  color: var(--message-text-other);
  word-wrap: break-word;
  word-break: break-word;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  max-width: 75%;
}

.message-bubble:hover .message-actions {
  opacity: 1;
}

.message-bubble.selected {
  box-shadow: 0 0 0 2px var(--brand-primary);
}

.message-wrapper.own .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 18px 18px 4px 18px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
  max-width: 75%;
}

.message-wrapper:not(.own) .message-bubble {
  background: var(--message-other);
  color: var(--message-other-text);
  border: 1px solid var(--message-other-border);
  border-radius: 18px 18px 18px 4px;
  max-width: 75%;
}

.reply-preview {
  display: flex;
  gap: 0.625rem;
  margin-bottom: 0.625rem;
  padding: 0.625rem 0.75rem;
  background: rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-md);
  font-size: 0.8125rem;
  backdrop-filter: blur(8px);
}

.reply-line {
  width: 4px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
  flex-shrink: 0;
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.6);
}

.reply-content {
  flex: 1;
  min-width: 0;
}

.reply-username {
  font-weight: 600;
  display: block;
  margin-bottom: 0.125rem;
}

.reply-text {
  margin: 0;
  opacity: 0.8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-actions {
  position: absolute;
  top: -1.5rem;
  right: 0.5rem;
  display: flex;
  gap: 0.25rem;
  background: var(--surface-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 0.25rem;
  box-shadow: var(--shadow-md);
  opacity: 0;
  transition: opacity 0.15s ease;
  z-index: 10;
}

.action-btn {
  background: transparent;
  border: none;
  padding: 0.25rem 0.375rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.15s ease;
  color: var(--text-secondary);
}

.action-btn:hover {
  background: var(--surface-hover);
  transform: scale(1.1);
}

.edit-mode {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.edit-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--input-bg);
  color: var(--input-text);
  font-size: 0.875rem;
  outline: none;
}

.edit-input:focus {
  border-color: var(--brand-primary);
}

.save-btn {
  padding: 0.5rem 1rem;
  background: var(--brand-primary);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.save-btn:hover {
  background: var(--brand-primary-hover);
}

.message-text {
  font-size: 0.9375rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: var(--radius-sm);
  margin-top: 0.5rem;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.message-image:hover {
  transform: scale(1.02);
}

.message-audio {
  width: 100%;
  max-width: 300px;
  margin-top: 0.5rem;
  border-radius: var(--radius-sm);
}

.message-time {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  opacity: 0.9;
  font-weight: 500;
}

.message-status {
  display: inline-flex;
  align-items: center;
}

.status-icon {
  font-size: 0.875rem;
  line-height: 1;
}

.status-seen {
  color: #43b581;
  filter: drop-shadow(0 0 2px rgba(67, 181, 129, 0.5));
}

.reactions-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.375rem;
}

.reaction-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.125rem 0.5rem;
  background: var(--surface-secondary);
  border: 1px solid var(--border-primary);
  border-radius: 999px;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.reaction-pill:hover {
  background: var(--surface-hover);
  border-color: var(--primary);
  transform: scale(1.05);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.reaction-emoji {
  font-size: 1rem;
  line-height: 1;
}

.reaction-count {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--text-secondary);
}

.reaction-picker {
  display: flex;
  gap: 0.375rem;
  padding: 0.625rem 0.75rem;
  background: var(--surface-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(102, 126, 234, 0.1);
  margin-top: 0.625rem;
  animation: scaleIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.picker-emoji {
  background: transparent;
  border: none;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  font-size: 1.375rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
}

.picker-emoji:hover {
  background: var(--surface-hover);
  transform: scale(1.25) rotate(-5deg);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(1rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(0.5rem);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>