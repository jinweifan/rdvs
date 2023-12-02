<template>
    <el-header>
        <FilterNav />
    </el-header>
    <el-main>
        <KeepAlive>
            <component :is="currentPage"></component>
        </KeepAlive>
    </el-main>
</template>

<script setup lang="ts">
import { computed, inject, provide, reactive, ref, watchEffect } from 'vue';

import CompanyCard from '@/views/main/company/CompanyCard.vue'
import CompanyDetail from '@/views/main/company/CompanyDetail.vue'
import Company from '@/views/main/company/CompanyView.vue'
import { useRoute } from 'vue-router';
const route = useRoute()
const company = ref({})
let industryQuery = ref('')
let searchInput = ref('')
provide('industryQuery', industryQuery)
provide('searchInput', searchInput)


let currentPage = computed(() => {
    console.log('route_name', route.name)
    switch (route.name) {
        case 'company':
            return CompanyCard
        case 'companyDetail':
            return CompanyDetail
    }
})


</script>

<style scoped></style>