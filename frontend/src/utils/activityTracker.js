const MAX_ACTIVITIES = 20

export function trackActivity(icon, text) {
  const activities = JSON.parse(localStorage.getItem('recentActivities') || '[]')
  
  const newActivity = {
    id: Date.now(),
    icon,
    text,
    time: getRelativeTime(new Date()),
    timestamp: new Date().toISOString()
  }
  
  activities.unshift(newActivity)
  
  if (activities.length > MAX_ACTIVITIES) {
    activities.pop()
  }
  
  localStorage.setItem('recentActivities', JSON.stringify(activities))
}

export function getRecentActivities(limit = 5) {
  const activities = JSON.parse(localStorage.getItem('recentActivities') || '[]')
  
  return activities.slice(0, limit).map(activity => ({
    ...activity,
    time: getRelativeTime(new Date(activity.timestamp))
  }))
}

function getRelativeTime(date) {
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
