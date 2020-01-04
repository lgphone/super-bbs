<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         @on-visible-change="changeModal"
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <div v-if="!loading">
      <Row>
        <Col span="4"><b>用户名:</b></Col>
        <Col span="8">{{formData.username}}</Col>
        <Col span="4"><b>邮箱:</b></Col>
        <Col span="8">{{formData.email}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>状态:</b></Col>
        <Col span="8">
        <Tag v-if="formData.status"
             color="green">启用</Tag>
        <Tag v-else
             color="red">禁用</Tag>
        </Col>
        <Col span="4"><b>角色:</b></Col>
        <Col span="8">
        <Tag color="red"
             v-if="formData.role_id===1">管理员</Tag>
        <Tag v-else>注册用户</Tag>
        </Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>性别:</b></Col>
        <Col span="8">{{formData.sex}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>创建时间:</b></Col>
        <Col span="8">{{formData.time_create}}</Col>
        <Col span="4"><b>修改时间:</b></Col>
        <Col span="8">{{formData.time_modify}}</Col>
      </Row>
    </div>
  </Modal>
</template>

<script>
import loadingSpin from '@/components/loading-spin'
import userAPI from '@/api/user'
export default {
  name: 'detail',
  components: {
    loadingSpin
  },
  props: {
    dialog: Object
  },
  data () {
    return {
      formData: {},
      loading: true
    }
  },
  methods: {
    async changeModal (val) {
      if (val) {
        this.loading = true
        try {
          this.formData = await userAPI.list({ 'uid': this.dialog.uid })
          this.loading = false
        } catch (e) {
          if (e.msg) {
            this.$Message.error(e.msg)
          } else {
            console.log(e)
            this.$Message.error('出了点小差')
          }
        }
      }
    }
  }
}
</script>
