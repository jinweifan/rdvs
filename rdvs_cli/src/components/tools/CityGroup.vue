<template>
    <el-scrollbar max-height="400px">
        <div v-for=" i in props.data ">
            <div v-if="i.hasOwnProperty('firstChar')">
                <span>{{ i.firstChar }}</span>
                <div>
                    <a @click="SwitchCity(j.name)" class="eb" v-for=" j in i.cityList">{{ j.name }}</a>
                </div>
            </div>
        </div>

        <a class="eb" @click="SwitchCity(i.name)" v-for=" i in props.data">{{ i.name }}</a>
    </el-scrollbar>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import { inject, ref } from 'vue';


const props = defineProps(['data'])
const localtionDialogVisible: any = inject('localtionDialogVisible')
const cityQuery: any = inject('cityQuery')


function SwitchCity(city: string) {
    localtionDialogVisible.value = false
    console.log(' localtionDialogVisible.value', localtionDialogVisible.value)
    cityQuery.value = city
    ElMessage({
        message: '城市切换为：' + city,
        type: 'success',
    })
}
</script>

<style scoped>
.eb {
    display: inline-block;
    margin: 5px;
    padding: 5px;
    width: 180px;
    color: #eee;
    text-decoration: none;
    cursor: pointer;
}

.eb:hover {
    color: #fff;
    font-weight: bold;
}
</style>