<template>
  <div class="scripts-container">
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索话术..."
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
    </div>
    
    <div class="filter-bar">
      <el-dropdown @command="handleFilterPosition" trigger="click">
        <el-button>
          {{ selectedPosition || '全部岗位' }}
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="">全部岗位</el-dropdown-item>
            <el-dropdown-item
              v-for="position in positions"
              :key="position.id"
              :command="position.name"
            >
              {{ position.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      
      <el-dropdown @command="handleFilterTone" trigger="click">
        <el-button>
          {{ selectedTone || '全部语气' }}
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="">全部语气</el-dropdown-item>
            <el-dropdown-item command="温和">温和</el-dropdown-item>
            <el-dropdown-item command="专业">专业</el-dropdown-item>
            <el-dropdown-item command="强硬">强硬</el-dropdown-item>
            <el-dropdown-item command="活泼">活泼</el-dropdown-item>
            <el-dropdown-item command="委婉">委婉</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    
    <div class="scripts-list" v-loading="loading">
      <div
        v-for="script in scripts"
        :key="script.id"
        class="script-card"
        @click="showScriptDetail(script)"
      >
        <div class="script-header">
          <h3 class="script-title">{{ script.title }}</h3>
          <div class="script-tags">
            <el-tag size="small" :type="getToneType(script.tone)">{{ script.tone }}</el-tag>
            <el-tag size="small" type="info">{{ script.scene_type }}</el-tag>
          </div>
        </div>
        <div class="script-content">{{ getPreviewContent(script) }}</div>
        <div class="script-footer">
          <div class="script-stats">
            <span><el-icon><View /></el-icon> {{ script.usage_count }}</span>
            <span><el-icon><StarFilled /></el-icon> {{ script.like_count }}</span>
          </div>
          <div class="script-actions">
            <el-button size="small" text @click.stop="copyScript(script)">
              <el-icon><DocumentCopy /></el-icon>
              复制
            </el-button>
            <el-button size="small" text @click.stop="toggleFavorite(script)">
              <el-icon><Star /></el-icon>
              {{ isFavorite(script.id) ? '已收藏' : '收藏' }}
            </el-button>
          </div>
        </div>
      </div>
      
      <el-empty
        v-if="!loading && scripts.length === 0"
        description="暂无话术"
      />
    </div>
    
    <el-drawer v-model="showDetail" title="话术详情" size="90%">
      <div v-if="currentScript" class="script-detail">
        <div class="detail-header">
          <h2>{{ currentScript.title }}</h2>
          <div class="detail-tags">
            <el-tag :type="getToneType(currentScript.tone)">{{ currentScript.tone }}</el-tag>
            <el-tag type="info">{{ currentScript.scene_type }}</el-tag>
            <el-tag v-if="currentScript.target_audience" type="success">
              {{ currentScript.target_audience }}
            </el-tag>
          </div>
        </div>
        
        <div class="detail-content">
          <h4>话术内容</h4>
          <div class="content-text">{{ currentScript.content }}</div>
          
          <div v-if="currentScript.brief_content" class="brief-content">
            <h4>简洁版</h4>
            <div class="content-text">{{ currentScript.brief_content }}</div>
          </div>
        </div>
        
        <div class="detail-actions">
          <el-button type="primary" :icon="DocumentCopy" @click="copyScript(currentScript)">
            复制话术
          </el-button>
          <el-button :icon="Star" @click="toggleFavorite(currentScript)">
            {{ isFavorite(currentScript.id) ? '取消收藏' : '收藏' }}
          </el-button>
          <el-button :icon="ChatDotRound" @click="adjustScript">
            调整话术
          </el-button>
        </div>
      </div>
    </el-drawer>
    
    <el-drawer v-model="showAdjust" title="调整话术" size="400px">
      <el-form label-position="top">
        <el-form-item label="语气调整">
          <el-select v-model="adjustForm.tone" placeholder="选择语气" style="width: 100%">
            <el-option label="温和" value="温和" />
            <el-option label="专业" value="专业" />
            <el-option label="强硬" value="强硬" />
            <el-option label="活泼" value="活泼" />
            <el-option label="委婉" value="委婉" />
          </el-select>
        </el-form-item>
        <el-form-item label="长度调整">
          <el-select v-model="adjustForm.length_type" placeholder="选择长度" style="width: 100%">
            <el-option label="简洁版" value="简洁版" />
            <el-option label="详细版" value="详细版" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdjust" :loading="adjustLoading" style="width: 100%">
            生成调整后话术
          </el-button>
        </el-form-item>
        <el-form-item v-if="adjustedContent">
          <el-input
            v-model="adjustedContent"
            type="textarea"
            :rows="6"
            readonly
          />
        </el-form-item>
        <el-form-item v-if="adjustedContent">
          <el-button @click="copyAdjusted" :icon="DocumentCopy" style="width: 100%">
            复制调整后话术
          </el-button>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getScripts, likeScript, addFavorite, removeFavorite, getFavorites } from '@/api/script'
import { getPositions } from '@/api/system'
import { adjustScript as adjustScriptApi } from '@/api/chat'
import { ElMessage } from 'element-plus'
import {
  Search, ArrowDown, View, StarFilled, DocumentCopy,
  Star, ChatDotRound
} from '@element-plus/icons-vue'

const router = useRouter()

const searchKeyword = ref('')
const selectedPosition = ref('')
const selectedTone = ref('')
const loading = ref(false)
const scripts = ref([])
const positions = ref([])
const favoriteIds = ref([])
const showDetail = ref(false)
const showAdjust = ref(false)
const currentScript = ref(null)
const adjustLoading = ref(false)
const adjustedContent = ref('')

const adjustForm = reactive({
  tone: '',
  length_type: ''
})

onMounted(async () => {
  await loadPositions()
  await loadScripts()
  await loadFavorites()
})

const loadPositions = async () => {
  try {
    positions.value = await getPositions()
  } catch (error) {
    console.error('加载岗位失败:', error)
  }
}

const loadScripts = async () => {
  loading.value = true
  try {
    const params = {
      keyword: searchKeyword.value,
      position_id: getPositionId(selectedPosition.value),
      tone: selectedTone.value
    }
    const response = await getScripts(params)
    scripts.value = response.scripts
  } catch (error) {
    console.error('加载话术失败:', error)
  } finally {
    loading.value = false
  }
}

const loadFavorites = async () => {
  try {
    const favorites = await getFavorites()
    favoriteIds.value = favorites.map(f => f.script_id)
  } catch (error) {
    console.error('加载收藏失败:', error)
  }
}

const getPositionId = (positionName) => {
  const position = positions.value.find(p => p.name === positionName)
  return position ? position.id : null
}

const handleSearch = debounce(() => {
  loadScripts()
}, 500)

function debounce(func, wait) {
  let timeout
  return function(...args) {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

const handleFilterPosition = (position) => {
  selectedPosition.value = position
  loadScripts()
}

const handleFilterTone = (tone) => {
  selectedTone.value = tone
  loadScripts()
}

const getPreviewContent = (script) => {
  const content = script.brief_content || script.content
  return content.length > 100 ? content.substring(0, 100) + '...' : content
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

const copyScript = async (script) => {
  const content = script.content
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const showScriptDetail = (script) => {
  currentScript.value = script
  showDetail.value = true
}

const adjustScript = () => {
  showDetail.value = false
  showAdjust.value = true
  adjustedContent.value = ''
  adjustForm.tone = currentScript.value.tone
  adjustForm.length_type = ''
}

const handleAdjust = async () => {
  adjustLoading.value = true
  try {
    const result = await adjustScriptApi({
      script_id: currentScript.value.id,
      tone: adjustForm.tone,
      length_type: adjustForm.length_type
    })
    adjustedContent.value = result.adjusted_content
  } catch (error) {
    console.error('调整话术失败:', error)
  } finally {
    adjustLoading.value = false
  }
}

const copyAdjusted = async () => {
  try {
    await navigator.clipboard.writeText(adjustedContent.value)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}
</script>

<style lang="scss" scoped>
.scripts-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.search-bar {
  padding: 15px 20px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.filter-bar {
  padding: 10px 20px;
  display: flex;
  gap: 10px;
  background: white;
  border-top: 1px solid #eee;
}

.scripts-list {
  padding: 20px;
}

.script-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:active {
    transform: scale(0.98);
  }
  
  .script-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 10px;
    
    .script-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
      margin: 0;
      flex: 1;
    }
    
    .script-tags {
      display: flex;
      gap: 6px;
      margin-left: 10px;
    }
  }
  
  .script-content {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
    margin-bottom: 12px;
  }
  
  .script-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    .script-stats {
      display: flex;
      gap: 15px;
      font-size: 12px;
      color: #999;
      
      span {
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
    
    .script-actions {
      display: flex;
      gap: 5px;
    }
  }
}

.script-detail {
  .detail-header {
    margin-bottom: 20px;
    
    h2 {
      font-size: 20px;
      margin: 0 0 12px 0;
    }
    
    .detail-tags {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
  }
  
  .detail-content {
    h4 {
      font-size: 14px;
      color: #999;
      margin: 20px 0 10px;
    }
    
    .content-text {
      background: #f5f5f5;
      padding: 16px;
      border-radius: 8px;
      line-height: 1.8;
      white-space: pre-wrap;
    }
    
    .brief-content {
      margin-top: 20px;
    }
  }
  
  .detail-actions {
    margin-top: 30px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
}
</style>
