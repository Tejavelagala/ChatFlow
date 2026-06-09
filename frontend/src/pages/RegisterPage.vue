<template>
  <div class="register-container">
    <!-- Left Side: Hero/Branding -->
    <div class="hero-section">
      <div class="hero-content">
        <!-- Logo & Branding -->
        <div class="brand-header">
          <div class="logo-icon">🚀</div>
          <h1 class="brand-name">Join ChatFlow</h1>
        </div>
        
        <!-- Tagline -->
        <p class="tagline">Start collaborating with your team today.</p>
        
        <!-- Feature Highlights -->
        <div class="features-list">
          <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <div class="feature-text">
              <h3>Quick Setup</h3>
              <p>Get started in less than 60 seconds</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div class="feature-text">
              <h3>Secure & Private</h3>
              <p>Your data is encrypted and protected</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">🌐</div>
            <div class="feature-text">
              <h3>Always Available</h3>
              <p>Access from anywhere, anytime</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">💯</div>
            <div class="feature-text">
              <h3>Free to Start</h3>
              <p>No credit card required</p>
            </div>
          </div>
        </div>
        
        <!-- Decorative Elements -->
        <div class="hero-decoration"></div>
      </div>
    </div>

    <!-- Right Side: Register Form -->
    <div class="form-section">
      <div class="form-wrapper">
        <!-- Theme Toggle -->
        <button @click="toggleTheme" class="theme-toggle" aria-label="Toggle theme">
          <span v-if="isDarkMode">☀️</span>
          <span v-else>🌙</span>
        </button>

        <!-- Register Card -->
        <div class="card-register">
          <div class="card-header">
            <h2>Create your account</h2>
            <p>Join thousands of teams using ChatFlow</p>
          </div>

          <form @submit.prevent="handleRegister" class="register-form">
            <!-- Username Input -->
            <div class="form-group">
              <label for="username" class="form-label">Username</label>
              <input
                id="username"
                v-model="username"
                type="text"
                class="input-modern"
                placeholder="Choose a username"
                required
                minlength="3"
                :disabled="isLoading"
                autocomplete="username"
              />
              <span class="input-helper">Minimum 3 characters</span>
            </div>

            <!-- Password Input with Toggle -->
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <div class="password-wrapper">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  class="input-modern"
                  placeholder="Create a strong password"
                  required
                  minlength="8"
                  :disabled="isLoading"
                  autocomplete="new-password"
                />
                <button
                  type="button"
                  class="password-toggle-btn"
                  @click="showPassword = !showPassword"
                  :disabled="!password || isLoading"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                >
                  <span v-if="showPassword">👁️</span>
                  <span v-else">👁️🗨️</span>
                </button>
              </div>
              <span class="input-helper">Minimum 8 characters</span>
            </div>

            <!-- Terms & Conditions -->
            <div class="form-group">
              <label class="checkbox-modern">
                <input type="checkbox" v-model="agreeToTerms" required>
                <span>I agree to the <a href="#" class="link-inline">Terms of Service</a> and <a href="#" class="link-inline">Privacy Policy</a></span>
              </label>
            </div>

            <!-- Success Message -->
            <div v-if="success" class="success-message">
              <span class="success-icon">✅</span>
              <div class="success-content">
                <strong>Account created successfully!</strong>
                <p>Redirecting to login...</p>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="error-message">
              <span class="error-icon">❌</span>
              <div class="error-content">
                <strong>Registration failed</strong>
                <p>{{ error }}</p>
              </div>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="btn-modern btn-register"
              :disabled="isLoading || !username || !password || !agreeToTerms"
            >
              <span v-if="isLoading" class="spinner-modern spinner-sm"></span>
              <span>{{ isLoading ? 'Creating Account...' : 'Create Account' }}</span>
            </button>
          </form>

          <!-- Footer -->
          <div class="card-footer">
            <p>Already have an account? <router-link to="/login" class="signin-link">Sign in</router-link></p>
          </div>
        </div>

        <!-- Additional Info -->
        <p class="terms-text">
          By creating an account, you agree to our <a href="#">Terms</a> and <a href="#">Privacy Policy</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useThemeStore } from '@/stores/themeStore'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

// Form state
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const agreeToTerms = ref(false)
const isLoading = ref(false)
const error = ref(null)
const success = ref(false)

// Theme
const isDarkMode = computed(() => themeStore.isDarkMode)

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const handleRegister = async () => {
  if (!username.value || !password.value || !agreeToTerms.value) return
  
  isLoading.value = true
  error.value = null
  success.value = false
  
  try {
    const result = await authStore.register(username.value, password.value)
    
    if (result) {
      // Success - show message and redirect
      success.value = true
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      // Failed - show error
      error.value = authStore.error || 'Registration failed. Please try again.'
    }
  } catch (err) {
    error.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ============================================
   Container & Layout
   ============================================ */

.register-container {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

/* ============================================
   Hero Section (Left Side)
   ============================================ */

.hero-section {
  flex: 1;
  background: linear-gradient(135deg, var(--success) 0%, var(--success-dark) 100%);
  padding: var(--space-4xl);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-20px, 20px) rotate(240deg); }
}

.hero-content {
  max-width: 600px;
  position: relative;
  z-index: 1;
}

.brand-header {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  margin-bottom: var(--space-2xl);
}

.logo-icon {
  font-size: 64px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.brand-name {
  font-size: var(--font-size-page-title);
  font-weight: var(--font-weight-bold);
  color: var(--text-inverse);
  margin: 0;
}

.tagline {
  font-size: var(--font-size-section-title);
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: var(--space-4xl);
  line-height: var(--line-height-relaxed);
}

.features-list {
  display: grid;
  gap: var(--space-xl);
}

.feature-item {
  display: flex;
  gap: var(--space-lg);
  align-items: flex-start;
  padding: var(--space-lg);
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all var(--transition-base);
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(10px);
}

.feature-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.feature-text h3 {
  font-size: var(--font-size-card-title);
  font-weight: var(--font-weight-semibold);
  color: var(--text-inverse);
  margin: 0 0 var(--space-xs) 0;
}

.feature-text p {
  font-size: var(--font-size-body-sm);
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.hero-decoration {
  position: absolute;
  bottom: -100px;
  right: -100px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: var(--radius-full);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

/* ============================================
   Form Section (Right Side)
   ============================================ */

.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-3xl);
  background: var(--bg-primary);
  position: relative;
}

.form-wrapper {
  width: 100%;
  max-width: 480px;
  animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.theme-toggle {
  position: absolute;
  top: var(--space-xl);
  right: var(--space-xl);
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: var(--surface);
  border: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.theme-toggle:hover {
  background: var(--surface-hover);
  transform: scale(1.1) rotate(15deg);
  box-shadow: var(--shadow-md);
}

/* ============================================
   Register Card
   ============================================ */

.card-register {
  background: var(--surface);
  border-radius: var(--radius-xl);
  padding: var(--space-3xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-primary);
  transition: all var(--transition-base);
}

.card-register:hover {
  box-shadow: var(--shadow-xl);
}

.card-header {
  margin-bottom: var(--space-2xl);
}

.card-header h2 {
  font-size: var(--font-size-section-title);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--space-sm) 0;
}

.card-header p {
  font-size: var(--font-size-body);
  color: var(--text-secondary);
  margin: 0;
}

/* ============================================
   Form Styles
   ============================================ */

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.input-modern {
  height: var(--input-height);
  border-radius: var(--radius-md);
  font-size: var(--font-size-body-sm);
  padding: 0 var(--space-lg);
  border: 2px solid var(--border-primary);
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: all 0.25s ease;
}

.input-modern:hover {
  border-color: var(--border-focus);
}

.input-modern:focus {
  border-color: var(--border-focus);
  background: var(--surface);
  box-shadow: 0 0 0 4px var(--primary-light);
  transform: translateY(-2px);
}

.input-modern:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-helper {
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
}

.password-wrapper {
  position: relative;
}

.password-toggle-btn {
  position: absolute;
  right: var(--space-lg);
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: var(--space-sm);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
  opacity: 0.6;
}

.password-toggle-btn:hover:not(:disabled) {
  opacity: 1;
  background: var(--bg-hover);
  transform: translateY(-50%) scale(1.1);
}

.password-toggle-btn:disabled {
  cursor: not-allowed;
  opacity: 0.3;
}

.checkbox-modern {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  cursor: pointer;
  user-select: none;
}

.checkbox-modern input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  cursor: pointer;
  accent-color: var(--primary);
  flex-shrink: 0;
}

.checkbox-modern span {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}

.link-inline {
  color: var(--primary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.link-inline:hover {
  color: var(--primary-hover);
  text-decoration: underline;
}

/* ============================================
   Success Message
   ============================================ */

.success-message {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--success-light);
  border: 1px solid var(--success);
  border-radius: var(--radius-md);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.success-content {
  flex: 1;
}

.success-content strong {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--success);
  margin-bottom: var(--space-xs);
}

.success-content p {
  font-size: var(--font-size-sm);
  color: var(--success-dark);
  margin: 0;
}

/* ============================================
   Error Message
   ============================================ */

.error-message {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--danger-light);
  border: 1px solid var(--danger);
  border-radius: var(--radius-md);
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.error-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.error-content {
  flex: 1;
}

.error-content strong {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--danger);
  margin-bottom: var(--space-xs);
}

.error-content p {
  font-size: var(--font-size-sm);
  color: var(--danger-dark);
  margin: 0;
}

/* ============================================
   Register Button
   ============================================ */

.btn-register {
  height: var(--input-height);
  font-weight: 600;
  border-radius: var(--radius-md);
  font-size: var(--font-size-body);
  background: var(--success);
  color: var(--text-inverse);
  border: none;
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.btn-register::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s;
}

.btn-register:hover:not(:disabled)::before {
  left: 100%;
}

.btn-register:hover:not(:disabled) {
  background: var(--success-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-register:active:not(:disabled) {
  transform: translateY(0);
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ============================================
   Card Footer
   ============================================ */

.card-footer {
  margin-top: var(--space-2xl);
  padding-top: var(--space-xl);
  border-top: 1px solid var(--border-primary);
  text-align: center;
}

.card-footer p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
}

.signin-link {
  color: var(--primary);
  font-weight: var(--font-weight-semibold);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.signin-link:hover {
  color: var(--primary-hover);
  text-decoration: underline;
}

.terms-text {
  margin-top: var(--space-xl);
  text-align: center;
  font-size: var(--font-size-body-sm);
  color: var(--text-tertiary);
}

.terms-text a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.terms-text a:hover {
  color: var(--primary);
  text-decoration: underline;
}

/* ============================================
   Responsive Design
   ============================================ */

@media (max-width: 1024px) {
  .register-container {
    flex-direction: column;
  }

  .hero-section {
    min-height: 40vh;
    padding: var(--space-2xl);
  }

  .hero-content {
    max-width: 100%;
  }

  .brand-header {
    justify-content: center;
  }

  .tagline {
    text-align: center;
  }

  .features-list {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-section {
    padding: var(--space-2xl);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: var(--space-xl);
  }

  .brand-name {
    font-size: var(--font-size-section-title);
  }

  .logo-icon {
    font-size: 48px;
  }

  .tagline {
    font-size: var(--font-size-body);
  }

  .features-list {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }

  .feature-item {
    padding: var(--space-md);
  }

  .form-section {
    padding: var(--space-lg);
  }

  .card-register {
    padding: var(--space-xl);
  }

  .theme-toggle {
    top: var(--space-md);
    right: var(--space-md);
  }
}

@media (max-width: 480px) {
  .card-header h2 {
    font-size: var(--font-size-2xl);
  }

  .input-modern,
  .btn-register {
    height: 48px;
  }
}
</style>
