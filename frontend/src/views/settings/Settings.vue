<template>
  <div class="settings">
    <el-card>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="个人设置" name="profile">
          <el-form label-width="100px" style="max-width: 500px">
            <el-form-item label="用户名">
              <el-input v-model="profile.username" />
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="profile.name" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profile.email" />
            </el-form-item>
            <el-form-item label="手机">
              <el-input v-model="profile.phone" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="修改密码" name="password">
          <el-form label-width="100px" style="max-width: 500px">
            <el-form-item label="当前密码">
              <el-input v-model="password.old" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="password.new" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认密码">
              <el-input v-model="password.confirm" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="系统设置" name="system">
          <el-form label-width="100px" style="max-width: 500px">
            <el-form-item label="语言">
              <el-select v-model="system.language">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            <el-form-item label="时区">
              <el-select v-model="system.timezone">
                <el-option label="中国标准时间 (UTC+8)" value="Asia/Shanghai" />
              </el-select>
            </el-form-item>
            <el-form-item label="主题">
              <el-radio-group v-model="system.theme">
                <el-radio value="light">浅色</el-radio>
                <el-radio value="dark">深色</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveSystem">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('profile')

const profile = reactive({
  username: 'admin',
  name: '管理员',
  email: 'admin@example.com',
  phone: '13800138000'
})

const password = reactive({
  old: '',
  new: '',
  confirm: ''
})

const system = reactive({
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  theme: 'light'
})

const handleSaveProfile = () => ElMessage.success('个人设置已保存')
const handleChangePassword = () => ElMessage.success('密码已修改')
const handleSaveSystem = () => ElMessage.success('系统设置已保存')
</script>

<style scoped>
.settings {
  padding: 20px;
}
</style>