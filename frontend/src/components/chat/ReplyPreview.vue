<template>
  <div class="reply-preview">
    <div class="reply-content">
      <strong>{{ replyingTo.username }}</strong>
      <p>{{ replyingTo.message }}</p>
    </div>
    <button class="cancel-reply" @click="$emit('cancel')">
      ✖
    </button>
  </div>
</template>

<script>
export default {
  name: 'ReplyPreview',
  props: {
    replyingTo: {
      type: Object,
      required: true
    }
  },
  emits: ['cancel']
}
</script>

<style scoped>
.reply-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(102,126,234,0.1);
  padding: 12px;
  border-radius: 14px;
  margin-bottom: 10px;
}

.reply-content p {
  margin: 0;
  font-size: 13px;
  opacity: 0.8;
}

.cancel-reply {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.cancel-reply:hover {
  color: #333;
}
</style>