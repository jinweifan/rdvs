<template>
    <div class="demo-pagination-block">
        <el-pagination style="  display: flex; justify-content: center; align-items: center;" hide-on-single-page
            :current-page="pagination.page" 
            :page-size="pagination.size" 
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total" 
            :small="small" :disabled="disabled" :background="background"
            layout=" sizes, prev, pager, next, jumper,total," @size-change="handleSizeChange"
            @current-change="handleCurrentChange" />
    </div>
</template>

<script setup lang="ts">
import { inject, ref } from 'vue';

// const pagiantion = defineProps<{
//     page: number
//     size: number
//     // pageSizes: number[]
//     total: number
// }>()

// const emit = defineEmits(['change:size', 'change:page'])

const pagination: any = inject('pagination')


const small = ref(false)
const disabled = ref(false)
const background = ref(false)

const handleSizeChange = (val: number) => {
    pagination.size = val
    console.log(`${val} items per size`)

}
const handleCurrentChange = (val: number) => {
    // emit('change:page', val)
    pagination.page = val
    console.log(`current page: ${val} `)

}
</script>

<style scoped>
.demo-pagination-block {
    margin: 1.25rem 0;
}
</style>