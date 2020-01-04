<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="inner"
             style="display: flex; background-color: #001d25;border-radius: 4px 4px 0 0;">
          <div class="avatar-big"><a href="javascript:"><img></a></div>
          <div style="flex-grow: 1;margin-left: 10px;">
            <div style="display: flex;">
              <div style="flex-grow: 1;"><a href="/#/index"
                   class="a-link-info"
                   style="">V22X</a><span style="color: #fff;"> › </span><span style="color: #fff;">{{data.sub_tab_info.zh}}</span></div>
              <div style="width: 200px;color: #fff;text-align:right;"><strong>主题总数 {{data.total}}</strong>
                <span v-if="$user"> •
                  <a class="a-link-info"
                     v-if="data.is_fav"
                     href="javascript:"
                     @click="handleFavTab('cal')">取消收藏</a>
                  <a class="a-link-info"
                     v-else
                     href="javascript:"
                     @click="handleFavTab('add')">加入收藏</a>
                </span></div>
            </div>
            <div style="color: #fff;font-size: 10px;">{{data.sub_tab_info.desc}}</div>
          </div>
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
        <loadingSpin v-if="loading"></loadingSpin>
        <div class="topic"
             v-if="!loading">
          <div class="cell topic-item"
               v-for="(item,k) in data.list"
               :key="k">
            <div class="avatar"><a :href="`/#/member?username=${item.user.username}`"><img :src="item.user.avatar_url"></a></div>
            <div class="topic-content">
              <div class="topic-title"><a class="a-link"
                   :href="`/#/t?uid=${item.uid}`">{{item.title}}</a></div>
              <div class="topic-info">
                <div v-if="item.up_count">
                  <Icon type="ios-arrow-up"
                        size="18" /><span style="margin-left: 3px;">{{item.up_count}}</span></div>
                <div v-if="item.down_count">
                  <Icon type="ios-arrow-down"
                        size="18" /><span style="margin-left: 3px;">{{item.down_count}}</span></div>
                <div><a class="a-link"
                     :href="`/#/member?username=${item.user.username}`">{{item.user.username}}</a></div>
                <div>创建于 {{item.time_create}}</div>
                <div v-if="item.last_reply_user">最后回复来自 <a class="a-link"
                     :href="`/#/member?username=${item.last_reply_user.username}`">{{item.last_reply_user.username}}</a></div>
              </div>
            </div>
            <div class="topic-comment">
              <Badge :text="String(item.comment_count)"
                     type="normal"></Badge>
            </div>
          </div>
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
    <div class="right-content">
      <userBox></userBox>
      <br>
      <div class="box">
        <div class="cell">
          <div style="margin-bottom: 10px;"><strong>父节点</strong></div>
          <div><a class="a-link"
               :href="`/#/index?tab=${data.sub_tab_info.tab.name}`">{{data.sub_tab_info.tab.zh}}</a></div>
        </div>
        <div class="cell"
             v-if="loading">
          <loadingSpin></loadingSpin>
        </div>
        <div class="cell"
             v-if="!loading">
          <div style="margin-bottom: 10px;"><strong>相关节点</strong></div>
          <div v-for="(item,k) in data.sub_tab_info.other_tabs"
               :key="k"
               style="margin-bottom: 5px;">
            <a class="a-link"
               :href="`/#/go?tab=${item.name}`">{{item.zh}}</a>
          </div>
        </div>
      </div>
    </div>
    <BackTop></BackTop>
  </div>
</template>
<script>
import loadingSpin from '@/components/loading-spin'
import userBox from '@/components/user-box'
import mainAPI from '@/api/main'
import tabAPI from '@/api/tab'
export default {
  components: {
    userBox,
    loadingSpin
  },
  data () {
    return {
      loading: false,
      selectTab: null,
      data: {
        total: 0,
        list: [],
        is_fav: false,
        sub_tab_info: {
          other_tabs: [],
          tab: {
            name: null
          },
          name: null,
          zh: null,
          desc: null
        }
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
    },
    async handleFavTab (action) {
      try {
        await tabAPI.favSubTab({ 'tab': this.query.tab, 'action': action })
        this.data.is_fav = !this.data.is_fav
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
    if (!this.$route.query.tab) {
      this.$router.push({ 'path': '/index' })
      return
    }
    this.query.tab = this.$route.query.tab
    if (parseInt(this.$route.query.page)) {
      this.query.page = parseInt(this.$route.query.page)
    }
    this.loading = true
    try {
      this.data = await mainAPI.go(this.query)
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
    this.query.tab = to.query.tab
    this.loading = true
    try {
      this.data = await mainAPI.go(this.query)
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
.topic {
  .topic-item {
    display: flex;
  }
  .topic-content {
    flex: 1;
    margin-left: 5px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    .topic-title {
      font-size: 16px;
      line-height: 130%;
      text-shadow: 0 1px 0 #fff;
    }
    .topic-info {
      display: flex;
      align-items: center;
      font-size: 12px;
      color: #ccc;
      div {
        margin-right: 10px;
      }
    }
  }
  .topic-comment {
    width: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
