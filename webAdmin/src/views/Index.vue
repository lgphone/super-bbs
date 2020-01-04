<template>
  <div>
    <Card>
      <ContentHeader :title="$route.meta.title"
                     :searchAble=false
                     :addAble=false>
      </ContentHeader>
      <Row class="content-body">
        <div>用户总数</div>
        <div>主题总数</div>
        <div>今日新增用户</div>
        <div>今日新增主题</div>
        <div>今日新增评论</div>
      </Row>
    </Card>
    <br>
    <CopyRight></CopyRight>
  </div>
</template>
<script>
import ContentHeader from '@/components/content-header'
import CopyRight from '@/components/copyright'
export default {
  components: {
    ContentHeader,
    CopyRight
  },
  data () {
    return {
      loading: false
    }
  },
  async created () {
    this.loading = true
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
    const timer = setInterval(async () => {
      console.log('refresh data')
      try {
        console.log('refresh data')
      } catch (e) {
        if (e.msg) {
          this.$Message.error(e.msg)
        } else {
          console.log(e)
          this.$Message.error('出了点小差')
        }
        clearInterval(timer)
      }
    }, 3000)
    this.$once('hook:beforeDestroy', () => {
      clearInterval(timer)
    })
  }
}
</script>
