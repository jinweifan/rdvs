<template>
    <el-row class="row" :gutter="20">
        <el-col style="margin: 20px 0; " v-for="(company, index) in companyList" :key="index" :span="6"
            @click="enterDetailPage(company._id)">
            <div class="card" style="cursor:pointer">
                <div class="top">
                    <span class="content">
                        <p class="title">{{ company.company_name }} </p>
                    </span>
                </div>
                <div class="bottom">
                    <div style="margin: 10px; padding-top:10px;border-top: 1px solid #fff;">
                        <span v-for="wl in company.welfare.slice(0, 3)">
                            <el-divider direction="vertical" />
                            <span>{{ wl }}</span>

                        </span>
                        <span v-if="company.welfare[0]">
                            <el-divider direction="vertical" />
                            <!-- <span>……</span> -->
                        </span>
                    </div>
                </div>
            </div>
        </el-col>
    </el-row>
    <Pagination />
</template>

<script setup lang="ts">
import router from '@/router';
import { companyStore } from '@/stores/companyDetail';
import { getCompanyDetail, getCompanySimpleInfoList } from '@/utils/api';
import { computed, inject, onMounted, provide, reactive, ref, watch, watchEffect } from 'vue'

const pagination = reactive({
    page: ref(1),
    size: ref(20),
    total: ref(0)
})
const company = companyStore()
let companyList: any = ref([])

let searchInput: any = inject('searchInput')

provide('pagination', pagination)


onMounted(async () => {
})

watchEffect(async () => {
    console.log('searchInput', searchInput)
    await getCompanySimpleInfoList(pagination.page, pagination.size, searchInput.value).then(resp => {
        companyList.value = resp.data
        pagination.page = resp.pagintion.page
        pagination.size = resp.pagintion.size
        pagination.total = resp.pagintion.total
    })
})


// 进入页面
async function enterDetailPage(company_id: string) {
    await company.updateCompany(company_id)
    router.push({ name: 'companyDetail', params: { company_id: company_id } })
}

</script>

<style scoped>
.row {
    padding: 20px;
}

.card {
    border: .0625rem solid #fff;
    border-radius: 2%;
    text-align: left;
    /* word-wrap: break-word; */
    /* width: 350px; */
    /* height: 150px; */
}

.bottom {
    min-width: 105px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.image {
    display: inline-block;
    box-sizing: border-box;
    vertical-align: top;
    width: 6.25rem;
    /* height: 6.25rem; */
    padding: .625rem;
}

.content {
    display: inline-block;
    box-sizing: border-box;
    padding: .625rem;
    /* margin: 10px; */
    margin-left: 0;

}

.content>.title {
    font-weight: bold;
    font-size: 1.125rem;
    /* display: inline; */
    /* text-align: right; */
    height: 1.875rem;
    /* width: 14rem; */
}
</style>