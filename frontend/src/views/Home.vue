<template>
  <div class="home-container">
    <!-- 顶部导航栏：显示用户信息和设置按钮 -->
    <div class="header">
      <div class="user-info">
        <el-avatar :size="40" :src="userStore.userInfo?.avatar_url">
          <el-icon><User /></el-icon>
        </el-avatar>
        <div class="user-text">
          <div class="username">{{ userStore.userInfo?.username }}</div>
          <div class="user-role">{{ userStore.userInfo?.role }}</div>
        </div>
      </div>
      <el-button text @click="router.push('/profile')">
        <el-icon :size="24"><Setting /></el-icon>
      </el-button>
    </div>
    
    <!-- 欢迎区域：展示个性化问候语 -->
    <div class="welcome-section">
      <h1>你好，{{ userStore.userInfo?.username }}</h1>
      <p>我是你的专属沟通搭子，有什么我可以帮你的吗？</p>
    </div>
    
    <!-- 快捷功能区域：提供三个主要功能入口 -->
    <div class="quick-actions">
      <div class="action-title">快捷功能</div>
      <div class="action-grid">
        <div class="action-card" @click="router.push('/chat')">
          <div class="icon-wrapper" style="background: #409EFF">
            <el-icon :size="28"><ChatDotRound /></el-icon>
          </div>
          <span>AI对话</span>
        </div>
        <div class="action-card" @click="router.push('/scripts')">
          <div class="icon-wrapper" style="background: #67C23A">
            <el-icon :size="28"><Collection /></el-icon>
          </div>
          <span>话术库</span>
        </div>
        <div class="action-card" @click="router.push('/favorites')">
          <div class="icon-wrapper" style="background: #E6A23C">
            <el-icon :size="28"><Star /></el-icon>
          </div>
          <span>我的收藏</span>
        </div>
      </div>
    </div>
    
    <div class="scenarios-section">
      <div class="section-title">常见场景</div>
      <div class="scenario-list">
        <div class="scenario-item" @click="startChat('需求沟通')">
          <div class="scenario-icon">
            <el-icon><ChatLineRound /></el-icon>
          </div>
          <div class="scenario-content">
            <div class="scenario-name">需求沟通</div>
            <div class="scenario-desc">高效传递需求，避免误解</div>
          </div>
          <el-icon class="arrow"><ArrowRight /></el-icon>
        </div>
        <div class="scenario-item" @click="startChat('项目推进')">
          <div class="scenario-icon" style="background: #E6F7FF">
            <el-icon color="#1890FF"><TrendCharts /></el-icon>
          </div>
          <div class="scenario-content">
            <div class="scenario-name">项目推进</div>
            <div class="scenario-desc">进度同步与风险沟通</div>
          </div>
          <el-icon class="arrow"><ArrowRight /></el-icon>
        </div>
        <div class="scenario-item" @click="startChat('Bug处理')">
          <div class="scenario-icon" style="background: #FFF1F0">
            <el-icon color="#F5222D"><Warning /></el-icon>
          </div>
          <div class="scenario-content">
            <div class="scenario-name">Bug处理</div>
            <div class="scenario-desc">专业反馈，高效协作</div>
          </div>
          <el-icon class="arrow"><ArrowRight /></el-icon>
        </div>
        <div class="scenario-item" @click="startChat('客户对接')">
          <div class="scenario-icon" style="background: #F0F5FF">
            <el-icon color="#2F54EB"><UserFilled /></el-icon>
          </div>
          <div class="scenario-content">
            <div class="scenario-name">客户对接</div>
            <div class="scenario-desc">专业得体，建立信任</div>
          </div>
          <el-icon class="arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const startChat = (scenario) => {
  router.push({
    path: '/chat',
    query: { initialMessage: `帮我找一些关于${scenario}的话术` }
  })
}
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-text {
  .username {
    font-size: 16px;
    font-weight: 600;
    color: #333;
  }
  
  .user-role {
    font-size: 12px;
    color: #999;
    margin-top: 2px;
  }
}

.welcome-section {
  padding: 30px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 14px;
    opacity: 0.9;
  }
}

.quick-actions {
  padding: 20px;
  
  .action-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 15px;
  }
  
  .action-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }
  
  .action-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 20px 10px;
    background: white;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:active {
      transform: scale(0.95);
    }
    
    .icon-wrapper {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    
    span {
      font-size: 13px;
      color: #666;
    }
  }
}

.scenarios-section {
  padding: 20px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 15px;
  }
  
  .scenario-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .scenario-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 16px;
    background: white;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:active {
      transform: scale(0.98);
      background: #fafafa;
    }
    
    .scenario-icon {
      width: 48px;
      height: 48px;
      border-radius: 10px;
      background: #F6FFED;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    
    .scenario-content {
      flex: 1;
      
      .scenario-name {
        font-size: 15px;
        font-weight: 600;
        color: #333;
        margin-bottom: 4px;
      }
      
      .scenario-desc {
        font-size: 13px;
        color: #999;
      }
    }
    
    .arrow {
      color: #ccc;
    }
  }
}
</style>
