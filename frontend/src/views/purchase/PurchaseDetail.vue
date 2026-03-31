<template>
  <div class="purchase-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
          <span>采购详情</span>
          <el-tag :type="statusType">待审批</el-tag>
        </div>
      </template>

      <!-- 基本信息 -->
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="订单号">PO-2026-0315-001</el-descriptions-item>
        <el-descriptions-item label="采购类型">办公用品</el-descriptions-item>
        <el-descriptions-item label="采购标题">办公设备采购</el-descriptions-item>
        <el-descriptions-item label="紧急程度">
          <el-tag type="warning">普通</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请人">张三</el-descriptions-item>
        <el-descriptions-item label="申请时间">2026-03-31 10:30</el-descriptions-item>
        <el-descriptions-item label="期望交付日期">2026-04-15</el-descriptions-item>
        <el-descriptions-item label="状态">待审批</el-descriptions-item>
      </el-descriptions>

      <!-- 商品明细 -->
      <el-divider>商品明细</el-divider>
      <el-table :data="goodsList" border stripe>
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="spec" label="规格型号" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column prop="price" label="单价" width="100">
          <template #default="{ row }">
            ¥{{ row.price.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="小计" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ (row.quantity * row.price).toLocaleString() }}</span>
          </template>
        </el-table-column>
      </el-table>

      <div class="total-summary">
        <span>商品总数：{{ totalQuantity }} 件</span>
        <span>预估总金额：<span class="amount">¥{{ totalAmount.toLocaleString() }}</span></span>
      </div>

      <!-- 审批流程 -->
      <el-divider>审批流程</el-divider>
      <el-timeline>
        <el-timeline-item timestamp="2026-03-31 10:30" placement="top">
          <el-card>
            <h4>提交申请</h4>
            <p>申请人：张三</p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item timestamp="待审批" placement="top" color="#E6A23C">
          <el-card>
            <h4>等待审批</h4>
            <p>审批人：部门经理</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>

      <!-- 操作按钮 -->
      <div class="actions">
        <el-button type="primary">通过</el-button>
        <el-button type="danger">拒绝</el-button>
        <el-button @click="handleBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const statusType = ref('warning')

const goodsList = ref([
  { name: 'A4纸', spec: '70g/㎡', unit: '包', quantity: 50, price: 25 },
  { name: '中性笔', spec: '0.5mm', unit: '支', quantity: 100, price: 2 },
  { name: '文件夹', spec: 'A4', unit: '个', quantity: 20, price: 15 },
  { name: '订书机', spec: '标准型', unit: '个', quantity: 5, price: 28 },
])

const totalQuantity = computed(() => goodsList.value.reduce((sum, item) => sum + item.quantity, 0))
const totalAmount = computed(() => goodsList.value.reduce((sum, item) => sum + item.quantity * item.price, 0))

const handleBack = () => router.back()
</script>

<style scoped>
.purchase-detail {
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

.total-summary {
  margin-top: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
  display: flex;
  justify-content: flex-end;
  gap: 32px;
  font-size: 14px;
}

.total-summary .amount {
  font-size: 18px;
}

.actions {
  margin-top: 24px;
  display: flex;
  gap: 12px;
}
</style>