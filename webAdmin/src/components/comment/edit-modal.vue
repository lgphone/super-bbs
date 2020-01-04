<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         @on-visible-change="changeModal"
         :mask-closable=false
         :width="900"
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <Form ref="formData"
          v-if="!loading"
          :model="formData"
          :label-width="100">
      <FormItem label="评论者:">
        <span>{{formData.user.username}}</span>
      </FormItem>
      <FormItem label="内容:">
        <Input v-model="formData.content"
               type="textarea"
               :rows="6"></Input>
      </FormItem>
      <FormItem label="喜欢数量:">
        <Input v-model="formData.like_count"
               style="width:200px"
               type="number"></Input>
      </FormItem>
      <FormItem>
        <Button type="primary"
                @click="handleSubmit('formData')">提交</Button>
        <Button @click="handleReset('formData')"
                style="margin-left: 8px">重置</Button>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
import loadingSpin from '@/components/loading-spin'
import commentAPI from '@/api/comment'
export default {
  name: 'edit',
  components: {
    loadingSpin
  },
  props: {
    dialog: Object
  },
  data () {
    return {
      originData: {},
      formData: {
        user: { username: null },
        topic: { name: null, uid: null }
      },
      loading: true
    }
  },
  methods: {
    async handleSubmit (name) {
      let postData = { uid: this.formData.uid }
      let diff = this.$diffObj(this.originData, this.formData)
      if (this.$_.isEqual(diff, {})) {
        this.$Message.warning('没有修改')
        return
      }
      Object.assign(postData, diff)
      try {
        await commentAPI.edit(postData)
        this.dialog.show = false
        this.$Message.success('修改成功')
        await this.$emit('getData')
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('出了点小差')
        }
      }
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    async changeModal (val) {
      if (val) {
        this.loading = true
        try {
          this.originData = await commentAPI.list({ 'uid': this.dialog.uid })
          this.formData = Object.assign({}, this.originData)
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
