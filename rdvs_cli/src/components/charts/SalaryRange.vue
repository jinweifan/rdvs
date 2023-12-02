<template>
    <h1>薪资区间</h1>
    <div class="salaryRange" ref="salaryRange"></div>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, watch } from "vue";
const echarts: any = inject('echarts')
const salaryRange = ref()
const props = defineProps<{
    salaryData: {
        columns: string[]
        min: number[]
        max: number[]
        mean: number[]
        // median: number[]
    }
}>()
let lineChart: any;

watch(props, () => {
    // console.log('salaryData', props.salaryData)
    salaryRangeChart()
})

const salaryRangeChart = () => {



    let option = {
        tooltip: { //提示框组件
            trigger: "axis",//触发类型。坐标轴触发
            axisPointer: {//坐标轴指示器配置项
                type: "cross",//指示器类型    十字准星指示器
                label: {//坐标轴指示器的文本标签
                    backgroundColor: "#e6b600",//文本标签的背景颜色就是x轴y轴上的内容

                },
            },
        },
        legend: {
            // data: ['最低薪资', '最高薪资', '中位数', '平均值'],
            data: ['最低薪资', '平均值', '最高薪资'],
            textStyle: {
                color: "#fff"
            }
        },
        grid: {
            top: '10%',
            left: '5%',
            right: '5%',
            bottom: '10%',
            containLabel: true // 包含文字
        },
        xAxis: [
            {
                type: 'category',
                // 设置坐标轴上文字颜色
                axisLine: {
                    lineStyle: {
                        color: "#fff"
                    }
                },
                boundaryGap: false,
                data: props.salaryData.columns
            }
        ],
        yAxis: [
            {
                type: 'value',
                // 设置坐标轴上文字颜色
                axisLine: {
                    lineStyle: {
                        color: "#fff"
                    }
                },
            }
        ],
        series: [

            {
                name: '最低薪资',
                type: 'line',
                stack: 'Total',
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0,
                        1, [
                        {
                            offset: 0,
                            color: "rgb(128, 255, 165)",
                        }, {
                            offset: 1,
                            color: "rgb(1, 191, 236)",
                        },
                    ]),
                },
                lineStyle: { // 设置线段样式
                    width: 0,
                },
                emphasis: {//设置高亮的图形样式和标签样式
                    focus: "series",//只显示选中的内容高亮
                },
                smooth: true,
                data: props.salaryData.min
            },

            // {
            //     name: '中位数',
            //     type: 'line',
            //     stack: 'Total',
            //     smooth: true,
            //     areaStyle: {
            //         opacity: 0.8,
            //         color: new echarts.graphic.LinearGradient(0, 0, 0,
            //             1, [
            //             {
            //                 offset: 0,
            //                 color: "rgb(55, 162, 255)",
            //             }, {
            //                 offset: 1,
            //                 color: "rgb(116, 21, 219)",
            //             },
            //         ]),
            //     },
            //     emphasis: {
            //         focus: 'series'
            //     },
            //     data: props.salaryData.median
            // },
            {
                name: '平均值',
                type: 'line',
                stack: 'Total',
                smooth: true,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0,
                        1, [
                        {
                            offset: 0,
                            color: "rgb(0, 221, 255)",
                        }, {
                            offset: 1,
                            color: "rgb(77, 119, 255)",
                        },
                    ]),
                },
                emphasis: {
                    focus: 'series'
                },
                data: props.salaryData.mean
            },

            {
                name: '最高薪资',
                type: 'line',
                stack: 'Total',
                smooth: true,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0,
                        1, [
                        {
                            offset: 0,
                            color: "rgb(255, 0, 135)",
                        }, {
                            offset: 1,
                            color: "rgb(135, 0, 157)",
                        },
                    ]),
                },
                emphasis: {
                    focus: 'series'
                },
                data: props.salaryData.max
            },  
        ]
    };
    option && lineChart.setOption(option)
}
onMounted(async () => {
    lineChart = echarts.init(salaryRange.value)
    salaryRangeChart()
})

</script>

<style scoped>
.salaryRange {
    height: 100%;
    width: 100%;
    /* padding: 10px; */

}
</style>