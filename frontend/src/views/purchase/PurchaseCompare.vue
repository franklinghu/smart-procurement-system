<template>
  <div class="purchase-compare">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
          <span>比价结果</span>
        </div>
      </template>

      <el-alert title="已为您找到 3 家供应商的商品报价" type="success" :closable="false" show-icon />

      <!-- 商品列表 -->
      <div class="goods-section">
        <h3>商品明细</h3>
        <el-table :data="goodsList" border stripe>
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="spec" label="规格型号" />
          <el-table-column prop="quantity" label="数量" width="80" />
        </el-table>
      </div>

      <!-- 供应商报价 -->
      <div class="compare-section">
        <h3>供应商报价对比</h3>
        <el-table :data="supplierPrices" border stripe>
          <el-table-column prop="supplier" label="供应商" width="150" />
          <el-table-column prop="delivery" label="交货期" width="100" />
          <el-table-column prop="total" label="总价" width="120">
            <template #default="{ row }">
              <span class="amount">¥{{ row.total.toLocaleString() }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="discount" label="折扣" width="80" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleSelect(row)">选择</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="actions">
        <el-button type="primary" size="large" @click="handleConfirm">确认报价并提交审批</el-button>
        <el-button size="large" @click="handleBack">取消</el-button>
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

const goodsList = ref([
  { name: 'A4纸', spec: '70g/㎡', quantity: 50 },
  { name: '中性笔', spec: '0.5mm', quantity: 100 },
])

const supplierPrices = ref([
  { id: 1, supplier: '得力集团', delivery: '3天', total: 2850, discount: '9.5折' },
  { id: 2, supplier: '齐心文具', delivery: '2天', total: 2920, discount: '无折扣' },
  { id: 3, supplier: '晨光科技', delivery: '5天', total: 2700, discount: '9折' },
])

const handleSelect = (row: any) => {
  ElMessage.success(`已选择 ${row.supplier}`)
}

const handleConfirm = () => {
  router.push('/purchase/confirm/1')
}

const handleBack = () => router.back()
</script>

<style scoped>
.purchase-compare {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.goods-section, .compare-section {
  margin-top: 24px;
}

.goods-section h3, .compare-section h3 {
  margin-bottom: 16px;
  color: #303133;
}

.amount {
  color: #f56c6c;
  font-weight: 600;
  font-size: 16px;
}

.actions {
  margin-top: 32px;
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>