import api from '@/common/api'

const index = params => api.get(`index`, params)
const go = params => api.get(`go`, params)

export default {
  index,
  go
}
