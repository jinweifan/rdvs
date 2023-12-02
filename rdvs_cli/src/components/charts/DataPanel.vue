<template>
    <div class="dt">
        <el-row>
            <el-col :span="12" style="border-right: 1px solid #fff; margin-top: .375rem;">
                <div class="data">
                    <el-statistic style="margin-top: 1.25rem;" title="当前数据量" :value="props.dataSize" />
                </div>
            </el-col>

            <el-col :span="12" style=" margin-top: .375rem;">
                <div class="data">
                    <el-statistic style="margin-top: 1.25rem;" title="当日新增数据量" :value="props.addedDaySize" />
                </div>
            </el-col>

        </el-row>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    dataSize: number
    addedDaySize: number
}>()


</script>

<style scoped>
.dt {
    height: 7.5rem;
    border: .0625rem solid rgba(255, 2550, 255, .8);
    margin: 1.25rem;

}

.data {
    /* font-size: 80px; */
    text-align: center;
    height: 100%;
    width: 100%;
    /* padding: 15px; */
    margin: 0.75rem;
}
</style>