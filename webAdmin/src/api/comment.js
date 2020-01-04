import api from '@/common/api'

const list = params => api.get(`comment`, params)
const create = params => api.post(`comment`, params)
const edit = params => api.put(`comment`, params)
const _delete = params => api._delete(`comment`, params)

export default {
  list,
  create,
  edit,
  _delete
}
