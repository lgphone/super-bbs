<template>
  <div style="display: flex;">
    <div class="left-content"
         style="position: relative; flex-grow: 1">
      <div class="box">
        <div class="cell"
             style="display: flex;">
          <div style="flex-grow: 1">
            <div style="margin-bottom:20px;"><a href="/#/index"
                 class="a-link">V22X</a><span> › </span><a :href="`/#/go?tab=${data.sub_tab.name}`"
                 class="a-link">{{data.sub_tab.zh}}</a></div>
            <div style="margin-bottom:10px;">
              <h2>{{data.title}}</h2>
            </div>
            <div>
              <span style="margin-right: 5px;"><Button size="small"
                        @click="handleUpDown('up')"
                        style="height: 20px;"
                        icon="ios-arrow-up">{{data.up_count}}</Button></span>
              <span style="margin-right: 15px;"><Button size="small"
                        @click="handleUpDown('down')"
                        style="height: 20px;"
                        icon="ios-arrow-down">{{data.down_count}}</Button></span>
              <span style="margin-right: 5px;"><a class="a-link"
                   :href="`/#/member?username=${data.user.username}`">{{data.user.username}}</a></span>·
              <span style="margin-right: 5px;color: #999;">创建于{{data.time_create}}</span>·
              <span style="margin-right: 5px;color: #999;">{{data.view_count}} 次点击</span>·
              <span v-if="$user&&$user.id === data.user.id"><Button size="small"
                        :to="`/t/append?uid=${data.uid}`">追加</Button></span>
            </div>
          </div>
          <div class="avatar-big"></div>
        </div>
        <div v-if="data.content"
             class="cell">
          <MarkdownPreview theme="oneDark"
                           :bordered="false"
                           :initialValue="data.content" />
        </div>
        <div class="cell append"
             v-for="(item,k) in data.appends"
             :key="k">
          <div style="color: #ccc;margin-bottom: 6px;">第{{k + 1}}条追加 * {{ item.time_create }}</div>
          <div>
            <MarkdownPreview theme="oneDark"
                             :bordered="false"
                             :initialValue="item.content" />
          </div>
        </div>
        <div class="cell"
             style="display: flex;justify-content: space-between;align-items: center;">
          <div style="display: flex;">
            <div style="margin-right: 10px;">
              <div v-if="$user&&$user.id === data.user.id"><Button size="small"
                        disabled>加入收藏</Button></div>
              <div v-else>
                <Button size="small"
                        v-if="data.is_fav"
                        @click="handleFav('cal')">取消收藏</Button>
                <Button size="small"
                        v-else
                        @click="handleFav('add')">加入收藏</Button>
              </div>
            </div>
            <div>
              <div v-if="$user&&$user.id === data.user.id||data.is_thank"><Button size="small"
                        shape="circle"
                        disabled>感谢</Button></div>
              <div v-else>
                <Button size="small"
                        shape="circle"
                        @click="handleThank()">感谢</Button>
              </div>
            </div>
          </div>
          <div>{{data.view_count}} 次点击</div>
        </div>
      </div>
      <br>
      <div class="box"
           v-if="data.comments">
        <div class="cell">{{data.comment_count}}条回复 * 直到 {{currentData}}</div>
        <div class="cell"
             v-if="data.comment_count > 100">
          <Page :total="data.comment_count"
                size="small"
                :current="query.page"
                :page-size="query.page_size"
                @on-change="changePage"
                show-elevator />
        </div>
        <div class="cell comment-item"
             v-for="(item,k) in data.comments"
             :key="k">
          <div class="avatar"><a :href="`/#/member?username=${item.user.username}`"><img :src="item.user.avatar_url"></a></div>
          <div class="comment-content">
            <div class="info">
              <div class="comment-user">
                <div style="display: flex;align-items: center;"><a class="a-link"
                     :href="`/#/member?username=${item.user.username}`">{{item.user.username}}</a>
                  <span style="margin-left: 10px;">回复于 {{item.time_create}}</span></div>
                <div style="margin-left: 8px;"><Button size="small"
                          v-if="$user&&$user.id === item.user.id||item.is_thank"
                          shape="circle"
                          disabled>感谢</Button>
                  <Button size="small"
                          v-else
                          shape="circle"
                          @click="handleCommentThank(item)">感谢</Button>
                </div>
              </div>
              <div class="comment-count">
                <a href="javascript:"
                   @click="handleReturnComment(item)">
                  <Icon type="md-arrow-round-back"
                        size="18"
                        style="margin-right: 10px;"></Icon>
                </a>
                <Badge :text="String(item.index)"
                       type="normal"></Badge>
              </div>
            </div>
            <div class="data">{{item.content}}</div>
          </div>
        </div>
        <div class="cell"
             v-if="data.comment_count > 100">
          <Page :total="data.comment_count"
                size="small"
                :current="query.page"
                :page-size="query.page_size"
                @on-change="changePage"
                show-elevator />
        </div>
      </div>
      <br>
      <div class="box">
        <div class="cell">添加一条新回复</div>
        <div class="cell">
          <Input v-model="comment"
                 type="textarea"
                 :rows="6"
                 placeholder="添加评论" />
          <div style="display: flex;margin-top: 10px;justify-content: space-between;align-items: center;">
            <div style="margin-right: 20px;"><Button @click="handleComment">回复</Button></div>
            <div>请尽量让自己的回复能够对别人有帮助</div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
      <br>
      <div class="box">
        <div class="inner">
          这是一个专门讨论 idea 的地方。
          <br>
          每个人的时间，资源是有限的，有的时候你或许能够想到很多 idea，但是由于现实的限制，却并不是所有的 idea 都能够成为现实。
          <br>
          那这个时候，不妨可以把那些 idea 分享出来，启发别人。
        </div>
      </div>
    </div>
    <BackTop></BackTop>
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
      currentData: new Date().toLocaleString(),
      data: {
        user: {
          id: null,
          username: null
        },
        sub_tab: {
          name: null,
          zh: null
        }
      },
      comment: null,
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
    handleReturnComment (item) {
      if (this.comment) {
        if (this.comment.search(` @${item.user.username} `) === -1) {
          this.comment += ` @${item.user.username} `
        }
      } else {
        this.comment = ` @${item.user.username} `
      }
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    },
    async handleFav (action) {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        await topicAPI.fav({ 'uid': this.query.uid, 'action': action })
        this.data.is_fav = !this.data.is_fav
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      }
    },
    async handleThank () {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        await topicAPI.thank({ 'uid': this.query.uid })
        this.data.is_thank = true
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      }
    },
    async handleCommentThank (item) {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        await topicAPI.commentThank({ 'uid': item.uid })
        this.data = await topicAPI.list(this.query)
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      }
    },
    async handleComment () {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        await topicAPI.comment({'uid': this.query.uid, 'comment': this.comment})
        this.comment = null
        this.data = await topicAPI.list(this.query)
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('服务器出了点小差')
        }
      }
    },
    async handleUpDown (action) {
      if (!this.$user) {
        this.$Message.error('登录后才可以操作哦')
        return
      }
      try {
        let tmp = await topicAPI.upDown({ 'uid': this.query.uid, 'action': action })
        this.data.up_count = tmp.up_count
        this.data.down_count = tmp.down_count
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
    this.query.uid = this.$route.query.uid
    if (parseInt(this.$route.query.page)) {
      this.query.page = parseInt(this.$route.query.page)
    }
    this.loading = true
    try {
      await topicAPI.addView({ 'uid': this.query.uid })
      this.data = await topicAPI.list(this.query)
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
  },
  async beforeRouteUpdate (to, from, next) {
    if (parseInt(to.query.page)) {
      this.query.page = parseInt(to.query.page)
    } else {
      this.query.page = 1
    }
    this.loading = true
    try {
      this.data = await topicAPI.list(this.query)
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
.append {
  background-color: #fffff9;
  border-left: 3px solid #fffbc1;
  padding: 10px;
  font-size: 14px;
  line-height: 120%;
  text-align: left;
  border-bottom: 1px solid #e2e2e2;
}
.comment-item {
  display: flex;
  .comment-content {
    flex-grow: 1;
    margin-left: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    .info {
      display: flex;
      justify-content: space-between;
      .comment-user {
        display: flex;
        a {
          font-weight: bold;
        }
      }
    }
    .data {
      font-size: 15px;
      color: black;
    }
  }
}
</style>
