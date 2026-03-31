<template>
  <div class="approval-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <span>审批管理</span>
        </div>
      </template>

      <el-table :data="tableData" stripe>
        <el-table-column prop="no" label="订单号" width="180" />
        <el-table-column prop="title" label="采购标题" min-width="200" />
        <el-table-column prop="amount" label="金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount">¥{{ row.amount.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType[row.status]">{{ statusText[row.status] }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applicant" label="申请人" width="100" />
        <el-table-column prop="date" label="申请时间" width="160" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">审批</el-button>
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const statusType: Record<string, string> = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger'
}

const statusText: Record<string, string> = {
  pending: '待审批',
  approved: '已通过',
  rejected: '已拒绝'
}

const tableData = ref([
  { id: '1', no: 'PO-2026-0315-001', title: '办公设备采购', amount: 5680, status: 'pending', applicant: '张三', date: '2026-03-31 10:30' },
  { id: '2', no: 'PO-2026-0314-008', title: '劳保用品采购', amount: 12350, status: 'pending', applicant: '李四', date: '2026-03-30 15:20' },
  { id: '3', no: 'PO-2026-0313-012', title: '维修备件采购', amount: 8920, status: 'approved', applicant: '王五', date: '2026-03-29 09:15' },
])

const handleView = (row: any) => {
  router.push(`/approval/${row.id}`)
}
</script>

<style scoped>
.approval-list {
  padding: 20px;
}

.table-header {
  font-size: 16px;
  font-weight: 500;
}

.amount {
  color: #f56c6c;
  font-weight: 500;
}
</style>