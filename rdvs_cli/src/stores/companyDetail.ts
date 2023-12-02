import { getCompanyDetail } from "@/utils/api";
import { defineStore } from "pinia";
// import route from '@/router';

export const companyStore = defineStore("company", {
  state: () => {
    return {
      //   currentRoute: "",
    };
  },
  getters: {},

  actions: {
    async updateCompany(company_id: string) {
      await getCompanyDetail(company_id).then((resp) => {
        this.$patch(resp.data.company);
        // console.log("state", this.$state);
      });
    },
  },
});
