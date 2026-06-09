<template>
  <div v-if="pinnedMessages.length > 0" class="pinned-messages-section">
    <div class="pinned-header">
      <span>📌 Pinned Messages ({{ pinnedMessages.length }})</span>
      <button @click="showPinned = !showPinned" class="toggle-btn">
        {{ showPinned ? '▼' : '▶' }}
      </button>
    </div>
    
    <div v-if="showPinned" class="pinned-list">
      <div
        v-for="msg in pinnedMessages"
        :key="msg.message_id"
        class="pinned-item"
      >
        <div class="pinned-content">
          <strong>{{ msg.username }}:</strong>
          <span>{{ msg.message }}</span>
        </div>
        <button
          v-if="isRoomOwner"
          @click="$emit('unpin', msg.message_id)"
          class="unpin-btn"
        >
          ✖
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PinnedMessages',
  props: {
    pinnedMessages: {
      type: Array,
      default: () => []
    },
    isRoomOwner: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showPinned: true
    }
  }
}
</script>

<style scoped>
.pinned-messages-section {
  background: #fff3cd;
  border-bottom: 2px solid #ffc107;
  padding: 12px 20px;
}

.pinned-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #856404;
}

.toggle-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #856404;
}

.pinned-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pinned-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.7);
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
}

.pinned-content {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.unpin-btn {
  background: transparent;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 16px;
  padding: 0 8px;
}

.unpin-btn:hover {
  transform: scale(1.2);
}
</style>
