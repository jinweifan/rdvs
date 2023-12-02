import { defineStore } from 'pinia'
// import { useRouter } from 'vue-router'
import router from '@/router'
interface ComponentInfo {
    path: string,
    name: string,
    component: string,
    meta: {
        icon: string,
        // title: string
    }
}

// 配置动态路由展示菜单
const routes = [
    { path: '', name: '首页', component: () => import('@/views/main/IndexView.vue'), meta: { icon: `Location`, isMenu: true } },
    { path: '/industry', name: '行业分析', component: () => import('@/views/main/IndustryView.vue'), meta: { icon: `Menu`, isMenu: true } },
    { path: '/company', name: '企业分析', component: () => import('@/views/main/company/CompanyView.vue'), meat: { icon: `Document`, isMenu: true } },
    { path: '/recruitment', name: '招聘信息', component: () => import('@/views/main/RecruitmentView.vue'), meat: { icon: `Setting`, isMenu: true } },
]

// let router = null;


export const useRouteListStore = defineStore('routerList', {
    state: () => {
        return {
            routerList: [] as ComponentInfo[],
        }
    },
    getters: {
        getRoutes: (state) => state,
    },
    actions: {
        initRouterList() {
            // console.log(router)
            // if (router.hasRoute('home')) {
            //     router.addRoute('home', {
            //         path: '/',
            //         name: 'home',
            //         component: () => import('@/views/HomeView.vue'),
            //         children: routes
            //     })
            //     console.log(router.getRoutes())
            //     return router.getRoutes()
            // }


        }
    }
})


