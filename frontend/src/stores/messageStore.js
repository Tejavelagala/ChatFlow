import { defineStore } from 'pinia'
import api from '../services/api'

export const useMessageStore = defineStore('message', {
  state: () => ({
    messages: [],
    currentPage: 1,
    hasMoreMessages: true,
    isLoading: false,
    error: null,
    editingMessageId: null,
    editedMessage: '',
    selectedMessageId: null,
    replyingTo: null
  }),

  getters: {
    allMessages: (state) => state.messages,
    messageCount: (state) => state.messages.length,
    isEditing: (state) => !!state.editingMessageId,
    replyingToMessage: (state) => state.replyingTo
  },

  actions: {
    async fetchMessages(roomId, page = 1) {
      this.isLoading = true
      try {
        const response = await api.get(`/api/chat/room-messages/${roomId}/?page=${page}`)
        const newMessages = response.data.results.reverse().map(msg => ({
          username: msg.sender,
          message: msg.content,
          image: msg.image,
          audio: msg.audio,
          file: msg.file,
          file_name: msg.file_name,
          file_size: msg.file_size,
          file_type: msg.file_type,
          file_url: msg.file_url,
          message_id: msg.id,
          is_seen: msg.is_seen,
          created_at: msg.timestamp,
          reactions: msg.reactions || {},
          status: msg.status || 'sent',
          delivered_at: msg.delivered_at,
          seen_at: msg.seen_at
        }))
        this.messages = page === 1 ? newMessages : [...newMessages, ...this.messages]
        this.hasMoreMessages = !!response.data.next
        this.currentPage = page
      } catch (error) {
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

    addMessage(message) {
      this.messages.push(message)
    },

    async deleteMessage(messageId) {
      try {
        await api.delete(`/api/chat/delete-message/${messageId}/`)
        this.messages = this.messages.filter(m => m.message_id !== messageId)
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async editMessage(messageId, content) {
      try {
        await api.put(`/api/chat/edit-message/${messageId}/`, { content })
        const message = this.messages.find(m => m.message_id === messageId)
        if (message) message.message = content
        this.editingMessageId = null
        this.editedMessage = ''
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    updateReactionFromWebSocket(messageId, reactions) {
      const message = this.messages.find(m => m.message_id === messageId)
      if (message) {
        message.reactions = reactions
      }
    },

    async pinMessage(messageId) {
      try {
        await api.post(`/api/chat/pin-message/${messageId}/`)
        const message = this.messages.find(m => m.message_id === messageId)
        if (message) message.is_pinned = true
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async unpinMessage(messageId) {
      try {
        await api.post(`/api/chat/unpin-message/${messageId}/`)
        const message = this.messages.find(m => m.message_id === messageId)
        if (message) message.is_pinned = false
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    startEditing(message) {
      this.editingMessageId = message.message_id
      this.editedMessage = message.message
    },

    cancelEditing() {
      this.editingMessageId = null
      this.editedMessage = ''
    },

    setReplyingTo(message) {
      this.replyingTo = message
    },

    cancelReply() {
      this.replyingTo = null
    },

    selectMessage(messageId) {
      this.selectedMessageId = messageId
    },

    clearMessages() {
      this.messages = []
      this.currentPage = 1
      this.hasMoreMessages = true
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    }
  }
})
