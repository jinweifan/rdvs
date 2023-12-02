<template>
    <h1>热门行业</h1>

    <div id="hotIndustry" ref="hotIndustry">
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive, ref, watch } from 'vue';
const echarts: any = inject('echarts')
const hotIndustry = ref()
const props = defineProps(["hotIndustry"])
let hiChart: any;

function lineChart() {
    let xdata = props.hotIndustry.map((v: { name: string; }) => v.name)
    let ydata = props.hotIndustry.map((v: { value: number; }) => v.value)
    let option = {
        tooltip: {
            trigger: "axis",
        },
        xAxis: {
            type: "value",
            axisLine: {
                lineStyle: {
                    color: "#fff"
                }
            }
        },
        yAxis: {
            data: xdata,
            inverse: true,
            type: "category",
            axisLine: {
                lineStyle: {
                    color: "#fff"
                }
            }
        },
        // 配置图表的位置
        grid: {
            top: '10%',
            left: '0%',
            right: '10%',
            bottom: '10%',
            containLabel: true // 包含文字
        },
        series: [
            {
                data: ydata,
                type: "bar",
                itemStyle: {
                    borderRadius: [0, 20, 20, 0],
                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                        {
                            offset: 0,
                            color: '#005eaa'
                        },
                        {
                            offset: 0.5,
                            color: '#339ca8'
                        },
                        {
                            offset: 1,
                            color: '#cda819'
                        }
                    ])
                }
            }
        ]
    }

    hiChart && hiChart.setOption(option)

    window.onresize = () => {
        hiChart.resize()
    }
    window.addEventListener("resize", () => {
        hiChart.resize()
    })
}



watch(props, () => {

    lineChart()
})
onMounted(() => {

    hiChart = echarts.init(hotIndustry.value)
    lineChart()

})
</script>

<style scoped>
#hotIndustry {
    height: 100%;
    width: 100%;
    /* margin: 20px;
    padding: 10px; */
}
</style>