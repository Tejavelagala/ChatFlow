# 💬 ChatFlow Frontend

> A production-ready real-time chat application built with Vue 3, Vite, and modern UX principles.

## 🚀 Features

### Core Functionality
- ✅ Real-time messaging with WebSocket
- ✅ Multiple chat rooms
- ✅ User authentication (JWT)
- ✅ Message reactions
- ✅ Reply to messages
- ✅ Edit/Delete messages
- ✅ Image & file sharing
- ✅ Voice messages
- ✅ Typing indicators
- ✅ Online presence
- ✅ Message search
- ✅ Pinned messages
- ✅ User profiles
- ✅ Dark mode

### UX Polish (U6 Sprint)
- ✅ Toast notifications on all actions
- ✅ Loading states everywhere
- ✅ Confirmation dialogs for dangerous actions
- ✅ Success micro-feedback animations
- ✅ Search result highlighting
- ✅ Keyboard shortcuts (Enter, Shift+Enter, Esc)
- ✅ Skeleton loaders
- ✅ Empty states with helpful messages
- ✅ Full accessibility (WCAG 2.1 AA)
- ✅ Mobile-first responsive design
- ✅ Smooth animations and transitions
- ✅ Connection status feedback

## 🛠️ Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **WebSocket**: Native WebSocket API
- **Notifications**: Vue Toastification
- **Virtual Scrolling**: Vue Virtual Scroller
- **Image Compression**: Browser Image Compression
- **Styling**: CSS Variables + Custom Design System

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test
```

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── assets/          # CSS and static assets
│   │   ├── theme.css    # Design system variables
│   │   └── components.css
│   ├── components/      # Vue components
│   │   ├── chat/        # Chat-specific components
│   │   └── common/      # Reusable components
│   ├── composables/     # Vue composables
│   │   └── useKeyboardShortcuts.js
│   ├── config/          # Configuration
│   ├── layouts/         # Layout components
│   ├── pages/           # Page components
│   ├── router/          # Vue Router config
│   ├── services/        # API services
│   ├── stores/          # Pinia stores
│   ├── utils/           # Utility functions
│   ├── App.vue          # Root component
│   └── main.js          # Entry point
├── public/              # Static assets
└── package.json
```

## 🎨 Design System

### CSS Variables
All colors, spacing, and typography use CSS variables defined in `theme.css`:

```css
/* Colors */
var(--primary)
var(--success)
var(--danger)
var(--warning)

/* Text */
var(--text-primary)
var(--text-secondary)

/* Spacing */
var(--space-sm)
var(--space-md)
var(--space-lg)

/* Shadows */
var(--shadow-sm)
var(--shadow-md)
var(--shadow-lg)
```

### Dark Mode
Automatic dark mode support with `.dark` class on `<html>`.

## 🧩 Key Components

### Common Components
- **ConfirmDialog** - Confirmation dialogs
- **EmptyState** - Empty state placeholders
- **ErrorState** - Error displays
- **LoadingSpinner** - Loading indicators
- **Modal** - Modal dialogs
- **SkeletonLoader** - Loading skeletons
- **SuccessFeedback** - Success animations
- **TextHighlight** - Search highlighting
- **NotificationCenter** - Notification panel

### Chat Components
- **ChatHeader** - Chat room header
- **ChatInput** - Message input with emoji picker
- **ChatMessages** - Message list with virtual scrolling
- **MessageBubble** - Individual message
- **TypingIndicator** - Typing status
- **OnlineUsers** - Online user list
- **MemberList** - Room members
- **Reactions** - Message reactions
- **ReplyPreview** - Reply preview
- **PinnedMessages** - Pinned messages

## 🎯 Stores (Pinia)

- **authStore** - Authentication state
- **roomStore** - Chat rooms
- **messageStore** - Messages
- **profileStore** - User profiles
- **presenceStore** - Online presence
- **notificationStore** - Notifications
- **themeStore** - Theme preferences

## ⌨️ Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line
- `Esc` - Close modal / Cancel reply

## ♿ Accessibility

- Semantic HTML5 elements
- ARIA labels and roles
- Keyboard navigation
- Focus indicators
- Screen reader support
- High contrast mode
- Reduced motion support

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 480px)

/* Tablet */
@media (max-width: 768px)

/* Desktop */
@media (max-width: 1024px)
```

## 🔧 Configuration

### Environment Variables
Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

### Runtime Config
See `src/config/runtime.js` for dynamic configuration.

## 🧪 Testing

See `TESTING_GUIDE.md` for comprehensive testing checklist.

```bash
npm run test
```

## 📚 Documentation

- **UX_POLISH_CHECKLIST.md** - Complete feature checklist
- **COMPONENT_USAGE_GUIDE.md** - Component usage examples
- **TESTING_GUIDE.md** - Testing procedures
- **U6_SUMMARY.md** - UX sprint summary

## 🎨 Animation Guidelines

```css
/* Fast interactions */
transition: all 150ms ease;

/* Standard transitions */
transition: all 200ms ease;

/* Modals and slides */
transition: all 300ms ease;

/* Smooth easing */
transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
```

## 🚀 Performance

- Lazy loading images
- Virtual scrolling for messages
- Debounced search
- Throttled typing indicators
- Optimized re-renders
- Tree-shakeable utilities

## 🔐 Security

- JWT authentication
- XSS protection
- CSRF protection
- Input sanitization
- Secure WebSocket connections

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📞 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ using Vue 3 + Vite**
