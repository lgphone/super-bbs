import api from '@/common/api'

const detail = params => api.get(`member`, params)
const listTopic = params => api.get('member/topic', params)
const listComment = params => api.get('member/comment', params)

export default {
  detail,
  listTopic,
  listComment
}
