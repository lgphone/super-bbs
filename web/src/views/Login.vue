<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"><a href="/#/index"
             class="a-link">V22X</a><span> › </span><span>登录</span>
        </div>
        <div class="cell">
          <div class="form-item">
            <div class="form-label"><strong>用户名</strong></div>
            <div class="form-content"><Input v-model="formData.username"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>密码</strong></div>
            <div class="form-content"><Input v-model="formData.password"
                     style="width: 200px;"
                     type='password' /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>图形验证码</strong></div>
            <div class="form-content"> <Input style="width: 80px;"
                     @on-change="checkImgCode()"
                     v-model="formData.code" />
              <img :src="codeImgSrc"
                   @click="refreshCode()"
                   style="margin-left: 10px;height: 20px;"
                   align="center"></img></div>
          </div>
          <div class="form-item">
            <div class="form-label"></div>
            <div class="form-content">
              <span><Button type='primary'
                        :loading="loading"
                        @click="handleLogin('formData')">登录</Button></span>
              <span style="margin-left: 10px;">
                <span style="margin-right:5px;">没有账号?</span>
                <Button to='/account/register'>注册</Button></span></div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-content">
    </div>
  </div>
</template>
<script>
import sleep from '@/common/sleep'
import accountAPI from '@/api/account'
export default {
  data () {
    return {
      loading: false,
      formData: {},
      codeImgSrc: ''
    }
  },
  methods: {
    async handleLogin (name) {
      if (this.loading) return
      if (!this.formData.username) {
        this.$Message.error('用户名不能为空')
        return
      }
      if (!this.formData.password) {
        this.$Message.error('密码不能为空')
        return
      }
      if (!this.formData.code) {
        this.$Message.error('验证码不能为空')
        return
      }
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
    },
    refreshCode () {
      this.codeImgSrc = '/api/v1/captcha' + '?t=' + new Date().getTime()
    },
    async checkImgCode () {
      if (this.formData.code.length !== 5) {
        return
      }
      try {
        await accountAPI.checkCode({ 'code': this.formData.code })
        this.$Message.success('验证码正确')
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('出了点小差')
        }
      }
    }
  },
  created () {
    this.codeImgSrc = '/api/v1/captcha' + '?t=' + new Date().getTime()
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
<style lang="scss">
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
</style>
