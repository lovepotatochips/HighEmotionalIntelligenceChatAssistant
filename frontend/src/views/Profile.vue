<template>
  <div class="profile-container">
    <div class="header">
      <div class="header-left">
        <el-button text @click="router.back()">
          <el-icon :size="22"><ArrowLeft /></el-icon>
        </el-button>
        <span class="title">个人中心</span>
      </div>
    </div>
    
    <div class="profile-content">
      <div class="profile-card">
        <div class="avatar-section">
          <el-avatar :size="80" :src="userStore.userInfo?.avatar_url">
            <el-icon :size="40"><User /></el-icon>
          </el-avatar>
          <div class="user-info">
            <h2>{{ userStore.userInfo?.username }}</h2>
            <el-tag>{{ userStore.userInfo?.role }}</el-tag>
          </div>
        </div>
      </div>
      
      <div class="settings-card">
        <div class="card-title">偏好设置</div>
        
        <div class="setting-item">
          <label>语气偏好</label>
          <el-select v-model="settings.tone" @change="updateSettings">
            <el-option label="温和" value="温和" />
            <el-option label="专业" value="专业" />
            <el-option label="强硬" value="强硬" />
            <el-option label="活泼" value="活泼" />
            <el-option label="委婉" value="委婉" />
          </el-select>
        </div>
        
        <div class="setting-item">
          <label>长度偏好</label>
          <el-select v-model="settings.length" @change="updateSettings">
            <el-option label="简洁版" value="简洁版" />
            <el-option label="详细版" value="详细版" />
          </el-select>
        </div>
        
        <div class="setting-item">
          <label>岗位</label>
          <el-select v-model="settings.role" @change="updateSettings">
            <el-option label="售前人员" value="售前人员" />
            <el-option label="项目经理" value="项目经理" />
            <el-option label="产品经理" value="产品经理" />
            <el-option label="前端开发" value="前端开发" />
            <el-option label="后端开发" value="后端开发" />
            <el-option label="UI设计师" value="UI设计师" />
            <el-option label="测试工程师" value="测试工程师" />
          </el-select>
        </div>
      </div>
      
      <div class="info-card">
        <div class="card-title">账号信息</div>
        
        <div class="info-item">
          <label>用户名</label>
          <span>{{ userStore.userInfo?.username }}</span>
        </div>
        
        <div class="info-item">
          <label>手机号</label>
          <span>{{ userStore.userInfo?.phone || '未设置' }}</span>
        </div>
        
        <div class="info-item">
          <label>邮箱</label>
          <span>{{ userStore.userInfo?.email || '未设置' }}</span>
        </div>
        
        <div class="info-item">
          <label>VIP状态</label>
          <el-tag :type="userStore.userInfo?.is_vip ? 'success' : 'info'">
            {{ userStore.userInfo?.is_vip ? 'VIP会员' : '普通用户' }}
          </el-tag>
        </div>
      </div>
      
      <div class="action-buttons">
        <el-button type="danger" @click="handleLogout" style="width: 100%">
          退出登录
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { updateUser } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, User } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const settings = reactive({
  tone: '温和',
  length: '简洁版',
  role: ''
})

onMounted(() => {
  if (userStore.userInfo) {
    settings.tone = userStore.userInfo.tone_preference || '温和'
    settings.length = userStore.userInfo.length_preference || '简洁版'
    settings.role = userStore.userInfo.role || ''
  }
})

const updateSettings = async () => {
  try {
    await updateUser({
      tone_preference: settings.tone,
      length_preference: settings.length,
      role: settings.role
    })
    await userStore.fetchUserInfo()
    ElMessage.success('设置已更新')
  } catch (error) {
    console.error('更新设置失败:', error)
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
  
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

.profile-content {
  padding: 20px;
}

.profile-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  color: white;
  margin-bottom: 20px;
  
  .avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    
    .user-info {
      h2 {
        font-size: 20px;
        font-weight: 600;
        margin: 0 0 8px 0;
      }
    }
  }
}

.settings-card,
.info-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  
  .card-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 20px;
  }
  
  .setting-item,
  .info-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f5f5f5;
    
    &:last-child {
      border-bottom: none;
    }
    
    label {
      font-size: 14px;
      color: #666;
    }
    
    span {
      font-size: 14px;
      color: #333;
    }
    
    .el-select {
      width: 150px;
    }
  }
}

.action-buttons {
  margin-top: 20px;
}
</style>
