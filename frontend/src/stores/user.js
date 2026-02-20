import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getUserInfo } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  function setUserInfo(info) {
    userInfo.value = info
  }

  async function login(username, password) {
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const response = await loginApi(formData)
      setToken(response.access_token)
      setUserInfo(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  async function register(userData) {
    try {
      const response = await registerApi(userData)
      return response
    } catch (error) {
      throw error
    }
  }

  async function fetchUserInfo() {
    try {
      const response = await getUserInfo()
      setUserInfo(response)
      return response
    } catch (error) {
      throw error
    }
  }

  function logout() {
    setToken('')
    setUserInfo(null)
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    logout
  }
})
