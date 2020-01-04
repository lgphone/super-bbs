import api from '@/common/api'

const check = () => api.get('account/check', { t: new Date().getTime() })

const profile = () => {
  return api.get(`account/profile`, { timestamp: new Date().getTime() })
}

const login = params => api.post(`account/login`, params)

const logout = () => {
  return api.post(`account/logout`)
}

export default {
  check,
  profile,
  login,
  logout
}
