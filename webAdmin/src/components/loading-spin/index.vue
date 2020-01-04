<template>
  <div class="spin-col">
    <Spin fix>
      <Icon type="ios-loading"
            size=18
            class="spin-icon-load"></Icon>
      <div>Loading</div>
    </Spin>
  </div>
</template>

<script>
export default {
  name: 'loading'
}
</script>

<style lang="scss" scoped>
@keyframes ani-demo-spin {
  from {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.spin-col {
  height: 300px;
  position: relative;
}
.spin-icon-load {
  animation: ani-demo-spin 1s linear infinite;
}
</style>
