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
            auth: false,
            title: '首页'
          }
        },
        {
          path: 'go',
          name: 'go',
          component: _import('Go'),
          meta: {
            auth: false,
            title: 'Go页面'
          }
        },
        {
          path: 'new',
          name: 'new',
          component: _import('New'),
          meta: {
            auth: true,
            title: '创作新主题'
          }
        },
        {
          path: 't',
          name: 't',
          component: _import('Topic'),
          meta: {
            auth: false,
            title: '详情'
          }
        },
        {
          path: 't/append',
          name: 't_append',
          component: _import('Append'),
          meta: {
            auth: true,
            title: '追加'
          }
        },
        {
          path: 'my/topics',
          name: 'my_topics',
          component: _import('MyFavTopic'),
          meta: {
            auth: true,
            title: '我收藏的主题'
          }
        },
        {
          path: 'my/nodes',
          name: 'my_nodes',
          component: _import('MyFavNode'),
          meta: {
            auth: true,
            title: '我收藏的节点'
          }
        },
        {
          path: 'my/following',
          name: 'my_following',
          component: _import('MyFavUserTopic'),
          meta: {
            auth: true,
            title: '我关注的用户以及他们的主题'
          }
        },
        {
          path: 'member',
          name: 'member',
          component: _import('Member'),
          meta: {
            auth: false,
            title: '用户详情页'
          }
        },
        {
          path: 'member/topic',
          name: 'member_topic',
          component: _import('MemberTopic'),
          meta: {
            auth: false,
            title: '用户Topic页'
          }
        },
        {
          path: 'member/comment',
          name: 'member_comment',
          component: _import('MemberComment'),
          meta: {
            auth: false,
            title: '用户Comment页'
          }
        },
        {
          path: 'setting',
          name: 'setting',
          component: _import('Setting'),
          meta: {
            auth: true,
            title: '用户Setting页'
          }
        },
        {
          path: '/account/register',
          name: 'register',
          meta: {
            auth: false
          },
          component: _import('Register')
        }, {
          path: '/account/login',
          name: 'login',
          meta: {
            auth: false
          },
          component: _import('Login')
        }
      ]
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
