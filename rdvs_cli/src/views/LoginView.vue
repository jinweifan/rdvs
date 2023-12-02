<template>
    <div id="main">
        <el-card class="box-card">
            <el-form ref="formRef" :model="dynamicValidateForm" size="large" class="demo-dynamic">
                <div class="title-container">
                    <h2 class="title text-center">职 聘 数 据 可 视 化 系 统</h2>
                </div>

                <el-form-item class="form-item" prop="username" :rules="userRlue" size="large">
                    <el-input v-model="dynamicValidateForm.username" :prefix-icon="User" placeholder="请输入手机号或邮箱！" />
                </el-form-item>

                <el-form-item class="form-item" prop="password" :rules="passwordRlue">
                    <el-input v-model="dynamicValidateForm.password" type="password" show-password :prefix-icon="Lock"
                        placeholder="请输入密码！">
                    </el-input>
                    <!-- <template #error>
                    <div style="height: 20px;">2</div>
                </template> -->
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" style="width: 90%; margin: auto;" size="default" round
                        @click="submitForm(formRef)">登&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;录</el-button>
                </el-form-item>


            </el-form>
            <div style="text-align: right; margin-top: 40px; color: #fff;">
                <router-link style="text-align: right; font-weight: bold; color: #fff;"
                    to="/register">没有账号，去注册！</router-link>
            </div>

        </el-card>
    </div>
    <!-- </el-row> -->
</template>

<script setup lang="ts">
import { getCurrentInstance, reactive, ref } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'
import { login } from "@/utils/api"
import { useRouter } from 'vue-router'
const formRef = ref<FormInstance>()
const dynamicValidateForm = reactive<{
    username: string
    password: string
}>({
    username: '',
    password: '',
})
const flag = ref(false)
const router = useRouter()
const userRlue =
{
    required: true,
    message: '账号不能为空！',
    trigger: 'blur',
}
const passwordRlue = {
    required: true,
    message: '密码不能为空！',
    trigger: 'blur',
}

interface DomainItem {
    username: string
    password: string
}

const removeDomain = (item: DomainItem) => {

}

const addDomain = () => {

}

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate(async (valid) => {
        if (valid) {
            console.log('submit!')
            await login(dynamicValidateForm).then(resp => {
                if (resp) {
                    // console.log('res: ', resp)
                    ElMessage({
                        message: '登录成功',
                        type: 'success'
                    });
                    localStorage.setItem("username", resp.username)
                    localStorage.setItem("user_id", resp.user_id)
                    localStorage.setItem("access_token", resp.access_token)
                    router.push('/')
                }
            })





        } else {
            console.log('error submit!')
            return false
        }
    })
}


</script>

<style scoped>
/* 布局 */
.el-row {
    margin-top: 100px;
}

/* 卡片 */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.box-card {
    width: 480px;
    padding: 50px;
    margin: 100px auto;
    position: absolute;
    top: 35%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
}

/* 表单 */
.title-container {
    margin-bottom: 30px;
}

.form-item {
    margin-bottom: 30px;
}

#main {
    height: 100vh;
    position: relative;
    overflow-y: hidden;
    width: 100%;
    background: linear-gradient(#bdc3c7, #2c3e50);
    ;
}
</style>
