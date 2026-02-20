<template>
  <div class="favorites-container">
    <div class="header">
      <div class="header-left">
        <el-button text @click="router.back()">
          <el-icon :size="22"><ArrowLeft /></el-icon>
        </el-button>
        <span class="title">我的收藏</span>
      </div>
      <el-button text @click="loadFavorites">
        <el-icon :size="22"><Refresh /></el-icon>
      </el-button>
    </div>
    
    <div class="favorites-list" v-loading="loading">
      <div
        v-for="favorite in favorites"
        :key="favorite.id"
        class="favorite-card"
      >
        <div class="favorite-header">
          <h3 class="favorite-title">{{ favorite.script.title }}</h3>
          <el-button text @click="removeFavorite(favorite.script_id)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
        <div class="favorite-content">
          {{ favorite.custom_content || favorite.script.content }}
        </div>
        <div class="favorite-footer">
          <el-tag size="small" :type="getToneType(favorite.script.tone)">
            {{ favorite.script.tone }}
          </el-tag>
          <el-tag size="small" type="info">{{ favorite.script.scene_type }}</el-tag>
          <span class="favorite-date">{{ formatDate(favorite.created_at) }}</span>
        </div>
      </div>
      
      <el-empty
        v-if="!loading && favorites.length === 0"
        description="暂无收藏的话术"
      >
        <el-button type="primary" @click="router.push('/scripts')">
          去收藏话术
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getFavorites, removeFavorite as removeFavoriteApi } from '@/api/script'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Refresh, Delete } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const favorites = ref([])

onMounted(() => {
  loadFavorites()
})

const loadFavorites = async () => {
  loading.value = true
  try {
    favorites.value = await getFavorites()
  } catch (error) {
    console.error('加载收藏失败:', error)
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (scriptId) => {
  try {
    await removeFavoriteApi(scriptId)
    favorites.value = favorites.value.filter(f => f.script_id !== scriptId)
    ElMessage.success('已取消收藏')
  } catch (error) {
    console.error('取消收藏失败:', error)
  }
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

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}
</script>

<style lang="scss" scoped>
.favorites-container {
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

.favorites-list {
  padding: 20px;
}

.favorite-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  
  .favorite-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    
    .favorite-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
      margin: 0;
      flex: 1;
    }
  }
  
  .favorite-content {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
    margin-bottom: 12px;
    max-height: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
  }
  
  .favorite-footer {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    
    .favorite-date {
      margin-left: auto;
      font-size: 12px;
      color: #999;
    }
  }
}
</style>
