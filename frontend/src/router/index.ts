import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 公共路由
const publicRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Login.vue'),
    meta: { title: '登录', public: true }
  }
]

// 需认证的路由
const protectedRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/Dashboard.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/purchase',
    name: 'Purchase',
    component: () => import('@/views/purchase/PurchaseList.vue'),
    meta: { title: '采购管理' }
  },
  {
    path: '/purchase/new',
    name: 'PurchaseNew',
    component: () => import('@/views/purchase/PurchaseNew.vue'),
    meta: { title: '新建采购' }
  },
  {
    path: '/purchase/compare/:id?',
    name: 'PurchaseCompare',
    component: () => import('@/views/purchase/PurchaseCompare.vue'),
    meta: { title: '比价结果' }
  },
  {
    path: '/purchase/confirm/:id',
    name: 'PurchaseConfirm',
    component: () => import('@/views/purchase/PurchaseConfirm.vue'),
    meta: { title: '确认申请' }
  },
  {
    path: '/purchase/:id',
    name: 'PurchaseDetail',
    component: () => import('@/views/purchase/PurchaseDetail.vue'),
    meta: { title: '采购详情' }
  },
  {
    path: '/approval',
    name: 'Approval',
    component: () => import('@/views/approval/ApprovalList.vue'),
    meta: { title: '审批管理' }
  },
  {
    path: '/approval/:id',
    name: 'ApprovalDetail',
    component: () => import('@/views/approval/ApprovalDetail.vue'),
    meta: { title: '审批详情' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/settings/Settings.vue'),
    meta: { title: '个人设置' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: [...publicRoutes, ...protectedRoutes]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.public) {
    next()
  } else if (!token && to.path !== '/login') {
    next('/login')
  } else {
    next()
  }
})

export default router