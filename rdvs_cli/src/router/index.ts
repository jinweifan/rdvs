import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",

      name: "home",
      component: () => import("@/views/HomeView.vue"),
      children: [
        {
          path: "/",
          name: "index",
          component: () => import("@/views/main/IndexView.vue"),
          meta: { icon: `Location`, isMenu: true },
        },
        {
          path: "/industry",
          name: "industry",
          component: () => import("@/views/main/IndustryView.vue"),
          meta: { icon: `Menu`, isMenu: true },
        },
        {
          path: "/company",
          name: "company",
          component: () => import("@/views/main/company/CompanyView.vue"),
          children: [
            {
              path: ":company_id",
              name: "companyDetail",

              component: () => import("@/views/main/company/CompanyDetail.vue"),
            },
          ],
        },
        {
          path: "/me",
          name: "me",
          component: () => import("@/views/MeView.vue"),
        },

        {
          path: "/recruitment",
          name: "recruitment",
          component: () => import("@/views/main/RecruitmentView.vue"),
          meta: { icon: `Setting`, isMenu: true },
        },
      ],
    },
    {
      path: "/about",
      name: "about",
      component: () => import("@/views/AboutView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/RegisterView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: () => import("@/views/NotFound.vue"),
    },
    {
      path: "/chinamap",
      name: "chinamap",
      component: () => import("@/components/charts/ChinaMap.vue"),
    },
  ],
});

export default router;
