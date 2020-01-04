<template>
  <div>
    <Card>
      <ContentHeader :title="$route.meta.title"
                     @on-search=handleSearch
                     :searchAble="true"
                     :searchKeyList="searchKeyList"
                     @on-add=handleAdd>
      </ContentHeader>
      <Row class="content-body">
        <Col span="24">
        <Table :columns="columns"
               :data="data"
               border
               @on-sort-change="sortData"
               :loading="loading">
          <template slot-scope="{ row }"
                    slot="tab">
            <span v-if="row.tab">{{row.tab.name}} - {{row.tab.zh}}</span>
          </template>
          <template slot-scope="{ row }"
                    slot="name">
            <a @click="handleDetail(row)">{{row.name}}</a>
          </template>
        </Table>
        </Col>
        <addModal :dialog="addDialog"
                  @getData="getData"></addModal>
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
import addModal from '@/components/sub-tab/add-modal'
import editModal from '@/components/sub-tab/edit-modal'
import detailModal from '@/components/sub-tab/detail-modal'
import subTabAPI from '@/api/sub_tab'
export default {
  name: 'list',
  components: {
    ContentHeader,
    CopyRight,
    addModal,
    editModal,
    detailModal
  },
  data () {
    return {
      columns: [
        { title: 'ID', key: 'id', width: 80, align: 'center', sortable: true },
        { title: '父节点', align: 'center', slot: 'tab' },
        { title: 'name', align: 'center', slot: 'name' },
        { title: '中文名称', align: 'center', key: 'zh' },
        { title: '序列号', align: 'center', key: 'sort_num' },
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
      addDialog: {
        show: false,
        title: '添加SubTab'
      },
      editDialog: {
        show: false,
        title: '修改SubTab信息'
      },
      detailDialog: {
        show: false,
        title: 'SubTab详情'
      },
      total: 0,
      searchKeyList: ['id', 'name', 'zh', 'sort_num', 'tab_id'],
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
      let res = await subTabAPI.list(Object.assign({}, this.query))
      this.total = res.total
      this.data = res.list
    },
    handleEdit (row) {
      this.editDialog.uid = row.uid
      this.editDialog.show = true
    },
    handleAdd () {
      this.addDialog.show = true
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
        content: `确定要删除${row.name} subTab吗?`,
        okText: '确定',
        cancelText: '取消',
        onOk: async () => {
          try {
            await subTabAPI._delete({ 'uid': row.uid })
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
