import api from '@/common/api'

const list = params => api.get(`topic`, params)
const create = params => api.post(`topic`, params)
const edit = params => api.put(`topic`, params)
const _delete = params => api._delete(`topic`, params)

export default {
  list,
  create,
  edit,
  _delete
}
