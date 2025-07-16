import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Index from '@/components/functions/Index'
import ApiTest from '@/components/functions/AiApiTest/ApiTest'
import AppTest from '@/components/functions/AiAppTest/AppTest'
import Testcases from '@/components/functions/AiTestcases/Testcases'
import WebTest from '@/components/functions/AiWebTest/WebTest'
import Configer from '@/components/functions/Configer'
import Registration from '@/components/functions/Registration'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/functions/Registration',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/functions/Configer',
          name: 'Configer',
          component: Configer
        },
        {
          path: '/functions/AiApiTest/ApiTest',
          name: 'ApiTest',
          component: ApiTest
        },
        {
          path: '/functions/AiAppTest/AppTest',
          name: 'AppTest',
          component: AppTest
        },
        {
          path: '/functions/AiTestcases/Testcases',
          name: 'Testcases',
          component: Testcases
        },
        {
          path: '/functions/AiWebTest/WebTest',
          name: 'WebTest',
          component: WebTest
        }
      ]
    }
  ]
})
