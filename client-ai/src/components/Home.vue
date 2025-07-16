<template>
  <el-container>
    <el-aside width="25%">
      <div class="menu" style="text-align: left;">
        <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            background-color="#0b6442"
            text-color="#fff"
            @select="changeSidebar"
            active-text-color="#ffd04b">
            <el-menu-item-group index="1">
                <template slot="title">Functional Testing</template>
                <el-menu-item index="1-1">Project Management</el-menu-item>
                <el-menu-item index="/functions/AiTestcases/Testcases">Test Case</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group index="2">
                <template slot="title">API Testing</template>
                <el-menu-item index="2-1">Project Dependency</el-menu-item>
                <el-menu-item index="2-2">Document Management</el-menu-item>
                <el-menu-item index="/functions/AiApiTest/ApiTest">API Testing</el-menu-item>
            </el-menu-item-group>
            <el-menu-item index="/functions/AiWebTest/WebTest">
                <i class="el-icon-mobile"></i>
                <span slot="title">Web Automation Testing</span>
            </el-menu-item>
            <el-menu-item index="/functions/AiAppTest/AppTest">
                <i class="el-icon-chat-dot-square"></i>
                <span slot="title">Mobile App Automation Testing</span>
            </el-menu-item>
            <el-menu-item index="/functions/Configer">
                <i class="el-icon-s-tools" ></i>
                <span slot="title">Project Configer</span>
            </el-menu-item>
        </el-menu>
      </div>
    </el-aside>
    <el-container>
        <el-header>Kia ora user. Welcome to my AI Test System</el-header>
        <el-row>
          <el-col :span="40">Username:</el-col>
          <el-col :span="1">{{ username }}</el-col>
          <el-button type="primary" size = "mini" @click = "userLogout" round icon="el-icon-turn-off" v-loading="logoutLoading">logout</el-button>
        </el-row>
        <el-main>
          <!-- 仔细看，核心在这，这里是路由的出口-->
          <router-view></router-view>
        </el-main>
    </el-container>
  </el-container>
</template>
 
<script>
  export default {
    data() {
          return {
            username: "",
            logoutLoading : ""
          }
    },
    created() {
      const loginUserName = JSON.parse(localStorage.getItem('userName'))
      localStorage.removeItem('userName') // 使用后清除
      console.log(loginUserName['username'])
      this.username = loginUserName['username']
    },
    mounted() {
        this.sidebarItem = this.$route.name;
    },
    methods: {
        changeSidebar(path) {
            this.$router.push(path);
        },
        userLogout() {
          this.logoutLoading = true
          // alert('校验通过，提交表单！');
          // 真正请求编辑
          this.$axios.post('/api/userLogout/',
            // {id: Number(row.id)},
            
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            }
          ).then((response) => {
            // 成功请求
            // 处理前端显示
            console.log(response)
            if (response.data.code == 1) { // 表示登陆时出现未知错误
              alert('There is a unknown bug duiring logouting！')
              this.logoutLoading = false
            } else { // 表示登出成功
              this.logoutLoading = false
              alert('Logout successfully！')
              // let nextWebsite = response.data.website
              this.$router.push({
                path: '/',
              })// 跳转到指定网页，后端来决定
            }
          }).catch((error) => {
            console.log(error)
          })
      }
    }
    
  }
</script>
 
 
 <style scoped>
    .menu{
    height: 730px;
    background-color:  #0b6442;
    font-size: larger;
    }
    .el-header {
    background-color: #0b6442;
    color: #f8f5f5;
    font-size:30px;
    text-align: center;
    line-height: 60px;
  }
    .el-aside {
    color: #333;
    text-align: center;
    line-height: 900px;
  }
 
  .el-main {
    background-color: #d1dbd7;
    color: #333;
    /* text-align: center; */
    line-height: 160px;
    padding: 0px ! important;
  }
 </style>