import request from './request'

/**
 * 获取脚本列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回脚本列表数据
 */
export function getScripts(params) {
  return request({
    url: '/scripts',
    method: 'get',
    params
  })
}

/**
 * 获取脚本详情
 * @param {string|number} id - 脚本ID
 * @returns {Promise} 返回脚本详情数据
 */
export function getScriptDetail(id) {
  return request({
    url: `/scripts/${id}`,
    method: 'get'
  })
}

/**
 * 点赞脚本
 * @param {string|number} id - 脚本ID
 * @returns {Promise} 返回点赞结果
 */
export function likeScript(id) {
  return request({
    url: `/scripts/${id}/like`,
    method: 'post'
  })
}

/**
 * 添加收藏
 * @param {Object} data - 收藏数据
 * @returns {Promise} 返回添加收藏结果
 */
export function addFavorite(data) {
  return request({
    url: '/scripts/favorites',
    method: 'post',
    data
  })
}

/**
 * 移除收藏
 * @param {string|number} scriptId - 脚本ID
 * @returns {Promise} 返回移除收藏结果
 */
export function removeFavorite(scriptId) {
  return request({
    url: `/scripts/favorites/${scriptId}`,
    method: 'delete'
  })
}

/**
 * 获取收藏列表
 * @returns {Promise} 返回收藏列表数据
 */
export function getFavorites() {
  return request({
    url: '/scripts/favorites/list',
    method: 'get'
  })
}
