<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell">
          <a href="/#/index"
             class="a-link">V22X</a><span> › </span><span>创作新主题</span>
        </div>
        <div class="cell">主题标题</div>
        <div class="cell"
             style="padding: 0px;"><textarea class="custom-input"
                    rows="1"
                    maxlength="120"
                    v-model="postForm.title"
                    placeholder="请输入主题标题，如果标题能够表达完整内容，则正文可以为空"></textarea></div>
        <div class="cell">正文</div>
        <div class="cell"><textarea class="custom-input"
                    rows="12"
                    v-model="postForm.content"></textarea></div>
        <div class="cell">
          <Select v-model="postForm.sub_tab_id"
                  filterable
                  style="width:260px">
            <Option v-for="item in tabs"
                    :value="item.id"
                    :key="item.id">{{ item.zh }} / {{item.name}}</Option>
          </Select>
        </div>
        <div class="cell"
             style="display: flex;justify-content: space-between;">
          <div><Button @click="handlePreview">预览主题</Button></div>
          <div><Button @click="handleNewPost">发布主题</Button></div>
        </div>
        <div class="cell"
             v-if="preview">
          <MarkdownPreview theme="oneDark"
                           :bordered="false"
                           :initialValue="postForm.content" />
        </div>
      </div>
    </div>
    <div class="right-content">
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
import tabAPI from '@/api/tab'
import topicAPI from '@/api/topic'
export default {
  components: {
    MarkdownPreview
  },
  data () {
    return {
      loading: false,
      preview: false,
      tabs: [],
      postForm: {
        title: null,
        sub_tab_id: null,
        content: null
      }
    }
  },
  methods: {
    handlePreview () {
      if (this.postForm.content) {
        this.preview = !this.preview
      }
      if(!this.postForm.content) {
        this.preview = false
      }
    },
    async handleNewPost () {
      if (!this.postForm.title) {
        this.$Message.error('请先输入标题哦')
        return
      }
      if (!this.postForm.sub_tab_id) {
        this.$Message.error('请选择好分类哦')
        return
      }
      try {
        await topicAPI.create(this.postForm)
        this.$router.push({
          path: '/index'
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
    this.loading = true
    try {
      this.tabs = await tabAPI.listSubTab()
    } catch (e) {
      if (e.msg) {
        this.$Message.error(e.msg)
      } else {
        console.log(e)
        this.$Message.error('服务器出了点小差')
      }
    } finally {
      this.loading = false
    }
  }
}
</script>
<style lang="scss">
.custom-input {
  width: 100%;
  border: none;
  resize: none;
  background-color: #f9f9f9;
  outline: 0;
  font-size: 14px;
  line-height: 20px;
  padding: 10px;
}
.custom-input:focus {
  background-color: #fff;
}
</style>
