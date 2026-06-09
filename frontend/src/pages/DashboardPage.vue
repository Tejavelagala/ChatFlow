<template>
  <div class="dashboard-wrapper">
    <!-- NAVBAR -->
    <nav class="dashboard-navbar" role="navigation" aria-label="Main navigation">
      <div class="navbar-left">
        <h1 class="navbar-logo">💬 ChatFlow</h1>
      </div>
      <div class="navbar-right">
        <ThemeToggle />
        <button
          class="navbar-btn"
          @click="showNotifications = !showNotifications"
          title="Notifications"
          aria-label="Open notifications"
          aria-describedby="notif-desc"
        >
          <span aria-hidden="true">🔔</span>
          <span id="notif-desc" class="sr-only">Notifications</span>
        </button>
        <button
          class="navbar-btn"
          @click="goToProfile"
          title="Profile"
          aria-label="Open profile"
          aria-describedby="profile-desc"
        >
          <span aria-hidden="true">👤</span>
          <span id="profile-desc" class="sr-only">Profile</span>
        </button>
        <button
          class="navbar-btn"
          @click="goToSettings"
          title="Settings"
          aria-label="Open settings"
          aria-describedby="settings-desc"
        >
          <span aria-hidden="true">⚙️</span>
          <span id="settings-desc" class="sr-only">Settings</span>
        </button>
        <button
          class="navbar-btn"
          @click="logout"
          title="Logout"
          aria-label="Logout from account"
          aria-describedby="logout-desc"
        >
          <span aria-hidden="true">🚪</span>
          <span id="logout-desc" class="sr-only">Logout</span>
        </button>
      </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main class="dashboard-container" role="main">
      <!-- HERO SECTION -->
      <section class="hero-section" aria-labelledby="welcome-heading">
        <div class="hero-content">
          <h2 id="welcome-heading" class="hero-title">Welcome back, {{ username }} 👋</h2>
          <p class="hero-subtitle">Continue collaborating with your team</p>
        </div>
        <button
          class="btn-create-room"
          @click="showCreateModal = true"
          aria-label="Create a new room"
        >
          <span aria-hidden="true">+</span> Create Room
        </button>
      </section>

      <!-- STATS CARDS -->
      <section class="stats-section" aria-labelledby="stats-heading">
        <h2 id="stats-heading" class="sr-only">Dashboard Statistics</h2>
        <div class="stats-grid">
          <article class="stat-card" aria-label="Total rooms">
            <div class="stat-icon" aria-hidden="true">💬</div>
            <div class="stat-content">
              <div class="stat-value" role="status">{{ rooms.length }}</div>
              <div class="stat-label">Rooms</div>
            </div>
          </article>
          <article class="stat-card" aria-label="Total members">
            <div class="stat-icon" aria-hidden="true">👥</div>
            <div class="stat-content">
              <div class="stat-value" role="status">{{ totalMembers }}</div>
              <div class="stat-label">Members</div>
            </div>
          </article>
          <article class="stat-card" aria-label="Total messages">
            <div class="stat-icon" aria-hidden="true">💌</div>
            <div class="stat-content">
              <div class="stat-value" role="status">{{ totalMessages }}</div>
              <div class="stat-label">Messages</div>
            </div>
          </article>
        </div>
      </section>

      <!-- LOADING STATE -->
      <section v-if="room.isLoading" class="loading-section" aria-label="Loading rooms">
        <div class="loading-grid">
          <SkeletonLoader v-for="i in 6" :key="i" variant="room" />
        </div>
      </section>

      <!-- EMPTY STATE -->
      <section v-else-if="rooms.length === 0" class="empty-section" aria-label="No rooms available">
        <EmptyState
          icon="💬"
          title="No Rooms Yet"
          message="Create your first room and start collaborating"
          actionText="Create Room"
          @action="showCreateModal = true"
        />
      </section>

      <!-- ROOM GRID -->
      <section v-else class="rooms-section" aria-labelledby="rooms-heading">
        <h2 id="rooms-heading" class="section-title">Your Rooms</h2>
        <div class="rooms-grid" role="list">
          <article
            v-for="room in rooms"
            :key="room.room_id"
            class="room-card"
            role="listitem"
            :aria-label="`${room.room_name} room with ${room.member_count || 1} members`"
          >
            <div class="room-header">
              <div class="room-avatar" aria-hidden="true">{{ getRoomAvatar(room.room_name) }}</div>
              <div class="room-info">
                <h3 class="room-name">{{ room.room_name }}</h3>
                <p class="room-meta">
                  <span class="room-members">{{ room.member_count || 1 }} Members</span>
                  <span class="room-separator" aria-hidden="true">•</span>
                  <span class="room-activity">{{ getLastActivity() }}</span>
                </p>
              </div>
            </div>
            <div class="room-actions">
              <button
                class="room-join-btn"
                @click="joinRoom(room.room_id)"
                :aria-label="`Open ${room.room_name} chat`"
              >
                Open Chat
              </button>
              <button
                v-if="room.owner === username"
                class="room-delete-btn"
                @click.stop="confirmDeleteRoom(room.room_id, room.room_name)"
                :aria-label="`Delete ${room.room_name} room`"
                title="Delete room"
              >
                🗑️
              </button>
            </div>
          </article>
        </div>
      </section>
    </main>

    <!-- CREATE ROOM MODAL -->
    <Modal
      :modelValue="showCreateModal"
      @close="showCreateModal = false"
      role="dialog"
      aria-labelledby="create-room-title"
      aria-describedby="create-room-desc"
    >
      <template #header>
        <h2 id="create-room-title" class="modal-title">Create New Room</h2>
      </template>
      <template #body>
        <p id="create-room-desc" class="sr-only">Enter a name for your new chat room</p>
        <div class="modal-form">
          <label for="room-name-input" class="input-label">Room Name</label>
          <input
            id="room-name-input"
            v-model="roomName"
            type="text"
            placeholder="e.g., General Chat"
            class="input-modern"
            @keyup.enter="createRoom"
            @keyup.escape="showCreateModal = false"
            aria-required="true"
            :aria-invalid="roomNameError ? 'true' : 'false'"
            aria-describedby="room-name-error"
          />
          <span v-if="roomNameError" id="room-name-error" class="input-error" role="alert">
            {{ roomNameError }}
          </span>
        </div>
      </template>
      <template #footer>
        <button
          class="btn-modern btn-secondary"
          @click="showCreateModal = false"
          aria-label="Cancel creating room"
        >
          Cancel
        </button>
        <button
          class="btn-modern btn-primary"
          @click="createRoom"
          :disabled="loading || !roomName.trim()"
          :aria-busy="loading"
          aria-label="Create new room"
        >
          {{ loading ? 'Creating...' : 'Create Room' }}
        </button>
      </template>
    </Modal>

    <!-- DELETE ROOM CONFIRMATION -->
    <ConfirmDialog
      :show="showDeleteConfirm"
      title="Delete Room?"
      :message="roomToDelete ? `Are you sure you want to delete '${roomToDelete.name}'? This action cannot be undone.` : ''"
      type="danger"
      confirmText="Delete"
      cancelText="Cancel"
      @confirm="deleteRoom"
      @cancel="cancelDelete"
    />

    <!-- NOTIFICATION CENTER -->
    <NotificationCenter
      :show="showNotifications"
      :notifications="notifications"
      @close="showNotifications = false"
    />
  </div>
</template>

<script>
import { useAuthStore } from '../stores/authStore'
import { useRoomStore } from '../stores/roomStore'
import { useToast } from 'vue-toastification'
import { trackActivity } from '../utils/activityTracker'
import Modal from '../components/common/Modal.vue'
import EmptyState from '../components/common/EmptyState.vue'
import SkeletonLoader from '../components/common/SkeletonLoader.vue'
import ThemeToggle from '../components/common/ThemeToggle.vue'
import ConfirmDialog from '../components/common/ConfirmDialog.vue'
import NotificationCenter from '../components/common/NotificationCenter.vue'

export default {
  name: 'DashboardPage',
  components: {
    Modal,
    EmptyState,
    SkeletonLoader,
    ThemeToggle,
    ConfirmDialog,
    NotificationCenter
  },
  setup() {
    return {
      auth: useAuthStore(),
      room: useRoomStore()
    }
  },
  data() {
    return {
      roomName: '',
      loading: false,
      showCreateModal: false,
      roomNameError: '',
      showDeleteConfirm: false,
      roomToDelete: null,
      showNotifications: false,
      notifications: []
    }
  },
  computed: {
    username() {
      return this.auth.username || 'User'
    },
    rooms() {
      return this.room.rooms || []
    },
    totalMembers() {
      return this.rooms.reduce((sum, r) => sum + (r.member_count || 1), 0)
    },
    totalMessages() {
      return this.rooms.reduce((sum, r) => sum + (r.message_count || 0), 0)
    },
    getInitials() {
      return (name) => {
        return name
          .split(' ')
          .map(w => w[0])
          .join('')
          .toUpperCase()
          .slice(0, 2)
      }
    },
    getRandomEmoji() {
      const emojis = ['💬', '🚀', '📚', '🎯', '⚡', '🔥', '✨', '🎨', '🌟', '💡']
      return () => emojis[Math.floor(Math.random() * emojis.length)]
    }
  },
  methods: {
    validateRoomName() {
      const trimmed = this.roomName.trim()
      if (!trimmed) {
        this.roomNameError = 'Room name is required'
        return false
      }
      if (trimmed.length < 2) {
        this.roomNameError = 'Room name must be at least 2 characters'
        return false
      }
      if (trimmed.length > 50) {
        this.roomNameError = 'Room name must not exceed 50 characters'
        return false
      }
      this.roomNameError = ''
      return true
    },
    async createRoom() {
      const toast = useToast()

      if (!this.validateRoomName()) {
        return
      }

      this.loading = true
      try {
        await this.room.createRoom(this.roomName.trim())
        toast.success('Room created successfully! 🎉')
        trackActivity('🚀', `Created room "${this.roomName.trim()}"`)
        this.roomName = ''
        this.roomNameError = ''
        this.showCreateModal = false
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Failed to create room'
        toast.error(errorMessage)
        this.roomNameError = errorMessage
      } finally {
        this.loading = false
      }
    },
    joinRoom(roomId) {
      this.$router.push(`/chat/${roomId}`)
    },
    logout() {
      this.auth.logout()
      this.$router.push('/login')
    },
    goToSettings() {
      this.$router.push('/settings')
    },
    goToProfile() {
      this.$router.push('/profile')
    },
    getRoomAvatar(roomName) {
      const seed = roomName.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      const emojis = ['💬', '🚀', '📚', '🎯', '⚡', '🔥', '✨', '🎨', '🌟', '💡']
      return emojis[seed % emojis.length]
    },
    getLastActivity() {
      const minutes = Math.floor(Math.random() * 30) + 1
      if (minutes === 1) return 'Active now'
      if (minutes < 5) return `${minutes} min ago`
      if (minutes < 60) return `${minutes} min ago`
      return 'Recently active'
    },
    confirmDeleteRoom(roomId, roomName) {
      this.roomToDelete = { id: roomId, name: roomName }
      this.showDeleteConfirm = true
    },
    async deleteRoom() {
      const toast = useToast()
      try {
        await this.room.deleteRoom(this.roomToDelete.id)
        toast.success('Room deleted successfully')
        this.showDeleteConfirm = false
        this.roomToDelete = null
      } catch (error) {
        toast.error('Failed to delete room')
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.roomToDelete = null
    }
  },
  watch: {
    showCreateModal(newVal) {
      if (!newVal) {
        this.roomName = ''
        this.roomNameError = ''
      }
    },
    '$route'() {
      if (this.$route.path === '/dashboard') {
        this.room.fetchRooms()
      }
    }
  },
  async mounted() {
    try {
      await this.room.fetchRooms()
    } catch (error) {
      const toast = useToast()
      toast.error('Failed to load rooms')
    }
  },
  async activated() {
    // Refresh data when navigating back to dashboard
    try {
      await this.room.fetchRooms()
    } catch (error) {
      console.error('Failed to refresh rooms:', error)
    }
  }
}
</script>

<style scoped>
/* ACCESSIBILITY */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg-primary);
}

/* NAVBAR */
.dashboard-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--surface);
  border-bottom: 1px solid var(--border-primary);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  gap: 1rem;
}

.navbar-left {
  display: flex;
  align-items: center;
  min-width: 0;
}

.navbar-logo {
  font-size: var(--font-size-section-title);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  white-space: nowrap;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.navbar-btn {
  width: 40px;
  height: 40px;
  min-width: 40px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-card-title);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.navbar-btn:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
}

.navbar-btn:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.navbar-btn:active {
  transform: translateY(0);
}

/* MAIN CONTENT */
.dashboard-container {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* HERO SECTION */
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
  padding: 24px;
  background: var(--surface);
  border-radius: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-primary);
}

.hero-content {
  flex: 1;
  min-width: 250px;
}

.hero-title {
  font-size: var(--font-size-page-title);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: var(--font-size-card-title);
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.btn-create-room {
  padding: 0.875rem 1.75rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-md);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
  height: var(--input-height);
}

.btn-create-room:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-create-room:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.btn-create-room:active {
  transform: translateY(0);
}

.btn-create-room:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* STATS SECTION */
.stats-section {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border-primary);
  border-radius: 20px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-card:focus-within {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.stat-icon {
  font-size: 2rem;
  flex-shrink: 0;
  line-height: 1;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: var(--font-size-section-title);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: var(--font-size-body-sm);
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

/* LOADING SECTION */
.loading-section {
  width: 100%;
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* EMPTY SECTION */
.empty-section {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* ROOMS SECTION */
.rooms-section {
  width: 100%;
}

.section-title {
  font-size: var(--font-size-section-title);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1.5rem 0;
  line-height: 1.2;
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  list-style: none;
  padding: 0;
  margin: 0;
}

/* ROOM CARD */
.room-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.room-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.room-card:focus-within {
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.room-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.room-avatar {
  width: 52px;
  height: 52px;
  min-width: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: var(--text-inverse);
  border-radius: 50%;
  font-weight: 600;
  font-size: 1.5rem;
  line-height: 1;
}

.room-info {
  flex: 1;
  min-width: 0;
}

.room-name {
  font-size: var(--font-size-card-title);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
  word-break: break-word;
}

.room-meta {
  font-size: var(--font-size-body-sm);
  color: var(--text-secondary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.room-members {
  white-space: nowrap;
}

.room-separator {
  opacity: 0.5;
}

.room-activity {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
  white-space: nowrap;
}

.room-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.room-join-btn {
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: var(--font-size-body-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex: 1;
}

.room-delete-btn {
  padding: 0.75rem;
  background: transparent;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-body);
  cursor: pointer;
  transition: all var(--transition-fast);
  opacity: 0;
}

.room-card:hover .room-delete-btn {
  opacity: 1;
}

.room-delete-btn:hover {
  background: #fee;
  border-color: #ef4444;
}

.room-join-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

.room-join-btn:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.room-join-btn:active {
  transform: translateY(0);
}

/* MODAL FORM */
.modal-title {
  margin: 0;
  font-size: var(--font-size-section-title);
  font-weight: 600;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-label {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  font-size: var(--font-size-body-sm);
}

.input-modern {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: var(--font-size-body);
  transition: all var(--transition-fast);
  font-family: inherit;
}

.input-modern:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
}

.input-modern:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-error {
  display: block;
  color: #ef4444;
  font-size: var(--font-size-body-sm);
  margin-top: 0.25rem;
}

.btn-modern {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: var(--font-size-body-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: inherit;
}

.btn-primary {
  background: var(--primary);
  color: var(--text-inverse);
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

.btn-primary:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
}

.btn-secondary:focus {
  outline: 2px solid var(--text-primary);
  outline-offset: 2px;
}

/* RESPONSIVE DESIGN */
@media (max-width: 1024px) {
  .dashboard-container {
    padding: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }

  .rooms-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard-navbar {
    padding: 1rem;
  }

  .navbar-logo {
    font-size: var(--font-size-card-title);
  }

  .dashboard-container {
    padding: 1rem;
    gap: 1.5rem;
  }

  .hero-section {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .btn-create-room {
    width: 100%;
    justify-content: center;
  }

  .hero-title {
    font-size: var(--font-size-section-title);
  }

  .hero-subtitle {
    font-size: var(--font-size-body);
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .rooms-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .room-card {
    padding: 1rem;
    gap: 0.75rem;
  }

  .section-title {
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  .dashboard-navbar {
    padding: 0.75rem;
  }

  .navbar-logo {
    font-size: 1.1rem;
  }

  .navbar-btn {
    width: 36px;
    height: 36px;
    font-size: 1.1rem;
  }

  .dashboard-container {
    padding: 0.75rem;
    gap: 1rem;
  }

  .hero-title {
    font-size: 1.25rem;
  }

  .hero-subtitle {
    font-size: 0.875rem;
  }

  .btn-create-room {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }

  .stat-card {
    padding: 0.75rem;
    gap: 1rem;
  }

  .stat-icon {
    font-size: 1.5rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .room-card {
    padding: 0.75rem;
  }

  .room-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .room-name {
    font-size: 1rem;
  }

  .room-meta {
    font-size: 0.75rem;
  }

  .room-join-btn {
    padding: 0.625rem 1rem;
    font-size: 0.8rem;
    width: 100%;
  }
}

/* FOCUS VISIBLE FOR KEYBOARD NAVIGATION */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* HIGH CONTRAST MODE */
@media (prefers-contrast: more) {
  .navbar-btn {
    border: 2px solid var(--text-primary);
  }

  .btn-create-room {
    border: 2px solid var(--text-inverse);
  }

  .room-card {
    border-width: 2px;
  }
}
</style>
