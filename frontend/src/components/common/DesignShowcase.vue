<template>
  <div class="design-showcase">
    <div class="showcase-container">
      <h1>Discord-Inspired Design System</h1>
      
      <!-- Colors Section -->
      <section class="showcase-section">
        <h2>Colors</h2>
        <div class="color-grid">
          <div class="color-item">
            <div class="color-swatch" style="background: var(--brand-primary)"></div>
            <span class="text-secondary">Brand Primary</span>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--success)"></div>
            <span class="text-secondary">Success</span>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--warning)"></div>
            <span class="text-secondary">Warning</span>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--danger)"></div>
            <span class="text-secondary">Danger</span>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--info)"></div>
            <span class="text-secondary">Info</span>
          </div>
        </div>
      </section>

      <!-- Buttons Section -->
      <section class="showcase-section">
        <h2>Buttons</h2>
        <div class="button-grid">
          <button class="btn btn-primary">Primary</button>
          <button class="btn btn-secondary">Secondary</button>
          <button class="btn btn-success">Success</button>
          <button class="btn btn-danger">Danger</button>
          <button class="btn btn-ghost">Ghost</button>
          <button class="btn btn-primary" disabled>Disabled</button>
        </div>
        <div class="button-grid" style="margin-top: var(--space-4)">
          <button class="btn btn-primary btn-sm">Small</button>
          <button class="btn btn-primary">Default</button>
          <button class="btn btn-primary btn-lg">Large</button>
        </div>
      </section>

      <!-- Form Controls Section -->
      <section class="showcase-section">
        <h2>Form Controls</h2>
        <div class="form-grid">
          <div>
            <label class="form-label">Username</label>
            <input type="text" class="form-control" placeholder="Enter username">
          </div>
          <div>
            <label class="form-label">Email</label>
            <input type="email" class="form-control" placeholder="Enter email">
          </div>
          <div>
            <label class="form-label">Message</label>
            <textarea class="form-control" placeholder="Enter message" rows="3"></textarea>
          </div>
        </div>
      </section>

      <!-- Cards Section -->
      <section class="showcase-section">
        <h2>Cards</h2>
        <div class="card-grid">
          <div class="card">
            <div class="card-header">Card Title</div>
            <div class="card-body">
              <p class="text-secondary">This is a card with header, body, and footer.</p>
            </div>
            <div class="card-footer">
              <button class="btn btn-primary btn-sm">Action</button>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <h3>Simple Card</h3>
              <p class="text-secondary">This card only has a body section.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Badges Section -->
      <section class="showcase-section">
        <h2>Badges</h2>
        <div class="badge-grid">
          <span class="badge badge-primary">Primary</span>
          <span class="badge badge-success">Success</span>
          <span class="badge badge-warning">Warning</span>
          <span class="badge badge-danger">Danger</span>
          <span class="badge badge-info">Info</span>
        </div>
      </section>

      <!-- Status Indicators Section -->
      <section class="showcase-section">
        <h2>Status Indicators</h2>
        <div class="status-grid">
          <div class="status-item">
            <span class="status-indicator status-online"></span>
            <span class="text-secondary">Online</span>
          </div>
          <div class="status-item">
            <span class="status-indicator status-idle"></span>
            <span class="text-secondary">Idle</span>
          </div>
          <div class="status-item">
            <span class="status-indicator status-dnd"></span>
            <span class="text-secondary">Do Not Disturb</span>
          </div>
          <div class="status-item">
            <span class="status-indicator status-offline"></span>
            <span class="text-secondary">Offline</span>
          </div>
        </div>
      </section>

      <!-- Typography Section -->
      <section class="showcase-section">
        <h2>Typography</h2>
        <div class="typography-grid">
          <h1>Heading 1</h1>
          <h2>Heading 2</h2>
          <h3>Heading 3</h3>
          <h4>Heading 4</h4>
          <p class="text-primary">Primary text - highest contrast</p>
          <p class="text-secondary">Secondary text - medium contrast</p>
          <p class="text-tertiary">Tertiary text - lower contrast</p>
          <p class="text-muted">Muted text - lowest contrast</p>
          <a href="#">Link text</a>
        </div>
      </section>

      <!-- Shadows Section -->
      <section class="showcase-section">
        <h2>Shadows</h2>
        <div class="shadow-grid">
          <div class="shadow-box shadow-sm">Small</div>
          <div class="shadow-box shadow-md">Medium</div>
          <div class="shadow-box shadow-lg">Large</div>
          <div class="shadow-box shadow-xl">Extra Large</div>
        </div>
      </section>

      <!-- Border Radius Section -->
      <section class="showcase-section">
        <h2>Border Radius</h2>
        <div class="radius-grid">
          <div class="radius-box rounded-sm">Small</div>
          <div class="radius-box rounded-md">Medium</div>
          <div class="radius-box rounded-lg">Large</div>
          <div class="radius-box rounded-xl">Extra Large</div>
          <div class="radius-box rounded-full" style="width: 80px; height: 80px;">Full</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// This is a showcase component - no logic needed
</script>

<style scoped>
.design-showcase {
  padding: var(--space-6);
  background: var(--bg-primary);
  min-height: 100vh;
}

.showcase-container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: var(--space-8);
  color: var(--text-primary);
}

.showcase-section {
  margin-bottom: var(--space-10);
}

.showcase-section h2 {
  margin-bottom: var(--space-4);
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 600;
}

/* Color Grid */
.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: var(--space-4);
}

.color-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.color-swatch {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}

/* Button Grid */
.button-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

/* Form Grid */
.form-grid {
  display: grid;
  gap: var(--space-4);
  max-width: 600px;
}

/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

/* Badge Grid */
.badge-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

/* Status Grid */
.status-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Typography Grid */
.typography-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

/* Shadow Grid */
.shadow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-6);
}

.shadow-box {
  padding: var(--space-6);
  background: var(--surface-primary);
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: 500;
}

/* Radius Grid */
.radius-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  align-items: center;
}

.radius-box {
  padding: var(--space-4) var(--space-6);
  background: var(--brand-primary);
  color: var(--text-inverse);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
