<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"
             style="display: flex;">
          <div style="flex-grow: 1;"><a href="/#/index"
               class="a-link">V22X</a><span> › </span><span>我关注的人的最新主题</span></div>
          <div style="width: 200px;color: #778087;text-align:right;"
               v-if="!loading"><strong>主题总数 {{data.total}}</strong></div>
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
              <div class="topic-title">
                <a class="a-link"
                   :href="`/#/t?uid=${item.uid}`">{{item.title}}</a>
              </div>
              <div class="topic-info">
                <div v-if="item.up_count">
                  <Icon type="ios-arrow-up"
                        size="18" /><span style="margin-left: 3px;">{{item.up_count}}</span></div>
                <div v-if="item.down_count">
                  <Icon type="ios-arrow-down"
                        size="18" /><span style="margin-left: 3px;">{{item.down_count}}</span></div>
                <div>
                  <Tag><a :href="`/#/go?tab=${item.sub_tab.name}`">{{item.sub_tab.zh}}</a></Tag>
                </div>
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
          <Page :total="data.total"
                size="small"
                :current="query.page"
                :page-size="query.page_size"
                @on-change="changePage"
                show-elevator />
        </div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
      <br>
      <div class="box">
        <div class="cell">我关注的人</div>
        <div class="cell"
             v-for="(item,k) in data.fav_users"
             :key="k">
          <a class="a-link"
             :href="`/#/member?username=${item.username}`">{{item.username}}</a>
        </div>
      </div>
    </div>
    <BackTop></BackTop>
  </div>
</template>
<script>
import loadingSpin from '@/components/loading-spin'
import userBox from '@/components/user-box'
import userAPI from '@/api/user'
export default {
  components: {
    userBox,
    loadingSpin
  },
  data () {
    return {
      loading: false,
      data: {
        total: 0,
        list: [],
        fav_users: []
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
    if (parseInt(this.$route.query.page)) {
      this.query.page = parseInt(this.$route.query.page)
    }
    this.loading = true
    try {
      this.data = await userAPI.listFav(this.query)
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
      this.data = await userAPI.listFav(this.query)
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
