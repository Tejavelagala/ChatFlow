import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import LoginPage from '../pages/LoginPage.vue'

describe('LoginPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders login page correctly', () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    expect(wrapper.text()).toContain('ChatFlow')
    expect(wrapper.text()).toContain('Login')
  })

  it('has username and password inputs', () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const inputs = wrapper.findAll('input')
    expect(inputs).toHaveLength(2)
    expect(inputs[0].attributes('placeholder')).toBe('Username')
    expect(inputs[1].attributes('placeholder')).toBe('Password')
  })

  it('has login button', () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('Login')
  })

  it('updates username on input', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const usernameInput = wrapper.findAll('input')[0]
    await usernameInput.setValue('testuser')
    expect(wrapper.vm.username).toBe('testuser')
  })

  it('updates password on input', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['router-link']
      }
    })
    
    const passwordInput = wrapper.findAll('input')[1]
    await passwordInput.setValue('testpass')
    expect(wrapper.vm.password).toBe('testpass')
  })
})