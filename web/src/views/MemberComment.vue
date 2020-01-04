<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"
             style="display: flex;">
          <div style="flex-grow: 1;"><a href="/#/index"
               class="a-link">V22X</a><span> › </span><a :href="`/#/member?username=${data.user.username}`"
               class="a-link">{{data.user.username}}</a><span> › </span><span>全部回复</span></div>
          <div style="width: 200px;color: #778087;text-align:right;"
               v-if="!loading"><strong>回复总数 {{data.total}}</strong></div>
        </div>
        <div class="cell"
             v-if="data.total > 100">
          <Page :total="data.total"
                size="small"
                :current="query.page"
                :page-size="query.page_size"
                @on-change="changePage"
                show-elevator />
        </div>
        <div class="cell">
          <div v-for="(item,k) in data.list"
               :key="k">
            <div style="background-color: #edf3f5;padding: 0;text-align: left;padding: 10px;font-size: 14px;display: flex;justify-content: space-between;">
              <div>回复了 <a class="a-link"
                   :href="`/#/member?username=${item.topic.user.username}`">{{item.topic.user.username}}</a> 创建的主题 › <a class="a-link"
                   :href="`/#/go?tab=${item.topic.sub_tab.name}`">{{item.topic.sub_tab.zh}}</a> › <a class="a-link"
                   :href="`/#/t?uid=${item.topic.uid}`">{{item.topic.title}}</a></div>
              <div>于 {{item.time_create}}</div>
            </div>
            <div class="cell">{{item.content}}</div>
          </div>
          <div class="inner"
               v-if="data.total > 100">
            <div>
              <Page :total="data.total"
                    size="small"
                    :current="query.page"
                    :page-size="query.page_size"
                    @on-change="changePage"
                    show-elevator />
            </div>
            <div style="margin: 5px 0 0 10px;">共{{data.total}}个主题，当前是第 {{query.page}} 页</div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
    </div>
    <BackTop></BackTop>
  </div>
</template>
<script>
import userBox from '@/components/user-box'
import memberAPI from '@/api/member'
export default {
  components: {
    userBox
  },
  data () {
    return {
      loading: false,
      data: {
        user: {
          username: null
        },
        list: [],
        total: 0
      },
      query: {
        page: 1,
        page_size: 50
      }
    }
  },
  methods: {
    changePage (page) {
      this.query.page = page
      this.$router.push({ 'path': this.$route.path, 'query': this.query })
    }
  },
  async created () {
    if (!this.$route.query.username) {
      this.$router.push({ 'path': '/index' })
      return
    }
    this.query.username = this.$route.query.username
    if (parseInt(this.$route.query.page)) {
      this.query.page = parseInt(this.$route.query.page)
    }
    this.loading = true
    try {
      this.data = await memberAPI.listComment(this.query)
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
  },
  async beforeRouteUpdate (to, from, next) {
    if (parseInt(to.query.page)) {
      this.query.page = parseInt(to.query.page)
    } else {
      this.query.page = 1
    }
    this.loading = true
    try {
      this.data = await memberAPI.listComment(this.query)
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
    next()
  }
}
</script>
<style lang="scss">
</style>
