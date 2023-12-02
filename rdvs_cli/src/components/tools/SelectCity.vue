<template>
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="热门城市" name="hotCity">
            <CityGroup :data="allCity.hotCityList" />
        </el-tab-pane>

        <el-tab-pane v-for="i in  allCity.cityGroup" :label="i.firstChar" :name="i.firstChar">
            <CityGroup :data="i.cityList" />
        </el-tab-pane>
    </el-tabs>
</template>
<script lang="ts" setup>
import { inject, ref, watchEffect } from 'vue'
import type { TabsPaneContext } from 'element-plus'

const activeName = ref('hotCity')
const allCity: any = inject('allCity')


const handleClick = (tab: TabsPaneContext, event: Event) => {
    console.log(tab, event)
}


watchEffect(() => {
    console.log('allCity', allCity.value)
})
</script>
<style>
.demo-tabs {
    height: 25rem;
   
}

</style>
  