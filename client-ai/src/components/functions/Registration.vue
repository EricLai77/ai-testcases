<template>
  <div class="registration">
    <h1>{{ msg }}</h1>
    <el-form :model="registrationForm" status-icon :rules="rules" ref="registrationForm" label-width="30%" class="demo-registrationForm">
      <el-form-item label="账号" prop="account">
        <el-input v-model="registrationForm.account" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="registrationForm.pass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="密码确认" prop="passCheck">
        <el-input type="password" v-model="registrationForm.passCheck" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registrationForm.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="signUp('registrationForm')">sign up</el-button>
        <router-link to="/">return Home</router-link>
      </el-form-item>
    </el-form>
  </div>
</template>
 
<script>
export default {
  name: 'Registration',
  data() {
    var validatePass2 = (rule, value, callback) => {
        if (value === '') {
            callback(new Error('请再次输入密码'));
        } else if (value !== this.registrationForm.pass) {
            callback(new Error('两次输入密码不一致!'));
        } else {
            callback();
        }
    };
    var validateEmail = (rule, value, callback) => {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!value) {
        callback(new Error('请输入邮箱'));
      } else if (!emailRegex.test(value)) {
        callback(new Error('邮箱格式不正确（示例：user@example.com）'));
      } else {
        callback();
      }
    };
    return {
      registrationForm: {
          account: '',
          pass: '',
          passCheck: '',
          email: ''
      },
      rules: {
        // 用户名规则：必填 + 长度限制 8-10
        account: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 6, max: 10, message: '长度在 6 到 10 个字符', trigger: 'blur' }
        ],
        // 密码规则：必填 + 自定义正则（至少6位字母数字）
        pass: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { 
            pattern: /^[a-zA-Z0-9]{6,}$/, 
            message: '密码需至少6位字母或数字', 
            trigger: 'blur' 
          }
        ],
        passCheck: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: validatePass2, trigger: 'blur' },
          { 
            pattern: /^[a-zA-Z0-9]{6,}$/, 
            message: '密码需至少6位字母或数字', 
            trigger: 'blur' 
          }
        ],
        email: [
          { required: true, message: '邮箱不能为空', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    signUp(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('校验通过');
          // 真正请求编辑
          this.$axios.post('/api/testRegister/',
            // {id: Number(row.id)},
            this.$qs.stringify({
              account: this.registrationForm.account,
              pass: this.registrationForm.pass,
              passCheck: this.registrationForm.passCheck,
              email: this.registrationForm.email
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
            if (response.data.code == 1) { // 表示该账号已注册
              alert('该账号已注册！')
            }else if (response.data.code == 2) {// 表示数据有问题
              alert('注册数据有问题！')
            }else if (response.data.code == 3) {// 注册过程有问题
              alert('注册过程有问题！')
            } 
            else { // 表示登陆成功
              alert('注册成功！')
              this.$router.push('/')// 跳转到指定网页，后端来决定
            }
          }).catch((error) => {
            console.log(error)
          })
        } else {
          console.log('校验失败');
          return false;
        }
      });
      
    }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
