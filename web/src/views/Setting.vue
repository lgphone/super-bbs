<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"><a href="/#/index"
             class="a-link">V22X</a><span> › </span><span>设置</span>
        </div>
        <div class="cell">
          <div class="form-item">
            <div class="form-label"></div>
            <div class="form-content"><strong>V22X 第 {{data.id}} 号会员</strong></div>
          </div>
          <br>
          <div class="form-item">
            <div class="form-label"><strong>用户名</strong></div>
            <div class="form-content">{{data.username}}</div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>邮箱地址</strong></div>
            <div class="form-content">{{data.email}}</div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>个人网站</strong></div>
            <div class="form-content"><Input v-model="data.site"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>所在地</strong></div>
            <div class="form-content"><Input v-model="data.location"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>所在公司</strong></div>
            <div class="form-content"><Input v-model="data.company"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label">
              <Icon type="logo-github"
                    size="30" />
            </div>
            <div class="form-content"><Input v-model="data.github"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label">
              <Icon type="logo-twitter"
                    color="#4086cd"
                    size="30" />
            </div>
            <div class="form-content"><Input v-model="data.twitter"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>微博地址</strong></div>
            <div class="form-content"><Input v-model="data.weibo"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>个人简介</strong></div>
            <div class="form-content"><Input type="textarea"
                     v-model="data.bio"
                     style="width: 200px;" /></div>
          </div>
          <br>
          <div class="form-item">
            <div class="form-label"><strong>主题列表隐私设置</strong></div>
            <div class="form-content"><Select v-model="data.privacy_level"
                      style="width: 150px">
                <Option v-for="item in privacyLevelList"
                        :value="item.value"
                        :key="item.value">{{ item.label }}</Option>
              </Select></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>性别</strong></div>
            <div class="form-content">
              <RadioGroup v-model="data.sex">
                <Radio :label="0">
                  <Icon type="ios-man"></Icon>
                  <span>男</span>
                </Radio>
                <Radio :label="1">
                  <Icon type="ios-woman"></Icon>
                  <span>女</span>
                </Radio>
              </RadioGroup>
            </div>
          </div>
          <div class="form-item">
            <div class="form-label"></div>
            <div class="form-content"><Button type='primary'
                      :loading='loading'
                      @click="handleUpdateProfile()">更新</Button></div>
          </div>
        </div>
      </div>
      <br>
      <div class="box">
        <div class="cell">
          <div class="form-item">
            <div class="form-label"><strong>原密码</strong></div>
            <div class="form-content"><Input v-model="passwordForm.password"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"><strong>新密码</strong></div>
            <div class="form-content"><Input v-model="passwordForm.new_password"
                     style="width: 200px;" /></div>
          </div>
          <div class="form-item">
            <div class="form-label"></div>
            <div class="form-content"><Button type='warning'
                      :loading='loading'
                      @click="handleUpdatePassword()">更改密码</Button></div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
    </div>
  </div>
</template>
<script>
import userBox from '@/components/user-box'
import accountAPI from '@/api/account'
export default {
  components: {
    userBox
  },
  data () {
    return {
      loading: false,
      privacyLevelList: [
        {
          label: '所有人可见',
          value: 0
        }, {
          label: '登录的人可见',
          value: 1
        }, {
          label: '仅自己可见',
          value: 2
        }
      ],
      data: {
        id: 0,
        username: '',
        email: '',
        sex: 0,
        avatar_url: '',
        site: '',
        location: '',
        company: '',
        github: '',
        twitter: '',
        weibo: '',
        bio: '',
        privacy_level: 0
      },
      passwordForm: {
        password: '',
        new_password: ''
      }
    }
  },
  methods: {
    async handleUpdateProfile () {
      try {
        this.data = await accountAPI.updateProfile(this.data)
        this.$Message.success('更新成功')
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      } finally {
        this.loading = false
      }
    },
    async handleUpdatePassword () {
      if (!this.passwordForm.password || !this.passwordForm.new_password) {
        this.$Message.error('请输入原密码和新密码')
        return
      }
      try {
        await accountAPI.updatePassword(this.passwordForm)
        this.$Message.success('更改成功,请重新登录')
        this.$router.push({ 'path': '/account/login' })
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      } finally {
        this.loading = false
      }
    }
  },
  async created () {
    this.loading = true
    try {
      this.data = await accountAPI.profile()
    } catch (e) {
      if (e.msg) {
        this.$Message.error(e.msg)
      } else {
        console.log(e)
        this.$Message.error('服务器出了点小差')
      }
    } finally {
      this.loading = false
    }
  }
}
</script>

