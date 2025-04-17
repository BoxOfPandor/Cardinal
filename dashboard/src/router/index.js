import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ModuleDetails from '../views/ModuleDetails.vue'
import SystemHealth from '../views/SystemHealth.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/modules/:moduleName',
    name: 'ModuleDetails',
    component: ModuleDetails,
    props: true
  },
  {
    path: '/system/health',
    name: 'SystemHealth',
    component: SystemHealth
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router