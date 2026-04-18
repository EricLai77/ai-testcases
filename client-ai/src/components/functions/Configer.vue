<template>
  <div class="Configer">
    <!-- 标题 -->
    <div class="page-header">
      <h1>{{ msg }}</h1>
      <el-button type="primary" @click="dialogFormCreatedVisible = true">
        Add a config
      </el-button>
    </div>

    <!-- 表格容器 -->
    <div class="table-container">
      <el-table
        v-loading="tableLoading"
        :data="tableData"
        border
        stripe
        style="width: 90%; max-width: 1000px;"
        height="800"
      >
        <el-table-column prop="key" label="Key" width="140"></el-table-column>
        <el-table-column prop="value" label="Value" width="300"></el-table-column>
        <el-table-column prop="update_time" label="Update Time" width="180"></el-table-column>
        <el-table-column prop="memo" label="Memo" width="200"></el-table-column>
        <el-table-column label="Operation" width="180">
          <template slot-scope="scope">
            <el-button @click="openEditDialog(scope.row)" type="text" size="small">Edit</el-button>
            <el-button
              @click="delInfo(scope.row)"
              :loading="deleteLoading[scope.row.key]"
              type="text"
              size="small"
              style="color: red;"
            >Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 创建配置 Dialog -->
    <el-dialog title="Create a new config" :visible.sync="dialogFormCreatedVisible">
      <el-form :model="formCreate">
        <el-form-item label="key" :label-width="formLabelWidth">
          <el-input v-model="formCreate.key"></el-input>
        </el-form-item>
        <el-form-item label="value" :label-width="formLabelWidth">
          <el-input v-model="formCreate.value"></el-input>
        </el-form-item>
        <el-form-item label="memo" :label-width="formLabelWidth">
          <el-input v-model="formCreate.memo"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormCreatedVisible = false">Cancel</el-button>
        <el-button type="primary" @click="createInfo" v-loading="createLoading">Confirm</el-button>
      </div>
    </el-dialog>

    <!-- 编辑配置 Dialog -->
    <el-dialog title="Edit this config" :visible.sync="dialogFormVisible">
      <el-form :model="formChange">
        <el-form-item label="key" :label-width="formLabelWidth">
          <el-input v-model="formChange.key" disabled></el-input>
        </el-form-item>
        <el-form-item label="value" :label-width="formLabelWidth">
          <el-input v-model="formChange.value"></el-input>
        </el-form-item>
        <el-form-item label="memo" :label-width="formLabelWidth">
          <el-input v-model="formChange.memo"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" v-loading="editLoading" @click="editInfo">Confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>
 
<script>
export default {
  name: "Configer",
  data() {
    return {
      msg: "Project Configuration",
      deleteLoading: {}, /*删除配置的loding缓存 */
      dialogFormVisible : false, /*编辑子窗口默认不可见 */
      dialogFormCreatedVisible : false, /*创建配置子窗口默认不可见 */
      formLabelWidth: '120px',/*编辑子界面的标签宽度 */
      editLoading: false,/*编辑进行时的loading变量 */
      createLoading: false,/*创建进行时的loading变量 */
      formChange: {
        key: '',
        value: '',
        memo: ''
      },
      formCreate: {
        key: '',
        value: '',
        memo: ''
      },
      tableData: [{
        key: 'ip',
        value: '123.123.123.13',
        update_time: '2025-10',
        memo: 'camp a'
      }, {
        key: 'ip2',
        value: '123.123.123.13',
        update_time: '2025-10',
        memo: 'camp a'
      },{
        key: 'ip6',
        value: '123.123.123.13',
        update_time: '2025-10',
        memo: 'camp a'
      }, {
        key: 'ip7',
        value: '123.123.123.13',
        update_time: '2025-10',
        memo: 'camp a'
      }, {
        key: 'ip8',
        value: '123.123.123.13',
        update_time: '2025-10',
        memo: 'camp a'
      }]
    };
  },
  methods: {
    updateDelLoading () {
      // 初始化每个删除按钮状态
      this.deleteLoading = {} // 先清空
      this.tableData.forEach(item => {
        this.$set(this.deleteLoading, item.id, false)
      })
    },
    openEditDialog (row) {
      console.log('open sub-window')
      console.log(row)
      this.formChange = JSON.parse(JSON.stringify(row))
      this.dialogFormVisible = true
      console.log('open sub-window finish')
    },
    formatDate(date) {
      const d = date || new Date();
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    editInfo () {
      if (!confirm('Do you confirm to edit this configer？')) {
        return
      }
      //console.log(row)
      // 执行编辑操作
      this.editLoading = true
      //console.log(row.key)
      console.log(this.formChange.key)
      console.log('begin edit')
      // 真正请求编辑
      this.$axios.post('/api/editConfig/',
        // {id: Number(row.id)},
        this.$qs.stringify({
          key: this.formChange.key,//key值不变
          value: this.formChange.value,
          memo: this.formChange.memo,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      ).then((response) => {
        // 成功请求
        // 处理前端显示
        // 要删除 id=2 的元素
        console.log(response)
        if (response.data.code !== 0) { // 表示编辑不成功
          alert('This edit operation failed!')
          this.editLoading = false
        } else { // 表示编辑成功
          alert('This edit operation is sucessful!')
          const index = this.tableData.findIndex(item => item.key === this.formChange.key)//找到被编辑的那一行
          console.log('look here')
          console.log(index)
          console.log('look here')
          if (index !== -1) {
            this.tableData[index].value = this.formChange.value
            this.tableData[index].memo = this.formChange.memo
            this.tableData[index].update_time = this.formatDate()
          }
          this.editLoading = false
          this.dialogFormVisible = false
        }
      }).catch((error) => {
        console.log(error)
        this.editLoading = false
        this.dialogFormVisible = false
      })
    },
    createInfo () {
      //if (!confirm('Do you confirm to create this configer？')) {
      //  return
      //}
      //console.log(row)
      // 执行编辑操作
      this.createLoading = true
      //console.log(row.key)
      console.log(this.formCreate.key)
      console.log('begin create')
      // 真正请求编辑
      this.$axios.post('/api/createConfig/',
        // {id: Number(row.id)},
        this.$qs.stringify({
          key: this.formCreate.key,//key值不变
          value: this.formCreate.value,
          memo: this.formCreate.memo,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      ).then((response) => {
        // 成功请求
        // 处理前端显示
        // 要删除 id=2 的元素
        console.log(response)
        if (response.data.code !== 0) { // 表示编辑不成功
          alert('This create operation failed!')
          this.editLoading = false
        } else { // 表示编辑成功
          alert('This create operation is sucessful!')
          this.tableData.push({
            key: this.formCreate.key,//key值不变
            value: this.formCreate.value,
            memo: this.formCreate.memo,
            update_time: this.formatDate()
          })
          this.createLoading = false
          this.dialogFormCreatedVisible = false
        }
      }).catch((error) => {
        console.log(error)
        this.createLoading = false
        this.dialogFormCreatedVisible = false
      })
    },
    delInfo (row) {
      if (!confirm('Do you confirm to delete this configer?')) {
        return
      }
      console.log(row)
      // 执行删除操作
      this.$set(this.deleteLoading, row.key, true)
      console.log('/api/deleteConfig/?id=' + row.key)
      console.log(row.key)
      // 真正请求删除
      this.$axios.post('/api/deleteConfig/',
        // {id: Number(row.id)},
        this.$qs.stringify({ key: row.key }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      ).then((response) => {
        // 成功请求
        // 处理前端显示
        // 要删除 key='xxx' 的元素
        console.log(response)
        if (response.data.code !== 0) { // 表示删除不成功
          alert('This delete operation failed!')
          this.$set(this.deleteLoading, row.key, false)
          this.updateDelLoading()
        } else { // 表示删除成功
          console.log(this.tableData)
          const targetkey = row.key
          console.log(targetkey)
          const delIndex = this.tableData.findIndex(item => item.key === targetkey)
          console.log(delIndex)
          if (delIndex !== -1) {
            this.tableData.splice(delIndex, 1) // 从索引位置删除 1 个元素
          }
          this.$set(this.deleteLoading, row.key, false)
          this.updateDelLoading()
        }
      }).catch((error) => {
        console.log(error)
        this.$set(this.deleteLoading, row.key, false)
        this.updateDelLoading()
      })
    }
  },
  created () {
    console.log('create')
    this.tableLoading = true
    this.$axios.get('/api/allConfigInfo/').then((response) => {
      console.log(response.data.msg)
      var resData = []
      for (var props in response.data.msg) {
        // console.log(response.data.msg[props])
        let perData = {'key': response.data.msg[props][1], 'value': response.data.msg[props][2], 'update_time': response.data.msg[props][3].slice(0, 10), 'memo': response.data.msg[props][4]}
        resData.push(perData)// 塞数据进入
      }
      console.log(resData)
      this.tableData = resData
      // 初始化删除列表的loading状态
      this.updateDelLoading()
      this.tableLoading = false
    }).catch((error) => {
      console.log(error.status)
      this.tableLoading = false
    })
    console.log('createFinish')
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.Configer {
  padding: 40px 20px;
  text-align: center;
  background: #f5f7fa; /* 淡灰背景 */
  min-height: 100vh;
}

/* 标题美化 */
.Configer h1 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
}

/* 按钮区域 */
.Configer .top-actions {
  margin-bottom: 20px;
}

/* 表格容器 */
.Configer .table-container {
  display: flex;
  justify-content: center;
}

/* 表格样式 */
::v-deep .el-table {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  background: white;
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px; /* 表头和表格的间距 */
}

.page-header h1 {
  font-size: 22px;
  margin: 0;
}
</style>
