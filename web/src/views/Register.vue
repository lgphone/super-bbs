<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"><a href="/#/index"
             class="a-link">V22X</a><span> › </span><span>注册新用户</span>
        </div>
        <div class="cell">
          <div class="form-item">
            <div class="form-label"><strong>用户名</strong></div>
            <div class="form-content"><Input v-model="formData.username"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>邮箱地址</strong></div>
            <div class="form-content"><Input v-model="formData.email"
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
            <div class="form-label"><strong>邮箱验证码</strong></div>
            <div class="form-content"><Input v-model="formData.email_code"
                     style="width: 80px;" />
              <span><Button style="margin-left: 10px;"
                        :loading='sendCodeLoading'
                        @click="handleSendCode()">发送验证码</Button></span></div>
          </div>
          <div class="form-item">
            <div class="form-label"></div>
            <div class="form-content"><Button type='primary'
                      style="width: 80px;"
                      :loading='loading'
                      @click="handleRegister('formData')">注册</Button></div>
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
      sendCodeLoading: false,
      loading: false,
      formData: {},
      codeImgSrc: ''
    }
  },
  methods: {
    async handleRegister (name) {
      if (this.loading) return
      if (!this.formData.username) {
        this.$Message.error('用户名不能为空')
        return
      }
      if (!this.formData.email) {
        this.$Message.error('邮箱不能为空')
        return
      }
      if (!this.formData.password) {
        this.$Message.error('密码不能为空')
        return
      }
      if (!this.formData.email_code) {
        this.$Message.error('邮箱验证码不能为空')
        return
      }
      try {
        this.loading = true
        await accountAPI.register(this.formData)
        this.$Message.success('注册成功,自动跳转到登陆页面')
        await Promise.race([
          sleep(500)
        ])
        this.$router.replace('/account/login')
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
    async handleSendCode () {
      if (!this.formData.email) {
        this.$Message.error('邮箱不能为空')
        return
      }
      if (!this.formData.code) {
        this.$Message.error('图形验证码不能为空')
        return
      }
      try {
        this.sendCodeLoading = true
        await accountAPI.sendEmailCode({ 'email': this.formData.email, 'code': this.formData.code })
        this.$Message.success('验证码发送成功,请检查收件箱')
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('出了点小差')
        }
      } finally {
        this.sendCodeLoading = false
      }
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
  }
}
</script>
