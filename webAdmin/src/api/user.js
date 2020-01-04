import api from '@/common/api'

const list = params => api.get(`user`, params)
const create = params => api.post(`user`, params)
const edit = params => api.put(`user`, params)
const _delete = params => api._delete(`user`, params)

export default {
  list,
  create,
  edit,
  _delete
}
