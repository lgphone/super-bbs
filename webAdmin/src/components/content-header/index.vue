<template>
  <Row class="content-header">
    <Col class="content-header-title"
         span="3">
    <h3>{{ title }}</h3>
    </Col>
    <Col class="content-header-con"
         span="20">
    <div class="content-header-button">
      <strong v-if="searchAble" style="margin-right: 5px;">搜索: </strong>
      <Select v-model="searchKey"
              v-if="searchAble"
              placeholder="搜索项"
              style="width:100px">
        <Option v-for="item in searchKeyList"
                :value="item"
                :key="item">{{ item }}</Option>
      </Select>
      <Input class="search-input content-header-item"
             v-if="searchAble"
             v-model="searchValue"
             placeholder="输入关键字搜索"></Input>
      <Button class="content-header-item"
              v-if="searchAble"
              @click="search()">搜索</Button>
      <Button class="content-header-item"
              v-if="addAble"
              @click="add()"
              type="primary">添加</Button>
      <slot name='header-button'></slot>
    </div>
    </Col>
  </Row>
</template>

<script>
export default {
  name: 'content-header',
  props: {
    title: String,
    searchAble: { type: Boolean, default: false },
    addAble: { type: Boolean, default: true },
    addTo: Boolean,
    searchKeyList: Array
  },
  data () {
    return {
      searchKey: null,
      searchValue: null
    }
  },
  methods: {
    search () {
      this.$emit('on-search', this.searchKey, this.searchValue)
    },
    add () {
      this.$emit('on-add')
    }
  }
}
</script>
