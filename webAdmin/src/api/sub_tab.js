import api from '@/common/api'

const list = params => api.get(`sub_tab`, params)
const create = params => api.post(`sub_tab`, params)
const edit = params => api.put(`sub_tab`, params)
const _delete = params => api._delete(`sub_tab`, params)

export default {
  list,
  create,
  edit,
  _delete
}
