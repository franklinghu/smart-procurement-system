<template>
  <div class="dashboard">
    <!-- 顶部导航 -->
    <div class="dashboard-header">
      <div class="header-left">
        <h2 class="page-title">控制台</h2>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <span class="username">管理员</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="settings">系统设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon pending">
            <el-icon :size="32"><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.pendingApproval }}</div>
            <div class="stat-label">待审批</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon processing">
            <el-icon :size="32"><ShoppingCart /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.processing }}</div>
            <div class="stat-label">采购中</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon suppliers">
            <el-icon :size="32"><OfficeBuilding /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.suppliers }}</div>
            <div class="stat-label">供应商</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon goods">
            <el-icon :size="32"><Box /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.goods }}</div>
            <div class="stat-label">商品数</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 内容区域 -->
    <el-row :gutter="20">
      <!-- 待办事项 -->
      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>📋 待办事项</span>
              <el-button type="primary" link>查看全部</el-button>
            </div>
          </template>
          <div class="todo-list">
            <div v-for="item in todos" :key="item.id" class="todo-item">
              <el-checkbox v-model="item.done" />
              <span :class="{ done: item.done }">{{ item.title }}</span>
              <el-tag :type="item.priorityType" size="small">{{ item.priority }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 快捷操作 -->
      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>⚡ 快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <div class="action-item" @click="router.push('/purchase/new')">
              <div class="action-icon">
                <el-icon :size="28"><Plus /></el-icon>
              </div>
              <span>新建采购</span>
            </div>
            <div class="action-item" @click="router.push('/purchase')">
              <div class="action-icon">
                <el-icon :size="28"><List /></el-icon>
              </div>
              <span>采购订单</span>
            </div>
            <div class="action-item" @click="router.push('/approval')">
              <div class="action-icon">
                <el-icon :size="28"><Check /></el-icon>
              </div>
              <span>审批管理</span>
            </div>
            <div class="action-item">
              <div class="action-icon">
                <el-icon :size="28"><Setting /></el-icon>
              </div>
              <span>系统设置</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最近采购 -->
    <el-row :gutter="20" class="recent-section">
      <el-col :span="24">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>📦 最近采购</span>
              <el-button type="primary" link @click="router.push('/purchase')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentPurchases" style="width: 100%">
            <el-table-column prop="no" label="订单号" width="180" />
            <el-table-column prop="title" label="采购标题" />
            <el-table-column prop="amount" label="金额" width="120">
              <template #default="{ row }">
                ¥{{ row.amount.toLocaleString() }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.statusType">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="创建时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link @click="router.push(`/purchase/${row.id}`)">
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowDown,
  Document,
  ShoppingCart,
  OfficeBuilding,
  Box,
  Plus,
  List,
  Check,
  Setting
} from '@element-plus/icons-vue'

const router = useRouter()

const stats = reactive({
  pendingApproval: 5,
  processing: 12,
  suppliers: 48,
  goods: 1256
})

const todos = ref([
  { id: 1, title: '审批 办公用品采购申请（¥5,680）', priority: '紧急', priorityType: 'danger', done: false },
  { id: 2, title: '确认 劳保用品订单（¥12,350）', priority: '高', priorityType: 'warning', done: false },
  { id: 3, title: '比价 工业润滑油采购', priority: '中', priorityType: 'info', done: false },
  { id: 4, title: '审核 供应商准入申请', priority: '低', priorityType: 'info', done: true }
])

const recentPurchases = ref([
  { id: '1', no: 'PO-2026-0315-001', title: '办公设备采购', amount: 5680, status: '待审批', statusType: 'warning', date: '2026-03-31 10:30' },
  { id: '2', no: 'PO-2026-0314-008', title: '劳保用品采购', amount: 12350, status: '采购中', statusType: 'primary', date: '2026-03-30 15:20' },
  { id: '3', no: 'PO-2026-0313-012', title: '维修备件采购', amount: 8920, status: '已完成', statusType: 'success', date: '2026-03-29 09:15' }
])

const handleCommand = (command: string) => {
  if (command === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    ElMessage.success('已退出登录')
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/settings')
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: #fff;
  padding: 16px 24px;
  border-radius: 8px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  color: #606266;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon.pending { background: #fef0f0; color: #f56c6c; }
.stat-icon.processing { background: #ecf5ff; color: #409eff; }
.stat-icon.suppliers { background: #f0f9eb; color: #67c23a; }
.stat-icon.goods { background: #fdf6ec; color: #e6a23c; }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.content-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.todo-item .done {
  text-decoration: line-through;
  color: #c0c4cc;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background: #f5f7fa;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: #ecf5ff;
  color: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.recent-section {
  margin-top: 20px;
}
</style>