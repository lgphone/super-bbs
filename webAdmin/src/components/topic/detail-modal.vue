<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         width="800"
         @on-visible-change="changeModal"
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <div v-if="!loading">
      <Row>
        <Col span="4"><b>标题:</b></Col>
        <Col span="8">{{formData.title}}</Col>
        <Col span="4"><b>创建者:</b></Col>
        <Col span="8">{{formData.user.username}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>所属父节点:</b></Col>
        <Col span="8">{{formData.tab.name}} - {{formData.tab.zh}}</Col>
        <Col span="4"><b>所属子节点:</b></Col>
        <Col span="8">{{formData.sub_tab.name}} - {{formData.sub_tab.zh}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>最后回复者:</b></Col>
        <Col span="8"
             v-if="formData.last_reply_user">{{formData.last_reply_user.username}}</Col>
        <Col span="8"
             v-else>暂无回复</Col>
        <Col span="4"><b>最后回复时间:</b></Col>
        <Col span="8"
             v-if="formData.last_reply_time">{{formData.last_reply_time}}</Col>
        <Col span="8"
             v-else>暂无回复</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>回复数量:</b></Col>
        <Col span="8">{{formData.comment_count}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>up_count:</b></Col>
        <Col span="8">{{formData.up_count}}</Col>
        <Col span="4"><b>up_count:</b></Col>
        <Col span="8">{{formData.down_count}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>内容:</b></Col>
        <Col>{{formData.content}}</Col>
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
import topicAPI from '@/api/topic'
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
        tab: { name: null, zh: null },
        sub_tab: { name: null, zh: null },
        last_reply_user: { username: null }
      },
      loading: true
    }
  },
  methods: {
    async changeModal (val) {
      if (val) {
        this.loading = true
        try {
          this.formData = await topicAPI.list({ 'uid': this.dialog.uid })
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
