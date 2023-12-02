<template>
    <h1>{{ experienceData.title }}</h1>
    <div id="EB" ref="EB">
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive, ref, watch } from 'vue';
const echarts: any = inject('echarts')
const EB = ref()
const props = defineProps(["experienceData"])
let ebChart: any;

watch(props, () => {

    pie()
})

function pie() {

    let data = props.experienceData.data

    let option = {
        grid: {
            top: '5%',
            left: '5%',
            right: '5%',
            bottom: '5%',
            containLabel: true // 包含文字
        },
        tooltip: {
            trigger: 'item'//触发类型item数据项图形触发 
        },
        legend: {
            orient: 'vertical',//图例列表的布局朝向vertical纵向 
            // center: 'left',
            // center: 'center',
            left: 'left',
            textStyle: {
                color: "#fff"
            }
        },


        series: [
            {
                name: '经验需求占比',
                type: 'pie',
                // 设置环形图
                radius: ['40%', '70%'],//饼图的半径。数组的第一项是内半径，第二项是外半径。
                // 设置环形图
                label: {//饼图图形上的文本标签
                    show: true,
                    position: "inside",//outside饼图扇区外侧inside饼图扇区内部center在饼图中心位置
                    color: "yellow"
                },
                labelLine: {//标签的视觉引导线配置
                    show: false
                },
                roseType: 'area',//是否展示成南丁格尔图，通过半径区分数据大小
                // itemStyle: {//设置内容样式
                //     color: '#c23531',
                //     shadowBlur: 200,
                //     shadowColor: 'rgba(0, 0, 0, 0.5)'
                // },
                data
            }
        ]
    }

    // 使用刚指定的配置项和数据显示图表。
    option && ebChart.setOption(option);
}



onMounted(() => {
    ebChart = echarts.init(EB.value)
    pie()
})
</script>

<style scoped>
#EB {
    height: 100%;
    width: 100%;
    /* margin: 20px;
    padding: 10px; */
}
</style>