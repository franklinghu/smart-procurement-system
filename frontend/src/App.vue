<template>
  <el-config-provider :locale="locale">
    <router-view />
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElConfigProvider } from 'element-plus'

const { locale } = useI18n()

// 根据用户设置或浏览器语言自动选择
const currentLocale = computed(() => locale.value || 'zh-CN')
</script>