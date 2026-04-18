<template>
  <div class="Index">
    <h1>{{ msg }}</h1>
    <el-form :model="loginForm" status-icon :rules="rules" ref="loginForm" label-width="30%" class="demo-loginForm">
      <el-form-item label="Username" prop="account">
        <el-input v-model="loginForm.account" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="Password" prop="pass">
        <el-input type="password" v-model="loginForm.pass" autocomplete="off" ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('loginForm')" v-loading="loginLoading">login</el-button>
        <el-button @click="goRegister()">sign up</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
 
<script>
export default {
  name: "Index",
  data() {
    return {
      msg: "Welcome to my AI Test System！",
      loginLoading: false,
      loginForm: {
          account: '',
          pass: '',
        },
      rules: {
        // 用户名规则：必填 + 长度限制 8-10
        account: [
          { required: true, message: 'please enter your username', trigger: 'blur' },
          { min: 6, max: 10, message: 'the length should be between  6 and 10 chars', trigger: 'blur' }
        ],
        // 密码规则：必填 + 自定义正则（至少6位字母数字）
        pass: [
          { required: true, message: 'please enter your password', trigger: 'blur' },
          { 
            pattern: /^[a-zA-Z0-9]{6,}$/, 
            message: 'the password should contain 6 numbers or letters at least', 
            trigger: 'blur' 
          }
        ]
      }
    };
  },
  created() {
    //this.resetForm()
  },
  activated() {
    console.log('Index activated')
},
  mounted() {
    console.log('Index mounted')
    console.log(this.$el.innerHTML)
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loginLoading = true
          // alert('校验通过，提交表单！');
          // 真正请求编辑
          this.$axios.post('/api/userLogin/',
            // {id: Number(row.id)},
            this.$qs.stringify({
              username: this.loginForm.account,
              password: this.loginForm.pass
            }),
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
              alert('There is a unknown bug duiring logining！')
              this.loginLoading = false
            }else if (response.data.code == 2) {// 表示账号或密码错误
              alert('Your username or password is not correct！')
              this.loginLoading = false
            } 
            else { // 表示登陆成功
              this.loginLoading = false
              alert('Login successfully！')
              // let nextWebsite = response.data.website
              localStorage.setItem('userName', JSON.stringify({ username: response.data.username}))
              this.$router.push({
                path: '/Home',
              })// 跳转到指定网页，后端来决定
            }
          }).catch((error) => {
            console.log(error)
          })
        } else {
          console.log('校验失败，阻止提交');
          return false;
        }
      });
    },
    resetForm() {
      this.loginForm.account = ''
      this.loginForm.pass = ''
    },
    goRegister() {
      this.$router.push('/functions/Registration')// 跳转到注册网页
    },
    enterSystem() {
      this.$router.push('/Home')// 跳转到注册网页
    }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.Index {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 从上方开始布局 */
  min-height: 100vh;
  padding-top: 20px; /* 整体往下留空，不会太顶 */
  background-color: #f9f9f9;
}

h1 {
  margin-bottom: 30px;
  font-size: 28px;
  color: #2c3e50;
}

.demo-loginForm {
  width: 400px;
  padding: 30px 40px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.el-form-item {
  margin-bottom: 20px;
}

/* 调整按钮行：横向并排 */
.el-form-item:last-child {
  display: flex;
  justify-content: space-between;
}

.el-button {
  flex: 1; /* 两个按钮等宽 */
  min-width: 120px;
  height: 38px;
  font-size: 14px;
}

/* 给两个按钮中间加点间隔 */
.el-button + .el-button {
  margin-left: 15px;
}


</style>
