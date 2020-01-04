import api from '@/common/api'

const list = params => api.get(`tab`, params)
const listSubTab = params => api.get(`sub_tab`, params)
const favSubTab = params => api.post(`sub_tab/fav`, params)
const listFavSubTab = params => api.get('sub_tab/fav', params)
export default {
  list,
  listSubTab,
  favSubTab,
  listFavSubTab
}
