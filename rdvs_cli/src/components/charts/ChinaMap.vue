<template>
    <div class="chinaMap" ref="chinaMap">

    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import * as echarts from "echarts"
import { getChinaMapCoordinates } from '@/utils/api';
import { mapData } from '@/assets/mapData';
const chinaMap = ref()


const map = async () => {
    let mapChart = echarts.init(chinaMap.value)
    const Coordinates: any = mapData
    echarts.registerMap("chinamap", Coordinates)
    let option = {
        geo: {
            type: "map",
            map: 'chinamap',
            roam: true, // 开启平移缩放
            zoom: 1.4, // 视角缩放比例 默认为1
            center: [104.072779, 30.663372], // 默认中心坐标
            label: {
                // show: true,// 显示文字
                // color: 'white',
                fontSize: 10
            },
            itemStyle: {
                areaColor: "white"
            }

        },
        // 地图上设置散点图
        series: [
            {
                type: "scatter",
                data: [
                    {
                        name: "北京市",
                        value: [
                            116.46, // 经度
                            39.92, // 维度
                            // 4000, // 插入的数据
                        ]
                    }
                ],
                coordinateSystem: "geo",  // 依赖的坐标，基于坐标系的方式定位
                symbolSize: 30, // 点的大小
                label: {
                    show: true
                }
            },
            {
                type: "effectScatter", // 涟漪效果散点图
                data: [
                    {
                        name: "成都市",
                        value: [
                            104.072779, 30.663372,
                            // 1, // 插入的数据
                        ]
                    }
                ],
                coordinateSystem: "geo",  // 依赖的坐标，基于坐标系的方式定位
                // symbolSize: 30, // 点的大小
                label: {
                    show: true
                },
                // 相关配置
                rippleEffect: {
                    number: 2, // 波纹大小 
                    scale: 4
                },
                itemStyle: {
                    color: 'red'
                }
            }
        ]

    }

    option && mapChart.setOption(option)
    window.addEventListener("resize", () => {
        mapChart.resize()
    })
}


onMounted(() => {
    map()
})




</script>

<style scoped>
.chinaMap {
    min-width: 200px;
    min-height: 200px;
    width: 20%;
    height: 20%;
    border: 1px solid red;
    margin: auto
}
</style>