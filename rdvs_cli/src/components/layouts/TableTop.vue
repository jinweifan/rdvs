<template>
    <el-table :data="props.hotIndustry" highlight-current-row style="width: 100%" height="100%">
        <el-table-column type="index" />
        <el-table-column property="name" label="热门行业" />
        <el-table-column property="value" label="需求量" />
    </el-table>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps(["hotIndustry"])

</script>

<style scoped></style>