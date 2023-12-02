<template>
    <el-page-header class="back" @back="goBack">
        <template #content>
            <span> {{ company.$state.company_name }} </span>
        </template>
    </el-page-header>

    <el-row class="el-row" :gutter="20">
        <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
            <ItemPanel style="height: 300px;margin: 0 ;">
                <EB :experience-data="vocationData" />
            </ItemPanel>
        </el-col>

        <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
            <ItemPanel style="height: 300px;margin: 0 ;">
                <DataNum :totalDemand="totalDemand" />
                <TagSet :tags="welfare_list" />
            </ItemPanel>
        </el-col>
        <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
            <ItemPanel style="height: 300px;margin: 0 ;">
                <EB :experience-data="experienceData" />
            </ItemPanel>
        </el-col>

    </el-row>
    <el-row class="el-row" :gutter="20">
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
            <ItemPanel>
                <SalaryRange :salary-data="salaryData" />
            </ItemPanel>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import router from '@/router';
import { companyStore } from '@/stores/companyDetail';
import { getCompanyDetail, getCompanyExperience, getCompanySalaryRange, getCompanyTotalDemand, getCompanyVocation, getExperience, getHotIndustry, getSalaryRange } from '@/utils/api';
import { computed, inject, onMounted, provide, ref, watch, watchEffect } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
let salaryData: any = ref({})
let experienceData: any = ref({})
let vocationData: any = ref(
    {
        "title": "职位占比",
        "data": [
            { "name": "技术", "value": 3000 },
            { "name": "产品", "value": 72 },
            { "name": "销售", "value": 1444 },
            { "name": "服务业", "value": 11 },
            { "name": "生产制造", "value": 18 },
            { "name": "市场", "value": 12 },
            { "name": "运营", "value": 11 }]
    })
let industryQuery = ref('')
let cityQuery = ref('')
let searchInput = ref('')
provide('industryQuery', industryQuery)
provide('cityQuery', cityQuery)
provide('searchInput', searchInput)

let totalDemand = ref({
    title: '当前需求量',
    num: 0
})

const company: any = companyStore()

const welfare_list = computed(() => {
    let welfare = company.$state.welfare
    if (welfare && welfare[0]) {
        return welfare
    }
    return []
})

watchEffect(async () => {
    let company_id: any = route.path.split('/').pop()
    if (route.path.split('/').length == 3 && company_id != 'company') {
        await company.updateCompany(company_id)
        console.log('state2', company.$state)
        await getCompanyTotalDemand(company_id).then(resp => {
            totalDemand.value.num = resp.data.totalDemand
        })


        // 获取薪资范围数据
        await getCompanySalaryRange(company_id).then(resp => {
            salaryData.value = resp.data
        })

        // 获取经验需求数据集
        await getCompanyExperience(company_id).then(resp => {
            experienceData.value = resp.data.dataExperiences
        })

        // 获取经验需求数据集
        await getCompanyVocation(company_id).then(resp => {
            vocationData.value = resp.data.dataExperiences
        })
    }




})
onMounted(async () => {

})

function goBack() {
    router.back()
    // router.
}
</script>

<style scoped>
.back {
    margin: 10px;
    padding: 10px;
}
</style>