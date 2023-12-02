<template>
    <el-page-header class="pageback" :icon="ArrowLeft">
        <template #content>
            <span> Title </span>
        </template>
    </el-page-header>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
</script>

<style scoped>
.pageback {
    /* margin-bottom: 20px; */
    padding: 10px;
    /* border-bottom: 1px solid #fff; */
}
</style>