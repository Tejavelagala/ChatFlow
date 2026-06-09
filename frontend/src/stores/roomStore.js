import { defineStore } from 'pinia'
import api from '../services/api'

export const useRoomStore = defineStore('room', {
  state: () => ({
    rooms: [],
    selectedRoom: null,
    currentRoom: null,
    members: [],
    pinnedMessages: [],
    isLoading: false,
    error: null,
    roomsCache: {}
  }),

  getters: {
    allRooms: (state) => state.rooms,
    selectedRoomData: (state) => state.selectedRoom,
    roomMembers: (state) => state.members,
    pinnedMsgs: (state) => state.pinnedMessages,
    isRoomOwner: (state) => (username) => state.currentRoom?.owner === username
  },

  actions: {
    async fetchRooms() {
      this.isLoading = true
      try {
        const response = await api.get('/api/chat/all-rooms/')
        this.rooms = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

    async createRoom(roomName) {
      try {
        const response = await api.post('/api/chat/create-room/', { room_name: roomName })
        this.rooms.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async deleteRoom(roomId) {
      try {
        await api.delete(`/api/chat/delete-room/${roomId}/`)
        this.rooms = this.rooms.filter(r => r.room_id !== roomId)
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async joinRoom(roomId) {
      try {
        const response = await api.post(`/api/chat/join-room/${roomId}/`)
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async selectRoom(roomId) {
      if (this.roomsCache[roomId]) {
        this.selectedRoom = this.roomsCache[roomId]
        this.currentRoom = this.roomsCache[roomId]
        return
      }
      try {
        const response = await api.get(`/api/chat/room/${roomId}/`)
        this.selectedRoom = response.data
        this.currentRoom = response.data
        this.roomsCache[roomId] = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async fetchMembers(roomId) {
      try {
        const response = await api.get(`/api/chat/room-members/${roomId}/`)
        this.members = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async fetchPinnedMessages(roomId) {
      try {
        const response = await api.get(`/api/chat/pinned-messages/${roomId}/`)
        this.pinnedMessages = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async promoteUser(roomId, username, role) {
      try {
        await api.post(`/api/chat/promote-user/${roomId}/`, { username, role })
        const member = this.members.find(m => m.username === username)
        if (member) member.role = role
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async banUser(roomId, username) {
      try {
        await api.post(`/api/chat/ban-user/${roomId}/`, { username })
        const member = this.members.find(m => m.username === username)
        if (member) member.is_banned = true
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async muteUser(roomId, username) {
      try {
        await api.post(`/api/chat/mute-user/${roomId}/`, { username })
        const member = this.members.find(m => m.username === username)
        if (member) member.is_muted = true
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async leaveRoom(roomId) {
      try {
        await api.post(`/api/chat/leave-room/${roomId}/`)
        this.rooms = this.rooms.filter(r => r.room_id !== roomId)
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    }
  }
})
