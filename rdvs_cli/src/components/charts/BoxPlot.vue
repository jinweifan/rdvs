<template>
    <h1>薪资区间</h1>

    <div id="BP" ref="BP">
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive, ref } from 'vue';
const echarts: any = inject('echarts')
const BP = ref()


function boxPlot() {
    let data = [
        ['行业', '最小值', '中位数', '最大值', '平均值'],
        ['互联网', 4000, 7000, 10000, 8000],
        ['销售', 4000, 7000, 10000, 8000],
        ['医疗', 4000, 7000, 10000, 8000],
        ['设计', 4000, 7000, 10000, 8000],
    ]
    let BPChart = echarts.init(BP.value)

    let option = {

        dataset: [
            {
                // prettier-ignore
                source: [
                    [12, 44, 55, 66, 2],
                    [23, 6, 16, 23, 1],
                ]
            },
            {
                transform: {
                    type: 'boxplot',
                    config: { itemNameFormatter: 'expr {value}' }
                }
            },
            {
                fromDatasetIndex: 1,
                fromTransformResult: 1
            }
        ],
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            nameGap: 30,
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            name: 'km/s minus 299,000',
            splitArea: {
                show: true
            }
        },
        series: [
            {
                name: 'boxplot',
                type: 'boxplot',
                datasetIndex: 1,
                dimensions: ['date', 'open', 'close', 'highest', 'lowest']

            },
            // {
            //     name: 'outlier',
            //     type: 'scatter',
            //     datasetIndex: 2
            // }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    BPChart.setOption(option);
}



onMounted(() => {
    boxPlot()
})
</script>

<style scoped>
#BP {
    height: 100%;
    width: 100%;

}
</style>




													
													
											