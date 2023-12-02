<template>
    <el-scrollbar height="160px" style="margin-top: 10px; border-top: 1px solid #fff; padding-top: 10px;">
        <h4 style="padding-bottom: 10px;">企业福利</h4>

        <el-tag class="tag" v-for="t in props.tags" v-if="props.tags.length > 0" :key="t" size="large" round effect="plain"
            style="cursor:pointer;">{{ t }}</el-tag>
        <h2 v-else>无</h2>
    </el-scrollbar>
</template>

<script setup lang="ts">

const props = defineProps(['tags'])


// console.log([].length > 0)
</script>

<style scoped>
.tag {
    margin: 5px 5px;
    color: #000;
    /* font-weight: bold; */
    border: none;
    /* background-image: linear-gradient(to right, #868f96 0%, #596164 100%); */

    background-color: #E4E4E1;
    background-image: radial-gradient(at top center, rgba(255, 255, 255, 0.03) 0%, rgba(0, 0, 0, 0.03) 100%), linear-gradient(to top, rgba(255, 255, 255, 0.1) 0%, rgba(143, 152, 157, 0.60) 100%);
    background-blend-mode: normal, multiply;
}
</style>