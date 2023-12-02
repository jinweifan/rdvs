import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";

import "~/styles/index.scss";
import "uno.css";
import "element-plus/theme-chalk/src/message.scss";

// 导入所有图标
import * as Icons from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { companyStore } from "./stores/companyDetail";
import ElementPlus from "element-plus";
import locale from "element-plus/lib/locale/lang/zh-cn";
import "dayjs/locale/zh-cn";

const app = createApp(App);
const pinia = createPinia();

const CommonPath = new Array("/", "/login", "/register");

router.beforeEach(async (to, from, next) => {
  let token = localStorage.getItem("access_token") || "";
  if (CommonPath.indexOf(to.path) > -1) {
    next();
  } else {
    if (token) {
      if (to.path.indexOf("/company/") != -1) {
        const company = companyStore();

        if (Object.keys(company.$state).length == 0) {
          ElMessage.warning("该公司不存在！");
          next("/company");
          return;
        }
      }
      next();
    } else {
      ElMessage.warning("请先登录！");
      next("/login");
    }
  }
});
// app.use(ElementPlus, { locale });
app.use(pinia);
app.use(router);
app.mount("#app");

// 注册全局组件
Object.keys(Icons).forEach((key) => {
  app.component(key, Icons[key as keyof typeof Icons]);
});
