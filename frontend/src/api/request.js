// 导入axios HTTP客户端库
import axios from 'axios'
// 导入Element Plus的消息提示组件
import { ElMessage } from 'element-plus'
// 导入用户状态管理store
import { useUserStore } from '@/stores/user'
// 导入路由实例
import router from '@/router'

// 创建axios实例，配置基础URL和超时时间
const request = axios.create({
  baseURL: '/api',  // API基础路径
  timeout: 10000    // 请求超时时间（毫秒）
})

// 请求拦截器：在发送请求前进行处理
request.interceptors.request.use(
  config => {
    // 获取用户store实例
    const userStore = useUserStore()
    // 如果用户已登录，在请求头中添加token
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    // 请求错误时返回Promise reject
    return Promise.reject(error)
  }
)

// 响应拦截器：处理响应数据和错误
request.interceptors.response.use(
  response => {
    // 成功响应时，直接返回响应数据
    return response.data
  },
  error => {
    // 错误处理
    if (error.response) {
      // 有响应但状态码非200
      const { status, data } = error.response
      
      // 401：未授权/登录过期
      if (status === 401) {
        const userStore = useUserStore()
        userStore.logout()      // 清除用户登录状态
        router.push('/login')    // 跳转到登录页
        ElMessage.error('登录已过期，请重新登录')
      } else if (status === 403) {
        // 403：禁止访问
        ElMessage.error('没有权限访问')
      } else if (status === 404) {
        // 404：资源不存在
        ElMessage.error('请求的资源不存在')
      } else if (status === 500) {
        // 500：服务器内部错误
        ElMessage.error('服务器错误，请稍后重试')
      } else {
        // 其他错误
        ElMessage.error(data.detail || '请求失败')
      }
    } else {
      // 无响应，可能是网络错误
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    // 返回Promise reject，让调用者可以继续处理错误
    return Promise.reject(error)
  }
)

export default request
