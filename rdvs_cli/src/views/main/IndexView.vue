<template>
    <div>
        <el-row>
            <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                <ItemPanel>
                    <HotIndustry :hotIndustry="hotIndustry.slice(0, 7)" />
                </ItemPanel>
                <ItemPanel>
                    <SalaryRange :salary-data="salaryData" />
                </ItemPanel>
            </el-col>
            <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                <DataPanel :dataSize="dataSize" :addedDaySize="addedDaySize" />
                <MapChart :hotCity="hotCity" />

            </el-col>
            <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                <ItemPanel>
                    <EB :experienceData="experienceData" />
                </ItemPanel>
                <ItemPanel>
                    <HotCity :hotCity="hotCity" />
                </ItemPanel>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive, ref, watch, watchEffect } from "vue";
import 'echarts/extension-src/bmap/bmap';
import { getDataAddedDay, getDataSize, getExperience, getHotCity, getHotIndustry, getSalaryRange } from "@/utils/api";


const echarts: any = inject('echarts')
let dataSize: any = ref(0)
let addedDaySize: any = ref(0)
let salaryData: any = ref({})
let experienceData: any = ref([])
let hotCity: any = ref([])
let hotIndustry: any = ref([])




watchEffect(async () => {
    // 获取薪资范围数据
    await getSalaryRange().then(resp => {
        salaryData.value = resp.data
    })


    // 获取系统数据总量数据
    await getDataSize().then(resp => {
        dataSize.value = resp.data.dataSize
    })

    // 获取当日新增数据
    await getDataAddedDay().then(resp => {
        addedDaySize.value = resp.data.addedDaySize
    })

    // 获取学历需求数据集
    await getExperience().then(resp => {
        experienceData.value = resp.data.dataExperiences
    })


    // 获取热门行业数据集
    await getHotIndustry().then(resp => {
        hotIndustry.value = resp.data.hotIndustry
    })

    // 获取热门城市数据集
    await getHotCity().then(resp => {
        hotCity.value = resp.data.hotCity
        console.log('hotCity', hotCity.value)
    })

})


setInterval(async () => {

    // 获取系统数据总量数据
    await getDataAddedDay().then(resp => {
        addedDaySize.value = resp.data.addedDaySize
    })

    await getDataSize().then(resp => {
        dataSize.value = resp.data.dataSize
    })


}, 5000)





</script>



<style scoped>
/* 响应式布局 */
.el-col {
    border-radius: .25rem;
}

.grid-content {
    border-radius: .25rem;
    min-height: 2.25rem;
}


/* 卡片 */
.box-card {
    width: 100%;
    min-height: 16.875rem;
    margin-bottom: 1.25rem;
}

/* 数据量统计卡片 */
.el-statistic {
    --el-statistic-content-font-size: 1.75rem;
    /* text-align: center; */
}

.statistic-card {
    height: 100%;
    padding: 1.25rem;
    border-radius: .25rem;
    background-color: var(--el-bg-color-overlay);
}

.statistic-footer {
    /* display: flex; */
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    font-size: .75rem;
    color: var(--el-text-color-regular);
    margin-top: 1rem;
}

.statistic-footer .footer-item {
    /* display: flex; */
    justify-content: space-between;
    align-items: center;
}

.statistic-footer .footer-item span:last-child {
    display: inline-flex;
    align-items: center;
    margin-left: .25rem;
}

.green {
    color: var(--el-color-success);
}


/* 热门职业 无线滚动 */
.infinite-list {
    height: 12.5rem;
    padding: 0;
    margin: 0;
    list-style: none;
}

.infinite-list .infinite-list-item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 3.125rem;
    background: var(--el-color-primary-light-9);
    margin: .625rem;
    color: var(--el-color-primary);
}

.infinite-list .infinite-list-item+.list-item {
    margin-top: .625rem;
}
</style>