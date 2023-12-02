<template>
    <el-tabs tab-position="left" v-model="activeName" class="demo-tabs" style="min-height: 50rem" @tab-click="handleClick">
        <el-tab-pane label="个人信息" name="first">

            <div class="box-card">
                <div class="info_header">
                    <div class="profile">
                        <el-avatar shape="square" :size="100" :src="meUrl" />
                    </div>
                    <div class="simple_info">
                        <div class="username">
                            <b>{{ capitalizeFirstLetter(userInfo.username) }}</b>
                            <div class="edit"
                                @click.prevent="(dialogVisible = true) && (updateInfo = `用户名`) && (updateParam = 'username') && (updateContent = userInfo.username)">
                                <el-icon>
                                    <EditPen />
                                </el-icon>
                                <i>修改</i>
                            </div>
                        </div>
                        <div class="desc" v-if="userInfo.desc">
                            {{ userInfo.desc }}
                            <div class="edit"
                                @click.prevent="(dialogVisible = true) && (updateInfo = `个性签名`) && (updateParam = 'desc') && (updateContent = userInfo.desc)">
                                <el-icon>
                                    <EditPen />
                                </el-icon>
                                <i>修改</i>
                            </div>
                        </div>
                        <div class="desc" v-else>
                            <span class="add"
                                @click="(dialogVisible = true) && (updateInfo = `个性签名`) && (updateParam = 'desc') && (updateContent = userInfo.desc)">
                                <i>什么话也没留下！</i>
                                <el-icon>
                                    <CirclePlus />
                                </el-icon>
                            </span>
                        </div>
                    </div>
                </div>

                <div class="info_content">
                    <div class="age">
                        <div class="lab"><b>年龄</b></div>
                        <div class="content" v-show="getAge(userInfo.birth)">{{ getAge(userInfo.birth) }}</div>
                        <div class="add" v-if="!getAge(userInfo.birth)"
                            @click="(dialogVisible = true) && (updateInfo = `年龄`) && (updateParam = 'birth') && (updateContent = userInfo.birth)">
                            <el-icon>
                                <CirclePlus />
                            </el-icon>
                            <i>添加年龄</i>
                        </div>
                        <div class="edit" v-else
                            @click.prevent="(dialogVisible = true) && (updateInfo = `年龄`) && (updateParam = 'birth') && (updateContent = userInfo.birth)">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <i>修改</i>
                        </div>
                    </div>

                    <div class="tel">
                        <div class="lab"><b>手机号</b></div>
                        <div class="content">{{ userInfo.tel }}</div>
                        <div class="edit"
                            @click.prevent="(dialogVisible = true) && (updateInfo = `手机号`) && (updateContent = userInfo.tel) && (updateParam = 'tel')">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <i>修改</i>
                        </div>
                    </div>
                    <div class="email">
                        <div class="lab"><b>邮箱</b></div>
                        <div class="content">{{ userInfo.email }}</div>
                        <div class="edit"
                            @click.prevent="(dialogVisible = true) && (updateInfo = `邮箱`) && (updateContent = userInfo.email) && (updateParam = 'email')">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <i>修改</i>
                        </div>
                    </div>
                    <div class="vocation">
                        <div class="lab"><b>职位</b></div>
                        <div class="content" v-show="userInfo.vocation">{{ userInfo.vocation }}</div>
                        <div class="add" v-if="!userInfo.vocation"
                            @click.prevent="(dialogVisible = true) && (updateInfo = `职位`) && (updateParam = 'vocation') && (updateContent = userInfo.vocation)">
                            <el-icon>
                                <CirclePlus />
                            </el-icon>
                            <i>添加职位</i>
                        </div>
                        <div class="edit" v-else
                            @click.prevent="(dialogVisible = true) && (updateInfo = `职位`) && (updateParam = 'vocation') && (updateContent = userInfo.vocation)">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <i>修改</i>
                        </div>
                    </div>
                    <div class="area">
                        <div class="lab"><b>地址</b></div>
                        <div class="content" v-show="userInfo.area">{{ userInfo.area }}</div>
                        <div class="add" v-if="!userInfo.area"
                            @click.prevent="(dialogVisible = true) && (updateInfo = `地址`) && (updateParam = 'area') && (updateContent = userInfo.area)">
                            <el-icon>
                                <CirclePlus />
                            </el-icon>
                            <i>添加地址</i>
                        </div>
                        <div class="edit" v-else
                            @click.prevent="(dialogVisible = true) && (updateInfo = `地址`) && (updateParam = 'area') && (updateContent = userInfo.area)">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <i>修改</i>
                        </div>
                    </div>
                </div>


                <el-dialog v-model="dialogVisible" :title="updateInfo" width="30%" :before-close="handleClose">
                    <!-- <span>{{ updateInfo }}</span> -->


                    <el-date-picker v-if="updateParam == 'birth'" v-model="userInfo.birth" type="date"
                        placeholder="选择出生日期" />
                    <el-input v-else v-model="updateContent" clearable placeholder="请输入" />
                    <template #footer>
                        <span class="dialog-footer">
                            <el-button type="primary" @click="updateSimpleInfo">
                                确认
                            </el-button>
                            <el-button @click="dialogVisible = false">取消</el-button>

                        </span>
                    </template>
                </el-dialog>

                <!-- <el-form ref="formRef" :model="userInfo" label-width="100px" size="large" class="demo-dynamic">

                    <el-form-item label="用户名" prop="username">
                        <el-input value="reddyfan"></el-input>
                    </el-form-item>
                    <el-form-item label="年龄" prop="age">
                        <el-input value="23"></el-input>
                    </el-form-item>
                    <el-form-item label="出生日期" prop="birth">
                        <el-input value="23"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" prop="gender">
                        <el-radio-group v-model="userInfo.gender">
                            <el-radio :label="1">男</el-radio>
                            <el-radio :label="0">女</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="手机号" prop="tel">
                        <el-input value="18783935413"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱" prop="email">
                        <el-input value="1312805094@qq.com"></el-input>
                    </el-form-item>
                    <el-form-item label="地址" prop="area">
                        <el-input value="上海·徐汇区·徐家汇"></el-input>
                    </el-form-item>
                    <el-form-item label="个人签名">
                        <el-input value="为喜欢的生活而活！" autosize type="textarea" />
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" style="width: 10%; margin: auto;" size="default" round
                            @click="submitForm('dynamicValidateForm')">保存</el-button>
                    </el-form-item>
                </el-form> -->

            </div>
        </el-tab-pane>
        <el-tab-pane label="安全设置" name="second">账号设置</el-tab-pane>
        <!-- <el-tab-pane label="隐私设置" name="third">隐私设置</el-tab-pane>
        <el-tab-pane label="我的收藏" name="fourth">我的收藏</el-tab-pane> -->
    </el-tabs>
</template>
<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, type TabsPaneContext } from 'element-plus'
import { getUserInfo, updatePersonalInfo } from '@/utils/api';
import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
    done()

}

const updateParam = ref('')
// const updateBirthContent = ref('')

const activeName = ref('first')

const squareUrl = 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png'
const meUrl = '	https://picx.zhimg.com/v2-b9422259ce7940d364072ae03cc725a4_xll.jpg?source=32738c0c'

const handleClick = (tab: TabsPaneContext, event: Event) => {
    console.log(tab, event)
}
let updateInfo = ref('修改')
let updateContent = ref('')

const userInfo: any = ref({
    user_id: '',
    username: '',
    birth: '',
    gender: true,
    tel: '',
    email: '',
    desc: '',
    vocation: '',
    area: ''


})

onMounted(async () => {
    await getUserInfo().then(resp => {

        userInfo.value = resp.data.user
    })
})



const submitForm = async (formEl: any) => {
    if (!formEl) return
    formEl.validate(async (valid: any) => {
        if (valid) {
            console.log('submit!')

        } else {
            console.log('error submit!')
            return false
        }
    })
}

function updateSimpleInfo() {
    let value = updateParam.value == 'birth' ? formatDate(userInfo.value.birth) : updateContent.value
    updatePersonalInfo(updateParam.value, value).then(resp => {
        // console.log('更新成功！')
        if (resp.code == 1001) {
            getUserInfo().then(resp => {
                userInfo.value = resp.data.user
                ElMessage.success('更新成功！')
            })
        } else {
            ElMessage.info('更新失败！')
        }

    })
    dialogVisible.value = false
}

// 首字母大写
function capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// 日期转年龄

function getAge(dateString: string) {
    var today = new Date();
    var birthDate = new Date(dateString);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}
// 格式化日期
function formatDate(dateString: string) {
    const date = new Date(dateString);
    const options: any = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return date.toLocaleDateString('zh-CN', options).replace(/\//g, '-');
}

</script>
<style>
.demo-tabs {
    margin: 40px;
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
    padding: 20px;

}

/* 表单 */
.title-container {
    margin-bottom: 30px;
}

.form-item {
    margin-bottom: 30px;
}


.info_header {
    padding: 30px;
    height: 150px;
    border: 1px #fff solid;
    border-radius: .625rem;
    /* background-color: azure; */
}

.info_header>div {
    float: left;
}

.info_header>.profile {
    width: 6.25rem;
    height: 6.25rem;
    /* background-color: aquamarine; */
}

.info_header>.simple_info {

    margin-left: 1.875rem;
    /* background-color: aquamarine; */
    height: 100%;
    width: 80%;
    padding: 1.25rem;
    text-align: left;

}

.username {
    font-size: 1.25rem;
}

.simple_info>div {
    margin-bottom: .9375rem;
}

.info_content {

    padding: 1.875rem;
}

.info_content>div {
    padding: 3.125rem;
    /* height: 6.25rem; */
    border-bottom: #fff 1px solid;
}

.info_content>div>div {
    float: left;
    /* padding: 10px; */
    font-size: 1.125rem;
}

.lab {
    text-align: right;
    display: inline-block;

    width: 5%;
}

.content {
    display: inline-block;
    text-align: left;
    /* width: 80%; */
    margin-left: 10%;

}

.edit {
    display: none;
    color: #2aa1eb;
    font-size: 15px;
    font-weight: normal;
    margin-left: 1.25rem;
    cursor: pointer;
}

.simple_info>div:hover .edit,
.info_content>div:hover .edit {
    display: inline-block;
}

.info_content .add {
    margin-left: 10%;
    vertical-align: text-bottom;
    cursor: pointer;
    color: #2aa1eb;
}

.edit>i {
    font-style: normal;
    margin-left: .3125rem;
    display: inline-block;
    vertical-align: center;
    color: #2aa1eb;
    cursor: pointer;
}
</style>
