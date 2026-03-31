<template>
  <div class="approval-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
          <span>审批详情</span>
        </div>
      </template>

      <el-descriptions title="采购信息" :column="2" border>
        <el-descriptions-item label="订单号">PO-2026-0315-001</el-descriptions-item>
        <el-descriptions-item label="采购标题">办公设备采购</el-descriptions-item>
        <el-descriptions-item label="申请人">张三</el-descriptions-item>
        <el-descriptions-item label="申请时间">2026-03-31 10:30</el-descriptions-item>
        <el-descriptions-item label="采购金额">
          <span class="amount">¥5,680</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag type="warning">待审批</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider>商品明细</el-divider>
      <el-table :data="goodsList" border stripe>
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column prop="price" label="单价" width="100">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
      </el-table>

      <el-divider>审批意见</el-divider>
      <el-input v-model="opinion" type="textarea" rows="4" placeholder="请输入审批意见" />

      <div class="actions">
        <el-button type="primary" size="large" @click="handleApprove">通过</el-button>
        <el-button type="danger" size="large" @click="handleReject">拒绝</el-button>
        <el-button size="large" @click="handleBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const opinion = ref('')
const goodsList = ref([
  { name: 'A4纸', quantity: 50, price: 25 },
  { name: '中性笔', quantity: 100, price: 2 },
])

const handleApprove = () => {
  ElMessage.success('审批通过')
  router.push('/approval')
}

const handleReject = () => {
  ElMessage.error('已拒绝')
  router.push('/approval')
}

const handleBack = () => router.back()
</script>

<style scoped>
.approval-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.amount {
  color: #f56c6c;
  font-weight: 600;
}

.actions {
  margin-top: 24px;
  display: flex;
  gap: 12px;
  justify-content: center;
}
</style>