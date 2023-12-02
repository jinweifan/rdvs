<template>
  <el-row class="row-bg" justify="space-between">
    <el-col :span="6" style="flex:none">
      <el-image @click="router.push('/')" style="width: 60px; height: 60px; cursor: pointer;"
        :src="isDark ? '/logo.png' : '/logo-white.png'" />
    </el-col>
    <el-col :span="8">
      <div style="height: 100%;line-height: 3.75rem">
        <h1>职&nbsp;聘&nbsp;数&nbsp;据&nbsp;可&nbsp;视&nbsp;化平&nbsp;台</h1>
      </div>
    </el-col>
    <el-col :span="6" style="flex:none">

      <button @click="() => $router.push('me')" class="border-none  bg-transparent cursor-pointer icon"
        style="height: var(--ep-menu-item-height);">
        <el-icon>
          <User />
        </el-icon>
      </button>

      <button @click="isCollapse = !isCollapse" class="border-none  bg-transparent cursor-pointer icon"
        style="height: var(--ep-menu-item-height);">
        <el-icon>
          <icon-menu />
        </el-icon>
      </button>

      <button @click="ClickDark" class="border-none  bg-transparent cursor-pointer icon"
        style="height: var(--ep-menu-item-height);">
        <i inline-flex i="dark:ep-moon ep-sunny" />
      </button>

      <button @click="toggleFullScreen" class="border-none  bg-transparent cursor-pointer icon"
        style="height: var(--ep-menu-item-height);">
        <el-icon>
          <FullScreen />
        </el-icon>
      </button>


      <button @click="logout" class="border-none  bg-transparent cursor-pointer icon"
        style="height: var(--ep-menu-item-height);">
        <el-icon>
          <SwitchButton />
        </el-icon>
      </button>

    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  Menu as IconMenu,
} from '@element-plus/icons-vue'
import { inject, onMounted, ref } from 'vue';
import { toggleDark } from '@/composables';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
const router = useRouter()
const isCollapse = inject('isCollapse', false)
// const isFullScreen = inject('isFullScreen', false) // 是否展开菜单栏
const isDark = ref(false) // 替换黑白Logo

const isFullScreen = ref(false);

const toggleFullScreen = () => {
  if (!isFullScreen.value) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
  isFullScreen.value = !isFullScreen.value;
};

// onMounted(() => {
//   document.documentElement.requestFullscreen();
//   isFullScreen.value = true;
// });


// 切换主题
function ClickDark() {
  isDark.value = !isDark.value

  toggleDark()
}

function logout() {
  // localStorage.removeItem('token')
  localStorage.clear()
  ElMessage({
    message: '退出登录~~~',
    type: 'success'
  });
  router.push('/login')
}
</script>

<style scoped>
.icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: .625rem;
}
</style>
