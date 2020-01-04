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
  name: 'add',
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
      formData: {},
      loading: true
    }
  },
  methods: {
    async handleSubmit (name) {
      if (!await this.$refs[name].validate()) return
      try {
        await tabAPI.create(this.formData)
        this.dialog.show = false
        this.$Message.success('添加成功')
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
        this.formData = {}
        try {
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
