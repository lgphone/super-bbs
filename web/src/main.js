import Vue from 'vue'
import 'babel-polyfill'
import App from '@/App.vue'
import router from '@/routers'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import 'normalize.css'
import _ from 'lodash'
import * as qs from 'qs'
import sleep from '@/common/sleep'
import * as date from '@/common/date'
import api from '@/common/api'
import session from '@/api/account'
import {
  goBack,
  setItem,
  getItem,
  getUuid,
  removeItem,
  removeAll,
  diffObj,
  sortArray
} from '@/utils'

Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.prototype.$_ = _
Vue.prototype.$api = api
Vue.prototype.$qs = qs
Vue.prototype.$date = date
Vue.prototype.$sleep = sleep
Vue.prototype.$goBack = goBack
Vue.prototype.$setItem = setItem
Vue.prototype.$getItem = getItem
Vue.prototype.$removeItem = removeItem
Vue.prototype.$removeAll = removeAll
Vue.prototype.$diffObj = diffObj
Vue.prototype.$getUuid = getUuid
Vue.prototype.$session = session
Vue.prototype.$sortArray = sortArray

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
