<template>
  <center>Copyright © {{year}} super-bbs </center>
</template>

<script>
export default {
  name: 'copyRight',
  computed: {
    year: function () {
      return this.$date.getThisYear()
    }
  }
}
</script>

<style lang="scss" scoped>
center {
  text-align: center;
}
</style>
