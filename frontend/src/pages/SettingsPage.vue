<template>
  <div class="settings-container">
    <div class="settings-header">
      <button class="back-btn" @click="$router.push('/dashboard')">
        ← Back
      </button>
      <h2>⚙️ Settings</h2>
      <button class="profile-btn" @click="$router.push('/profile')">
        👤 Profile
      </button>
    </div>

    <div class="settings-content">
      <!-- PROFILE SECTION -->
      <div class="settings-section">
        <h3>Profile Settings</h3>
        
        <div class="avatar-upload">
          <div class="avatar-preview">
            <img v-if="profile.avatar" :src="profile.avatar" />
            <div v-else class="avatar-placeholder">
              {{ username.charAt(0).toUpperCase() }}
            </div>
          </div>
          <input
            type="file"
            ref="avatarInput"
            hidden
            accept="image/*"
            @change="uploadAvatar"
          />
          <button class="btn btn-secondary" @click="$refs.avatarInput.click()">
            Change Avatar
          </button>
        </div>

        <div class="form-group">
          <label>Username</label>
          <input
            v-model="profile.username"
            type="text"
            class="form-control"
            disabled
          />
          <small>Username cannot be changed</small>
        </div>

        <div class="form-group">
          <label>Bio</label>
          <textarea
            v-model="profile.bio"
            class="form-control"
            rows="3"
            placeholder="Tell us about yourself..."
          ></textarea>
        </div>

        <button class="btn btn-primary" @click="updateProfile">
          Save Profile
        </button>
      </div>

      <!-- THEME SECTION -->
      <div class="settings-section">
        <h3>Appearance</h3>
        
        <div class="theme-options">
          <div class="theme-option" @click="setTheme('light')">
            <div class="theme-preview light" :class="{ active: theme === 'light' }">
              ☀️
            </div>
            <span>Light</span>
          </div>
          
          <div class="theme-option" @click="setTheme('dark')">
            <div class="theme-preview dark" :class="{ active: theme === 'dark' }">
              🌙
            </div>
            <span>Dark</span>
          </div>
        </div>
      </div>

      <!-- NOTIFICATIONS SECTION -->
      <div class="settings-section">
        <h3>Notifications</h3>
        
        <div class="setting-item">
          <div>
            <strong>Browser Notifications</strong>
            <p>Receive notifications for new messages</p>
          </div>
          <label class="switch">
            <input
              type="checkbox"
              v-model="notificationsEnabled"
              @change="toggleNotifications"
            />
            <span class="slider"></span>
          </label>
        </div>

        <div class="setting-item">
          <div>
            <strong>Sound Notifications</strong>
            <p>Play sound for new messages</p>
          </div>
          <label class="switch">
            <input
              type="checkbox"
              v-model="soundEnabled"
              @change="toggleSound"
            />
            <span class="slider"></span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useProfileStore } from '../stores/profileStore'
import api from '../services/api'
import { notifySuccess, notifyError } from '../utils/toast'

export default {
  name: 'SettingsPage',
  setup() {
    return {
      profileStore: useProfileStore()
    }
  },
  data() {
    return {
      username: localStorage.getItem('username'),
      theme: localStorage.getItem('theme') || 'light',
      notificationsEnabled: localStorage.getItem('notifications') === 'true',
      soundEnabled: localStorage.getItem('sound') === 'true'
    }
  },
  computed: {
    profile() {
      return this.profileStore.profile || {
        username: this.username,
        bio: '',
        avatar: null
      }
    }
  },
  methods: {
    async fetchProfile() {
      await this.profileStore.fetchProfile()
    },

    async uploadAvatar(event) {
      const file = event.target.files[0]
      if (!file) return

      try {
        const formData = new FormData()
        formData.append('avatar', file)
        await this.profileStore.updateProfile(formData)
        notifySuccess('Avatar updated successfully')
      } catch (error) {
        notifyError('Failed to upload avatar')
      }
    },

    async updateProfile() {
      try {
        await this.profileStore.updateProfile({ bio: this.profile.bio })
        notifySuccess('Profile updated successfully')
      } catch (error) {
        notifyError('Failed to update profile')
      }
    },

    setTheme(theme) {
      this.theme = theme
      localStorage.setItem('theme', theme)
      document.documentElement.setAttribute('data-theme', theme)
      notifySuccess(`Theme changed to ${theme}`)
    },

    toggleNotifications() {
      localStorage.setItem('notifications', this.notificationsEnabled)
      
      if (this.notificationsEnabled) {
        this.requestNotificationPermission()
      }
    },

    toggleSound() {
      localStorage.setItem('sound', this.soundEnabled)
    },

    async requestNotificationPermission() {
      if ('Notification' in window) {
        const permission = await Notification.requestPermission()
        if (permission !== 'granted') {
          this.notificationsEnabled = false
          localStorage.setItem('notifications', 'false')
        }
      }
    }
  },
  mounted() {
    this.fetchProfile()
  }
}
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: var(--background);
  padding: 40px 20px;
}

.settings-header {
  max-width: 800px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.settings-header h2 {
  color: var(--text-primary);
  font-size: var(--font-size-page-title);
  font-weight: 700;
  flex: 1;
}

.back-btn,
.profile-btn {
  border: none;
  background: var(--card);
  padding: 10px 20px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.back-btn:hover,
.profile-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.settings-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-section {
  background: var(--card);
  padding: 30px;
  border-radius: 20px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.settings-section:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.settings-section h3 {
  margin-bottom: 20px;
  color: var(--text-primary);
  font-size: var(--font-size-section-title);
  font-weight: 600;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid var(--border);
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: var(--font-size-page-title);
  color: white;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group small {
  display: block;
  margin-top: 5px;
  color: var(--text-muted);
  font-size: var(--font-size-body-sm);
}

.theme-options {
  display: flex;
  gap: 20px;
}

.theme-option {
  cursor: pointer;
  text-align: center;
}

.theme-preview {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-page-title);
  border: 3px solid transparent;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
}

.theme-preview:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.theme-preview.light {
  background: var(--surface);
}

.theme-preview.dark {
  background: var(--surface);
}

.theme-preview.active {
  border-color: var(--primary);
  transform: scale(1.08);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid var(--border);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item p {
  margin: 5px 0 0;
  font-size: var(--font-size-body-sm);
  color: var(--text-secondary);
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #cbd5e1;
  transition: 0.4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background: var(--primary);
}

.dark .settings-container {
  background: var(--background);
}

input:checked + .slider:before {
  transform: translateX(26px);
}
</style>
