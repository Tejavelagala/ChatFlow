import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import RegisterPage from '../pages/RegisterPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'

describe('RegisterPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders register page', () => {
    const wrapper = mount(RegisterPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    expect(wrapper.text()).toContain('ChatFlow')
    expect(wrapper.text()).toContain('Register')
  })

  it('has username and password inputs', () => {
    const wrapper = mount(RegisterPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const inputs = wrapper.findAll('input')
    expect(inputs.length).toBeGreaterThanOrEqual(2)
  })
})

describe('DashboardPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.setItem('username', 'testuser')
  })

  it('renders dashboard page', () => {
    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    expect(wrapper.text()).toContain('ChatFlow')
  })

  it('has create room input', () => {
    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const input = wrapper.find('.room-input')
    expect(input.exists()).toBe(true)
  })

  it('has create button', () => {
    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const button = wrapper.find('.create-btn')
    expect(button.exists()).toBe(true)
  })
})
