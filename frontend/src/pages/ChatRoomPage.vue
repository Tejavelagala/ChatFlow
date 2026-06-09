<template>
  <div class="app-layout" :class="{ dark: darkMode }">
    <!-- SIDEBAR - ROOMS -->
    <div class="sidebar rooms-sidebar" :class="{ mobileOpen: mobileSidebar }">
      <div class="sidebar-header">
        <h3 class="sidebar-title">💬 ChatFlow</h3>
      </div>
      
      <input
        v-model="searchQuery"
        type="text"
        placeholder="🔍 Search rooms..."
        class="search-input"
      />
      
      <div class="rooms-list">
        <div
          v-for="room in filteredRooms"
          :key="room.room_id"
          class="room-item"
          :class="{ active: room.room_id === roomId }"
          @click="switchRoom(room.room_id)"
        >
          <div class="room-avatar">
            {{ room.room_name.charAt(0).toUpperCase() }}
          </div>
          <div class="room-info">
            <div class="room-header">
              <span class="room-name"># {{ room.room_name }}</span>
              <span v-if="notifications[room.room_id]" class="notification-badge">
                {{ notifications[room.room_id] }}
              </span>
            </div>
            <div class="room-preview">
              <template v-if="roomPreviews[room.room_id]">
                <strong>{{ roomPreviews[room.room_id].username }}:</strong>
                {{ roomPreviews[room.room_id].lastMessage }}
              </template>
              <template v-else>
                <span class="no-messages">No messages yet</span>
              </template>
            </div>
          </div>
          <button 
            v-if="room.owner === username" 
            class="delete-btn" 
            @click.stop="deleteRoom(room.room_id)"
            title="Delete room"
          >
            ✖
          </button>
        </div>
      </div>
    </div>

    <!-- CHAT SECTION - MESSAGES -->
    <div class="chat-section">
      <div class="mobile-topbar">
        <button class="menu-btn" @click="mobileSidebar = !mobileSidebar">☰</button>
        <h4>{{ currentRoom?.room_name || 'ChatFlow' }}</h4>
        <button class="menu-btn" @click="mobileMembers = !mobileMembers">👥</button>
      </div>

      <ChatHeader
        :roomName="currentRoom?.room_name"
        :darkMode="darkMode"
        :searchQuery="searchQuery"
        :connectionStatus="connectionStatus"
        @toggle-theme="toggleTheme"
        @update-search="searchQuery = $event"
        @show-profile="showProfileModal = true"
        @open-settings="$router.push('/settings')"
        @logout="logout"
      />

      <ChatMessages
        ref="chatMessages"
        :messages="messages"
        :filteredMessages="filteredMessages"
        :searchQuery="searchQuery"
        :loadingMessages="loadingMessages"
        :pinnedMessages="pinnedMessages"
        :isRoomOwner="currentRoom?.owner === username"
        :username="username"
        :roomName="currentRoom?.room_name"
        :selectedMessageId="selectedMessageId"
        :editingMessageId="editingMessageId"
        :editedMessage="editedMessage"
        @scroll="handleScroll"
        @unpin-message="unpinMessage"
        @select-message="message.selectMessage"
        @react-message="reactToMessage"
        @start-editing="message.startEditing"
        @delete-message="deleteMessage"
        @reply-message="message.setReplyingTo"
        @pin-message="pinMessage"
        @update-edit="message.editedMessage = $event"
        @save-edit="saveEditedMessage"
      />

      <TypingIndicator :typingUser="typingUser" />

      <ChatInput
        :message="inputMessage"
        :replyingTo="replyingTo"
        :imagePreview="imagePreview"
        :recording="recording"
        :roomId="roomId"
        @update-message="inputMessage = $event"
        @send-message="sendMessage"
        @cancel-reply="message.cancelReply"
        @send-image="sendImage"
        @cancel-image="cancelImage"
        @upload-image="uploadImage"
        @file-uploaded="handleFileUploaded"
        @toggle-recording="toggleRecording"
        @add-emoji="inputMessage += $event"
      />
    </div>

    <!-- MEMBERS SIDEBAR -->
    <div class="sidebar members-sidebar" :class="{ mobileOpen: mobileMembers }">
      <div class="sidebar-header">
        <h3 class="sidebar-title">Members</h3>
      </div>
      
      <OnlineUsers :onlineUsers="onlineUsers" />
      
      <MemberList
        :members="members"
        :userRole="userRole"
        :username="username"
        :showLeaveButton="currentRoom?.owner !== username"
        @promote-user="promoteUser"
        @ban-user="banUser"
        @mute-user="muteUser"
        @leave-room="leaveRoom"
      />
    </div>

    <!-- PROFILE MODAL -->
    <div v-if="showProfileModal" class="profile-modal" @click.self="showProfileModal = false">
      <div class="profile-card">
        <div class="profile-avatar">
          <img v-if="profile.userProfile?.avatar" :src="profile.userProfile.avatar" />
          <div v-else>{{ username.charAt(0).toUpperCase() }}</div>
        </div>
        <h2>{{ username }}</h2>
        <p>{{ profile.userProfile?.bio || 'No bio yet' }}</p>
        <button class="close-profile-btn" @click="showProfileModal = false">Close</button>
      </div>
    </div>

    <!-- CONFIRMATION DIALOGS -->
    <ConfirmDialog
      :show="showDeleteConfirm"
      title="Delete Message?"
      message="This action cannot be undone."
      type="danger"
      confirmText="Delete"
      @confirm="confirmDeleteMessage"
      @cancel="showDeleteConfirm = false"
    />

    <ConfirmDialog
      :show="showLeaveConfirm"
      title="Leave Room?"
      message="Are you sure you want to leave this room?"
      type="warning"
      confirmText="Leave"
      @confirm="confirmLeaveRoom"
      @cancel="showLeaveConfirm = false"
    />

    <ConfirmDialog
      :show="showDeleteRoomConfirm"
      title="Delete Room?"
      message="This will permanently delete the room and all its messages. This action cannot be undone."
      type="danger"
      confirmText="Delete"
      @confirm="confirmDeleteRoom"
      @cancel="showDeleteRoomConfirm = false"
    />
  </div>
</template>

<script>
import { useAuthStore } from '../stores/authStore'
import { useRoomStore } from '../stores/roomStore'
import { useProfileStore } from '../stores/profileStore'
import { useThemeStore } from '../stores/themeStore'
import { useNotificationStore } from '../stores/notificationStore'
import { usePresenceStore } from '../stores/presenceStore'
import { useMessageStore } from '../stores/messageStore'
import api from '../services/api'
import { getWsBaseUrl } from '../config/runtime'
import { notifyInfo, notifySuccess, notifyError } from '../utils/toast'
import { showNotification } from '../utils/notifications'
import { trackActivity } from '../utils/activityTracker'
import throttle from 'lodash/throttle'
import ChatHeader from '../components/chat/ChatHeader.vue'
import ChatMessages from '../components/chat/ChatMessages.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import TypingIndicator from '../components/chat/TypingIndicator.vue'
import OnlineUsers from '../components/chat/OnlineUsers.vue'
import MemberList from '../components/chat/MemberList.vue'
import ConfirmDialog from '../components/common/ConfirmDialog.vue'

export default {
  name: 'ChatRoomPage',
  components: {
    ChatHeader,
    ChatMessages,
    ChatInput,
    TypingIndicator,
    OnlineUsers,
    MemberList,
    ConfirmDialog
  },
  setup() {
    return {
      auth: useAuthStore(),
      room: useRoomStore(),
      profile: useProfileStore(),
      theme: useThemeStore(),
      notification: useNotificationStore(),
      presence: usePresenceStore(),
      message: useMessageStore()
    }
  },
  data() {
    return {
      roomId: this.$route.params.roomId,
      socket: null,
      socketConnected: false,
      connectionStatus: 'connecting',
      reconnectAttempts: 0,
      maxReconnectAttempts: 10,
      reconnectTimer: null,
      heartbeatInterval: null,
      pendingMessages: [],
      intentionalDisconnect: false,
      searchQuery: '',
      roomPreviews: {},
      imagePreview: null,
      selectedImage: null,
      mobileSidebar: false,
      mobileMembers: false,
      mediaRecorder: null,
      audioChunks: [],
      recording: false,
      showProfileModal: false,
      typingTimeout: null,
      inputMessage: '',
      showDeleteConfirm: false,
      messageToDelete: null,
      showLeaveConfirm: false,
      showDeleteRoomConfirm: false,
      roomToDelete: null,
      sendTypingThrottled: null
    }
  },
  computed: {
    username() {
      return this.auth.username
    },
    darkMode() {
      return this.theme.darkMode
    },
    rooms() {
      return this.room.rooms
    },
    currentRoom() {
      return this.room.currentRoom
    },
    members() {
      return this.room.members
    },
    pinnedMessages() {
      return this.room.pinnedMessages
    },
    messages() {
      return this.message.messages
    },
    onlineUsers() {
      return this.presence.onlineUsers
    },
    typingUser() {
      return this.presence.typingUser
    },
    notifications() {
      return this.notification.notifications
    },
    userRole() {
      const member = this.members.find(m => m.username === this.username)
      return member ? member.role : 'member'
    },
    filteredRooms() {
      if (!this.searchQuery) return this.rooms
      const query = this.searchQuery.toLowerCase()
      return this.rooms.filter(room => room.room_name.toLowerCase().includes(query))
    },
    filteredMessages() {
      if (!this.searchQuery) return this.messages
      const query = this.searchQuery.toLowerCase()
      return this.messages.filter(msg => msg.message?.toLowerCase().includes(query))
    },
    editingMessageId() {
      return this.message.editingMessageId
    },
    editedMessage() {
      return this.message.editedMessage
    },
    selectedMessageId() {
      return this.message.selectedMessageId
    },
    replyingTo() {
      return this.message.replyingTo
    },
    loadingMessages() {
      return this.message.isLoading
    },
    hasMoreMessages() {
      return this.message.hasMoreMessages
    }
  },
  methods: {
    handleReaction(data) {
      this.message.updateReactionFromWebSocket(data.message_id, data.reactions)
    },
    handleMessage(data) {
      this.message.addMessage(data)
      this.scrollToBottom()
      if (document.hidden && data.username !== this.username) {
        showNotification(data.username, data.message)
      }
      this.roomPreviews[this.roomId] = {
        lastMessage: data.message,
        username: data.username
      }
      if (data.username !== this.username) {
        this.notification.addNotification(this.roomId)
        this.socket.send(JSON.stringify({
          type: 'delivered',
          message_id: data.message_id
        }))
        setTimeout(() => {
          this.socket.send(JSON.stringify({
            type: 'seen',
            message_id: data.message_id,
            username: this.username
          }))
        }, 1000)
      }
    },
    handleDelivered(data) {
      const msg = this.messages.find(m => m.message_id === data.message_id)
      if (msg) {
        msg.status = 'delivered'
        msg.delivered_at = data.delivered_at
      }
    },
    handleSeen(data) {
      const msg = this.messages.find(m => m.message_id === data.message_id)
      if (msg) {
        msg.status = 'seen'
        msg.seen_at = data.seen_at
      }
    },
    handleTyping(data) {
      if (data.username !== this.username) {
        this.presence.setUserTyping(data.username)
        clearTimeout(this.typingTimeout)
        this.typingTimeout = setTimeout(() => {
          this.presence.clearTyping(data.username)
        }, 1500)
      }
    },
    handleOnlineUsers(data) {
      console.log('📊 ONLINE_USERS received:', data.users)
      this.presence.setOnlineUsers(data.users)
    },
    connectWebSocket() {
      const token = localStorage.getItem('access')
      if (!token) {
        console.error('❌ WS CONNECT FAILED: No access token found')
        notifyError('Authentication required')
        this.$router.push('/login')
        return
      }
      if (!this.username) {
        console.error('❌ WS CONNECT FAILED: No username')
        notifyError('Unable to connect: missing username')
        return
      }
      if (this.socket && [WebSocket.CONNECTING, WebSocket.OPEN].includes(this.socket.readyState)) {
        console.log('⚠️ WS CONNECT SKIPPED: Already connecting/connected')
        return
      }
      
      this.intentionalDisconnect = false
      this.connectionStatus = 'connecting'
      
      // Build WebSocket URL with token query parameter
      const query = new URLSearchParams({ token }).toString()
      const wsUrl = `${getWsBaseUrl()}/ws/chat/${encodeURIComponent(this.roomId)}/${encodeURIComponent(this.username)}/?${query}`
      
      console.log('🔌 WS CONNECTING:', {
        roomId: this.roomId,
        username: this.username,
        tokenPresent: !!token,
        tokenLength: token?.length,
        tokenPrefix: token?.substring(0, 20) + '...',
        wsUrl: wsUrl.replace(/token=[^&]+/, 'token=***')
      })

      this.socket = new WebSocket(wsUrl)
      this.socket.onopen = () => {
        console.log('✅ WS CONNECTED:', this.roomId, this.username)
        this.connectionStatus = 'connected'
        this.socketConnected = true
        this.reconnectAttempts = 0
        if (this.reconnectTimer) {
          clearTimeout(this.reconnectTimer)
          this.reconnectTimer = null
        }
        this.startHeartbeat()
        this.flushPendingMessages()
      }
      this.socket.onclose = (event) => {
        console.log('🔌 WS CLOSED:', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
          intentional: this.intentionalDisconnect
        })
        
        this.connectionStatus = 'disconnected'
        this.socketConnected = false
        this.clearHeartbeat()
        this.socket = null

        if (this.intentionalDisconnect || event.code === 1000) {
          console.log('✅ WS CLOSED INTENTIONALLY')
          return
        }

        if (event.code === 4401) {
          console.error('❌ WS AUTH FAILED: Token invalid or expired')
          notifyError('Session expired. Please log in again.')
          this.auth.logout()
          this.$router.replace('/login')
          return
        }

        if (event.code === 4403) {
          console.error('❌ WS ACCESS DENIED: No permission to room')
          notifyError('You do not have access to this chat room.')
          this.$router.replace('/dashboard')
          return
        }

        console.warn('⚠️ WS DISCONNECTED UNEXPECTEDLY, will reconnect')
        this.reconnectWebSocket()
      }
      this.socket.onerror = (error) => {
        console.error('❌ WS ERROR:', error)
        this.connectionStatus = 'disconnected'
      }
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'error') {
          console.error('WebSocket Error:', data.message)
          return
        }
        const handlers = {
          message: this.handleMessage,
          delivered: this.handleDelivered,
          seen: this.handleSeen,
          typing: this.handleTyping,
          online_users: this.handleOnlineUsers,
          reaction: this.handleReaction,
          pong: () => {}
        }
        const handler = handlers[data.type]
        if (handler) {
          handler.call(this, data)
        } else if (data.message) {
          this.handleMessage(data)
        }
      }
    },
    reconnectWebSocket() {
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer)
      }
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        this.connectionStatus = 'disconnected'
        notifyError('Failed to reconnect. Please refresh the page')
        return
      }
      this.connectionStatus = 'connecting'
      this.reconnectAttempts++
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
      console.log(`🔄 Reconnecting in ${delay/1000}s... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      this.reconnectTimer = setTimeout(() => {
        this.reconnectTimer = null
        this.connectWebSocket()
      }, delay)
    },
    startHeartbeat() {
      this.heartbeatInterval = setInterval(() => {
        if (this.socket && this.socket.readyState === 1) {
          this.socket.send(JSON.stringify({ type: 'ping' }))
        }
      }, 30000)
    },
    clearHeartbeat() {
      if (this.heartbeatInterval) {
        clearInterval(this.heartbeatInterval)
        this.heartbeatInterval = null
      }
    },
    flushPendingMessages() {
      while (this.pendingMessages.length > 0) {
        const msg = this.pendingMessages.shift()
        this.socket.send(JSON.stringify(msg))
      }
    },
    sendMessage() {
      if (this.inputMessage.trim() === '') return
      const payload = {
        type: 'message',
        message: this.inputMessage,
        username: this.username,
        reply_to: this.replyingTo ? this.replyingTo.message_id : null
      }
      if (this.socket && this.socket.readyState === 1) {
        this.socket.send(JSON.stringify(payload))
        trackActivity('💬', 'Sent a message')
      } else {
        this.pendingMessages.push(payload)
      }
      this.inputMessage = ''
      this.message.cancelReply()
    },
    async toggleRecording() {
      if (this.recording) {
        this.mediaRecorder.stop()
        this.recording = false
        return
      }
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      this.mediaRecorder = new MediaRecorder(stream)
      this.audioChunks = []
      this.mediaRecorder.ondataavailable = (event) => {
        this.audioChunks.push(event.data)
      }
      this.mediaRecorder.onstop = () => {
        this.sendAudio()
      }
      this.mediaRecorder.start()
      this.recording = true
    },
    async sendAudio() {
      try {
        const blob = new Blob(this.audioChunks, { type: 'audio/webm' })
        const formData = new FormData()
        formData.append('audio', blob, 'voice.webm')
        formData.append('room_id', this.roomId)
        const response = await api.post('/api/chat/upload-audio/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.message.addMessage({
          username: response.data.sender,
          audio: response.data.audio,
          message_id: response.data.id,
          created_at: response.data.timestamp
        })
        this.scrollToBottom()
      } catch (error) {
        notifyError('Failed to send audio')
      }
    },
    handleFileUploaded(fileData) {
      this.message.addMessage({
        username: fileData.sender,
        message: fileData.content,
        file: fileData.file,
        file_name: fileData.file_name,
        file_size: fileData.file_size,
        file_type: fileData.file_type,
        file_url: fileData.file_url,
        message_id: fileData.id,
        created_at: fileData.timestamp,
        status: 'sent'
      })
      this.scrollToBottom()
    },
    async pinMessage(messageId) {
      try {
        await this.room.fetchPinnedMessages(this.roomId)
      } catch (error) {
        notifyError(error.response?.data?.error || 'Failed to pin message')
      }
    },
    async unpinMessage(messageId) {
      try {
        await api.post(`/api/chat/unpin-message/${messageId}/`)
        await this.room.fetchPinnedMessages(this.roomId)
      } catch (error) {
        notifyError('Failed to unpin message')
      }
    },
    handleScroll() {
      const container = this.$refs.chatMessages
      if (!container) return
      if (container.scrollTop < 50 && this.hasMoreMessages && !this.loadingMessages) {
        this.loadMoreMessages()
      }
    },
    async loadMoreMessages() {
      this.message.currentPage += 1
      await this.message.fetchMessages(this.roomId, this.message.currentPage)
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatMessages
        if (container) container.scrollTop = container.scrollHeight
      })
    },
    async switchRoom(roomId) {
      this.notification.clearNotifications(roomId)
      this.mobileSidebar = false
      
      // Join room first (creates ChatRoomMember record)
      try {
        await this.room.joinRoom(roomId)
      } catch (error) {
        console.error('Failed to join room:', error)
        notifyError('Failed to join room')
        return
      }
      
      // Then navigate
      this.$router.push(`/chat/${roomId}`)
    },
    async deleteRoom(roomId) {
      this.roomToDelete = roomId
      this.showDeleteRoomConfirm = true
    },
    async confirmDeleteRoom() {
      const toast = useToast()
      try {
        await this.room.deleteRoom(this.roomToDelete)
        toast.success('Room deleted')
        this.$router.push('/dashboard')
      } catch (error) {
        toast.error('Failed to delete room')
      } finally {
        this.showDeleteRoomConfirm = false
        this.roomToDelete = null
      }
    },
    toggleTheme() {
      this.theme.toggleTheme()
    },
    logout() {
      this.intentionalDisconnect = true
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer)
        this.reconnectTimer = null
      }
      if (this.socket) this.socket.close(1000, 'logout')
      this.auth.logout()
      this.$router.replace('/login')
    },
    async deleteMessage(messageId) {
      this.messageToDelete = messageId
      this.showDeleteConfirm = true
    },
    async confirmDeleteMessage() {
      const toast = useToast()
      try {
        await this.message.deleteMessage(this.messageToDelete)
        toast.success('Message deleted')
      } catch (error) {
        toast.error('Failed to delete message')
      } finally {
        this.showDeleteConfirm = false
        this.messageToDelete = null
      }
    },
    async reactToMessage(messageId, emoji) {
      if (this.socket && this.socket.readyState === 1) {
        this.socket.send(JSON.stringify({
          type: 'reaction',
          message_id: messageId,
          emoji: emoji
        }))
        trackActivity('😀', 'Reacted to message')
      }
    },
    async saveEditedMessage(messageId) {
      try {
        await this.message.editMessage(messageId, this.message.editedMessage)
      } catch (error) {
        notifyError('Failed to update message')
      }
    },
    async leaveRoom() {
      this.showLeaveConfirm = true
    },
    async confirmLeaveRoom() {
      const toast = useToast()
      try {
        await this.room.leaveRoom(this.roomId)
        toast.success('Left room successfully')
        this.$router.push('/dashboard')
      } catch (error) {
        toast.error(error.response?.data?.error || 'Failed to leave room')
      } finally {
        this.showLeaveConfirm = false
      }
    },
    async promoteUser(username, role) {
      if (!role) return
      try {
        await this.room.promoteUser(this.roomId, username, role)
      } catch (error) {
        notifyError(error.response?.data?.error || 'Failed to promote user')
      }
    },
    async banUser(username) {
      try {
        await this.room.banUser(this.roomId, username)
      } catch (error) {
        notifyError(error.response?.data?.error || 'Failed to ban user')
      }
    },
    async muteUser(username) {
      try {
        await this.room.muteUser(this.roomId, username)
      } catch (error) {
        notifyError(error.response?.data?.error || 'Failed to mute user')
      }
    },
    uploadImage(event) {
      const file = event.target.files[0]
      if (!file) return
      this.imagePreview = URL.createObjectURL(file)
      this.selectedImage = file
    },
    async sendImage() {
      try {
        if (!this.selectedImage) return
        let fileToUpload = this.selectedImage
        if (this.selectedImage.size > 1024 * 1024) {
          const imageCompression = (await import('browser-image-compression')).default
          fileToUpload = await imageCompression(this.selectedImage, {
            maxSizeMB: 1,
            maxWidthOrHeight: 1920
          })
        }
        const formData = new FormData()
        formData.append('image', fileToUpload)
        formData.append('room_id', this.roomId)
        const response = await api.post('/api/chat/upload-image/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.message.addMessage({
          username: response.data.sender,
          image: response.data.image,
          message_id: response.data.id,
          created_at: response.data.timestamp
        })
        this.scrollToBottom()
        this.selectedImage = null
        this.imagePreview = null
      } catch (error) {
        notifyError('Image upload failed')
      }
    },
    cancelImage() {
      this.selectedImage = null
      this.imagePreview = null
    },
    handleOnline() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        return
      }
      this.connectionStatus = 'connecting'
      this.reconnectAttempts = 0
      this.reconnectWebSocket()
      console.log('📡 Network back online')
    },
    handleOffline() {
      this.connectionStatus = 'disconnected'
      this.clearHeartbeat()
      notifyError('Connection lost')
    }
  },
  async mounted() {
    await this.room.fetchRooms()
    await this.message.fetchMessages(this.roomId)
    await this.profile.fetchProfile()
    await this.room.fetchPinnedMessages(this.roomId)
    await this.room.fetchMembers(this.roomId)
    this.connectWebSocket()
    window.addEventListener('online', this.handleOnline)
    window.addEventListener('offline', this.handleOffline)
    
    // Initialize throttled typing function
    this.sendTypingThrottled = throttle(() => {
      if (this.socket && this.socket.readyState === 1) {
        this.socket.send(JSON.stringify({
          type: 'typing',
          username: this.username
        }))
      }
    }, 1000)
  },
  beforeUnmount() {
    this.intentionalDisconnect = true
    this.clearHeartbeat()
    
    // Clean up reconnection timer
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    
    // Clean up WebSocket
    if (this.socket) {
      this.socket.close(1000, 'component unmounted')
      this.socket = null
    }
    
    // Clean up timeouts
    if (this.typingTimeout) {
      clearTimeout(this.typingTimeout)
      this.typingTimeout = null
    }
    
    // Clean up throttled function
    if (this.sendTypingThrottled) {
      this.sendTypingThrottled.cancel()
      this.sendTypingThrottled = null
    }
    
    // Remove event listeners
    window.removeEventListener('online', this.handleOnline)
    window.removeEventListener('offline', this.handleOffline)
  }
}
</script>

<style scoped>
.app-layout {
  display: grid;
  grid-template-columns: 280px 1fr 240px;
  gap: 0;
  height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow: hidden;
}

/* ROOMS SIDEBAR */
.rooms-sidebar {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.sidebar-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-primary);
  background: var(--surface);
}

.sidebar-title {
  font-size: var(--font-size-card-title);
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.search-input {
  width: calc(100% - 2rem);
  margin: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  outline: none;
  background: var(--input-bg);
  color: var(--text-primary);
  font-size: var(--font-size-body-sm);
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.rooms-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.room-item {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.75rem 0.875rem;
  margin-bottom: 0.375rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  background: transparent;
  border: 1px solid transparent;
}

.room-item:hover {
  background: var(--bg-hover);
  border-color: var(--border-primary);
}

.room-item.active {
  background: var(--primary-light);
  border-color: var(--primary);
}

.room-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 70%;
  background: var(--primary);
  border-radius: 0 4px 4px 0;
}

.room-avatar {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: var(--radius-md);
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--font-size-body);
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.room-info {
  flex: 1;
  min-width: 0;
}

.room-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.125rem;
}

.room-name {
  font-weight: 600;
  font-size: var(--font-size-body);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.room-preview {
  font-size: var(--font-size-body-sm);
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.room-preview strong {
  color: var(--text-primary);
  font-weight: 500;
}

.no-messages {
  font-style: italic;
  opacity: 0.7;
}

.notification-badge {
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  border-radius: var(--radius-md);
  background: var(--danger);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-body-sm);
  font-weight: 700;
  flex-shrink: 0;
}

.delete-btn {
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s ease;
  opacity: 0;
  flex-shrink: 0;
}

.room-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: var(--danger-bg);
  color: var(--danger);
}

/* CHAT SECTION */
.chat-section {
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  overflow: hidden;
  padding: 0;
}

.mobile-topbar {
  display: none;
}

/* MEMBERS SIDEBAR */
.members-sidebar {
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* PROFILE MODAL */
.profile-modal {
  position: fixed;
  inset: 0;
  background: var(--bg-overlay);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 4000;
  animation: fadeIn 0.2s ease;
}

.profile-card {
  width: 90%;
  max-width: 400px;
  background: var(--surface-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 2rem;
  text-align: center;
  box-shadow: var(--shadow-xl);
  animation: scaleIn 0.2s ease;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: var(--radius-round);
  overflow: hidden;
  margin: 0 auto 1.5rem;
  background: var(--brand-primary);
  color: var(--text-inverse);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-page-title);
  font-weight: 700;
  border: 4px solid var(--border-subtle);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-card h2 {
  color: var(--text-primary);
  font-size: var(--font-size-section-title);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.profile-card p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.close-profile-btn {
  background: var(--brand-primary);
  color: var(--text-inverse);
  border: none;
  padding: 0.75rem 2rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.close-profile-btn:hover {
  background: var(--brand-primary-hover);
}

/* MOBILE RESPONSIVE */
@media (max-width: 1024px) {
  .app-layout {
    grid-template-columns: 1fr;
  }

  .rooms-sidebar,
  .members-sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    width: 280px;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    box-shadow: var(--shadow-xl);
  }

  .rooms-sidebar {
    left: 0;
  }

  .members-sidebar {
    right: 0;
    left: auto;
    transform: translateX(100%);
  }

  .rooms-sidebar.mobileOpen {
    transform: translateX(0);
  }

  .members-sidebar.mobileOpen {
    transform: translateX(0);
  }

  .mobile-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background: var(--surface-primary);
    border-bottom: 1px solid var(--border-subtle);
  }

  .mobile-topbar h4 {
    margin: 0;
    font-size: var(--font-size-body);
    font-weight: 600;
  }

  .menu-btn {
    border: none;
    background: transparent;
    font-size: var(--font-size-card-title);
    cursor: pointer;
    color: var(--text-primary);
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    transition: all 0.15s ease;
  }

  .menu-btn:hover {
    background: var(--surface-hover);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
