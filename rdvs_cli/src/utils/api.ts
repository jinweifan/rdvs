import request from "@/utils/request";
// import qs from "qs";

// 检查用户名是否存在
export function checkUser(username?: string, tel?: string, email?: string) {
  return request({
    url: "api/users/",
    method: "get",
    params: { username: username, tel: tel, email: email },
  });
}

export function searchRelationContent(searchString: string) {
  return request({
    url: "api/common/searchRelationContent",
    method: "get",
    params: { searchString: searchString },
  });
}

// 注册
export function register(data: any) {
  return request({
    url: "api/users/register/",
    method: "post",
    data: data,
  });
}

// 登录
export function login(data: any): Promise<any> {
  return request({
    url: "api/users/login/",
    method: "post",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    data: data,
  });
}

// 获取信息
export function getUserInfo(): Promise<any> {
  let user_id = localStorage.getItem("user_id");
  return request({
    url: `api/users/${user_id}`,
    method: "get",
  });
}

// 登录
export function updatePersonalInfo(key: string, value: any): Promise<any> {
  let user_id = localStorage.getItem("user_id");
  return request({
    url: `api/users/${user_id}`,
    method: "patch",
    data: { key: key, value: value },
  });
}

// 获取地图数据
export async function getChinaMapCoordinates() {
  return await request({
    url: "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json",
    method: "get",
  });
}

// 获取公司基本信息
export async function getCompanySimpleInfoList(
  page: number = 1,
  size: number = 20,
  searchInput: any = null,
  industryQuery: any = null,
  cityQuery: any = null
): Promise<any> {
  return await request({
    url: "api/companies",
    method: "get",
    params: {
      page: page,
      size: size,
      searchInput: searchInput,
      industryQuery: industryQuery,
      cityQuery: cityQuery,
    },
  });
}

// 获取公司基本信息
export async function getCompanyTotalDemand(company_id: string): Promise<any> {
  return await request({
    url: `api/companies/${company_id}/totalDemand`,
    method: "get",
  });
}

// 获取企业数
export async function getCompanyDetail(company_id: string): Promise<any> {
  return await request({
    url: `api/companies/${company_id}`,
    method: "get",
  });
}

// 获取招聘基本信息
export async function getJobList(
  page: number = 1,
  size: number = 20,
  industryQuery: any = null,
  cityQuery: any = null
): Promise<any> {
  return await request({
    url: "api/jobs",
    method: "get",
    params: {
      page: page,
      size: size,
      industryQuery: industryQuery,
      cityQuery: cityQuery,
    },
  });
}

// 获取薪资区间数据
export async function getSalaryRange(
  industryQuery: any = null,
  cityQuery: any = null
): Promise<any> {
  return await request({
    url: "api/charts/salary",
    method: "get",
    params: {
      industryQuery: industryQuery,
      cityQuery: cityQuery,
    },
  });
}

// 获取薪资区间数据
export async function getCompanySalaryRange(company_id: string): Promise<any> {
  return await request({
    url: `api/charts/company/${company_id}/salary`,
    method: "get",
  });
}

// 获取系统数据量
export async function getDataSize(): Promise<any> {
  return await request({
    url: "api/charts/dataSize",
    method: "get",
  });
}

// 获取当日新增数据量
export async function getDataAddedDay(): Promise<any> {
  return await request({
    url: "api/charts/dataAddedDay",
    method: "get",
  });
}

// 获取经验需求数据集
export async function getExperience(
  industryQuery: any = null,
  cityQuery: any = null
): Promise<any> {
  return await request({
    url: "api/charts/eb",
    method: "get",
    params: {
      industryQuery: industryQuery,
      cityQuery: cityQuery,
    },
  });
}

// 获取经验占比
export async function getCompanyExperience(company_id: string): Promise<any> {
  return await request({
    url: `api/charts/company/${company_id}/eb`,
    method: "get",
  });
}

// 获取职位占比
export async function getCompanyVocation(company_id: string): Promise<any> {
  return await request({
    url: `api/charts/company/${company_id}/vocation`,
    method: "get",
  });
}

// 获取热门城市数据集
export async function getHotCity(): Promise<any> {
  return await request({
    url: "api/charts/hotCity",
    method: "get",
  });
}

// 获取热门行业数据集
export async function getHotIndustry(
  industryQuery: any = null,
  cityQuery: any = null
): Promise<any> {
  return await request({
    url: "api/charts/hotIndustry",
    method: "get",
    params: {
      industryQuery: industryQuery,
      cityQuery: cityQuery,
    },
  });
}

// 获取热门行业数据集
export async function getIndustries(): Promise<any> {
  return await request({
    url: "api/industries",
    method: "get",
  });
}

// 获取热门行业数据集
export async function getIndustriesWC(industryQuery: any = null): Promise<any> {
  return await request({
    url: "api/charts/skillWordCloud",
    params: { industryQuery: industryQuery },
    method: "get",
  });
}

// 获取所有城市
export async function getAllCity(): Promise<any> {
  return await request({
    url: "api/common/allCity",
    method: "get",
  });
}

// 获取单条招聘信息
export async function getSingleJobDeail(job_id: string): Promise<any> {
  return await request({
    url: `api/jobs/${job_id}`,
    method: "get",
  });
}
