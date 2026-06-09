import { defineStore } from 'pinia'

export const usePresenceStore = defineStore('presence', {
  state: () => ({
    onlineUsers: [],
    typingUsers: {},
    lastSeen: {}
  }),

  getters: {
    allOnlineUsers: (state) => state.onlineUsers,
    isUserOnline: (state) => (username) => state.onlineUsers.includes(username),
    isUserTyping: (state) => (username) => !!state.typingUsers[username],
    typingUser: (state) => Object.keys(state.typingUsers)[0] || ''
  },

  actions: {
    setOnlineUsers(users) {
      this.onlineUsers = users
    },

    addOnlineUser(username) {
      if (!this.onlineUsers.includes(username)) {
        this.onlineUsers.push(username)
      }
    },

    removeOnlineUser(username) {
      this.onlineUsers = this.onlineUsers.filter(u => u !== username)
    },

    setUserTyping(username) {
      this.typingUsers[username] = true
      setTimeout(() => {
        delete this.typingUsers[username]
      }, 1500)
    },

    clearTyping(username) {
      delete this.typingUsers[username]
    },

    setLastSeen(username, timestamp) {
      this.lastSeen[username] = timestamp
    }
  }
})
