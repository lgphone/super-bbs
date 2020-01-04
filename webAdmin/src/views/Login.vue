<template>
  <div class="app-login">
    <div class="login-inner">
      <div class="login-box">
        <Card :bordered="false">
          <h3 class="login-title">欢迎登录</h3>
          <Form ref="formData"
                :model="formData"
                :rules="ruleValidate">
            <FormItem prop="email">
              <Input prefix="ios-contact"
                     placeholder='用户'
                     v-model="formData.username" />
            </FormItem>
            <FormItem prop="password">
              <Input prefix="ios-lock"
                     placeholder='密码'
                     v-model="formData.password"
                     type='password' />
            </FormItem>
            <FormItem>
              <Button :loading="loading"
                      style="width: 100%"
                      type='primary'
                      @click="handleLogin('formData')">登录</Button>
            </FormItem>
          </Form>
        </Card>
        <div class="cpy"> © {{ new Date().getFullYear() }} <a href="https://github.com"
             target="_blank">super-bbs</a> 版权所有.</div>
      </div>
    </div>
  </div>
</template>

<script>
import accountAPI from '@/api/account'
export default {
  data () {
    return {
      loading: false,
      formData: {},
      ruleValidate: {
        username: [{ required: true, message: '用户不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }]
      },
      canRegister: true
    }
  },
  methods: {
    async handleLogin (name) {
      //
      if (this.loading) return
      /* check form data */
      if (!await this.$refs[name].validate()) return
      this.loading = true
      try {
        await accountAPI.login(this.formData)
        this.$Message.success('登入成功')
        this.$router.replace('/')
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
  mounted () {
    var that = this
    document.onkeydown = function (e) {
      var key = window.event.keyCode
      if (key === 13 || key === 100) {
        that.handleLogin('formData')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.app-login {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("../assets/bg-img.png");
  background-repeat: repeat;
  .login-inner {
    width: 100%;
    height: 100%;
    position: absolute;
    background-color: rgba(0, 0, 0, 0.2);
    .login-box {
      position: relative;
      width: 300px;
      margin: 0 auto;
      margin-top: 200px;
      .login-title {
        text-align: center;
        height: 30px;
        line-height: 30px;
        margin-bottom: 10px;
        color: #08a7a1;
        font-weight: 700;
      }
    }
    .cpy {
      font-weight: 300;
      margin-top: 20px;
      height: 30px;
      line-height: 30px;
      text-align: center;
    }
  }
}
</style>
