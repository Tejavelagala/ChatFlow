const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const wsBaseUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://127.0.0.1:8000'

export function getApiBaseUrl() {
  return apiBaseUrl
}

export function getWsBaseUrl() {
  return wsBaseUrl
}
