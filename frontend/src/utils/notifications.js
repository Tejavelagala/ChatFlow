export async function requestNotificationPermission() {
  if (!("Notification" in window)) {
    return false
  }

  if (Notification.permission === "granted") {
    return true
  }

  const permission = await Notification.requestPermission()
  return permission === "granted"
}

export function showNotification(title, body) {
  if (Notification.permission !== "granted") {
    return
  }

  const notification = new Notification(title, {
    body,
    icon: "/favicon.ico",
  })

  notification.onclick = () => {
    window.focus()
    notification.close()
  }

  // Optional sound alert
  const audio = new Audio('/message.mp3')
  audio.play().catch(() => {
    // Ignore audio play errors (user interaction required)
  })
}