<template>
    <div class="item">
        <slot />
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.item {
    height: 25rem;
    /* border: .0625rem solid blue; */
    border: 0.25px solid rgba(255, 2550, 255, .8);
    margin: 1.25rem;
    padding: 0.625rem;
    /* background-color: rgba(12, 130, 255, .85); */
}
</style>