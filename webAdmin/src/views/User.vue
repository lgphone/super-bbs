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
                    slot="username">
            <a @click="handleDetail(row)">{{row.username}}</a>
          </template>
          <template slot-scope="{ row }"
                    slot="role_id">
            <Tag color="red" v-if="row.role_id===1">管理员</Tag>
            <Tag v-else>注册用户</Tag>
          </template>
          <template slot-scope="{ row }"
                    slot="status">
            <Tag color="green"
                 v-if="row.status">启用</Tag>
            <Tag color="red"
                 v-else>禁用中</Tag>
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
import addModal from '@/components/user/add-modal'
import editModal from '@/components/user/edit-modal'
import detailModal from '@/components/user/detail-modal'
import userAPI from '@/api/user'
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
        { title: '用户名', align: 'center', slot: 'username' },
        { title: 'email', align: 'center', key: 'email' },
        { title: '角色ID', align: 'center', slot: 'role_id' },
        { title: '状态', align: 'center', slot: 'status' },
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
              }, '修改')
            ])
          }
        }
      ],
      data: [],
      loading: false,
      addDialog: {
        show: false,
        title: '添加用户'
      },
      editDialog: {
        show: false,
        title: '修改用户信息'
      },
      detailDialog: {
        show: false,
        title: '用户详情'
      },
      total: 0,
      searchKeyList: ['id', 'email', 'username', 'role_id'],
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
      let res = await userAPI.list(Object.assign({}, this.query))
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
