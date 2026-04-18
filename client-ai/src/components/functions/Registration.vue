<template>
  <div class="registration">
    <h1>{{ msg }}</h1>
    <el-form :model="registrationForm" status-icon :rules="rules" ref="registrationForm" label-width="30%" class="demo-registrationForm">
      <el-form-item label="username" prop="username">
        <el-input v-model="registrationForm.username" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="password" prop="password">
        <el-input type="password" v-model="registrationForm.password" autocomplete="off" show-password></el-input>
      </el-form-item>
      <el-form-item label="password confirm" prop="password2">
        <el-input type="password" v-model="registrationForm.password2" autocomplete="off" show-password></el-input>
      </el-form-item>
      <el-form-item label="email" prop="email">
        <el-input v-model="registrationForm.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="first name" prop="first_name">
        <el-input v-model="registrationForm.first_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="last name" prop="last_name">
        <el-input v-model="registrationForm.last_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="signUp('registrationForm')" :disabled="loading">{{ loading ? 'loading...' : 'sign up' }}</el-button>
        <router-link to="/">home</router-link>
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
            callback(new Error('please enter your password'));
        } else if (value !== this.registrationForm.password) {
            callback(new Error('two password do not match!'));
        } else {
            callback();
        }
    };
    var validateEmail = (rule, value, callback) => {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!value) {
        callback(new Error('please enter your email'));
      } else if (!emailRegex.test(value)) {
        callback(new Error('the format of email is not correct（for example：user@example.com）'));
      } else {
        callback();
      }
    };
    return {
      loading: false,
      registrationForm: {
        username: '',
        password: '',
        password2: '',
        email: '',
        first_name: '',
        last_name: ''
      },
      rules: {
        // 用户名规则：必填 + 长度限制 8-10
        username: [
          { required: true, message: 'please enter your username', trigger: 'blur' },
          { min: 6, max: 10, message: 'the length should be between  6 and 10 chars', trigger: 'blur' }
        ],
        // 密码规则：必填 + 自定义正则（至少6位字母数字）
        password: [
          { required: true, message: 'please enter your password', trigger: 'blur' },
          { 
            pattern: /^[a-zA-Z0-9]{6,}$/, 
            message: 'the password should contain 6 numbers or letters at least', 
            trigger: 'blur' 
          }
        ],
        password2: [
          { required: true, message: 'please enter your password', trigger: 'blur' },
          { validator: validatePass2, trigger: 'blur' },
          { 
            pattern: /^[a-zA-Z0-9]{6,}$/, 
            message: 'the password should contain 6 numbers or letters at least', 
            trigger: 'blur' 
          }
        ],
        email: [
          { required: true, message: 'the email is required', trigger: 'blur' },
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
          this.loading = true
          // 真正请求编辑
          this.$axios.post('/api/register/',
            // {id: Number(row.id)},
            this.$qs.stringify(this.registrationForm),
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
              alert('该注册过程有问题！')
              this.loading = false
            }
            else { // 表示登陆成功
              alert('注册成功！')
              // 清空表单
              this.registrationForm = {
                username: '',
                email: '',
                password: '',
                password2: '',
                first_name: '',
                last_name: ''
              }
              this.loading = false
              this.$router.push({
                path: '/',
              })// 跳转到指定网页，后端来决定
            }
          }).catch((error) => {
            console.log(error)
            this.loading = false
          })
        } else {
          console.log('校验失败');
          this.loading = false
          return false;
        }
      });
      
    }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.registration {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
}

.demo-registrationForm {
  width: 450px; /* 控制表单宽度 */
  background: #fff;
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.form-actions .el-button {
  flex: 1;
  min-width: 120px;
}

.form-actions .el-button + .el-button {
  margin-left: 15px;
}

</style>
