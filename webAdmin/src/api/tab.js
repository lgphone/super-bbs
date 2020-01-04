import api from '@/common/api'

const list = params => api.get(`tab`, params)
const create = params => api.post(`tab`, params)
const edit = params => api.put(`tab`, params)
const _delete = params => api._delete(`tab`, params)

export default {
  list,
  create,
  edit,
  _delete
}
