<template>
  <div class="main-layout">
    <div class="main-header">
      <div class="content">
        <div class="logo"><a href="/#/">V22X</a></div>
        <div class="search">
          <Input v-model="searchKey"
                 placeholder="search ..."
                 size="small"
                 style="width: 160px" />
          <Button style="margin-left:5px"
                  size="small"
                  icon="ios-search">搜</Button>
        </div>
        <div class="menu">
          <span class="menu-item"><a href="/#/">首页</a></span>
          <span v-if="$user">
            <span class="menu-item"><a :href="`/#/member?username=${$user.username}`">{{$user.username}}</a></span>
            <span class="menu-item"><a href="/#/setting">设置</a></span>
            <span class="menu-item"><a @click="handlerLogOut">登出</a></span>
          </span>
          <span v-else>
            <span class="menu-item"><a href="/#/account/register">注册</a></span>
            <span class="menu-item"><a href="/#/account/login">登录</a></span>
          </span>
        </div>
      </div>
    </div>
    <div class="main-content">
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
    <div class="main-footer">
      <center>Copyright © {{year}} V22X </center>
    </div>
  </div>
</template>
<script>
import accountAPI from '@/api/account'
export default {
  data () {
    return {
      searchKey: null,
      userInfo: null
    }
  },
  methods: {
    async handlerLogOut () {
      try {
        this.loading = true
        await accountAPI.logout()
        this.$Message.success('退出成功')
        window.location.href = '/index'
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('出了点小差')
        }
      } finally {
        this.loading = false
      }
    }
  },
  computed: {
    year: function () {
      return this.$date.getThisYear()
    }
  }
}
</script>
<style lang="scss">
a {
  color: #555;
}
a:hover {
  color: #000;
}
.box {
  border: 1px solid #dcdee2;
  border-color: #e8eaec;
  background: #fff;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.2s ease-in-out;
}
.inner {
  padding: 10px;
  font-size: 14px;
  line-height: 150%;
  text-align: left;
}
.cell {
  padding: 10px;
  font-size: 14px;
  line-height: 120%;
  text-align: left;
  border-bottom: 1px solid #e2e2e2;
}
.a-link {
  color: #778087;
  text-decoration: none;
  word-break: break-word;
}
.a-link:hover {
  color: #4d5256;
  text-decoration: underline;
}
.a-link-info {
  text-decoration: none;
  word-break: break-word;
  color: #03c8ff;
}
.a-link-info:hover {
  color: #03c8ff;
  text-decoration: underline;
}
.center {
  text-align: center;
}
.avatar {
  width: 48px;
  height: 48px;
  background-color: cadetblue;
  border-radius: 4px;
}
.avatar-big {
  width: 73px;
  height: 73px;
  background-color: cadetblue;
  border-radius: 4px;
}
.form-item {
  display: flex;
  align-items: center;
  padding: 5px;
  .form-label {
    width: 120px;
    margin-right: 10px;
    text-align: right;
  }
}
.main-layout {
  background-color: white;
  .main-header {
    text-align: center;
    height: 44px;
    line-height: 44px;
    font-size: 15px;
    font-weight: 500;
    border-bottom: 1px solid rgba(0, 0, 0, 0.22);
    padding: 0 20px;
    .content {
      min-width: 600px;
      max-width: 1100px;
      margin: 0 auto;
      display: block;
      .logo {
        a {
          color: black;
        }
        width: 100px;
        font-size: 200%;
        font-weight: bold;
        color: black;
        float: left;
      }
      .search {
        float: left;
        margin-left: 10px;
      }
      .menu {
        float: right;
        margin-right: 10px;
        .menu-item {
          margin-left: 10px;
          a:hover {
            color: #778087;
          }
        }
      }
      .layout-nav {
        width: 420px;
        margin: 0 auto;
        margin-right: 20px;
      }
    }
  }
  .main-content {
    padding-top: 20px;
    padding-bottom: 20px;
    text-align: center;
    background-color: #e2e2e2;
    box-shadow: inset 0px 12px 8px -12px #848383;
    .content {
      min-width: 600px;
      max-width: 1100px;
      min-height: 800px;
      margin: 0 auto;
      .left-content {
        flex-grow: 1;
      }
      .right-content {
        width: 260px;
        min-width: 260px;
        margin-left: 20px;
      }
    }
  }
  .main-footer {
    border-top: 1px solid rgba(0, 0, 0, 0.22);
    padding-top: 10px;
  }
}
</style>
