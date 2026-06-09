import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: {},
    unreadCount: 0,
    browserNotificationsEnabled: localStorage.getItem('notifications') === 'true',
    soundEnabled: localStorage.getItem('sound') === 'true'
  }),

  getters: {
    roomNotifications: (state) => state.notifications,
    totalUnread: (state) => state.unreadCount,
    isBrowserNotificationsEnabled: (state) => state.browserNotificationsEnabled,
    isSoundEnabled: (state) => state.soundEnabled
  },

  actions: {
    addNotification(roomId) {
      if (!this.notifications[roomId]) {
        this.notifications[roomId] = 0
      }
      this.notifications[roomId] += 1
      this.unreadCount += 1
    },

    clearNotifications(roomId) {
      if (this.notifications[roomId]) {
        this.unreadCount -= this.notifications[roomId]
        this.notifications[roomId] = 0
      }
    },

    clearAllNotifications() {
      this.notifications = {}
      this.unreadCount = 0
    },

    toggleBrowserNotifications() {
      this.browserNotificationsEnabled = !this.browserNotificationsEnabled
      localStorage.setItem('notifications', this.browserNotificationsEnabled)
    },

    toggleSound() {
      this.soundEnabled = !this.soundEnabled
      localStorage.setItem('sound', this.soundEnabled)
    }
  }
})
