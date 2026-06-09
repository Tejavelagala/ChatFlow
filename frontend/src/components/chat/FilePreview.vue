<template>
  <div class="file-preview">
    <div class="file-icon">
      {{ getFileIcon(fileType) }}
    </div>
    <div class="file-info">
      <div class="file-name">{{ fileName }}</div>
      <div class="file-size">{{ formatFileSize(fileSize) }}</div>
    </div>
    <a :href="fileUrl" download class="download-btn">
      ⬇️
    </a>
  </div>
</template>

<script>
export default {
  name: 'FilePreview',
  props: {
    fileName: String,
    fileSize: Number,
    fileType: String,
    fileUrl: String
  },
  methods: {
    getFileIcon(type) {
      const icons = {
        pdf: '📄',
        doc: '📝',
        docx: '📝',
        txt: '📃',
        zip: '🗜️',
        rar: '🗜️',
        xlsx: '📊',
        pptx: '📊',
        csv: '📊'
      }
      return icons[type] || '📎'
    },
    
    formatFileSize(bytes) {
      if (!bytes) return '0 B'
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    }
  }
}
</script>

<style scoped>
.file-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0,0,0,0.05);
  padding: 12px;
  border-radius: 12px;
  margin-top: 8px;
  max-width: 300px;
}

.file-icon {
  font-size: 32px;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-weight: 500;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 2px;
}

.download-btn {
  font-size: 20px;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.2s;
}

.download-btn:hover {
  transform: scale(1.2);
}
</style>
