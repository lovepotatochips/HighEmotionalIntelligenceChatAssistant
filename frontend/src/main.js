// 导入 Vue 核心库的 createApp 函数
import { createApp } from 'vue'
// 导入 Pinia 状态管理库
import { createPinia } from 'pinia'
// 导入 Element Plus UI 组件库
import ElementPlus from 'element-plus'
// 导入 Element Plus 样式文件
import 'element-plus/dist/index.css'
// 导入 Element Plus 中文语言包
import zhCn from 'element-plus/es/locale/lang/zh-cn'
// 导入 Element Plus 图标库
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 导入路由配置
import router from './router'
// 导入根组件
import App from './App.vue'
// 导入全局样式文件
import './styles/index.scss'

// 创建 Vue 应用实例
const app = createApp(App)
// 创建 Pinia 状态管理实例
const pinia = createPinia()

// 遍历并注册所有 Element Plus 图标组件为全局组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册 Pinia 状态管理插件
app.use(pinia)
// 注册 Vue Router 路由插件
app.use(router)
// 注册 Element Plus UI 组件库，并配置中文语言环境
app.use(ElementPlus, {
  locale: zhCn
})

// 将 Vue 应用挂载到 DOM 中的 #app 元素
app.mount('#app')
