<template>
  <div class="purchase-list">
    <!-- 顶部搜索栏 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable style="width: 160px" />
        </el-form-item>
        <el-form-item label="采购标题">
          <el-input v-model="searchForm.title" placeholder="请输入标题" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待审批" value="pending" />
            <el-option label="采购中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作栏 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <span>采购订单列表</span>
          <el-button type="primary" :icon="Plus" @click="handleCreate">新建采购</el-button>
        </div>
      </template>

      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="no" label="订单号" width="180" />
        <el-table-column prop="title" label="采购标题" min-width="200" />
        <el-table-column prop="type" label="采购类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
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
        <el-table-column prop="creator" label="申请人" width="100" />
        <el-table-column prop="date" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
            <el-button type="primary" link v-if="row.status === 'pending'" @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" link v-if="row.status === 'pending'" @click="handleCancel(row)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)

const searchForm = reactive({
  orderNo: '',
  title: '',
  status: '',
  dateRange: []
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 15
})

const statusType: Record<string, string> = {
  pending: 'warning',
  processing: 'primary',
  completed: 'success',
  cancelled: 'info'
}

const statusText: Record<string, string> = {
  pending: '待审批',
  processing: '采购中',
  completed: '已完成',
  cancelled: '已取消'
}

const tableData = ref([
  { id: '1', no: 'PO-2026-0315-001', title: '办公设备采购', type: '办公用品', amount: 5680, status: 'pending', creator: '张三', date: '2026-03-31 10:30' },
  { id: '2', no: 'PO-2026-0314-008', title: '劳保用品采购', type: '劳保用品', amount: 12350, status: 'processing', creator: '李四', date: '2026-03-30 15:20' },
  { id: '3', no: 'PO-2026-0313-012', title: '维修备件采购', type: '维修备件', amount: 8920, status: 'completed', creator: '王五', date: '2026-03-29 09:15' },
  { id: '4', no: 'PO-2026-0312-005', title: '清洁用品采购', type: '清洁用品', amount: 3200, status: 'cancelled', creator: '赵六', date: '2026-03-28 14:00' },
  { id: '5', no: 'PO-2026-0311-003', title: '五金工具采购', type: '五金工具', amount: 15680, status: 'completed', creator: '张三', date: '2026-03-27 11:30' },
])

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

const handleReset = () => {
  searchForm.orderNo = ''
  searchForm.title = ''
  searchForm.status = ''
  searchForm.dateRange = []
  handleSearch()
}

const handleCreate = () => {
  router.push('/purchase/new')
}

const handleView = (row: any) => {
  router.push(`/purchase/${row.id}`)
}

const handleEdit = (row: any) => {
  ElMessage.info('编辑功能开发中')
}

const handleCancel = (row: any) => {
  ElMessageBox.confirm('确定要取消该采购订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    row.status = 'cancelled'
    ElMessage.success('已取消')
  }).catch(() => {})
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  handleSearch()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  handleSearch()
}
</script>

<style scoped>
.purchase-list {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card :deep(.el-card__body) {
  padding: 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.amount {
  color: #f56c6c;
  font-weight: 500;
}

.pagination {
  padding: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>