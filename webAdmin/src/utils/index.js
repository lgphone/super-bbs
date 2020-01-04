import uuidv4 from 'uuid/v4'
import router from '@/routers'
import _ from 'lodash'

export function goBack () {
  router.go(-1)
}

export function setItem (name, value) {
  sessionStorage.setItem(name, value)
}

export function getItem (name) {
  return sessionStorage.getItem(name)
}

export function removeItem (name) {
  sessionStorage.removeItem(name)
}

export function diffObj (oldObj, newObj, ignoreKeys) {
  let dif = {}
  for (let k in newObj) {
    if (Array.isArray(ignoreKeys)) {
      if (!ignoreKeys.includes(k)) {
        if (!_.isEqual(newObj[k], oldObj[k])) {
          dif[k] = newObj[k]
        }
      }
    } else {
      if (!_.isEqual(newObj[k], oldObj[k])) {
        dif[k] = newObj[k]
      }
    }
  }
  return dif
}

export function removeAll () {
  sessionStorage.clear()
}

export function getUuid () {
  return uuidv4()
}

export function isValidIP (params) {
  const reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
  return reg.test(params)
}

export function sortArray (prop) {
  return function (obj1, obj2) {
    let val1 = obj1[prop]
    let val2 = obj2[prop]
    if (!isNaN(Number(val1)) && !isNaN(Number(val2))) {
      val1 = Number(val1)
      val2 = Number(val2)
    }
    if (val1 < val2) {
      return -1
    } else if (val1 > val2) {
      return 1
    } else {
      return 0
    }
  }
}

export default {
  goBack,
  setItem,
  getItem,
  getUuid,
  removeItem,
  removeAll,
  diffObj,
  isValidIP,
  sortArray
}
