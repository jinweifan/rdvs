<template>
    <el-row class="row-bg" justify="space-evenly">
        <el-col class="el-col" :xs="6" :sm="6" :md="6" :lg="6" :xl="6">
            <!-- 行业过滤 -->
            <el-cascader :options="industry_options" :props="industry_props" clearable filterable separator="&"
                style="width: 21.875rem;" placeholder="请选择或搜索行业" @change="cascaderChanged"> </el-cascader>
        </el-col>
        <el-col class="el-col" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
            <!-- 搜索 -->
            <SearchInput />
        </el-col>
        <el-col class="el-col" :xs="6" :sm="6" :md="6" :lg="6" :xl="6">
            <el-button :icon="Location" circle @click="localtionDialogVisible = true" />
        </el-col>
        <el-dialog v-model="localtionDialogVisible" title="城市定位" width="50%" draggable>
            <select-city />
        </el-dialog>
    </el-row>
    <el-divider content-position="center" style="margin: 0;"></el-divider>
</template>

<script setup lang="ts">
import { inject, onMounted, provide, ref } from 'vue';
import { Location, Search } from '@element-plus/icons-vue'
import { getIndustries, searchRelationContent } from '@/utils/api';
import { ElMessage } from 'element-plus';

// 搜索
const searcSelect = ref('searchInput')

const searchInput: any = inject('searchInput')
const industryQuery: any = inject('industryQuery')
// 定位对话框
const localtionDialogVisible = ref(false)
provide('localtionDialogVisible', localtionDialogVisible)

// 行业过滤
const industry_props = {
    checkStrictly: true,
}

let industry_options: any = ref([]);


onMounted(async () => {
    await getIndustries().then(resp => {
        industry_options.value = resp.data
    })
})

function cascaderChanged(val: any) {
    industryQuery.value = val ? val.join('&') : null
    console.log('industryQuery - ', industryQuery.value)
    ElMessage({
        message: `行业切换为：${industryQuery.value != null ? industryQuery.value : '整体'}`,
        type: 'success',
    })

}

</script>

<style scoped>
.el-col {
    padding: 20px 0;
}
</style>