<template>
  <div class="members-section">
    <div class="section-header">
      <span class="header-icon">👥</span>
      <h6>Members</h6>
      <span class="count-badge">{{ members.length }}</span>
    </div>
    
    <div class="members-list">
      <div
        v-for="member in members"
        :key="member.username"
        class="member-item"
      >
        <div class="member-main">
          <div class="member-avatar" :class="member.role">
            {{ member.username.charAt(0).toUpperCase() }}
          </div>
          <div class="member-details">
            <div class="member-name-row">
              <span class="member-name">{{ member.username }}</span>
              <span v-if="member.is_muted" class="status-icon" title="Muted">🔇</span>
              <span v-if="member.is_banned" class="status-icon" title="Banned">🚫</span>
            </div>
            <span class="member-role-badge" :class="member.role">
              {{ getRoleIcon(member.role) }} {{ member.role }}
            </span>
          </div>
        </div>
        
        <!-- ADMIN CONTROLS -->
        <div v-if="userRole === 'owner' && member.username !== username" class="admin-controls">
          <select 
            @change="$emit('promote-user', member.username, $event.target.value)" 
            class="role-select"
          >
            <option value="">Change Role</option>
            <option value="admin">Admin</option>
            <option value="moderator">Moderator</option>
            <option value="member">Member</option>
          </select>
          <button @click="$emit('mute-user', member.username)" class="action-btn mute-btn" title="Mute">
            🔇
          </button>
          <button @click="$emit('ban-user', member.username)" class="action-btn ban-btn" title="Ban">
            🚫
          </button>
        </div>
      </div>
    </div>

    <!-- LEAVE ROOM BUTTON -->
    <button
      v-if="showLeaveButton"
      class="leave-room-btn"
      @click="$emit('leave-room')"
    >
      <span>🚺</span>
      Leave Room
    </button>
  </div>
</template>

<script>
export default {
  name: 'MemberList',
  props: {
    members: {
      type: Array,
      default: () => []
    },
    userRole: {
      type: String,
      default: 'member'
    },
    username: {
      type: String,
      required: true
    },
    showLeaveButton: {
      type: Boolean,
      default: false
    }
  },
  emits: ['promote-user', 'ban-user', 'mute-user', 'leave-room'],
  methods: {
    getRoleIcon(role) {
      const icons = {
        owner: '👑',
        admin: '🛡️',
        moderator: '⭐',
        member: '👤'
      }
      return icons[role] || '👤'
    }
  }
}
</script>

<style scoped>
.members-section {
  margin-top: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, rgba(88, 101, 242, 0.18) 0%, rgba(114, 137, 218, 0.08) 100%);
  border-radius: var(--radius-lg);
  margin-bottom: 0.875rem;
  border: 1.5px solid rgba(88, 101, 242, 0.25);
  box-shadow: 0 2px 8px rgba(88, 101, 242, 0.15);
}

.header-icon {
  font-size: 1.125rem;
}

.section-header h6 {
  flex: 1;
  margin: 0;
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--brand-primary);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.count-badge {
  background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%);
  color: white;
  padding: 0.25rem 0.625rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  box-shadow: 0 2px 6px rgba(88, 101, 242, 0.35);
  min-width: 1.5rem;
  text-align: center;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.member-item {
  padding: 0.875rem;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  margin-bottom: 0.5rem;
}

.member-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(88, 101, 242, 0.4);
  transform: translateX(6px);
  box-shadow: 0 4px 12px rgba(88, 101, 242, 0.2);
}

.member-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.member-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.member-avatar.owner {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.5);
}

.member-avatar.admin {
  background: linear-gradient(135deg, #f04747 0%, #dc2626 100%);
  box-shadow: 0 4px 12px rgba(240, 71, 71, 0.5);
}

.member-avatar.moderator {
  background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%);
  box-shadow: 0 4px 12px rgba(88, 101, 242, 0.5);
}

.member-avatar.member {
  background: linear-gradient(135deg, #7289da 0%, #5b6eae 100%);
  box-shadow: 0 4px 12px rgba(114, 137, 218, 0.5);
}

.member-details {
  flex: 1;
  min-width: 0;
}

.member-name-row {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.25rem;
}

.member-name {
  font-weight: 700;
  font-size: 0.9375rem;
  color: #1a1a2e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: 0.01em;
}

.status-icon {
  font-size: 0.75rem;
  opacity: 0.7;
}

.member-role-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.6875rem;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.member-role-badge.owner {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid #fbbf24;
}

.member-role-badge.admin {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border: 1px solid #f87171;
}

.member-role-badge.moderator {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border: 1px solid #60a5fa;
}

.member-role-badge.member {
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  color: #374151;
  border: 1px solid #9ca3af;
}

.admin-controls {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.role-select {
  flex: 1;
  min-width: 100px;
  background: var(--input-bg);
  color: var(--input-text);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 0.375rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.role-select:hover {
  border-color: var(--brand-primary);
}

.role-select:focus {
  outline: none;
  border-color: var(--brand-primary);
  box-shadow: 0 0 0 2px rgba(88, 101, 242, 0.1);
}

.action-btn {
  padding: 0.375rem 0.625rem;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s ease;
  font-weight: 600;
}

.mute-btn {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(251, 191, 36, 0.3);
}

.mute-btn:hover {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(251, 191, 36, 0.4);
}

.ban-btn {
  background: linear-gradient(135deg, #f04747 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(240, 71, 71, 0.3);
}

.ban-btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(240, 71, 71, 0.4);
}

.leave-room-btn {
  width: 100%;
  margin-top: 1.25rem;
  padding: 1rem;
  border: none;
  background: linear-gradient(135deg, #f04747 0%, #dc2626 100%);
  color: white;
  border-radius: var(--radius-lg);
  font-weight: 800;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  box-shadow: 0 4px 16px rgba(240, 71, 71, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.leave-room-btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(240, 71, 71, 0.5);
}

.leave-room-btn:active {
  transform: translateY(0);
}
</style>