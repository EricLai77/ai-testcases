// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import axios from 'axios'
// import CryptoJS from 'crypto-js'
import qs from 'qs'// axios 已内置，无需单独安装
import dayjs from 'dayjs'
import Cookies from 'js-cookie';

axios.defaults.withCredentials = true // 全局生效

Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.prototype.$qs = qs
Vue.prototype.$dayjs = dayjs
Vue.prototype.$Cookies = Cookies

Vue.use(ElementUI);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})



// 响应拦截
axios.interceptors.response.use(response => {
  console.log('响应拦截')
  //console.log(response.data.encrypted)
  //const bytes = CryptoJS.AES.decrypt(response.data.encrypted, keyJiami)
  // response.data = JSON.parse(bytes.toString(CryptoJS.enc.Utf8))
  //console.log(response.data)
  return response
}, error =>{
  const{status} = error.response
  if (status === 401){
    router.push('/Home')
  }
  return Promise.reject(error)
})
