<template>
    <div id="main">

        <el-card class="box-card">
            <b style="font-size: 30px;"> 页面不存在！</b>

            <div>
                <RouterLink to="/">返回首页</RouterLink><b>或</b>
                <RouterLink to="/login">去登录</RouterLink>
            </div>

        </el-card>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
#main {
    height: 100vh;
    position: relative;
    overflow-y: hidden;
    width: 100%;
    background: linear-gradient(#bdc3c7, #2c3e50);

}

.box-card {
    text-align: left;
    padding: 50px 100px;
    position: absolute;
    top: 45%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
}
</style>