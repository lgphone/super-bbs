import * as http from './http'

const handleResponse = res => {
  if (!res.data || res.data.code !== 1000) {
    console.error(
      res.config.method,
      res.config.url,
      res.config.params,
      res.config.data
    )
    throw res.data || res
  }
  return res.data.data
}

class Api {
  constructor (baseUrl) {
    this.baseUrl = baseUrl
  }

  _getUrl (url) {
    return `/${this.baseUrl}/${url}`
  }

  async get (url, data) {
    let res = await http.get(this._getUrl(url), data)
    return handleResponse(res)
  }

  async post (url, data) {
    let res = await http.post(this._getUrl(url), data)
    return handleResponse(res)
  }

  async put (url, data) {
    let res = await http.put(this._getUrl(url), data)
    return handleResponse(res)
  }

  async _delete (url, data) {
    let res = await http._delete(this._getUrl(url), data)
    return handleResponse(res)
  }

  async postForm (url, data) {
    let res = await http.postForm(this._getUrl(url), data)
    return handleResponse(res)
  }
}

const api = new Api('api/admin')

export default api
