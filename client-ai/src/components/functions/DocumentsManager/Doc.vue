<template>
 <div class="Doc">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>Project Management</span>
        <el-button 
          style="float: right; padding: 3px 0" 
          type="text"
          @click="showCreateProjectDialog = true">
          Create a new project
        </el-button>
      </div>
      <el-table v-loading="projecttableLoading" :data="projects" style="width: 100%">
        <el-table-column prop="name" label="Project Name"></el-table-column>
        <el-table-column prop="description" label="Description"></el-table-column>
        <el-table-column prop="created_at" label="Created Time" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="280">
          <template slot-scope="scope">
            <el-button size="mini" @click="viewProject(scope.row)">View</el-button>
            <el-button size="mini" v-loading="loading_deleteproject" @click="deleteProject(scope.row)">Delete</el-button>
            <el-button size="mini" type="primary" @click="uploadDocument(scope.row)">Upload</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 新建项目对话框 -->
    <el-dialog title="Create a new project" :visible.sync="showCreateProjectDialog" width="500px">
      <el-form :model="newProject" label-width="120px" class="project-form">
        <el-form-item label="Project Name">
          <el-input v-model="newProject.name" style="max-width: 300px;" />
        </el-form-item>
        <el-form-item label="Description">
          <el-input
            type="textarea"
            v-model="newProject.description"
            style="max-width: 300px;"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="showCreateProjectDialog = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="createProject"
          v-loading="loading_createproject"
        >Confirm</el-button>
      </div>
    </el-dialog>
    <!-- 上传文档对话框 -->
    <el-dialog 
      title="Upload requirement documents" 
      :visible.sync="showUploadDialog"
      width="500px"
    >
      <div class="upload-dialog-body">
        <!-- 上传组件 -->
        <el-upload
          class="upload-demo"
          drag
          action=""
          :before-upload="beforeUpload"
          :auto-upload="false"
          :on-change="handleFileChange"
          accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          :file-list="fileList">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            Drag here，or <em>Press 'Upload'</em>
          </div>
          <div class="el-upload__tip" slot="tip">NOTE: Docx Only</div>
        </el-upload>

        <!-- 表单 -->
        <el-form :model="documentForm" label-width="60px" class="upload-form">
          <el-form-item label="Name">
            <el-input v-model="documentForm.name"></el-input>
          </el-form-item>
        </el-form>
      </div>

      <!-- 底部按钮 -->
      <div slot="footer" class="dialog-footer">
        <el-button @click="showUploadDialog = false">Cancel</el-button>
        <el-button type="primary" @click="submitDocument" v-loading="loading_uploaddoc">Upload</el-button>
      </div>
    </el-dialog>


    <!-- 项目详情抽屉 -->
    <el-drawer
      title="Project Details"
      :visible.sync="drawerVisible"
      direction="rtl"
      size="60%">
      <div class="project-detail">
        <el-divider class="compact-divider"></el-divider>

        <h3 class="doc-title">Requirement Documents</h3>
        <el-table 
          :data="currentProject.documents" 
          class="compact-table"
          border
          size="small" 
          style="width:100%">
          <el-table-column prop="name" label="Name"></el-table-column>
          <el-table-column prop="uploaded_at" label="Upload Time" width="160">
            <template slot-scope="scope">
              {{ formatDate(scope.row.uploaded_at) }}
            </template>
          </el-table-column>
          <el-table-column label="Operations" width="160">
            <template slot-scope="scope">
              <el-button size="mini" @click="viewDocument(scope.row)">View</el-button>
              <el-button size="mini" v-loading="loading_deletedocument" @click="deleteDocument(scope.row)">Delete</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-drawer>

  <!-- 文档详情对话框 -->
  <el-dialog 
    :title="currentDocument.name" 
    :visible.sync="showDocumentDialog" 
    width="80%"
    top="5vh">
    <el-tabs v-model="activeSection">
      <el-tab-pane 
        v-for="section in currentDocument.sections" 
        :key="section.section_number"
        :label="section.heading || `Section ${section.section_number}`"
        :name="String(section.section_number)">
        <pre class="document-content">{{ section.content }}</pre>
      </el-tab-pane>
    </el-tabs>
    <div slot="footer" class="dialog-footer">
      <el-button @click="showDocumentDialog = false">Cancel</el-button>
    </div>
  </el-dialog>
 </div>
</template>
 
<script>
export default {
  name: "Doc",
  data() {
    return {
      msg: "doc",
      loading_createproject: false,
      loading_deleteproject: false,
      loading_deletedocument: false,
      loading_uploaddoc: false,
      projecttableLoading: false,
      projects: [],
      showCreateProjectDialog: false,
      newProject: {
        name: '',
        description: ''
      },
      showUploadDialog: false,
      fileList: [],
      documentForm: {
        name: '',
        file: null,
        project_id: null
      },
      drawerVisible: false,
      currentProject: {
        name: '',
        description: '',
        created_at: '',
        documents: []
      },
      showDocumentDialog: false,
      currentDocument: {
        name: '',
        sections: []
      },
      activeSection: '1'
    };
  },
  created() {
    this.loadProjects()
  },
  methods:{
    submitDocument() {
      if (this.fileList.length === 0) {
        this.$message.warning('Please select a file to submit')
        return
      }
      if (!confirm('Do you confirm to upload this document？')) {
        return
      }
      console.log('begin to upload')
      this.loading_uploaddoc = true
      // 1. 使用 FormData 包装数据
      const formData = new FormData()
      formData.append('name', this.documentForm.name)
      formData.append('project', this.documentForm.project_id)

      // 2. 正确附加文件（假设 this.documentForm.file 是 FileList 对象）
      const file = this.fileList[0].raw // 获取第一个文件
      console.log(file)
      formData.append('original_file', file)
      
      console.log(formData)
      // 真正请求编辑
      this.$axios.post('/api/mydocuments/documents/', formData,
        {
          headers: {
            'X-CSRFToken': this.$Cookies.get('csrftoken'),
          }
        }
      ).then((response) => {
        // 成功请求
        console.log('upload doc')
        console.log(response)
        console.log(response.data)
        // 表示编辑成功
        this.$message.success('you have submited the file successfully')
        this.loading_uploaddoc = false
        this.showUploadDialog = false
        this.fileList = []
        this.documentForm = { name: '', file: null, project_id: null }
        this.loadProjects()
      }).catch((error) => {
        console.log(error)
        this.loading_uploaddoc = false
        this.$message.error('there are some problem during uploading!')
      }) 
    },
    // 文件类型验证
    beforeUpload(file) {
      const isDocx = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || 
                    file.name.endsWith('.docx');
      if (!isDocx) {
        this.$message.error('Docx Only！');
        return false; // 阻止上传
      }
      return true;
    },
     viewDocument(document) {
      window.open(document.original_file, '_blank');
      // window.open(`https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(document.original_file.url)}`)
      // this.currentDocument = document
      // this.showDocumentDialog = true
    },
    downloadDocument(document) {
      window.open(document.original_file, '_blank')
    },
    handleFileChange(file, fileList) {
      console.log('提交了一个文件')
      this.fileList = fileList.slice(-1) // 只保留最新上传的文件
      this.documentForm.file = file.raw
      if (!this.documentForm.name) {
        this.documentForm.name = file.name.replace('.docx', '')
      }
      
      console.log('当前文件:', this.documentForm.file); // 调试用
    },
    uploadDocument(project) {
      this.documentForm.project_id = project.id
      this.showUploadDialog = true
    },
    deleteProject(project) {
     if (!confirm('Do you confirm to delete this project？')) {
        return
      }
      this.loading_deleteproject = true
      // 真正请求编辑
      var projectId = project.id
      this.$axios.post(`/api/mydocuments/projects/${projectId}/delete/`,
        {},
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.$Cookies.get('csrftoken'),
          }
        }
      ).then((response) => {

        console.log(response)
        if (response.data.code !== 0) { // 表示编辑不成功
          alert('This delete operation failed!')
          this.loading_deleteproject = false
        } else { // 表示编辑成功
          this.$message.success('You have deleted a project successfully.')
          this.loading_deleteproject = false
          this.loadProjects()
        }
      }).catch((error) => {
        console.log(error)
        this.loading_deleteproject = false
      })
    },
    deleteDocument(document) {
     if (!confirm('Do you confirm to delete this document？')) {
        return
      }
      this.loading_deletedocument = true
      // 真正请求编辑
      var documentId = document.id
      console.log(documentId)
      console.log(this.$Cookies.get('csrftoken'))
      this.$axios.post(`/api/mydocuments/documents/${documentId}/delete/`,
        {},
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.$Cookies.get('csrftoken'),
          }
        }
      ).then((response) => {

        console.log(response)
        if (response.data.code !== 0) { // 表示编辑不成功
          alert('This delete operation failed!')
          this.loading_deletedocument = false
        } else { // 表示编辑成功
          this.$message.success('You have deleted a document successfully.')
          this.loading_deletedocument = false
          this.drawerVisible = false
          this.loadProjects()
        }
      }).catch((error) => {
        console.log(error)
        this.loading_deletedocument = false
      })
    },
    viewProject(project) {
      this.currentProject = project
      this.drawerVisible = true
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    loadProjects() {
      console.log('读取数据')
      this.projecttableLoading = true
      this.$axios.get('/api/mydocuments/projects/').then((response) => {
        console.log(response.data)
        this.projects = response.data
        this.projecttableLoading = false
      }).catch((error) => {
        this.projecttableLoading = false
        this.$message.error('Loading project list failed!')
        console.error(error)
        this.$router.push({
                path: '/',
              })// 跳转到指定网页，后端来决定
      })
    },
    createProject() {
      if (!confirm('Do you confirm to create this project？')) {
        return
      }
      this.loading_createproject = true
      // 真正请求编辑
      this.$axios.post('/api/mydocuments/projects/',
        this.$qs.stringify({
          name: this.newProject.name,
          description: this.newProject.description,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.$Cookies.get('csrftoken'),
          }
        }
      ).then((response) => {
        // 成功请求
        console.log('create project')
        console.log(response)
        console.log(response.data)
        // 表示编辑成功
        this.$message.success('You have created a project successfully.')
        this.loading_createproject = false
        this.showCreateProjectDialog = false
        this.newProject = { name: '', description: '' }
        this.loadProjects()
        
      }).catch((error) => {
        console.log(error)
        this.loading_createproject = false
        this.showCreateProjectDialog = false
      })

    },
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
::v-deep .el-card__header {
  padding: 10px 14px;
}
::v-deep .el-card__body {
  padding: 10px 14px;
}

::v-deep .el-table th {
  padding: 6px 8px !important;  /* 上下左右缩小 */
  height: 6px;                 /* 限制高度 */
  line-height: 32px;            /* 垂直居中 */
  font-size: 13px;              /* 字体缩小 */
}
::v-deep .el-table td {
  padding: 6px 8px !important;
  height: 32px;
  line-height: 32px;
  font-size: 13px;
}

::v-deep .el-button--mini {
  padding: 2px 8px;
  font-size: 12px;
}

/* 减少 padding */
.project-detail {
  padding: 10px 20px; /* 减少 padding */
}

.project-title {
  font-size: 16px;   /* 缩小标题 */
  margin-bottom: 6px;
}

.project-desc {
  font-size: 14px;
  margin: 2px 0;     /* 缩小段落间距 */
}

.project-time {
  font-size: 13px;
  color: #666;
  margin: 2px 0 8px 0;
}

.compact-divider {
  margin: 8px 0;     /* 缩小分割线上下空隙 */
}

.doc-title {
  font-size: 14px;
  margin: 6px 0;
}

.compact-table ::v-deep .el-table__row {
  height: 36px;  /* 缩小表格行高 */
}

.compact-table ::v-deep th, 
.compact-table ::v-deep td {
  padding: 6px 8px; /* 缩小单元格内边距 */
}

/* 缩小 Dialog 内边距 */
::v-deep .el-dialog__body {
  padding: 12px 16px !important;
}

/* 上传框缩小高度 */
::v-deep .el-upload-dragger {
  padding: 8px 0 !important;
  height: 50px !important;      /* 默认 180px，这里调小 */
  line-height: 50px !important;
}

/* 上传提示文字（Docx Only）和上传框间距缩小 */
::v-deep .el-upload__tip {
  margin-top: 0px !important;
  font-size: 8px;
}

/* 表单项之间的间距缩小 */
::v-deep .el-form-item {
  margin-bottom: 5px !important;   /* 默认 22px */
}

/* 输入框高度缩小 */
::v-deep .el-input__inner {
  height: 20px !important;     /* 默认 40px */
  line-height: 32px !important;
  font-size: 13px;
}
</style>
