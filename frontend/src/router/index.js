import {
  createRouter,
  createWebHistory
} from 'vue-router'

import LoginPage from
'../pages/LoginPage.vue'

import RegisterPage from
'../pages/RegisterPage.vue'

import DashboardPage from
'../pages/DashboardPage.vue'

import ChatRoomPage from
'../pages/ChatRoomPage.vue'

import SettingsPage from
'../pages/SettingsPage.vue'

import ProfilePage from
'../pages/ProfilePage.vue'

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(
      atob(token.split('.')[1])
    )
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: LoginPage,
  },
  {
    path: '/register',
    component: RegisterPage,
  },
  {
    path: '/dashboard',
    component: DashboardPage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/chat/:roomId',
    component: ChatRoomPage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/settings',
    component: SettingsPage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    component: ProfilePage,
    meta: {
      requiresAuth: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(
  (to, from, next) => {
    const token =
      localStorage.getItem(
        'access'
      )

    if (
      to.meta.requiresAuth &&
      (!token || isTokenExpired(token))
    ) {
      localStorage.clear()
      next('/login')
      return
    }

    if (
      (
        to.path === '/login'
        ||
        to.path === '/register'
      )
      &&
      token
      &&
      !isTokenExpired(token)
    ) {
      next('/dashboard')
      return
    }

    next()
  }
)

export default router