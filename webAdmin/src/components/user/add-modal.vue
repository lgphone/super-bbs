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
      <FormItem label="用户名:"
                prop="username">
        <Input v-model="formData.username"
               style="width:200px"></Input>
      </FormItem>
      <FormItem label="邮箱:">
        <Input v-model="formData.email"
               style="width:200px"></Input>
      </FormItem>
      <FormItem label="状态:">
        <i-switch v-model="formData.status" />
      </FormItem>
      <FormItem label="角色:"
                prop="role_id">
        <Select v-model="formData.role_id"
                style="width:200px">
          <Option v-for="(item,k) in roleList"
                  :value="item.id"
                  :key="k">{{ item.name }}</Option>
        </Select>
      </FormItem>
      <FormItem label="密码:">
        <Input v-model="formData.password"
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
import userAPI from '@/api/user'
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
        username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
        role_id: [{ required: true, message: '用户角色不能为空', trigger: 'blur', type: 'number' }]
      },
      roleList: [
        { 'id': 0, 'name': '普通用户' },
        { 'id': 1, 'name': '管理员' }
      ],
      formData: {
        role_id: 0
      },
      loading: true
    }
  },
  methods: {
    async handleSubmit (name) {
      if (!await this.$refs[name].validate()) return
      try {
        await userAPI.create(this.formData)
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
        this.formData = {
          role_id: 0
        }
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
