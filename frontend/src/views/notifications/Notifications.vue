<template>
  <div class="notifications">
    <el-card>
      <template #header>
        <div class="header">
          <span>消息中心</span>
          <el-button type="primary" link @click="handleMarkAllRead">全部标记已读</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="全部消息" name="all">
          <div class="notification-list">
            <div 
              v-for="item in notifications" 
              :key="item.id" 
              :class="['notification-item', { unread: !item.read }]"
              @click="handleClick(item)"
            >
              <div class="notification-icon">
                <el-icon :size="24">
                  <Bell v-if="item.type === 'approval_required'" />
                  <SuccessFilled v-else-if="item.type === 'approved'" />
                  <WarningFilled v-else-if="item.type === 'rejected'" />
                  <Message v-else />
                </el-icon>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ item.title }}</div>
                <div class="notification-text">{{ item.content }}</div>
                <div class="notification-time">{{ item.time }}</div>
              </div>
              <el-tag v-if="!item.read" type="danger" size="small">未读</el-tag>
            </div>
            
            <el-empty v-if="notifications.length === 0" description="暂无消息" />
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="未读消息" name="unread">
          <div class="notification-list">
            <div 
              v-for="item in unreadNotifications" 
              :key="item.id" 
              class="notification-item unread"
              @click="handleClick(item)"
            >
              <div class="notification-icon">
                <el-icon :size="24"><Bell /></el-icon>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ item.title }}</div>
                <div class="notification-text">{{ item.content }}</div>
                <div class="notification-time">{{ item.time }}</div>
              </div>
              <el-tag type="danger" size="small">未读</el-tag>
            </div>
            
            <el-empty v-if="unreadNotifications.length === 0" description="暂无未读消息" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Bell, SuccessFilled, WarningFilled, Message } from '@element-plus/icons-vue'

const activeTab = ref('all')

const notifications = ref([
  { id: '1', title: '审批提醒：办公设备采购', content: '您有一个采购申请需要审批，金额：¥5,680', type: 'approval_required', read: false, time: '2026-03-31 10:30' },
  { id: '2', title: '审批通过：劳保用品采购', content: '您的采购申请已通过审批', type: 'approved', read: false, time: '2026-03-30 15:20' },
  { id: '3', title: '审批驳回：清洁用品采购', content: '您的采购申请已被驳回，原因：预算不足', type: 'rejected', read: true, time: '2026-03-29 09:15' },
  { id: '4', title: '订单同步成功：维修备件采购', content: '采购订单已成功同步到ERP系统', type: 'order_synced', read: true, time: '2026-03-28 14:00' },
])

const unreadNotifications = computed(() => 
  notifications.value.filter(n => !n.read)
)

const handleClick = (item: any) => {
  if (!item.read) {
    item.read = true
    ElMessage.success('已标记为已读')
  }
}

const handleMarkAllRead = () => {
  notifications.value.forEach(n => n.read = true)
  ElMessage.success('已全部标记为已读')
}
</script>

<style scoped>
.notifications {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-list {
  display: flex;
  flex-direction: column;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.3s;
}

.notification-item:hover {
  background: #f5f7fa;
}

.notification-item.unread {
  background: #f0f9eb;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #ecf5ff;
  color: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.notification-text {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 12px;
  color: #909399;
}
</style>