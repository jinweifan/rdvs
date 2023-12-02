<template>
    <div class="data">
        <el-statistic :title="totalDemand.title" :value="totalDemand.num" />
    </div>
</template>

<script setup lang="ts">
const props = defineProps(['totalDemand'])
</script>

<style scoped>
.data {
    text-align: center;
    margin: 0.75rem;
}
</style>