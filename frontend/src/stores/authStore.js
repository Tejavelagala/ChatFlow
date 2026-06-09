import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: localStorage.getItem('username'),
    access: localStorage.getItem('access'),
    refresh: localStorage.getItem('refresh'),
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
    currentUser: (state) => state.username
  },

  actions: {
    async login(username, password) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.post('/auth/jwt/create/', { username, password })
        this.access = response.data.access
        this.refresh = response.data.refresh
        this.username = username
        localStorage.setItem('access', this.access)
        localStorage.setItem('refresh', this.refresh)
        localStorage.setItem('username', this.username)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async register(username, password) {
      this.isLoading = true
      this.error = null
      try {
        await api.post('/auth/users/', { username, password })
        return true
      } catch (error) {
        console.error('Registration error:', error.response?.data)
        
        // Handle different error types
        if (error.response?.data) {
          const errorData = error.response.data
          
          // Username errors
          if (errorData.username) {
            this.error = Array.isArray(errorData.username) 
              ? errorData.username[0] 
              : errorData.username
          }
          // Password errors
          else if (errorData.password) {
            this.error = Array.isArray(errorData.password)
              ? errorData.password.join(' ')
              : errorData.password
          }
          // General errors
          else if (errorData.detail) {
            this.error = errorData.detail
          }
          // Non-field errors
          else if (errorData.non_field_errors) {
            this.error = errorData.non_field_errors[0]
          }
          // Fallback
          else {
            this.error = 'Registration failed. Please check your input.'
          }
        } else {
          this.error = error.message || 'Registration failed'
        }
        
        return false
      } finally {
        this.isLoading = false
      }
    },

    logout() {
      this.username = null
      this.access = null
      this.refresh = null
      localStorage.clear()
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    }
  }
})
