<template>
  <div>
    <Card>
      <ContentHeader :title="$route.meta.title"
                     @on-search=handleSearch
                     :searchAble="true"
                     :searchKeyList="searchKeyList"
                     :addAble="false">
      </ContentHeader>
      <Row class="content-body">
        <Col span="24">
        <Table :columns="columns"
               :data="data"
               border
               @on-sort-change="sortData"
               :loading="loading">
          <template slot-scope="{ row }"
                    slot="user">
            <span v-if="row.user">{{row.user.username}}</span>
          </template>
          <template slot-scope="{ row }"
                    slot="title">
            <a @click="handleDetail(row)">{{row.title}}</a>
          </template>
          <template slot-scope="{ row }"
                    slot="tab">
            <span>{{row.tab.name}} - {{row.tab.zh}}</span>
          </template>
          <template slot-scope="{ row }"
                    slot="sub_tab">
            <span>{{row.sub_tab.name}} - {{row.sub_tab.zh}}</span>
          </template>
          <template slot-scope="{ row }"
                    slot="last_reply_user">
            <span v-if="row.last_reply_user">{{row.last_reply_user.username}}</span>
            <span v-else>暂无回复</span>
          </template>
          <template slot-scope="{ row }"
                    slot="last_reply_time">
            <span v-if="row.last_reply_time">{{row.last_reply_time}}</span>
            <span v-else>暂无回复</span>
          </template>
        </Table>
        </Col>
        <editModal :dialog="editDialog"
                   @getData="getData"></editModal>
        <detailModal :dialog="detailDialog"></detailModal>
      </Row>
    </Card>
    <br>
    <Page :total="total"
          :current="query.page"
          :page-size="query.pageSize"
          @on-change="changePage"
          @on-page-size-change="changePageSize"
          show-sizer />
    <br>
    <CopyRight></CopyRight>
  </div>
</template>

<script>
import ContentHeader from '@/components/content-header'
import CopyRight from '@/components/copyright'
import editModal from '@/components/topic/edit-modal'
import detailModal from '@/components/topic/detail-modal'
import topicAPI from '@/api/topic'
export default {
  name: 'list',
  components: {
    ContentHeader,
    CopyRight,
    editModal,
    detailModal
  },
  data () {
    return {
      columns: [
        { title: 'ID', key: 'id', width: 80, align: 'center', sortable: true },
        { title: '创建者', align: 'center', slot: 'user' },
        { title: '标题', align: 'center', slot: 'title' },
        { title: '所属父节点', align: 'center', slot: 'tab' },
        { title: '所属子节点', align: 'center', slot: 'sub_tab' },
        { title: '内容长度', align: 'center', key: 'content_length' },
        { title: '最后回复者', align: 'center', slot: 'last_reply_user' },
        { title: '最后回复时间', align: 'center', slot: 'last_reply_time' },
        { title: '点击量', align: 'center', key: 'view_count' },
        { title: '回复数量', align: 'center', key: 'comment_count' },
        { title: 'up_count', align: 'center', key: 'up_count' },
        { title: 'down_count', align: 'center', key: 'down_count' },
        {
          title: '操作',
          key: 'action',
          width: 130,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleEdit(params.row)
                  }
                }
              }, '修改'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.handleDelete(params.row)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      data: [],
      loading: false,
      editDialog: {
        show: false,
        title: '修改Topic信息'
      },
      detailDialog: {
        show: false,
        title: 'Topic详情'
      },
      total: 0,
      searchKeyList: ['id', 'user_id', 'title', 'tab_id', 'sub_tab_id', 'last_reply_user_id'],
      query: {
        page: 1,
        page_size: 10,
        odb_: null,
        odt_: null,
        sk_: null,
        sv_: null
      }
    }
  },
  methods: {
    changePage (page) {
      this.query.page = page
    },
    changePageSize (pageSize) {
      this.query.page_size = pageSize
    },
    sortData (item) {
      this.query.odb_ = item.key
      this.query.odt_ = item.order
    },
    async getData () {
      let res = await topicAPI.list(Object.assign({}, this.query))
      this.total = res.total
      this.data = res.list
    },
    handleEdit (row) {
      this.editDialog.uid = row.uid
      this.editDialog.show = true
    },
    handleDetail (row) {
      this.detailDialog.uid = row.uid
      this.detailDialog.show = true
    },
    handleSearch (searchKey, searchValue) {
      this.query.page = 1
      this.query.page_size = 10
      this.query.sk_ = searchKey
      this.query.sv_ = searchValue
    },
    async handleDelete (row) {
      this.$Modal.confirm({
        title: '警告!',
        content: `确定要删除${row.title} Topic吗?`,
        okText: '确定',
        cancelText: '取消',
        onOk: async () => {
          try {
            await topicAPI._delete({ 'uid': row.uid })
            this.$Message.success('删除成功')
            await this.getData()
          } catch (e) {
            if (e.msg) {
              this.$Message.error(e.msg)
            } else {
              console.log(e)
              this.$Message.error('出了点小差')
            }
          }
        }
      })
    }
  },
  watch: {
    query: {
      async handler (oldVal, newVal) {
        this.loading = true
        try {
          await this.getData()
          this.$Message.success('请求成功')
        } catch (e) {
          if (e.msg) {
            this.$Message.error(e.msg)
          } else {
            console.log(e)
            this.$Message.error('出了点小差')
          }
        } finally {
          this.loading = false
        }
      },
      deep: true
    }
  },
  async mounted () {
    this.loading = true
    try {
      await this.getData()
      this.$Message.success('请求成功')
    } catch (e) {
      if (e.msg) {
        this.$Message.error(e.msg)
      } else {
        console.log(e)
        this.$Message.error('出了点小差')
      }
    } finally {
      this.loading = false
    }
  }
}
</script>
