<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- Hero Profile Header -->
      <div class="profile-hero">
        <div class="cover-banner" :style="coverStyle">
          <button class="edit-cover-btn" @click="$refs.coverInput.click()">
            <span>📷</span> Change Cover
          </button>
          <input ref="coverInput" type="file" hidden accept="image/*" @change="uploadCover" />
          <SuccessFeedback
            :show="showCoverSuccess"
            text="Cover Updated"
            icon="✓"
            style="position: absolute; top: 1rem; left: 50%; transform: translateX(-50%);"
          />
        </div>
        
        <div class="profile-header-content">
          <div class="avatar-container" @mouseenter="showAvatarHover = true" @mouseleave="showAvatarHover = false">
            <div class="avatar-wrapper">
              <img v-if="profile.avatar" :src="profile.avatar" class="avatar-large" alt="Profile avatar" />
              <div v-else class="avatar-placeholder-large">
                {{ username.charAt(0).toUpperCase() }}
              </div>
              <div v-if="showAvatarHover" class="avatar-overlay" @click="$refs.avatarInput.click()">
                <span class="camera-icon">📷</span>
                <span class="change-text">Change Photo</span>
              </div>
              <div v-if="uploadingAvatar" class="avatar-uploading">
                <div class="spinner"></div>
                <span>Uploading...</span>
              </div>
              <SuccessFeedback
                :show="showAvatarSuccess"
                text="Avatar Updated"
                icon="✓"
                style="position: absolute; bottom: -2rem; left: 50%; transform: translateX(-50%);"
              />
            </div>
            <input ref="avatarInput" type="file" hidden accept="image/*" @change="uploadAvatar" />
          </div>
          
          <div class="profile-info">
            <h1 class="profile-name">{{ profile.username || username }}</h1>
            <p class="profile-title">{{ profile.bio || 'AI & ML Student' }}</p>
            <div class="profile-meta">
              <span class="meta-item">
                <span class="status-dot" :class="statusClass"></span>
                {{ statusText }}
              </span>
              <span class="meta-divider">•</span>
              <span class="meta-item">📅 Joined {{ joinedDate }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">💬</div>
          <div class="stat-content">
            <div class="stat-value">{{ totalMessages }}</div>
            <div class="stat-label">Messages Sent</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏠</div>
          <div class="stat-content">
            <div class="stat-value">{{ roomsCount }}</div>
            <div class="stat-label">Rooms Joined</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">😀</div>
          <div class="stat-content">
            <div class="stat-value">{{ reactionsGiven }}</div>
            <div class="stat-label">Reactions Given</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📎</div>
          <div class="stat-content">
            <div class="stat-value">{{ filesShared }}</div>
            <div class="stat-label">Files Shared</div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="profile-grid">
        <!-- Left Column: Profile Settings -->
        <div class="profile-left">
          <!-- Bio Section -->
          <div class="profile-card bio-card">
            <div class="card-header">
              <h3>✏️ About Me</h3>
            </div>
            <div class="card-body">
              <textarea
                v-model="editableBio"
                ref="bioTextarea"
                class="bio-textarea"
                placeholder="Tell us about yourself... Share your interests, skills, or what you're working on!"
                maxlength="250"
                rows="4"
                @input="autoResize"
              ></textarea>
              <div class="bio-footer">
                <span class="bio-preview" v-if="editableBio">{{ editableBio.split('\n')[0].substring(0, 50) }}{{ editableBio.length > 50 ? '...' : '' }}</span>
                <span class="char-counter" :class="{ 'char-limit': editableBio.length > 200, 'char-warning': editableBio.length > 230 }">
                  {{ editableBio.length }} / 250
                </span>
              </div>
            </div>
          </div>

          <!-- Profile Information -->
          <div class="profile-card">
            <div class="card-header">
              <h3>Profile Information</h3>
            </div>
            <div class="card-body">
              <div class="info-grid">
                <div class="info-item">
                  <div class="info-icon">👤</div>
                  <div class="info-content">
                    <span class="info-label">Username</span>
                    <span class="info-value">@{{ username }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">📧</div>
                  <div class="info-content">
                    <span class="info-label">Email</span>
                    <span class="info-value">{{ userEmail }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">📅</div>
                  <div class="info-content">
                    <span class="info-label">Joined Date</span>
                    <span class="info-value">{{ joinedDate }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">🚪</div>
                  <div class="info-content">
                    <span class="info-label">Rooms Joined</span>
                    <span class="info-value">{{ roomsCount }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div style="position: relative;">
            <button class="btn-save" @click="updateProfile" :disabled="isSaving">
              <span v-if="!isSaving">💾 Save Profile</span>
              <span v-else class="saving-state">
                <div class="spinner-small"></div>
                Saving...
              </span>
            </button>
            <SuccessFeedback
              :show="showSaveSuccess"
              text="Profile Saved"
              icon="✓"
              style="position: absolute; top: -2.5rem; left: 50%; transform: translateX(-50%);"
            />
          </div>
        </div>

        <!-- Right Column: Activity & Status -->
        <div class="profile-right">
          <!-- Online Status Card -->
          <div class="profile-card status-card">
            <div class="card-header">
              <h3>Status</h3>
            </div>
            <div class="card-body">
              <div class="status-options">
                <div class="status-option" :class="{ active: currentStatus === 'online' }" @click="setStatus('online')">
                  <span class="status-indicator-large online"></span>
                  <span class="status-label">Online</span>
                </div>
                <div class="status-option" :class="{ active: currentStatus === 'away' }" @click="setStatus('away')">
                  <span class="status-indicator-large away"></span>
                  <span class="status-label">Away</span>
                </div>
                <div class="status-option" :class="{ active: currentStatus === 'offline' }" @click="setStatus('offline')">
                  <span class="status-indicator-large offline"></span>
                  <span class="status-label">Offline</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="profile-card activity-card">
            <div class="card-header">
              <h3>Recent Activity</h3>
            </div>
            <div class="card-body">
              <div class="activity-list">
                <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                  <div class="activity-icon">{{ activity.icon }}</div>
                  <div class="activity-content">
                    <p class="activity-text">{{ activity.text }}</p>
                    <span class="activity-time">{{ activity.time }}</span>
                  </div>
                </div>
                <div v-if="recentActivities.length === 0" class="no-activity">
                  <span class="empty-icon">📭</span>
                  <p>No recent activity</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="profile-card">
            <div class="card-header">
              <h3>Quick Actions</h3>
            </div>
            <div class="card-body">
              <div class="quick-actions">
                <button class="action-btn" @click="$router.push('/dashboard')">
                  <span class="action-icon">🏠</span>
                  <span>Dashboard</span>
                </button>
                <button class="action-btn" @click="$router.push('/settings')">
                  <span class="action-icon">⚙️</span>
                  <span>Settings</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useProfileStore } from '../stores/profileStore'
import { notifySuccess, notifyError } from '../utils/toast'
import { getRecentActivities } from '../utils/activityTracker'
import SuccessFeedback from '../components/common/SuccessFeedback.vue'

export default {
  name: 'ProfilePage',
  components: {
    SuccessFeedback
  },
  setup() {
    return {
      profileStore: useProfileStore()
    }
  },
  data() {
    return {
      username: localStorage.getItem('username') || 'User',
      editableBio: '',
      showAvatarHover: false,
      uploadingAvatar: false,
      isSaving: false,
      currentStatus: 'online',
      coverImage: null,
      recentActivities: [],
      roomsCount: 0,
      showSaveSuccess: false,
      showAvatarSuccess: false,
      showCoverSuccess: false,
      totalMessages: 0,
      reactionsGiven: 0,
      filesShared: 0
    }
  },
  computed: {
    profile() {
      return this.profileStore.profile || {
        username: this.username,
        bio: '',
        avatar: null,
        online: true,
        email: '',
        joined_date: null,
        rooms_count: 0
      }
    },
    statusClass() {
      return this.currentStatus
    },
    statusText() {
      const statusMap = {
        online: 'Online',
        away: 'Away',
        offline: 'Last seen today'
      }
      return statusMap[this.currentStatus] || 'Online'
    },
    coverStyle() {
      if (this.profile.cover_image) {
        return { backgroundImage: `url(${this.profile.cover_image})` }
      }
      if (this.coverImage) {
        return { backgroundImage: `url(${this.coverImage})` }
      }
      return {}
    },
    userEmail() {
      return this.profile.email || localStorage.getItem('email') || 'user@example.com'
    },
    joinedDate() {
      if (this.profile.joined_date) {
        return new Date(this.profile.joined_date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
      }
      const date = localStorage.getItem('joinedDate')
      if (date) {
        return new Date(date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
      }
      return 'May 2024'
    }
  },
  methods: {
    async fetchProfile() {
      try {
        await this.profileStore.fetchProfile()
        this.editableBio = this.profile.bio || ''
        this.currentStatus = this.profile.online ? 'online' : 'offline'
        this.roomsCount = this.profile.rooms_count || 0
      } catch (error) {
        console.error('Failed to fetch profile:', error)
      }
    },

    async uploadAvatar(event) {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 5 * 1024 * 1024) {
        notifyError('Avatar size must be less than 5MB')
        return
      }

      this.uploadingAvatar = true
      try {
        const formData = new FormData()
        formData.append('avatar', file)
        await this.profileStore.updateProfile(formData)
        this.showAvatarSuccess = true
        setTimeout(() => { this.showAvatarSuccess = false }, 2000)
        notifySuccess('✅ Avatar updated successfully')
      } catch (error) {
        notifyError('Failed to upload avatar')
      } finally {
        this.uploadingAvatar = false
      }
    },

    async uploadCover(event) {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 5 * 1024 * 1024) {
        notifyError('Cover image size must be less than 5MB')
        return
      }

      try {
        const formData = new FormData()
        formData.append('cover_image', file)
        await this.profileStore.updateProfile(formData)
        this.showCoverSuccess = true
        setTimeout(() => { this.showCoverSuccess = false }, 2000)
        notifySuccess('✅ Cover image updated successfully')
      } catch (error) {
        notifyError('Failed to upload cover image')
      }
    },

    async updateProfile() {
      this.isSaving = true
      try {
        await this.profileStore.updateProfile({ bio: this.editableBio })
        this.showSaveSuccess = true
        setTimeout(() => { this.showSaveSuccess = false }, 2000)
        notifySuccess('✅ Profile updated successfully')
      } catch (error) {
        notifyError('Failed to update profile')
      } finally {
        this.isSaving = false
      }
    },

    setStatus(status) {
      this.currentStatus = status
      localStorage.setItem('userStatus', status)
      notifySuccess(`Status changed to ${status}`)
    },

    async loadActivities() {
      this.recentActivities = getRecentActivities(5)
    },

    async loadRoomsCount() {
      // Rooms count is now fetched from profile API
      this.roomsCount = this.profile.rooms_count || 0
    },

    autoResize() {
      const textarea = this.$refs.bioTextarea
      if (textarea) {
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
      }
    },

    loadStatistics() {
      // Load from localStorage or API
      this.totalMessages = parseInt(localStorage.getItem('totalMessages') || '0')
      this.reactionsGiven = parseInt(localStorage.getItem('reactionsGiven') || '0')
      this.filesShared = parseInt(localStorage.getItem('filesShared') || '0')
    }
  },
  mounted() {
    this.fetchProfile()
    this.loadActivities()
    this.loadRoomsCount()
    this.loadStatistics()
    
    const savedCover = localStorage.getItem('coverImage')
    if (savedCover) {
      this.coverImage = savedCover
    }

    const savedStatus = localStorage.getItem('userStatus')
    if (savedStatus) {
      this.currentStatus = savedStatus
    }

    this.$nextTick(() => {
      this.autoResize()
    })
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding-bottom: 40px;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Profile Header */
.profile-hero {
  background: var(--surface);
  border-radius: 0 0 20px 20px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  margin-bottom: 30px;
}

.cover-banner {
  height: 160px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  position: relative;
  background-size: cover;
  background-position: center;
}

.edit-cover-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: var(--font-size-body-sm);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.edit-cover-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: translateY(-2px);
}

.profile-header-content {
  padding: 0 40px 30px;
  display: flex;
  gap: 30px;
  align-items: flex-end;
  margin-top: -70px;
  position: relative;
  z-index: 10;
}

.avatar-container {
  position: relative;
  flex-shrink: 0;
  cursor: pointer;
}

.avatar-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  border-radius: var(--radius-full);
  border: 6px solid var(--surface);
  overflow: hidden;
  background: var(--primary);
  box-shadow: var(--shadow-xl);
}

.avatar-large {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder-large {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-page-title);
  font-weight: bold;
  color: var(--text-inverse);
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.camera-icon {
  font-size: 32px;
}

.change-text {
  color: var(--text-inverse);
  font-size: var(--font-size-body-sm);
  font-weight: 600;
}

.avatar-uploading {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--text-inverse);
  font-size: var(--font-size-body-sm);
  font-weight: 600;
}

.profile-info {
  flex: 1;
  padding-top: 20px;
  min-width: 0;
}

.profile-name {
  font-size: var(--font-size-page-title);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  line-height: 1.2;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-title {
  font-size: var(--font-size-body);
  color: var(--text-secondary);
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.profile-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
  font-weight: 500;
}

.meta-divider {
  color: var(--text-tertiary);
  opacity: 0.5;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
  border: 2px solid var(--surface);
}

.status-dot.online { background: var(--status-online); }
.status-dot.away { background: var(--status-idle); }
.status-dot.offline { background: var(--status-offline); }

/* Statistics Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 0 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-primary);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.stat-icon {
  font-size: 36px;
  flex-shrink: 0;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-section-title);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: var(--font-size-body-sm);
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Profile Grid */
.profile-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
  padding: 0 20px;
}

.profile-left,
.profile-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: var(--surface);
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-primary);
  overflow: hidden;
  transition: all 0.3s ease;
}

.profile-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-primary);
}

.card-header h3 {
  font-size: var(--font-size-card-title);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-body {
  padding: 20px;
}

/* Bio Section */
.bio-card {
  border-left: 4px solid var(--primary);
}

.bio-textarea {
  width: 100%;
  min-height: 120px;
  max-height: 300px;
  padding: 15px;
  background: var(--input-bg);
  border: 2px solid transparent;
  border-radius: 12px;
  color: var(--text-primary);
  font-size: var(--font-size-body);
  line-height: 1.6;
  resize: none;
  overflow-y: auto;
  transition: all 0.3s ease;
  font-family: inherit;
}

.bio-textarea:focus {
  outline: none;
  border-color: var(--brand-primary);
  background: var(--surface-primary);
}

.bio-textarea::placeholder {
  color: var(--text-muted);
}

.bio-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  gap: 10px;
}

.bio-preview {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
  font-style: italic;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.char-counter {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
  font-weight: 600;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.char-counter.char-limit {
  color: var(--warning);
}

.char-counter.char-warning {
  color: var(--danger);
  animation: pulse 1s ease-in-out infinite;
}

/* Profile Information Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: var(--bg-secondary);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: var(--surface-hover);
  transform: translateX(5px);
}

.info-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: 10px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-label {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: var(--font-size-body);
  color: var(--text-primary);
  font-weight: 600;
}

/* Save Button */
.btn-save {
  width: 100%;
  padding: 16px;
  background: var(--primary);
  color: var(--text-inverse);
  border: none;
  border-radius: 12px;
  font-size: var(--font-size-body);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-save:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.saving-state {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Status Card */
.status-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.status-option {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: var(--bg-secondary);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.status-option:hover {
  background: var(--surface-hover);
  transform: translateX(5px);
}

.status-option.active {
  background: var(--primary-light);
  border-color: var(--brand-primary);
}

.status-indicator-large {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  border: 3px solid var(--surface);
}

.status-indicator-large.online { background: var(--status-online); }
.status-indicator-large.away { background: var(--status-idle); }
.status-indicator-large.offline { background: var(--status-offline); }

.status-label {
  font-size: var(--font-size-body-sm);
  font-weight: 600;
  color: var(--text-primary);
}

/* Activity Section */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: var(--surface-hover);
  transform: translateX(5px);
}

.activity-icon {
  font-size: 20px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: 8px;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: var(--font-size-body-sm);
  color: var(--text-primary);
  margin-bottom: 4px;
}

.activity-time {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
}

.no-activity {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-tertiary);
}

.empty-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 10px;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
}

.action-btn:hover {
  background: var(--surface-hover);
  transform: translateX(5px);
}

.action-icon {
  font-size: 20px;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
}

.action-btn:hover {
  background: var(--bg-hover);
  transform: translateX(5px);
}

/* Spinner */
.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--text-inverse);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--text-inverse);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Mobile Responsive */
@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-icon {
    font-size: 28px;
  }

  .stat-value {
    font-size: 22px;
  }

  .profile-header-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 20px 30px;
    gap: 20px;
  }

  .profile-info {
    padding-top: 10px;
  }

  .avatar-wrapper {
    width: 120px;
    height: 120px;
  }

  .profile-name {
    font-size: 1.75rem;
    margin-bottom: 6px;
  }

  .profile-title {
    font-size: var(--font-size-body-sm);
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .cover-banner {
    height: 110px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
    padding: 0 10px;
  }

  .profile-grid {
    padding: 0 10px;
  }

  .card-body {
    padding: 15px;
  }

  .profile-header-content {
    padding: 0 15px 20px;
  }
}
</style>
