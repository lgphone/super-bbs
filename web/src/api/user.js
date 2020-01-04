import api from '@/common/api'

const fav = params => api.post(`user/fav`, params)
const listFav = params => api.get(`user/fav`, params)

export default {
  fav,
  listFav
}
