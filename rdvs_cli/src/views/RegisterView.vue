<template>
    <div id="main">
        <el-card class="box-card">
            <el-form ref="formRef" :model="dynamicValidateForm" :rules="rules" :hide-required-asterisk="true"
                label-width="100px" size="large" class="demo-dynamic">
                <div class="title-container">
                    <h2 class="title text-center">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;职 聘 数 据 可 视 化 系 统 注 册</h2>
                </div>

                <el-form-item label="用户名" prop="username">
                    <el-input :suffix-icon="isRightUsername" placeholder="请输入用户名" @change="usernameIsExist"
                        v-model="dynamicValidateForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" show-password placeholder="请输入密码" @change="checkPassword"
                        v-model="dynamicValidateForm.password" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="repassword">
                    <el-input type="password" show-password placeholder="确认密码" v-model="dynamicValidateForm.repassword"
                        autocomplete="off"></el-input>
                </el-form-item>

                <el-form-item label="手机号" prop="tel">
                    <el-input :suffix-icon="isRightTel" @change="telIsExist" placeholder="请输入手机号"
                        v-model="dynamicValidateForm.tel"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input :suffix-icon="isRightEmail" @change="emailIsExist" placeholder="请输入邮箱"
                        v-model="dynamicValidateForm.email"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-radio-group v-model="dynamicValidateForm.gender">
                        <el-radio :label="true">男</el-radio>
                        <el-radio :label="false">女</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="width: 90%; margin: auto;" size="default" round
                        @click="submitForm(formRef)">注&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;册</el-button>
                </el-form-item>



            </el-form>


        </el-card>
    </div>
    <!-- </el-row> -->
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'
import { checkUser, login, register } from "@/utils/api"
import router from '@/router'
import { Select, CloseBold } from '@element-plus/icons-vue'
let telReg = /^1[3-9]\d{9}$/;
let emailReg = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
let passwordReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$/;
const dynamicValidateForm = reactive<{
    username: string
    password: string
    email: string
    repassword: string
    gender: boolean
    tel: string
}>({
    username: '',
    password: '',
    gender: true,
    email: '',
    repassword: '',
    tel: ''
})
const flag = ref(false)

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

const rules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_-]{4,16}$/, message: '用户名必须是4-16位字母、数字、下划线、减号', trigger: 'blur' },
    ],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { pattern: emailReg, message: '请输入正确的邮箱', trigger: 'blur' },
    ],
    tel: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: telReg, message: '请输入正确的手机号', trigger: 'blur' },
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { pattern: passwordReg, message: '密码必须是6-18位字母、数字、下划线、减号', trigger: 'blur' },
    ],
    repassword: [
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        {
            validator: (rule: any, value: any, callback: any) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== dynamicValidateForm.password) {
                    callback(new Error('两次输入密码不一致'));
                } else {
                    callback();
                }
            },
            trigger: 'blur',
        },
    ],
});


const formRef = ref<FormInstance>()
import { ElMessage, type FormInstance } from 'element-plus'

const submitForm = async (formEl: FormInstance | undefined) => {
    console.log(formEl)
    if (!formEl) return
    formEl.validate(async (valid: any) => {
        if (valid) {
            console.log('submit!')
            await register(dynamicValidateForm).then(data => {
                console.log('data', data)
                if (data) {
                    ElMessage.success('注册成功！');
                    router.push('/login')
                }
            })



        } else {
            console.log('error submit!')
            return false
        }
    })
}



let isRightUsername: any = ref(null)
let isRightTel: any = ref(null)
let isRightEmail: any = ref(null)
async function usernameIsExist() {
    if (dynamicValidateForm.username.length > 2) {
        await checkUser(dynamicValidateForm.username).then(resp => {
            if (resp.data.flag) {
                isRightUsername.value = CloseBold
            }
            else {
                isRightUsername.value = Select
            }
        })
    } else {
        isRightUsername.value = null
    }
}
async function telIsExist() {
    if (telReg.test(dynamicValidateForm.tel)) {
        await checkUser('', dynamicValidateForm.tel).then(resp => {
            if (!resp.data.flag) {
                isRightTel.value = Select
            } else {
                isRightTel.value = CloseBold
            }
        })
    } else {
        isRightTel.value = CloseBold
    }
}


async function emailIsExist() {
    if (emailReg.test(dynamicValidateForm.email)) {
        await checkUser('', '', dynamicValidateForm.email).then(resp => {
            if (!resp.data.flag) {
                isRightEmail.value = Select
            } else {
                isRightEmail.value = CloseBold
            }
        })
    } else {
        isRightEmail.value = CloseBold
    }

}

function checkPassword() {
    if (passwordReg.test(dynamicValidateForm.password))
        console.log('密码中包含至少一个大写字母、一个小写字母和一个数字， 确保密码长度为 8 到 16 位')
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
    width: 600px;
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
