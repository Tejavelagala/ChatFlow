<template>
  <div class="u1-showcase">
    <div class="showcase-container">
      <!-- Header -->
      <div class="showcase-header">
        <h1>U1 — Design System Foundation</h1>
        <p class="text-secondary">Single source of truth for ChatFlow</p>
      </div>

      <!-- Color Palette -->
      <section class="showcase-section">
        <h2>Color Palette</h2>
        <div class="color-grid">
          <div class="color-card">
            <div class="color-swatch" style="background: var(--primary)"></div>
            <div class="color-info">
              <strong>Primary</strong>
              <code>#5865F2</code>
            </div>
          </div>
          <div class="color-card">
            <div class="color-swatch" style="background: var(--success)"></div>
            <div class="color-info">
              <strong>Success</strong>
              <code>#22C55E</code>
            </div>
          </div>
          <div class="color-card">
            <div class="color-swatch" style="background: var(--danger)"></div>
            <div class="color-info">
              <strong>Danger</strong>
              <code>#EF4444</code>
            </div>
          </div>
          <div class="color-card">
            <div class="color-swatch" style="background: var(--warning)"></div>
            <div class="color-info">
              <strong>Warning</strong>
              <code>#F59E0B</code>
            </div>
          </div>
        </div>
      </section>

      <!-- Buttons -->
      <section class="showcase-section">
        <h2>Buttons</h2>
        <div class="component-demo">
          <button class="btn-modern">Primary Button</button>
          <button class="btn-modern btn-secondary">Secondary</button>
          <button class="btn-modern btn-success">Success</button>
          <button class="btn-modern btn-danger">Danger</button>
          <button class="btn-modern btn-warning">Warning</button>
          <button class="btn-modern btn-ghost">Ghost</button>
          <button class="btn-modern btn-outline">Outline</button>
        </div>
        <div class="component-demo">
          <button class="btn-modern btn-sm">Small</button>
          <button class="btn-modern">Default</button>
          <button class="btn-modern btn-lg">Large</button>
          <button class="btn-modern" disabled>Disabled</button>
        </div>
      </section>

      <!-- Cards -->
      <section class="showcase-section">
        <h2>Cards</h2>
        <div class="cards-grid">
          <div class="card-modern">
            <div class="card-header">
              <h3>Card Title</h3>
            </div>
            <div class="card-body">
              <p>This is a modern card component with header, body, and footer sections.</p>
            </div>
            <div class="card-footer">
              <button class="btn-modern btn-secondary btn-sm">Cancel</button>
              <button class="btn-modern btn-sm">Confirm</button>
            </div>
          </div>

          <div class="card-modern card-interactive">
            <div class="card-body">
              <h3>Interactive Card</h3>
              <p class="text-secondary">Hover over this card to see the effect</p>
            </div>
          </div>

          <div class="card-modern card-primary">
            <div class="card-body">
              <h3>Primary Card</h3>
              <p class="text-secondary">Card with primary color accent</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Inputs -->
      <section class="showcase-section">
        <h2>Form Inputs</h2>
        <div class="form-demo">
          <div>
            <label class="input-label">Username</label>
            <input type="text" class="input-modern" placeholder="Enter your username">
          </div>
          <div>
            <label class="input-label required">Email</label>
            <input type="email" class="input-modern" placeholder="your@email.com">
            <span class="input-helper">We'll never share your email</span>
          </div>
          <div>
            <label class="input-label">Message</label>
            <textarea class="input-modern" placeholder="Type your message here..."></textarea>
          </div>
          <div class="input-group">
            <input type="text" class="input-modern" placeholder="Search...">
            <button class="btn-modern">Search</button>
          </div>
        </div>
      </section>

      <!-- Badges -->
      <section class="showcase-section">
        <h2>Badges</h2>
        <div class="component-demo">
          <span class="badge-modern">Primary</span>
          <span class="badge-modern badge-secondary">Secondary</span>
          <span class="badge-modern badge-success">Success</span>
          <span class="badge-modern badge-danger">Danger</span>
          <span class="badge-modern badge-warning">Warning</span>
          <span class="badge-modern badge-info">Info</span>
          <span class="badge-modern badge-outline">Outline</span>
        </div>
        <div class="component-demo">
          <span class="badge-modern badge-sm">Small</span>
          <span class="badge-modern">Default</span>
          <span class="badge-modern badge-lg">Large</span>
        </div>
      </section>

      <!-- Alerts -->
      <section class="showcase-section">
        <h2>Alerts</h2>
        <div class="alerts-demo">
          <div class="alert-modern alert-info">
            <div class="alert-icon">ℹ️</div>
            <div class="alert-content">
              <div class="alert-title">Information</div>
              <div class="alert-message">This is an informational alert message.</div>
            </div>
          </div>
          <div class="alert-modern alert-success">
            <div class="alert-icon">✅</div>
            <div class="alert-content">
              <div class="alert-title">Success</div>
              <div class="alert-message">Your action was completed successfully!</div>
            </div>
          </div>
          <div class="alert-modern alert-warning">
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
              <div class="alert-title">Warning</div>
              <div class="alert-message">Please review this warning message.</div>
            </div>
          </div>
          <div class="alert-modern alert-danger">
            <div class="alert-icon">❌</div>
            <div class="alert-content">
              <div class="alert-title">Error</div>
              <div class="alert-message">An error occurred. Please try again.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Avatars -->
      <section class="showcase-section">
        <h2>Avatars</h2>
        <div class="component-demo">
          <div class="avatar-wrapper">
            <div class="avatar-modern avatar-sm">JD</div>
            <span class="avatar-status online"></span>
          </div>
          <div class="avatar-wrapper">
            <div class="avatar-modern">JD</div>
            <span class="avatar-status online"></span>
          </div>
          <div class="avatar-wrapper">
            <div class="avatar-modern avatar-lg">JD</div>
            <span class="avatar-status idle"></span>
          </div>
          <div class="avatar-wrapper">
            <div class="avatar-modern avatar-xl">JD</div>
            <span class="avatar-status dnd"></span>
          </div>
        </div>
      </section>

      <!-- Progress Bars -->
      <section class="showcase-section">
        <h2>Progress Bars</h2>
        <div class="progress-demo">
          <div class="progress-modern">
            <div class="progress-bar" style="width: 25%"></div>
          </div>
          <div class="progress-modern">
            <div class="progress-bar progress-success" style="width: 50%"></div>
          </div>
          <div class="progress-modern">
            <div class="progress-bar progress-warning" style="width: 75%"></div>
          </div>
          <div class="progress-modern">
            <div class="progress-bar progress-danger" style="width: 100%"></div>
          </div>
        </div>
      </section>

      <!-- Loading Spinner -->
      <section class="showcase-section">
        <h2>Loading Spinners</h2>
        <div class="component-demo">
          <div class="spinner-modern spinner-sm"></div>
          <div class="spinner-modern"></div>
          <div class="spinner-modern spinner-lg"></div>
        </div>
      </section>

      <!-- Typography -->
      <section class="showcase-section">
        <h2>Typography</h2>
        <div class="typography-demo">
          <h1>Heading 1</h1>
          <h2>Heading 2</h2>
          <h3>Heading 3</h3>
          <h4>Heading 4</h4>
          <h5>Heading 5</h5>
          <h6>Heading 6</h6>
          <p>This is a paragraph with <strong>bold text</strong> and <a href="#">a link</a>.</p>
          <p class="text-secondary">Secondary text color</p>
          <p class="text-tertiary">Tertiary text color</p>
          <small>Small text</small>
        </div>
      </section>

      <!-- Spacing & Shadows -->
      <section class="showcase-section">
        <h2>Shadows</h2>
        <div class="shadows-demo">
          <div class="shadow-box shadow-sm">Small</div>
          <div class="shadow-box shadow-md">Medium</div>
          <div class="shadow-box shadow-lg">Large</div>
          <div class="shadow-box shadow-xl">Extra Large</div>
        </div>
      </section>

      <!-- Border Radius -->
      <section class="showcase-section">
        <h2>Border Radius</h2>
        <div class="radius-demo">
          <div class="radius-box rounded-sm">8px</div>
          <div class="radius-box rounded-md">12px</div>
          <div class="radius-box rounded-lg">18px</div>
          <div class="radius-box rounded-xl">24px</div>
          <div class="radius-box rounded-full">Full</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// U1 Design System Showcase
</script>

<style scoped>
.u1-showcase {
  min-height: 100vh;
  padding: var(--space-3xl);
  background-color: var(--bg-primary);
}

.showcase-container {
  max-width: 1200px;
  margin: 0 auto;
}

.showcase-header {
  margin-bottom: var(--space-4xl);
  text-align: center;
}

.showcase-header h1 {
  margin-bottom: var(--space-md);
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.showcase-section {
  margin-bottom: var(--space-4xl);
}

.showcase-section h2 {
  margin-bottom: var(--space-xl);
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--border-primary);
}

/* Color Grid */
.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-xl);
}

.color-card {
  text-align: center;
}

.color-swatch {
  width: 100%;
  height: 100px;
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow-md);
}

.color-info strong {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: var(--font-size-sm);
}

.color-info code {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* Component Demo */
.component-demo {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
  align-items: center;
  padding: var(--space-xl);
  background-color: var(--bg-secondary);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-md);
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-xl);
}

/* Form Demo */
.form-demo {
  display: grid;
  gap: var(--space-xl);
  max-width: 600px;
}

/* Alerts Demo */
.alerts-demo {
  display: grid;
  gap: var(--space-lg);
}

/* Progress Demo */
.progress-demo {
  display: grid;
  gap: var(--space-lg);
}

/* Typography Demo */
.typography-demo {
  display: grid;
  gap: var(--space-lg);
}

/* Shadows Demo */
.shadows-demo {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-xl);
}

.shadow-box {
  padding: var(--space-2xl);
  background-color: var(--surface);
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: var(--font-weight-medium);
}

/* Radius Demo */
.radius-demo {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xl);
  align-items: center;
}

.radius-box {
  padding: var(--space-xl) var(--space-2xl);
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: var(--text-inverse);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 100px;
}

.radius-box.rounded-full {
  width: 100px;
  height: 100px;
}
</style>
