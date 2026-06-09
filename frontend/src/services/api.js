import axios from 'axios'
import { getApiBaseUrl } from '../config/runtime'
import { notifyError } from '../utils/toast'

const api = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
})

// REQUEST INTERCEPTOR: Add access token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// RESPONSE INTERCEPTOR: Handle token refresh & errors
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // Token expired - attempt refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refresh = localStorage.getItem('refresh')
        const response = await axios.post(
          `${getApiBaseUrl()}/auth/jwt/refresh/`,
          { refresh }
        )

        const newAccess = response.data.access
        localStorage.setItem('access', newAccess)
        originalRequest.headers.Authorization = `Bearer ${newAccess}`

        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed - logout user
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    // Centralized error handling
    if (error.response?.status === 403) {
      notifyError('Permission denied')
    } else if (error.response?.status === 404) {
      notifyError('Resource not found')
    } else if (error.response?.status >= 500) {
      notifyError('Server error. Please try again later')
    } else if (error.message === 'Network Error') {
      notifyError('Network error. Check your connection')
    }

    return Promise.reject(error)
  }
)

export default api
