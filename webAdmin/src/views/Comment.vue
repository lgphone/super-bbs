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
                    slot="topic">
            <span>{{row.topic.title}} - {{row.topic.id}}</span>
          </template>
          <template slot-scope="{ row }"
                    slot="content">
            <a @click="handleDetail(row)">{{row.content.slice(0,10)}}...</a>
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
import editModal from '@/components/comment/edit-modal'
import detailModal from '@/components/comment/detail-modal'
import commentAPI from '@/api/comment'
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
        { title: '所属主题', align: 'center', slot: 'topic' },
        { title: '评论内容', align: 'center', slot: 'content' },
        { title: '喜欢量', align: 'center', key: 'like_count', sortable: true },
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
        title: '修改评论信息'
      },
      detailDialog: {
        show: false,
        title: '评论详情'
      },
      total: 0,
      searchKeyList: ['id', 'user_id', 'topic_id'],
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
      let res = await commentAPI.list(Object.assign({}, this.query))
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
        content: `确定要删除 ${row.id} 这条评论吗?`,
        okText: '确定',
        cancelText: '取消',
        onOk: async () => {
          try {
            await commentAPI._delete({ 'uid': row.uid })
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
