import { defineStore } from 'pinia'
import api from '../services/api'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profile: null,
    isLoading: false,
    error: null
  }),

  getters: {
    userProfile: (state) => state.profile,
    userAvatar: (state) => state.profile?.avatar,
    userBio: (state) => state.profile?.bio,
    isOnline: (state) => state.profile?.online
  },

  actions: {
    async fetchProfile() {
      this.isLoading = true
      try {
        const response = await api.get('/api/chat/profile/')
        this.profile = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

    async updateProfile(data) {
      this.isLoading = true
      try {
        const formData = new FormData()
        
        if (data instanceof FormData) {
          for (let [key, value] of data.entries()) {
            formData.append(key, value)
          }
        } else {
          Object.keys(data).forEach(key => {
            if (data[key] !== null && data[key] !== undefined) {
              formData.append(key, data[key])
            }
          })
        }
        
        const response = await api.put('/api/chat/profile/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        
        this.profile = { ...response.data }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async uploadAvatar(file) {
      try {
        const formData = new FormData()
        formData.append('avatar', file)
        const response = await api.put('/api/chat/profile/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.profile = response.data
        return response.data
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
