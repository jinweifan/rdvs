<template>
  <div class="common-layout">
    <div id="screen">
      <el-container>
        <el-header style=" border-bottom: 1px solid #fff;">
          <BaseHeader />
        </el-header>
        <el-container>
          <el-row>
            <el-col :xs="bs" :sm="bs" :md="bs" :lg="bs" :xl="bs" v-if="isCollapse" :key="bs">
              <BaseSide />
            </el-col>
            <el-col :xs="br" :sm="br" :md="br" :lg="br" :xl="br" :key="br">
              <KeepAlive>
                <component :is="currentPage"></component>
              </KeepAlive>
            </el-col>
          </el-row>
          <el-footer style="margin-top: 50px;">
            <!-- Footer -->
            <div>
              <div>备案号：蜀ICP备2021023220号-1</div>
            </div>
          </el-footer>
        </el-container>
      </el-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouteListStore } from '@/stores/routerList'
import { ElMessage } from 'element-plus';
import { isNull, slice } from 'lodash';
import { computed, inject, onMounted, provide, ref, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Index from '@/views/main/IndexView.vue'
import Industry from '@/views/main/IndustryView.vue'
import Company from '@/views/main/company/CompanyView.vue'
import Recruitment from '@/views/main/RecruitmentView.vue'
import Me from '@/views/MeView.vue'
import CompanyDetail from '@/views/main/company/CompanyDetail.vue'
import CompanyCard from '@/views/main/company/CompanyCard.vue'
import { getAllCity } from '@/utils/api';
const store = useRouteListStore()
store.initRouterList()
const router = useRouter()
provide('router', router)
// 菜单栏是否展开
let isCollapse = ref(false)
let bs: any = ref(0)
let br: any = ref(24)
const allCity = ref({})
provide('allCity', allCity)
provide('isCollapse', isCollapse)


onMounted(() => {
  getAllCity().then(resp => {
    console.log('Home City')
    allCity.value = resp.city
  })
})


const route = useRoute()

let currentPage: any = computed(() => {
  console.log('path', route.path)
  if (route.name == 'industry')
    return Industry
  else if (route.name == 'recruitment')
    return Recruitment
  else if (route.path.indexOf('/company') != -1)
    return Company
  else if (route.path.indexOf('/me') != -1)
    return Me
  else if (route.name == 'index')
    return Index

})





watchEffect(() => {
  if (isCollapse.value == true) {
    const token = localStorage.getItem("access_token");
    !token && ElMessage.warning("请先登录！") && router.push('/login')
    bs.value = 2
    br.value = 22
  } else {
    bs.value = 0
    br.value = 24
  }
})

// 是否全屏展示
const isFullScreen = ref(false)
provide('isFullScreen', isFullScreen)

// 全屏
watch(isFullScreen, () => {
  if (isFullScreen.value) {
    if (document.fullscreenEnabled) {
      let screenElemnt = document.getElementById('screen')
      if (screenElemnt)
        screenElemnt.requestFullscreen()
    } else {
      console.log('无法进入全屏')
    }
  } else {
    if (document.fullscreenElement) {
      console.log("处于全屏可以退出全屏");
      document.exitFullscreen();
    } else {
      console.log("未处于全屏");
    }
  }

})


</script>

<style scoped></style>