<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="inner">
          <div class="tab">
            <span v-for="(item,k) in indexData.tabs"
                  :key="k">
              <a class="tab-item-current"
                 :href="`/#/index?tab=${item.name}`"
                 v-if="item.name === selectTab">{{item.zh}}</a>
              <a class="tab-item"
                 :href="`/#/index?tab=${item.name}`"
                 v-else>{{item.zh}}</a>
            </span>
          </div>
        </div>
        <div class="sub-tab">
          <span v-for="(item,k) in subTabs"
                :key="k">
            <a class="sub-tab-item a-link"
               :href="`/#/go?tab=${item.name}`">{{item.zh}}</a>
          </span>
        </div>
        <loadingSpin v-if="loading"></loadingSpin>
        <div class="topic"
             v-if="!loading">
          <div class="cell topic-item"
               v-for="(item,k) in indexData.topics"
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
             v-if="indexData.tab_topic_count > 80"><a class="a-link"
             href="/#/recent"><span>→</span>更多新主题</a></div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
      <br>
      <div class="box">
        <div class="inner">
          <a class="a-link">
            <Icon type="ios-ice-cream" /><span style="margin-left: 5px;">领取今日的登录奖励</span></a>
        </div>
      </div>
      <br>
      <div v-if="indexData.fav_tabs">
        <div class="box">
          <div class="cell">我收藏的节点</div>
          <div class="cell"
               v-for="(item,k) in indexData.fav_tabs"
               :key="k"><a class="a-link"
               :href="`/#/go?tab=${item.name}`">{{item.zh}}</a></div>
        </div>
      </div>
      <br>
      <div class="box">
        <div class="cell">今日热议主题</div>
        <div class="cell"
             v-for="(item,k) in indexData.hot_topics"
             :key="k"><a class="a-link"
             :href="`/#/t?uid=${item.uid}`">{{item.title}}</a></div>
      </div>
      <br>
      <div class="box">
        <div class="cell">社区运行状况</div>
        <div class="inner">
          <div style="display: flex; text-align: right;">
            <div style="width: 70px;margin-right: 10px;">注册会员</div>
            <div><strong>{{indexData.user_count}}</strong></div>
          </div>
          <div style="display: flex; text-align: right;">
            <div style="width: 70px;margin-right: 10px;">主题</div>
            <div><strong>{{indexData.topic_count}}</strong></div>
          </div>
          <div style="display: flex; text-align: right;">
            <div style="width: 70px;margin-right: 10px;">回复</div>
            <div><strong>{{indexData.comment_count}}</strong></div>
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
import indexMixedAPI from '@/api/main'
export default {
  components: {
    userBox,
    loadingSpin
  },
  data () {
    return {
      loading: false,
      selectTab: null,
      indexData: {
        tabs: [],
        topics: []
      }
    }
  },
  computed: {
    subTabs: function () {
      if (this.indexData.tabs.length > 0) {
        let tab = this.indexData.tabs.find(item => item.name === this.selectTab)
        if (tab && tab.sub_tabs) {
          return tab.sub_tabs
        } else {
          return []
        }
      } else {
        return []
      }
    }
  },
  async created () {
    this.selectTab = this.$route.query.tab ? this.$route.query.tab : 'tech'
    this.loading = true
    try {
      this.indexData = await indexMixedAPI.index({ 'tab': this.selectTab })
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
    this.selectTab = to.query.tab ? to.query.tab : 'tech'
    this.loading = true
    try {
      this.indexData = await indexMixedAPI.index({ 'tab': this.selectTab })
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
.tab {
  .tab-item {
    display: inline-block;
    font-size: 14px;
    line-height: 14px;
    padding: 5px 8px;
    margin-right: 5px;
    color: #555;
  }
  .tab-item:hover {
    background-color: #f5f5f5;
    color: #000;
    text-decoration: none;
  }
  .tab-item-current {
    display: inline-block;
    font-size: 14px;
    line-height: 14px;
    padding: 5px 8px;
    margin-right: 5px;
    border-radius: 3px;
    background-color: #334;
    color: #fff;
  }
  .tab-item-current:hover {
    color: #fff;
  }
}
.sub-tab {
  background-color: #f9f9f9;
  padding: 10px 10px 10px 20px;
  font-size: 12px;
  line-height: 100%;
  text-align: left;
  border-bottom: 1px solid #e2e2e2;
  .sub-tab-item {
    padding: 5px 8px;
    margin-right: 5px;
  }
}
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
