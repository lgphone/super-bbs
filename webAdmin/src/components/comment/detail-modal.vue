<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         @on-visible-change="changeModal"
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <div v-if="!loading">
      <Row>
        <Col span="4"><b>评论者:</b></Col>
        <Col span="8">{{formData.user.username}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>主题名称:</b></Col>
        <Col span="8">{{formData.topic.title}}</Col>
        <Col span="4"><b>喜欢数量:</b></Col>
        <Col span="8">{{formData.like_count}}</Col>
      </Row>
      <br>
      <Row>
        <Row>
          <Col span="4"><b>内容:</b></Col>
          <Col>{{formData.content}}</Col>
        </Row>
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
import commentAPI from '@/api/comment'
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
      formData: {
        user: { username: null },
        topic: { name: null, uid: null }
      },
      loading: true
    }
  },
  methods: {
    async changeModal (val) {
      if (val) {
        this.loading = true
        try {
          this.formData = await commentAPI.list({ 'uid': this.dialog.uid })
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
