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
          :rules="ruleValidate"
          :label-width="100">
      <FormItem label="标题:"
                prop="title">
        <Input v-model="formData.title"
               style="width:200px"></Input>
      </FormItem>
      <FormItem label="创建者:">
        <span>{{formData.user.username}}</span>
      </FormItem>
      <FormItem label="内容:">
        <Input v-model="formData.content"
               type="textarea"
               :rows="6"></Input>
      </FormItem>
      <FormItem label="所属节点:">
        <Select v-model="formData.tab_id"
                filterable
                style="width:200px">
          <Option v-for="(item,k) in tabList"
                  :value="item.id"
                  :key="k">{{ item.name }} - {{item.zh}}</Option>
        </Select>
      </FormItem>
      <FormItem label="所属子节点:"
                prop="sub_tab_id">
        <Select v-model="formData.sub_tab_id"
                filterable
                style="width:200px">
          <Option v-for="(item,k) in subTabList"
                  :value="item.id"
                  :key="k">{{ item.name }} - {{item.zh}}</Option>
        </Select>
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
import subTabAPI from '@/api/sub_tab'
import topicAPI from '@/api/topic'
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
        sub_tab_id: [{ required: true, message: '所属子节点不能为空', trigger: 'blur', type: 'number' }],
        title: [{ required: true, message: '标题不能为空', trigger: 'blur' }]
      },
      tabList: [],
      subTabList: [],
      originData: {},
      formData: {
        user: { username: null },
        tab_id: null,
        sub_tab_id: null
      },
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
        await topicAPI.edit(postData)
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
          this.tabList = await tabAPI.list()
          this.originData = await topicAPI.list({ 'uid': this.dialog.uid })
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
  },
  watch: {
    'formData.tab_id': {
      async handler (oldVal, newVal) {
        try {
          this.subTabList = await subTabAPI.list({ 'tab_id': this.formData.tab_id })
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
