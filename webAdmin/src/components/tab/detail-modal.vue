<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         @on-visible-change="changeModal"
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <div v-if="!loading">
      <Row>
        <Col span="4"><b>name:</b></Col>
        <Col span="8">{{formData.name}}</Col>
        <Col span="4"><b>中文名称:</b></Col>
        <Col span="8">{{formData.zh}}</Col>
      </Row>
      <br>
      <Row>
        <Col span="4"><b>序列号:</b></Col>
        <Col span="8">{{formData.sort_num}}</Col>
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
import tabAPI from '@/api/tab'
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
          this.formData = await tabAPI.list({ 'uid': this.dialog.uid })
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
