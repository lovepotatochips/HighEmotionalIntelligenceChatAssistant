import request from './request'

export function getPositions() {
  return request({
    url: '/system/positions',
    method: 'get'
  })
}

export function getCategories(positionId) {
  return request({
    url: '/system/categories',
    method: 'get',
    params: { position_id: positionId }
  })
}

export function healthCheck() {
  return request({
    url: '/system/health',
    method: 'get'
  })
}
