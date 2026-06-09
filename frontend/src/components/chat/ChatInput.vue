<template>
  <div class="chat-input-wrapper">
    <!-- REPLY PREVIEW -->
    <ReplyPreview
      v-if="replyingTo"
      :replyingTo="replyingTo"
      @cancel="$emit('cancel-reply')"
    />

    <!-- IMAGE PREVIEW -->
    <div v-if="imagePreview" class="image-preview">
      <img :src="imagePreview" class="preview-img" />
      <div class="preview-actions">
        <button class="btn btn-success btn-sm" @click="$emit('send-image')">Send</button>
        <button class="btn btn-danger btn-sm" @click="$emit('cancel-image')">Cancel</button>
      </div>
    </div>

    <!-- INPUT COMPOSER -->
    <div class="message-composer">
      <button class="composer-btn" @click="toggleEmojiPicker" title="Add emoji">😊</button>
      
      <input 
        type="file"
        ref="imageInput"
        hidden
        accept="image/*"
        @change="$emit('upload-image', $event)"
      />
      <button class="composer-btn" @click="$refs.imageInput.click()" title="Upload image">🖼️</button>

      <FileUpload 
        :roomId="roomId" 
        @file-uploaded="$emit('file-uploaded', $event)"
      />

      <input
        :value="message"
        @input="$emit('update-message', $event.target.value)"
        @keydown="handleKeyDown"
        type="text"
        class="message-input"
        placeholder="Type your message..."
        aria-label="Message input"
      />

      <button 
        class="composer-btn record-btn" 
        :class="{ recording: recording }"
        @click="$emit('toggle-recording')"
        title="Voice message"
      >
        {{ recording ? '⏹️' : '🎤' }}
      </button>

      <button class="send-btn" @click="$emit('send-message')" title="Send message">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
        </svg>
      </button>
    </div>

    <!-- EMOJI PICKER -->
    <div v-if="showEmojiPicker" class="emoji-picker" v-click-outside="closeEmojiPicker">
      <div class="emoji-grid">
        <button
          v-for="emoji in allEmojis"
          :key="emoji"
          class="emoji-item"
          @click="addEmoji(emoji)"
        >
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import FileUpload from '../common/FileUpload.vue'
import ReplyPreview from './ReplyPreview.vue'

const EMOJI_CATEGORIES = {
  smileys: [
    '😀', '😁', '😂', '😃', '😄', '😅', '😆', '😇', '😈', '😉',
    '😊', '😋', '😌', '😍', '😎', '😏', '😐', '😑', '😒', '😓',
    '😔', '😕', '😖', '😗', '😘', '😙', '😚', '😛', '😜', '😝',
    '😞', '😟', '😠', '😡', '😢', '😣', '😤', '😥', '😦', '😧'
  ],
  gestures: [
    '👋', '👏', '🙌', '👐', '🤝', '🤲', '🤜', '🤛', '✊', '👊',
    '👍', '👎', '☝️', '👆', '👇', '👈', '👉', '🖐️', '✋', '🖖'
  ],
  hearts: [
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔',
    '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟', '💌', '💋'
  ],
  symbols: [
    '🔥', '💯', '✨', '⭐', '🌟', '💫', '🎉', '🎊', '🎈', '🎁',
    '🏆', '🥇', '🥈', '🥉', '🎖️', '🏅', '⚡', '💥', '🌈', '☀️'
  ]
}

export default {
  name: 'ChatInput',
  components: {
    FileUpload,
    ReplyPreview
  },
  props: {
    message: {
      type: String,
      default: ''
    },
    replyingTo: {
      type: Object,
      default: null
    },
    imagePreview: {
      type: String,
      default: null
    },
    recording: {
      type: Boolean,
      default: false
    },
    roomId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showEmojiPicker: false
    }
  },
  computed: {
    allEmojis() {
      return [
        ...EMOJI_CATEGORIES.smileys,
        ...EMOJI_CATEGORIES.gestures,
        ...EMOJI_CATEGORIES.hearts,
        ...EMOJI_CATEGORIES.symbols
      ]
    }
  },
  methods: {
    toggleEmojiPicker() {
      this.showEmojiPicker = !this.showEmojiPicker
    },
    closeEmojiPicker() {
      this.showEmojiPicker = false
    },
    addEmoji(emoji) {
      this.$emit('add-emoji', emoji)
      this.showEmojiPicker = false
    },
    handleKeyDown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        this.$emit('send-message')
      }
      if (event.key === 'Escape') {
        if (this.replyingTo) {
          this.$emit('cancel-reply')
        }
        if (this.showEmojiPicker) {
          this.closeEmojiPicker()
        }
      }
    }
  },
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value()
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  },
  emits: [
    'update-message',
    'send-message',
    'cancel-reply',
    'send-image',
    'cancel-image',
    'upload-image',
    'file-uploaded',
    'toggle-recording',
    'add-emoji'
  ]
}
</script>

<style scoped>
.chat-input-wrapper {
  padding: 1rem;
  background: var(--bg-primary);
  border-top: 1px solid var(--border-subtle);
}

.image-preview {
  background: var(--surface-secondary);
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1rem;
}

.preview-img {
  max-width: 200px;
  max-height: 200px;
  border-radius: var(--radius-sm);
  margin-bottom: 0.75rem;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
}

.message-composer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--input-bg);
  border-radius: 999px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  min-height: 52px;
}

.message-composer:focus-within {
  background: var(--surface-hover);
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.12), 0 6px 16px rgba(102, 126, 234, 0.25);
  transform: translateY(-1px);
}

.composer-btn {
  background: transparent;
  border: none;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.25rem;
  color: var(--text-secondary);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 36px;
  height: 36px;
}

.composer-btn:hover {
  background: var(--surface-hover);
  color: var(--primary);
  transform: scale(1.1);
}

.record-btn.recording {
  background: linear-gradient(135deg, rgba(240, 71, 71, 0.25) 0%, rgba(220, 38, 38, 0.25) 100%);
  color: #f04747;
  animation: recordPulse 1.5s ease-in-out infinite;
  box-shadow: 0 0 16px rgba(240, 71, 71, 0.5), 0 0 0 4px rgba(240, 71, 71, 0.1);
}

.message-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.625rem 0.75rem;
  font-size: 0.9375rem;
  color: var(--input-text);
  font-weight: 500;
}

.message-input::placeholder {
  color: var(--input-placeholder);
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 0.625rem;
  border-radius: 50%;
  cursor: pointer;
  color: white;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
  width: 40px;
  height: 40px;
}

.send-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.send-btn:hover::before {
  width: 300px;
  height: 300px;
}

.send-btn:hover {
  background: linear-gradient(135deg, #5a56e0 0%, #6a3f92 100%);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
}

.send-btn svg {
  position: relative;
  z-index: 1;
}

.send-btn:active {
  transform: translateY(0) scale(1);
}

.emoji-picker {
  position: absolute;
  bottom: 100%;
  left: 1rem;
  margin-bottom: 0.75rem;
  background: var(--surface-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(102, 126, 234, 0.1);
  padding: 1rem;
  max-width: 320px;
  z-index: 100;
  animation: slideUp 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 0.25rem;
  max-height: 240px;
  overflow-y: auto;
}

.emoji-item {
  background: transparent;
  border: none;
  padding: 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.emoji-item:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  transform: scale(1.25) rotate(-5deg);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

@keyframes recordPulse {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.7;
    transform: scale(1.05);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(0.5rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>