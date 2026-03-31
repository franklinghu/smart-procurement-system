<template>
  <div class="purchase-confirm">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
          <span>确认申请</span>
        </div>
      </template>

      <el-steps :active="2" finish-status="success" align-center>
        <el-step title="填写采购信息" />
        <el-step title="比价选择" />
        <el-step title="确认提交" />
      </el-steps>

      <el-divider />

      <!-- 确认信息 -->
      <el-descriptions title="采购信息确认" :column="2" border>
        <el-descriptions-item label="订单号">PO-2026-0315-001</el-descriptions-item>
        <el-descriptions-item label="采购标题">办公设备采购</el-descriptions-item>
        <el-descriptions-item label="选择供应商">得力集团</el-descriptions-item>
        <el-descriptions-item label="交货期">3天</el-descriptions-item>
        <el-descriptions-item label="总价">
          <span class="amount">¥2,850</span>
        </el-descriptions-item>
        <el-descriptions-item label="折扣">9.5折</el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <!-- 审批人选择 -->
      <div class="approver-section">
        <h3>选择审批人</h3>
        <el-radio-group v-model="selectedApprover">
          <el-radio value="manager">部门经理 - 张经理</el-radio>
          <el-radio value="director">采购总监 - 李总监</el-radio>
          <el-radio value="cfo">财务总监 - 王总监</el-radio>
        </el-radio-group>
      </div>

      <div class="actions">
        <el-button type="primary" size="large" @click="handleSubmit">提交审批</el-button>
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
const selectedApprover = ref('manager')

const handleSubmit = () => {
  ElMessage.success('提交成功，等待审批')
  router.push('/purchase')
}

const handleBack = () => router.back()
</script>

<style scoped>
.purchase-confirm {
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
  font-size: 18px;
}

.approver-section {
  margin: 24px 0;
}

.approver-section h3 {
  margin-bottom: 16px;
}

.approver-section .el-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.actions {
  margin-top: 32px;
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>