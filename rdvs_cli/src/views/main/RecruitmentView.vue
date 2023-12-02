<template>
    <el-container>
        <el-header>
            <FilterNav />
        </el-header>
        <el-main>
            <el-table :data="jobList" height="740">
                <el-table-column prop="job_name" label="职位" />
                <el-table-column prop="salary" label="薪资" />
                <el-table-column prop="job_experience" label="经验要求" />
                <el-table-column prop="job_degree" label="学历要求" />
                <el-table-column prop="brand_name" label="公司" />
                <el-table-column prop="brand_industry" label="行业" />
                <el-table-column prop="job_area" label="地址" />
                <el-table-column prop="pub_time" label="发布时间" />

                <el-table-column align="center" label="操作">
                    <template #default="scope">
                        <el-button @click="veiwDetail(scope.row._id)">查看详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <Pagination />



            <el-dialog v-model="isDisplayTable" title="招聘详情" width="40%" draggable>
                <el-form :model="jobDetailForm" label-width="120px">
                    <el-form-item label="招聘职位">
                        <el-input v-model="jobDetailForm.job_name" />
                    </el-form-item>
                    <el-form-item label="工作地区">
                        <el-input v-model="jobDetailForm.job_area" />
                    </el-form-item>
                    <el-form-item label="工作薪资">
                        <el-input v-model="jobDetailForm.salary" />
                    </el-form-item>
                    <el-form-item label="工作地区">
                        <el-input v-model="jobDetailForm.job_degree" />
                    </el-form-item>
                    <el-form-item label="发布时间">
                        <el-date-picker v-model="jobDetailForm.pub_time" type="date" format="YYYY/MM/DD"
                            value-format="YYYY-MM-DD"></el-date-picker>
                    </el-form-item>


                    <el-form-item label="职位技能">
                        <el-input v-model="jobDetailForm.skills" autosize type="textarea" />
                    </el-form-item>
                    <el-form-item label="职位福利">
                        <el-input v-model="jobDetailForm.welfares" autosize type="textarea" />
                    </el-form-item>

                    <el-form-item label="工作详情">
                        <el-input v-model="jobDetailForm.details" :rows="5" type="textarea" />
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="isDisplayTable = false">返回</el-button>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <span class="dialog-footer">
                    </span>
                </template>
            </el-dialog>

        </el-main>
    </el-container>
</template>

<script setup lang="ts">
import { getJobList, getSingleJobDeail } from '@/utils/api';
import { onMounted, provide, reactive, ref, watch, watchEffect } from 'vue';

import { ElDrawer, ElMessageBox } from 'element-plus'


const jobList: any = ref([])
const isDisplayTable = ref(false)
const jobDetailForm: any = ref({})
const pagination = reactive({
    page: ref(1),
    size: ref(20),
    total: ref(0)
})
let industryQuery = ref('')
let searchInput = ref('')
let cityQuery = ref('')

provide('pagination', pagination)
provide('industryQuery', industryQuery)
provide('searchInput', searchInput)
provide('cityQuery', cityQuery)


watchEffect(async () => {
    // 获取招聘数据
    await getJobList(
        pagination.page,
        pagination.size,
        industryQuery.value,
        cityQuery.value
    ).then(resp => {
        jobList.value = resp.data
        pagination.page = resp.pagintion.page
        pagination.size = resp.pagintion.size
        pagination.total = resp.pagintion.total
    })
})

async function veiwDetail(job_id: any) {
    console.log('_id:', job_id)
    isDisplayTable.value = true
    await getSingleJobDeail(job_id).then(resp => {
        console.log('job：', resp.data.job)
        jobDetailForm.value = resp.data.job
    })

}










</script>

<style scoped></style>