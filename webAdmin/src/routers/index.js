import Vue from 'vue'
import Router from 'vue-router'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import accountAPI from '@/api/account'

Vue.use(Router)

const _import = file => () => import('@/views/' + file + '.vue')

let router = new Router({
  routes: [
    {
      path: '/',
      name: '/',
      meta: {},
      component: _import('Layer'),
      redirect: '/index',
      children: [
        {
          path: 'index',
          name: 'index',
          component: _import('Index'),
          meta: {
            auth: true,
            title: '首页'
          }
        },
        {
          path: '/user',
          name: 'user',
          component: _import('User'),
          menu: true,
          meta: {
            auth: true,
            icon: 'ios-contacts',
            title: '用户管理'
          }
        },
        {
          path: '/tab',
          name: 'tab',
          component: _import('Tab'),
          menu: true,
          meta: {
            auth: true,
            icon: 'ios-contacts',
            title: '类别管理'
          }
        },
        {
          path: '/sub_tab',
          name: 'sub_tab',
          component: _import('SubTab'),
          menu: true,
          meta: {
            auth: true,
            icon: 'ios-contacts',
            title: '子类别管理'
          }
        },
        {
          path: '/topic',
          name: 'topic',
          component: _import('Topic'),
          menu: true,
          meta: {
            auth: true,
            icon: 'ios-contacts',
            title: '主题管理'
          }
        },
        {
          path: '/comment',
          name: 'comment',
          component: _import('Comment'),
          menu: true,
          meta: {
            auth: true,
            icon: 'ios-contacts',
            title: '评论管理'
          }
        }
      ]
    },
    {
      path: '/account/login',
      name: 'login',
      meta: {
        auth: false
      },
      component: _import('Login')
    },
    {
      path: '*',
      name: 'default',
      redirect: '/index'
    }
  ]
})

// 路由拦截器
router.beforeEach(async function (to, from, next) {
  ViewUI.LoadingBar.start()
  window.scrollTo(0, 0)
  try {
    // 组件实例添加用户对象 $user
    if (to.fullPath !== from.fullPath) {
      Vue.prototype.$user = await accountAPI.check()
      if (to.meta.auth && !Vue.prototype.$user) {
        ViewUI.Message.error('登录后才可以操作哦')
        next({
          path: '/account/login'
        })
      } else {
        next()
      }
    }
  } catch (e) {
    console.log(e)
    if (e.msg) {
      ViewUI.Message.error(e.msg)
    } else {
      console.log(e)
      ViewUI.Message.error('服务器出了点小差')
    }
    ViewUI.LoadingBar.error()
  }
})

router.afterEach(() => {
  ViewUI.LoadingBar.finish()
})

export default router
