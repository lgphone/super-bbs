import axios from 'axios'
import qs from 'qs'

export const get = (url, params) => {
  return axios.get(url, {
    params,
    paramsSerializer (params) {
      return qs.stringify(params, { arrayFormat: 'repeat' })
    }
  })
}

export const post = (url, params) => {
  return axios.post(url, params)
}

export const put = (url, params) => {
  return axios.put(url, params)
}

export const _delete = (url, params) => {
  return axios.delete(url, {
    params,
    paramsSerializer (params) {
      return qs.stringify(params, { arrayFormat: 'repeat' })
    }
  })
}

export const postForm = (url, params) => {
  let formData = new FormData()
  Object.keys(params).forEach(key => {
    formData.append(key, params[key])
  })
  return axios.post(url, formData)
}
