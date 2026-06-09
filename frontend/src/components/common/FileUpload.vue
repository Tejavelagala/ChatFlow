<template>
  <div class="file-upload">
    <input
      type="file"
      ref="fileInput"
      hidden
      @change="handleFileSelect"
      accept=".pdf,.doc,.docx,.txt,.zip,.rar,.xlsx,.pptx,.csv"
    />
    
    <button class="btn btn-secondary" @click="$refs.fileInput.click()">
      📎
    </button>

    <div v-if="uploading" class="upload-progress">
      <div class="progress">
        <div 
          class="progress-bar" 
          :style="{ width: uploadProgress + '%' }"
        >
          {{ uploadProgress }}%
        </div>
      </div>
      <small>Uploading {{ selectedFile?.name }}...</small>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'
import { useToast } from 'vue-toastification'

export default {
  name: 'FileUpload',
  props: {
    roomId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadProgress: 0
    }
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 10 * 1024 * 1024) {
        const toast = useToast()
        toast.error('File size must be less than 10MB')
        return
      }

      this.selectedFile = file
      this.uploadFile()
    },

    async uploadFile() {
      const toast = useToast()
      this.uploading = true

      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        formData.append('room_id', this.roomId)

        const response = await api.post('/api/chat/upload-file/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            this.uploadProgress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            )
          }
        })

        this.$emit('file-uploaded', response.data)
        toast.success('File uploaded successfully')
        
      } catch (error) {
        console.error(error)
        toast.error(error.response?.data?.error || 'File upload failed')
      } finally {
        this.uploading = false
        this.uploadProgress = 0
        this.selectedFile = null
        this.$refs.fileInput.value = ''
      }
    }
  }
}
</script>

<style scoped>
.upload-progress {
  position: absolute;
  bottom: 80px;
  left: 20px;
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  min-width: 250px;
  z-index: 100;
}

.progress {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar {
  height: 100%;
  background: #667eea;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-body-sm);
  color: white;
}
</style>
