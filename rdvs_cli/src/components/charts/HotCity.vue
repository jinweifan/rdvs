<template>
    <h1>热门城市</h1>
    <div id="hotCity" ref="hotCityTop"></div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive, ref, watch } from 'vue';

const echarts = inject('echarts') as any
const hotCityTop = ref()
const props = defineProps(["hotCity"])
let hcChart: any;


function lineChart() {
    let ydata = props.hotCity.slice(-7).map((v: { name: string; }) => v.name)
    let xdata = props.hotCity.slice(-7).map((v: { value: number[]; }) => v.value[2])
    console.log(ydata)
    console.log(xdata)
    let option = {
        tooltip: {
            trigger: "axis",
        },
        grid: {
            left: "80",
            right: "20",
            bottom: "20",
            top: "20",
            containLabel: false,
        },
        xAxis: {
            type: "value",
            show: false,
        },
        yAxis: {
            type: "category",
            data: ydata,
            // inverse: true,
            axisLine: {
                show: false,
                lineStyle: {
                    color: "#fff"
                }
            },
            axisTick: {
                show: false,
            },
            axisLabel: {
                margin: 70,
                width: 60,
                align: "left",
                overflow: "truncate",
                formatter: function (value: any, index: any) {
                    let ind = index + 1;
                    if (ind == ydata.length) {
                        return "{one|" + (ydata.length - index) + "} {a|" + value + "}";
                    } else if (ind + 1 == ydata.length) {
                        return "{two|" + (ydata.length - index) + "} {b|" + value + "}";
                    } else if (ind + 2 == ydata.length) {
                        return (
                            "{three|" + (ydata.length - index) + "} {c|" + value + "}"
                        );
                    }
                    if (ydata.length - index > 9) {
                        return (
                            "{five|" + (ydata.length - index) + "} {d|" + value + "}"
                        );
                    }
                    return "{four|" + (ydata.length - index) + "} {d|" + value + "}";
                },
                rich: {
                    // a: {
                    //     color: "#59c9f9",
                    // },
                    // b: {
                    //     color: "#59c9f9",
                    // },
                    // c: {
                    //     color: "#59c9f9",
                    // },
                    // d: {
                    //     color: "#59c9f9",
                    // },
                    // 第一名
                    one: {
                        backgroundColor: "#E86452",
                        color: "white",
                        width: 12,
                        height: 16,
                        padding: [1, 0, 0, 5],
                        borderRadius: 10,
                        fontSize: 11,
                    },
                    // 第二名
                    two: {
                        backgroundColor: "#FF9845",
                        color: "white",
                        width: 12,
                        height: 16,
                        padding: [1, 0, 0, 5],
                        borderRadius: 10,
                        fontSize: 11,
                    },
                    // 第三名
                    three: {
                        backgroundColor: "#F6BD16",
                        color: "white",
                        width: 12,
                        height: 16,
                        padding: [1, 0, 0, 5],
                        borderRadius: 10,
                        fontSize: 11,
                    },
                    // 一位数
                    four: {
                        backgroundColor: "rgba(0,0,0,0.15)",
                        color: "white",
                        width: 12,
                        height: 16,
                        padding: [1, 0, 0, 5],
                        borderRadius: 10,
                        fontSize: 11,
                    },
                    // 两位数
                    five: {
                        backgroundColor: "rgba(0,0,0,0.15)",
                        color: "white",
                        width: 16,
                        height: 16,
                        padding: [1, 0, 0, 1],
                        borderRadius: 10,
                        fontSize: 11,
                    },
                },
            },
        },
        series: [{
            type: "bar",
            data: xdata,
            showBackground: true,
            sort: 'descending',
            label: {
                show: true,
                position: "right",
                color: "#fff",
            },
            barWidth: 20,
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

            },

        },],
    };

    hcChart && hcChart.setOption(option)

}
watch(props, () => {

    lineChart()
})

onMounted(() => {
    hcChart = echarts.init(hotCityTop.value)
    lineChart()
})
</script>

<style scoped>
#hotCity {
    height: 100%;
    width: 100%;
    /* margin: 20px;
    padding: 10px; */
}
</style>