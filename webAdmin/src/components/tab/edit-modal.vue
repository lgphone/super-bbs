<template>
  <Modal v-model="dialog.show"
         :title="dialog.title"
         :loading=true
         @on-visible-change="changeModal"
         :mask-closable=false
         :footer-hide=true>
    <loadingSpin v-if="loading"></loadingSpin>
    <Form ref="formData"
          v-if="!loading"
          :model="formData"
          :rules="ruleValidate"
          :label-width="100">
      <FormItem label="name:"
                prop="name">
        <Input v-model="formData.name"
               style="width:200px"></Input>
      </FormItem>
      <FormItem label="中文名称:"
                prop="zh">
        <Input v-model="formData.zh"
               style="width:200px"></Input>
      </FormItem>
      <FormItem label="序列号:">
        <Input v-model="formData.sort_num"
               type="number"
               style="width:200px"></Input>
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
import tabAPI from '@/api/tab'
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
      ruleValidate: {
        name: [{ required: true, message: '名字不能为空', trigger: 'blur' }],
        zh: [{ required: true, message: '中文名字不能为空', trigger: 'blur' }]
      },
      originData: {},
      formData: {},
      loading: true
    }
  },
  methods: {
    async handleSubmit (name) {
      if (!await this.$refs[name].validate()) return
      let postData = { uid: this.formData.uid }
      let diff = this.$diffObj(this.originData, this.formData)
      if (this.$_.isEqual(diff, {})) {
        this.$Message.warning('没有修改')
        return
      }
      Object.assign(postData, diff)
      try {
        await tabAPI.edit(postData)
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
          this.originData = await tabAPI.list({ 'uid': this.dialog.uid })
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
