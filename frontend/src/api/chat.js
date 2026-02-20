import request from './request'

/**
 * 发送消息
 * @param {Object} data - 消息数据
 * @returns {Promise} - 请求结果
 */
export function sendMessage(data) {
  return request({
    url: '/chat/message',
    method: 'post',
    data
  })
}

/**
 * 调整脚本
 * @param {Object} data - 调整数据
 * @returns {Promise} - 请求结果
 */
export function adjustScript(data) {
  return request({
    url: '/chat/adjust',
    method: 'post',
    data
  })
}

/**
 * 获取聊天历史
 * @param {string} sessionId - 会话ID
 * @returns {Promise} - 请求结果
 */
export function getChatHistory(sessionId) {
  return request({
    url: `/chat/history/${sessionId}`,
    method: 'get'
  })
}
