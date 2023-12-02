<template>
    <div class="map" ref="chinaMap">
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, onUpdated, ref, watch, watchEffect } from 'vue';
import chinaJson from '@/assets/chinaMap.json'
const chinaMap = ref()
const echarts = inject('echarts') as any
const isCollapse = inject('isCollapse') as any
let mapChart: any;
const props = defineProps(["hotCity"])
watch(props, () => {
    map()
})
const map = async () => {

    echarts.registerMap("china", chinaJson)
    let data = props.hotCity
    let option = {
        geo: {
            map: 'china',
            // show: true,
            zoom: 1.25,
            roam: true,
            center: [104.072779, 30.663372], // 默认中心坐标
            scaleLimit: { //滚轮缩放的极限控制
                min: 1,
                max: 5
            },

            emphasis: {
                show: true,
                textStyle: {
                    color: '#fff'
                },
                label: { fontSize: 10 }
            },
            regions: [
                {
                    name: "南海诸岛",
                    itemStyle: {
                        // 隐藏地图南海诸岛
                        // opacity: 0, // 为 0 时不绘制该图形
                    },
                    label: {
                        show: false // 隐藏文字
                    }
                }
            ],

            itemStyle: {

                areaColor: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                    {
                        offset: 0,
                        color: '#a1c4fd'
                    },
                    // {
                    //     offset: 0.5,
                    //     color: '#87A7D9'
                    // },
                    {
                        offset: 1,
                        color: '#c2e9fb'
                    }
                ]),
                borderWidth: 0.7,//设置外层边框
                borderColor: "rgba(65,154,225, .5)",//地图外边框颜色rgba(43, 196, 243, 1)
                label: {
                    show: true,//是否显示标签
                    textStyle: {
                        color: "rgba(255,255,255,.5)"//地图文字的颜色
                    }
                }
            },


        },
        title: {
            text: "热门城市",
            left: "45%",
            textStyle: {
                color: 'white',
                fontSize: 20,
                textShadowBlur: 10,
                textShadowColor: 'rgba(0,0,0,.5)'
            }

        },

        tooltip: {
            show: true,
            trigger: 'item',
            formatter: (params: any) => {
                const data = params.data
                return `<div style="text-align: left;">
                        <div>城市：${data.name}</div>
                        <div>招聘数：${data.value[2]}</div>
                    </div>`
            }
        },
        visualMap: {
            type: 'continuous',
            min: 1,
            max: 10000,
            calculable: true,
            inRange: {
                // color: ["#7085B6", "#44107A", "#FFF800"],
                color: ["#50a3ba", "#eac736", "#d94e5d"]
                // ["#231557", "#44107A", "#FFF800"]
            },
            text: ['High', 'Low'],
            textStyle: 'white'
        },
        // 地图上设置散点图
        series: [
            {
                coordinateSystem: "geo",  // 依赖的坐标，基于坐标系的方式定位
                type: "effectScatter",
                data: data,
                showEffectOn: 'render',
                emphasis: {
                    scale: true
                },
                symbolSize: 10, // 点的大小
                label: {
                    formatter: '{b}',
                    position: 'center',
                    // show: true
                }
                , rippleEffect: {
                    brushType: 'stroke',
                    number: 1, // 波纹大小 
                    // scale: 4
                },
                itemStyle: {//控制散点的样式
                    color: {
                        type: 'radial',
                        x: 0.5,
                        y: 0.5,
                        r: 0.5,
                        colorStops: [{
                            offset: 0,
                            color: 'red'
                        }, {
                            offset: 0.8,
                            color: 'red'
                        }, {
                            offset: 1,
                            color: 'red'
                        }],
                        global: true // 缺省为 false
                    },

                },



            },

        ]

    }

    option && mapChart.setOption(option)
    window.onresize = () => {
        mapChart.resize()
    }
    window.addEventListener("resize", () => {
        mapChart.resize()
    })




}




onMounted(() => {

    mapChart = echarts.init(chinaMap.value)
    map()
})


</script>

<style scoped>
.map {
    height: 42.5rem;
    /* border: .0625rem solid blue; */
    border: 0.25px solid rgba(255, 2550, 255, .8);
    margin: 1.25rem;
    padding: 0.625rem;
    /* background-color: rgba(12, 130, 255, .85); */
}
</style>