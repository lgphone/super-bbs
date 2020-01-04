<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"
             style="display: flex;border-radius: 4px 4px 0 0;">
          <div class="avatar-big"><a href="javascript:"><img></a></div>
          <div style="flex-grow: 1;margin-left: 10px;">
            <div style="display: flex;flex-direction: column;justify-content: space-between;">
              <div style="display: flex;justify-content: space-between;">
                <div style="display: flex;align-items: center;">
                  <h1 style="margin: 5px 0;color: black;display: inline-block;">{{data.user.username}}</h1>
                  <span style="margin-left: 10px;">
                    <Icon :type="data.user.sex === 0 ? 'ios-man' : 'ios-woman'"
                          size="25"></Icon>
                  </span>
                </div>
                <div style="width: 150px;text-align:right;">
                  <span v-if="!loading&&$user&&$user.username !== data.user.username">
                    <Button type="default"
                            @click="handleFavUser('cal')"
                            v-if="data.is_fav">取消特别关注</Button>
                    <Button type="warning"
                            @click="handleFavUser('add')"
                            v-else>加入特别关注</Button>
                  </span>
                </div>
              </div>
              <div style="color: #999;margin-top: 5px;">V22X 第 {{data.user.id}} 号会员，加入于 {{data.user.time_create}}</div>
              <div style="color: #999;margin-top: 5px;">
                <span style="margin-right: 10px;">被 <strong>{{data.user.be_fav_user_count}}</strong> 人关注</span>
                <span>关注了 <strong>{{data.user.fav_user_count}}</strong> 人</span>
              </div>
            </div>
          </div>
        </div>
        <div class="cell">
          <div>
            <Button type="info"
                    icon="md-home"
                    v-if="data.user.site"
                    :to="data.user.site"
                    target="_blank"
                    class="widget-item">{{data.user.site}}</Button>
            <Button type="default"
                    icon="md-locate"
                    v-if="data.user.location"
                    class="widget-item">{{data.user.location}}</Button>
            <Button type="primary"
                    icon="md-briefcase"
                    v-if="data.user.company"
                    class="widget-item">{{data.user.company}}</Button>
            <Button type="success"
                    icon="logo-github"
                    v-if="data.user.github"
                    :to="data.user.github"
                    target="_blank"
                    class="widget-item">{{data.user.github}}</Button>
            <Button type="primary"
                    icon="logo-twitter"
                    v-if="data.user.twitter"
                    :to="data.user.twitter"
                    target="_blank"
                    class="widget-item">{{data.user.twitter}}</Button>
            <Button type="warning"
                    v-if="data.user.weibo"
                    :to="data.user.weibo"
                    target="_blank"
                    class="widget-item">微博 {{data.user.weibo}}</Button>
          </div>
          <div style="margin-top: 20px;color: rgb(0,0,0)">{{data.user.bio}}</div>
        </div>
      </div>
      <br>
      <div class="box">
        <div class="cell">
          <div>{{data.user.username}} 的所有主题</div>
        </div>
        <div v-if="data.is_open"
             class="topic">
          <div class="cell topic-item"
               v-for="(item,k) in data.topics"
               :key="k">
            <div class="avatar"><a :href="`/#/member?username=${data.user.username}`"><img :src="data.user.avatar_url"></a></div>
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
                     :href="`/#/member?username=${data.user.username}`">{{data.user.username}}</a></div>
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
          <div class="cell"
               v-if="data.topics.length"><a class="a-link"
               :href="`/#/member/topic?username=${data.user.username}`">» {{data.user.username}} 创建的更多主题</a></div>
        </div>
        <div v-else
             class="inner"
             style="display: flex;align-items: center;">
          <div style="margin-left: 20px;margin-right: 20px;">
            <Avatar icon="ios-lock"
                    size="120">
            </Avatar>
          </div>
          <div style="margin-left: 10px;">根据 {{data.user.username}} 的设置，主题列表被隐藏</div>
        </div>
      </div>
      <br>
      <div class="box">
        <div class="cell">{{data.user.username}} 最近回复了</div>
        <div v-for="(item,k) in data.comments"
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
        <div class="cell"
             v-if="data.comments.length"><a class="a-link"
             :href="`/#/member/comment?username=${data.user.username}`">» {{data.user.username}} 创建的更多回复</a></div>
      </div>
    </div>
    <div class="right-content">
    </div>
  </div>
</template>
<script>
import memberAPI from '@/api/member'
import userAPI from '@/api/user'
export default {
  data () {
    return {
      loading: false,
      data: {
        is_open: true,
        user: {
          username: null
        },
        comments: [],
        topics: []
      }
    }
  },
  methods: {
    async handleFavUser (action) {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        await userAPI.fav({ 'uid': this.data.user.uid, 'action': action })
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
    if (!this.$route.query.username) {
      this.$router.push({ 'path': '/index' })
      return
    }
    this.loading = true
    try {
      this.data = await memberAPI.detail({ 'username': this.$route.query.username })
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
.widget-item {
  margin-right: 10px;
  margin-bottom: 5px;
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
