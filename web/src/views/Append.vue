<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell">
          <a href="/#/index"
             class="a-link">V22X</a><span> › </span>
          <a :href="`/#/go?sub_tab=${data.sub_tab.name}`"
             class="a-link">{{data.sub_tab.zh}}</a><span> › </span>
          <a :href="`/#/t/?uid=${data.uid}`"
             class="a-link">{{data.title}}</a><span> › </span>
          <span>增加附言</span>
        </div>
        <div class="cell">
          <Input v-model="content"
                 type="textarea"
                 :rows="16"
                 placeholder="追加内容" />
          <div style="display: flex;margin-top: 10px;">
            <div style="margin-right: 20px;"><Button @click="handlePreview">预览主题</Button></div>
            <div><Button @click="handleAppend">提交</Button></div>
          </div>
        </div>
        <div class="cell">
          <div>请在确有必要的情况下再使用此功能为原主题补充信息</div>
        </div>
        <div class="cell"
             v-if="preview">
          <MarkdownPreview theme="oneDark"
                           :bordered="false"
                           :initialValue="content" />
        </div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
      <br>
      <div class="box">
        <div class="cell">
          <div>社区指导原则</div>
        </div>
        <div class="inner">
          <div>
            <Icon type="md-water" />尊重原创</div>
          <div>
            <Icon type="md-water" />友好互助</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { MarkdownPreview } from 'vue-meditor'
import userBox from '@/components/user-box'
import topicAPI from '@/api/topic'
export default {
  components: {
    userBox,
    MarkdownPreview
  },
  data () {
    return {
      loading: false,
      preview: false,
      data: {
        sub_tab: {
          name: null,
          zh: null
        }
      },
      content: null
    }
  },
  methods: {
    handlePreview () {
      if (this.content) {
        this.preview = !this.preview
      }
      if(!this.content) {
        this.preview = false
      }
    },
    async handleAppend () {
      if (!this.content) {
        this.$Message.error('内容不能为空哦')
        return
      }
      try {
        await topicAPI.append({
          'uid': this.$route.query.uid,
          'content': this.content
        })
        this.$router.push({
          path: '/t',
          query: { 'uid': this.$route.query.uid }
        })
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      }
    }
  },
  async created () {
    if (!this.$route.query.uid) {
      this.$router.push({ 'path': '/index' })
      return
    }
    this.loading = true
    try {
      this.data = await topicAPI.list({ 'uid': this.$route.query.uid })
    } catch (e) {
      if (e.msg) {
        this.$Message.error(e.msg)
      } else {
        console.log(e)
        this.$Message.error('服务器出了点小差')
      }
      this.$router.push({ 'path': '/index' })
    } finally {
      this.loading = false
    }
  }
}
</script>
