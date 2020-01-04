<template>
  <div style="display: flex;">
    <div class="left-content">
      <div class="box">
        <div class="cell"><a href="/#/index"
             class="a-link">V22X</a><span> › </span><span>我收藏的节点</span>
        </div>
        <div class="cell"
             v-if="loading">
          <loadingSpin></loadingSpin>
        </div>
        <div class="inner"
             v-if="!loading"
             style="display: flex;">
          <Card style="width:150px;margin-right: 20px;"
                v-for="(item,k) in data"
                :key="k">
            <a :href="`/#/go?tab=${item.name}`">
              <div style="text-align:center">
                <img>
                <h2>{{item.zh}}</h2>
                <div style="margin-top: 5px;">
                  <Icon type="ios-text" /><strong style="margin-left: 5px;">{{item.topic_count}}</strong></div>
              </div>
            </a>
          </Card>
        </div>
        <div class="inner"></div>
      </div>
    </div>
    <div class="right-content">
      <userBox></userBox>
    </div>
  </div>
</template>
<script>
import loadingSpin from '@/components/loading-spin'
import userBox from '@/components/user-box'
import tabAPI from '@/api/tab'
export default {
  components: {
    userBox,
    loadingSpin
  },
  data () {
    return {
      loading: false,
      data: []
    }
  },
  async created () {
    this.loading = true
    try {
      this.data = await tabAPI.listFavSubTab()
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
</style>
