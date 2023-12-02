<template>
  <el-config-provider namespace="ep">
    <RouterView />
  </el-config-provider>
</template>

<script setup lang="ts">
import { ref, watch, onUpdated, provide, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import type HomeViewVue from './views/HomeView.vue'
import * as echarts from "echarts"
import request from "@/utils/request"
// 全局注入echarts
provide('echarts', echarts)
provide('requests', request)

const router = useRouter()


</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  text-align: center;
  color: var(--ep-text-color-primary);
  height: 110%;
}

.element-plus-logo {
  width: 50%;
}
</style>
