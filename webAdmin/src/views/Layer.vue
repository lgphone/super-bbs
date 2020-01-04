<template>
  <Layout class="main-layout">
    <Header class="main-header">
      <div class="header-logo">
        <h2><a style="color: #fff;"
             href="/#/index">{{siteTitle}}</a></h2>
      </div>
      <div class="header-menu">
        <div class="header-menu-item">
          <Dropdown @on-click="handleLogOut">
            <a href="javascript:void(0)">
              <Icon type="md-contact"
                    size="30" />
              <span style="margin-left: 10px;">{{$user.username}}</span>
              <Icon type="ios-arrow-down"></Icon>
            </a>
            <DropdownMenu slot="list">
              <DropdownItem name="logout">退出</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </div>
      </div>
    </Header>
    <Sider hide-trigger
           class="main-menu">
      <Menu :active-name="$route.path"
            theme="dark"
            width="auto"
            accordion>
        <MenuItem name="/index"
                  to="/index">首页</MenuItem>
        <MenuItem name="/user"
                  to="/user">用户管理</MenuItem>
        <MenuItem name="/tab"
                  to="/tab">类别管理</MenuItem>
        <MenuItem name="/sub_tab"
                  to="/sub_tab">子类别管理</MenuItem>
        <MenuItem name="/topic"
                  to="/topic">主题管理</MenuItem>
        <MenuItem name="/comment"
                  to="/comment">评论管理</MenuItem>
      </Menu>
    </Sider>
    <Content class='main-content'>
      <router-view></router-view>
    </Content>
  </Layout>
</template>
<script>
import sleep from '@/common/sleep'
export default {
  data () {
    return {
      currentRoutePath: this.$route.path,
      siteTitle: 'SuperBBS Admin'
    }
  },
  methods: {
    async handleLogOut (name) {
      await this.$session.logout()
      await Promise.race([
        sleep(500)
      ])
      window.location.href = '/#/account/login'
    }
  },
  created () {
    console.log(this.$route.path)
  }
}
</script>
<style lang="scss">
.main-layout {
  background: #fff;
  height: 100%;
  .main-header {
    position: fixed;
    padding: 0 16px 0 0;
    z-index: 10;
    width: 100%;
    height: 55px;
    line-height: 55px;
    background-color: white;
    .header-logo {
      float: left;
      width: 200px;
      text-align: center;
      background-color: #515a6e;
    }
    .header-menu {
      float: right;
      .header-menu-item {
        display: inline-block;
        text-align: center;
        margin: 0 10px;
        min-width: 50px;
      }
    }
  }
  .main-menu {
    position: fixed;
    left: 0;
    height: 100%;
    overflow: auto;
    margin-top: 55px;
  }
  .main-content {
    background-color: #f8f8f9;
    border-radius: 1px;
    border-radius: 5px;
    margin-left: 200px;
    margin-top: 55px;
    padding: 16px;
    min-height: 200px;
    .content-header {
      border-bottom: 1px solid #e8eaec;
      padding-bottom: 10px;
      .search-input {
        width: 200px;
      }
      .content-header-item {
        margin: 0 5px;
        text-align: center;
      }
    }
    .content-body {
      margin-top: 10px;
      min-height: 400px;
      background-color: white;
      border-radius: 3px;
    }
  }
}
</style>
