<template>
  <div class="chat-container">
    <!-- 聊天头部：显示标题和设置按钮 -->
    <div class="chat-header">
      <div class="header-left">
        <el-button text @click="router.back()">
          <el-icon :size="22"><ArrowLeft /></el-icon>
        </el-button>
        <span class="title">AI对话</span>
      </div>
      <el-button text @click="showSettings = true">
        <el-icon :size="22"><Setting /></el-icon>
      </el-button>
    </div>
    
    <!-- 聊天消息区域：显示用户和AI的对话 -->
    <div class="chat-messages" ref="messagesRef">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message-item', message.type]"
      >
        <div class="message-avatar">
          <el-avatar v-if="message.type === 'user'" :size="36">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div v-else class="ai-avatar">
            <el-icon :size="20"><ChatDotRound /></el-icon>
          </div>
        </div>
        <div class="message-content">
          <div class="message-text">{{ message.content }}</div>
          
          <!-- 话术卡片：显示推荐的话术 -->
          <div v-if="message.scripts && message.scripts.length > 0" class="script-cards">
            <div
              v-for="script in message.scripts"
              :key="script.id"
              class="script-card"
              @click="viewScript(script)"
            >
              <div class="script-header">
                <span class="script-title">{{ script.title }}</span>
                <el-tag size="small" :type="getToneType(script.tone)">{{ script.tone }}</el-tag>
              </div>
              <div class="script-preview">{{ getPreviewContent(script) }}</div>
              <div class="script-actions">
                <el-button size="small" text @click.stop="copyScript(script)">
                  <el-icon><DocumentCopy /></el-icon>
                  复制
                </el-button>
                <el-button size="small" text @click.stop="toggleFavorite(script)">
                  <el-icon><Star /></el-icon>
                  {{ isFavorite(script.id) ? '已收藏' : '收藏' }}
                </el-button>
                <el-dropdown @command="(cmd) => adjustScript(script, cmd)">
                  <el-button size="small" text>
                    <el-icon><MagicStick /></el-icon>
                    调整
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="温和">温和语气</el-dropdown-item>
                      <el-dropdown-item command="专业">专业语气</el-dropdown-item>
                      <el-dropdown-item command="简洁">简洁版</el-dropdown-item>
                      <el-dropdown-item command="详细">详细版</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 加载中提示：显示AI正在输入的动画 -->
      <div v-if="loading" class="message-item assistant">
        <div class="message-avatar">
          <div class="ai-avatar">
            <el-icon :size="20"><ChatDotRound /></el-icon>
          </div>
        </div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 输入区域：用户输入消息 -->
    <div class="chat-input">
      <el-input
        v-model="inputMessage"
        type="textarea"
        :rows="3"
        placeholder="描述你的沟通场景，我会帮你找到合适的话术..."
        @keydown.enter.prevent="handleSend"
        :disabled="loading"
      />
      <el-button
        type="primary"
        :icon="Promotion"
        :loading="loading"
        @click="handleSend"
        :disabled="!inputMessage.trim()"
      >
        发送
      </el-button>
    </div>
    
    <!-- 设置抽屉：配置对话参数 -->
    <el-drawer v-model="showSettings" title="对话设置" size="280px">
      <el-form label-position="top">
        <el-form-item label="语气偏好">
          <el-select v-model="settings.tone" style="width: 100%">
            <el-option label="温和" value="温和" />
            <el-option label="专业" value="专业" />
            <el-option label="强硬" value="强硬" />
            <el-option label="活泼" value="活泼" />
            <el-option label="委婉" value="委婉" />
          </el-select>
        </el-form-item>
        <el-form-item label="长度偏好">
          <el-select v-model="settings.length" style="width: 100%">
            <el-option label="简洁版" value="简洁版" />
            <el-option label="详细版" value="详细版" />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位">
          <el-select v-model="settings.position" placeholder="选择岗位" style="width: 100%">
            <el-option label="售前人员" value="售前人员" />
            <el-option label="项目经理" value="项目经理" />
            <el-option label="产品经理" value="产品经理" />
            <el-option label="前端开发" value="前端开发" />
            <el-option label="后端开发" value="后端开发" />
            <el-option label="UI设计师" value="UI设计师" />
            <el-option label="测试工程师" value="测试工程师" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { sendMessage, adjustScript as adjustScriptApi } from '@/api/chat'
import { addFavorite, removeFavorite, getFavorites } from '@/api/script'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft, Setting, User, ChatDotRound, Promotion,
  DocumentCopy, Star, MagicStick
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref(null)
const showSettings = ref(false)
const sessionId = ref('')
const favoriteIds = ref([])

const settings = reactive({
  tone: userStore.userInfo?.tone_preference || '温和',
  length: userStore.userInfo?.length_preference || '简洁版',
  position: userStore.userInfo?.role || ''
})

onMounted(async () => {
  sessionId.value = Date.now().toString()
  
  if (route.query.initialMessage) {
    inputMessage.value = route.query.initialMessage
    await handleSend()
  }
  
  await loadFavorites()
})

const loadFavorites = async () => {
  try {
    const favorites = await getFavorites()
    favoriteIds.value = favorites.map(f => f.script_id)
  } catch (error) {
    console.error('加载收藏失败:', error)
  }
}

const isFavorite = (scriptId) => {
  return favoriteIds.value.includes(scriptId)
}

const toggleFavorite = async (script) => {
  try {
    if (isFavorite(script.id)) {
      await removeFavorite(script.id)
      favoriteIds.value = favoriteIds.value.filter(id => id !== script.id)
      ElMessage.success('已取消收藏')
    } else {
      await addFavorite({ script_id: script.id })
      favoriteIds.value.push(script.id)
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
  }
}

const getPreviewContent = (script) => {
  const content = settings.length === '简洁版' && script.brief_content
    ? script.brief_content
    : script.content
  return content.length > 80 ? content.substring(0, 80) + '...' : content
}

const getToneType = (tone) => {
  const types = {
    '温和': 'success',
    '专业': 'primary',
    '强硬': 'danger',
    '活泼': 'warning',
    '委婉': 'info'
  }
  return types[tone] || 'default'
}

const copyScript = async (script) => {
  const content = settings.length === '简洁版' && script.brief_content
    ? script.brief_content
    : script.content
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const adjustScript = async (script, command) => {
  try {
    let tone = settings.tone
    let lengthType = null
    
    if (['温和', '专业', '强硬', '活泼', '委婉'].includes(command)) {
      tone = command
    } else if (['简洁', '详细'].includes(command)) {
      lengthType = command + '版'
    }
    
    const result = await adjustScriptApi({
      script_id: script.id,
      tone: tone,
      length_type: lengthType
    })
    
    ElMessage.success({
      message: result.adjusted_content,
      duration: 5000
    })
    
    await navigator.clipboard.writeText(result.adjusted_content)
  } catch (error) {
    console.error('调整话术失败:', error)
  }
}

const viewScript = (script) => {
  const content = settings.length === '简洁版' && script.brief_content
    ? script.brief_content
    : script.content
  ElMessage.success({
    message: content,
    duration: 5000
  })
}

const handleSend = async () => {
  const message = inputMessage.value.trim()
  if (!message || loading.value) return
  
  messages.value.push({
    type: 'user',
    content: message
  })
  
  inputMessage.value = ''
  loading.value = true
  
  await nextTick()
  scrollToBottom()
  
  try {
    const response = await sendMessage({
      message,
      session_id: sessionId.value,
      position: settings.position,
      tone: settings.tone,
      length: settings.length
    })
    
    messages.value.push({
      type: 'assistant',
      content: response.reply,
      scripts: response.scripts
    })
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败，请重试')
  } finally {
    loading.value = false
  }
}

const scrollToBottom = () => {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}
</script>

<style lang="scss" scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  background: white;
  border-bottom: 1px solid #eee;
  
  .header-left {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .title {
      font-size: 18px;
      font-weight: 600;
      color: #333;
    }
  }
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  padding-bottom: 10px;
  
  .message-item {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    
    &.user {
      flex-direction: row-reverse;
      
      .message-content {
        background: #409EFF;
        color: white;
        border-radius: 16px 16px 0 16px;
      }
    }
    
    &.assistant {
      .message-content {
        background: white;
        color: #333;
        border-radius: 16px 16px 16px 0;
      }
    }
    
    .message-avatar {
      flex-shrink: 0;
      
      .ai-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      }
    }
    
    .message-content {
      max-width: 75%;
      padding: 12px 16px;
      word-wrap: break-word;
    }
    
    .message-text {
      line-height: 1.6;
      white-space: pre-wrap;
    }
    
    .script-cards {
      margin-top: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    
    .script-card {
      background: #ffffff;
      border: 1px solid #e4e7ed;
      border-radius: 10px;
      padding: 12px;
      cursor: pointer;
      transition: all 0.3s;
      
      &:active {
        transform: scale(0.98);
      }
      
      .script-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
        
        .script-title {
          font-size: 14px;
          font-weight: 600;
          color: #303133;
        }
      }
      
      .script-preview {
        font-size: 13px;
        color: #606266;
        margin-bottom: 10px;
        line-height: 1.5;
      }
      
      .script-actions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        
        .el-button {
          color: #606266;
          padding: 4px 8px;
          font-size: 12px;
          
          .el-icon {
            margin-right: 3px;
          }
          
          &:hover {
            color: #409EFF;
          }
        }
      }
    }
  }
  
  .typing-indicator {
    display: flex;
    gap: 4px;
    padding: 8px 0;
    
    span {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ccc;
      animation: typing 1.4s infinite;
      
      &:nth-child(2) {
        animation-delay: 0.2s;
      }
      
      &:nth-child(3) {
        animation-delay: 0.4s;
      }
    }
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px 20px;
  background: white;
  border-top: 1px solid #eee;
  
  .el-textarea {
    flex: 1;
  }
  
  .el-button {
    height: auto;
    align-self: flex-end;
  }
}
</style>
