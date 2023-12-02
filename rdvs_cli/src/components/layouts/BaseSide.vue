<template>
  <el-menu default-active="1" class="el-menu-vertical-demo" :collapse="!isCollapse" @open="handleOpen"
    @close="handleClose" @select="handleSelect" router>

    <el-menu-item v-for="(item, index) in routes" :index="item.path">
      <el-icon>
        <component :is="item.icon" />
      </el-icon>
      <template #title> {{ item.name }}</template>
    </el-menu-item>

  </el-menu>
</template>

<script lang="ts" setup>
import { inject, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';


// 菜单栏
const isCollapse = inject('isCollapse', false)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log('展开')
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  // console.log(key, keyPath)
}

// 配置动态路由展示菜单
const routes = [
  { path: '/', name: '首页', component: () => import('@/views/HomeView.vue'), icon: `Location`, redirect: '/' },
  { path: '/industry', name: '行业分析', component: () => import('@/views/main/IndustryView.vue'), icon: `Menu`, redirect: '/industry' },
  { path: '/company', name: '企业分析', component: () => import('@/views/main/company/CompanyView.vue'), icon: `Document`, redirect: '/company' },
  { path: '/recruitment', name: '招聘信息', component: () => import('@/views/main/RecruitmentView.vue'), icon: `Setting`, redirect: '/recruitment' },
]


const router = useRouter()
const handleSelect = (path: string, keyPath: string[], routeResult: any): void => {
  router.push(path)
  // router.
}


</script>

<style scoped>
/*.el-menu-vertical-demo:not(.el-menu--collapse) {*/
/*  width: 200px;*/
/*  min-height: 400px;*/
/*}*/
</style>
