import request from './request'

export function login(formData) {
  return request({
    url: '/auth/login',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

export function getUserInfo() {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

export function updateUser(data) {
  return request({
    url: '/auth/me',
    method: 'put',
    data
  })
}
