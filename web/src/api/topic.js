import api from '@/common/api'

const list = params => api.get(`topic`, params)
const create = params => api.post(`topic`, params)
const append = params => api.post(`topic/append`, params)
const comment = params => api.post(`topic/comment`, params)
const fav = params => api.post(`topic/fav`, params)
const listFav = params => api.get(`topic/fav`, params)
const addView = params => api.post(`topic/view`, params)
const upDown = params => api.post(`topic/up_down`, params)
const thank = params => api.post(`topic/thank`, params)
const commentThank = params => api.post(`topic/comment/thank`, params)

export default {
  list,
  create,
  append,
  comment,
  fav,
  listFav,
  upDown,
  thank,
  commentThank,
  addView
}
