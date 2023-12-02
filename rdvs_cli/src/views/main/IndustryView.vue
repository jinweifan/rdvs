<template>
    <el-container>
        <el-header>
            <FilterNav />
        </el-header>

        <el-main>
            <el-row class="el-row" :gutter="20">
                <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                    <ItemPanel style="height: 300px;margin: 0 ;">
                        <div v-if="!Object.keys(hotIndustry).length">数据不存在！</div>
                        <TableTop v-else :hot-industry="hotIndustry" />
                    </ItemPanel>
                </el-col>

                <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                    <ItemPanel style="height: 300px;margin: 0 ;">
                        <EB :experience-data="experienceData" />
                    </ItemPanel>
                </el-col>
                <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
                    <ItemPanel style="height: 300px;margin: 0 ;">
                        <WorldCloud :url ="wcURL"/>
                    </ItemPanel>
                </el-col>

            </el-row>
            <el-row class="el-row" :gutter="20">
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                    <ItemPanel>
                        <h1 v-if="!Object.keys(salaryData).length">数据不存在！</h1>
                        <SalaryRange  v-else-if="Object.keys(salaryData).length && salaryData.columns.length > 1"  :salary-data="salaryData" />
                        <div  class="salary" v-else>
                            <div style="text-align:  center;font-weight: bold; font-size: 25px;">薪资区间</div>
                            <div v-for="i in salaryData.columns"><label >职业：</label>{{ i }}</div>
                            <div v-for="i in salaryData.max"><label >最高薪资：</label>{{ i }}</div>
                            <div v-for="i in salaryData.mean"><label >平均薪资：</label>{{ i }}</div>
                            <div v-for="i in salaryData.min"><label >最低薪资：</label>{{ i }}</div>
                        </div>
                    </ItemPanel>    
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script setup lang="ts">
import TableTop from '@/components/layouts/TableTop.vue'
import { getExperience, getHotIndustry, getIndustriesWC, getSalaryRange } from '@/utils/api';

import { computed, inject, onMounted, provide, ref, watch, watchEffect } from 'vue';

let salaryData: any = ref({
    columns: [],
    max: [],
    mean: [],
    min: []
})
let experienceData: any = ref([])
let hotIndustry: any = ref([])
let wcURL: any = ref(null)
let industryQuery = ref('')
let cityQuery = ref('')
let searchInput = ref('')
provide('industryQuery', industryQuery)
provide('cityQuery', cityQuery)
provide('searchInput', searchInput)



watchEffect(async () => {

    // 获取热门行业数据集
    await getHotIndustry(industryQuery.value,cityQuery.value).then(resp => {
        hotIndustry.value = resp.data.hotIndustry
    })

     // 获取薪资范围数据
     await getSalaryRange(industryQuery.value,cityQuery.value).then(resp => {
        salaryData.value = resp.data
    })

    // 获取学历需求数据集
    await getExperience(industryQuery.value,cityQuery.value).then(resp => {
        experienceData.value = resp.data.dataExperiences
    })

      // 获取学历需求数据集
      await getIndustriesWC(industryQuery.value).then(resp => {
        wcURL.value = resp.data.wc_url
    })

})

const tz = computed(()=>{
    console.log(' salaryData.value.columns.length ', salaryData.value.columns.length )
    if( salaryData.value.columns.length != 0 ) {
        let data = salaryData.value.columns.map((col:any, i:any) => ({
            column: col,
            max: salaryData.value.max[i],
            min: salaryData.value.min[i],
            mean: salaryData.value.mean[i]
}));
    console.log('data',data)
        return  data
    }

    return {}
  
})



// onMounted(async () => {
   


// })

</script>

<style scoped>
.echartContent {
    min-height: 300px;
    width: 100%;

}

.el-row {
    margin: 20px;
}

.salary > div{
    margin: 2.5rem 0;
    border-bottom: 1px solid #fff;
    font-size:1.25rem;
}
</style>