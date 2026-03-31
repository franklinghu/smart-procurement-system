<template>
  <div class="supplier-list">
    <el-card>
      <template #header>
        <div class="table-header">
          <span>供应商管理</span>
          <el-button type="primary" :icon="Plus" @click="handleAdd">新增供应商</el-button>
        </div>
      </template>

      <el-table :data="tableData" stripe>
        <el-table-column prop="code" label="编码" width="100" />
        <el-table-column prop="name" label="供应商名称" min-width="200" />
        <el-table-column prop="contact" label="联系人" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="rating" label="评分" width="100">
          <template #default="{ row }">
            <el-rate v-model="row.rating" disabled text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link @click="handleView(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const tableData = ref([
  { id: '1', code: 'SUP001', name: '得力集团', contact: '张经理', phone: '13800138001', rating: 4.5, status: 'active' },
  { id: '2', code: 'SUP002', name: '齐心文具', contact: '李经理', phone: '13800138002', rating: 4.2, status: 'active' },
  { id: '3', code: 'SUP003', name: '晨光科技', contact: '王经理', phone: '13800138003', rating: 4.8, status: 'active' },
  { id: '4', code: 'SUP004', name: '史泰博', contact: '赵经理', phone: '13800138004', rating: 4.0, status: 'inactive' },
])

const handleAdd = () => ElMessage.info('新增供应商功能开发中')
const handleEdit = (row: any) => ElMessage.info(`编辑 ${row.name}`)
const handleView = (row: any) => ElMessage.info(`查看 ${row.name}`)
</script>

<style scoped>
.supplier-list {
  padding: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>