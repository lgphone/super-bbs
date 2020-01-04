import api from '@/common/api'

const check = () => api.get('account/check', { t: new Date().getTime() })

const profile = () => {
  return api.get(`account/profile`, { t: new Date().getTime() })
}

const login = params => api.post(`account/login`, params)
const register = params => api.post(`account/register`, params)
const updateProfile = params => api.post(`account/profile`, params)
const updatePassword = params => api.post('account/password', params)

const logout = () => {
  return api.post(`account/logout`)
}

const checkCode = params => api.post('captcha/check', params)

const sendEmailCode = params => api.post('email/send', params)

export default {
  check,
  profile,
  login,
  updateProfile,
  updatePassword,
  logout,
  register,
  checkCode,
  sendEmailCode
}
