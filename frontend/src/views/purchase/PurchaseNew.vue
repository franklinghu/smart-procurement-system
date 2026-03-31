<template>
  <div class="purchase-new">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
          <span>新建采购申请</span>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <!-- 基本信息 -->
        <el-divider>基本信息</el-divider>
        
        <el-form-item label="采购标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入采购标题" style="width: 400px" />
        </el-form-item>
        
        <el-form-item label="采购类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择采购类型" style="width: 200px">
            <el-option label="办公用品" value="办公用品" />
            <el-option label="劳保用品" value="劳保用品" />
            <el-option label="维修备件" value="维修备件" />
            <el-option label="清洁用品" value="清洁用品" />
            <el-option label="五金工具" value="五金工具" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="紧急程度" prop="urgency">
          <el-radio-group v-model="form.urgency">
            <el-radio value="low">普通</el-radio>
            <el-radio value="medium">紧急</el-radio>
            <el-radio value="high">加急</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="期望交付日期" prop="deliveryDate">
          <el-date-picker
            v-model="form.deliveryDate"
            type="date"
            placeholder="选择期望交付日期"
            style="width: 200px"
            :disabled-date="disabledDate"
          />
        </el-form-item>
        
        <el-form-item label="备注说明">
          <el-input v-model="form.remark" type="textarea" rows="3" placeholder="请输入备注说明" style="width: 400px" />
        </el-form-item>

        <!-- 商品明细 -->
        <el-divider>商品明细</el-divider>
        
        <div class="goods-table">
          <el-table :data="form.goods" border stripe>
            <el-table-column label="商品名称" min-width="200">
              <template #default="{ row, $index }">
                <el-form-item :prop="`goods.${$index}.name`" :rules="{ required: true, message: '请输入商品名称', trigger: 'blur' }" style="margin: 0">
                  <el-input v-model="row.name" placeholder="商品名称" />
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="规格型号" width="150">
              <template #default="{ row }">
                <el-input v-model="row.spec" placeholder="规格型号" />
              </template>
            </el-table-column>
            <el-table-column label="单位" width="80">
              <template #default="{ row }">
                <el-input v-model="row.unit" placeholder="个" />
              </template>
            </el-table-column>
            <el-table-column label="数量" width="100">
              <template #default="{ row, $index }">
                <el-form-item :prop="`goods.${$index}.quantity`" :rules="{ required: true, message: '请输入数量', trigger: 'blur' }" style="margin: 0">
                  <el-input-number v-model="row.quantity" :min="1" :max="99999" controls-position="right" style="width: 100%" />
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="预估单价" width="120">
              <template #default="{ row, $index }">
                <el-form-item :prop="`goods.${$index}.price`" :rules="{ required: true, message: '请输入单价', trigger: 'blur' }" style="margin: 0">
                  <el-input-number v-model="row.price" :min="0" :precision="2" controls-position="right" style="width: 100%" />
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="{ row }">
                <span class="subtotal">¥{{ (row.quantity * row.price).toLocaleString() }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80" align="center">
              <template #default="{ $index }">
                <el-button type="danger" :icon="Delete" circle @click="handleRemoveGoods($index)" :disabled="form.goods.length === 1" />
              </template>
            </el-table-column>
          </el-table>
          
          <el-button type="primary" :icon="Plus" style="margin-top: 16px" @click="handleAddGoods">添加商品</el-button>
        </div>
        
        <!-- 费用汇总 -->
        <div class="summary">
          <div class="summary-item">
            <span>商品总数：</span>
            <span class="value">{{ totalQuantity }} 件</span>
          </div>
          <div class="summary-item">
            <span>预估总金额：</span>
            <span class="value amount">¥{{ totalAmount.toLocaleString() }}</span>
          </div>
        </div>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit('compare')">提交并比价</el-button>
          <el-button size="large" @click="handleSubmit('draft')">保存草稿</el-button>
          <el-button @click="handleBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Plus, Delete } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const formRef = ref<FormInstance>()

const form = reactive({
  title: '',
  type: '',
  urgency: 'low',
  deliveryDate: '',
  remark: '',
  goods: [
    { name: '', spec: '', unit: '个', quantity: 1, price: 0 }
  ]
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入采购标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择采购类型', trigger: 'change' }],
  deliveryDate: [{ required: true, message: '请选择期望交付日期', trigger: 'change' }]
}

const totalQuantity = computed(() => {
  return form.goods.reduce((sum, item) => sum + item.quantity, 0)
})

const totalAmount = computed(() => {
  return form.goods.reduce((sum, item) => sum + item.quantity * item.price, 0)
})

const disabledDate = (time: Date) => {
  return time.getTime() < Date.now() - 8.64e7
}

const handleAddGoods = () => {
  form.goods.push({ name: '', spec: '', unit: '个', quantity: 1, price: 0 })
}

const handleRemoveGoods = (index: number) => {
  form.goods.splice(index, 1)
}

const handleSubmit = async (type: string) => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    if (type === 'compare') {
      ElMessage.success('提交成功，进入比价流程')
      router.push('/purchase/compare')
    } else {
      ElMessage.success('已保存为草稿')
      router.push('/purchase')
    }
  })
}

const handleBack = () => {
  router.back()
}
</script>

<style scoped>
.purchase-new {
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.goods-table {
  margin: 20px 0;
}

.subtotal {
  font-weight: 500;
  color: #f56c6c;
}

.summary {
  margin-top: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
  display: flex;
  justify-content: flex-end;
  gap: 32px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-item .value {
  font-size: 16px;
  font-weight: 600;
}

.summary-item .amount {
  color: #f56c6c;
  font-size: 20px;
}
</style>