<template>
    <div>
        <el-autocomplete style="width: 43.75rem;" v-model="searchInput" :trigger-on-focus="false"
            :fetch-suggestions="querySearchAsync" @select="handleSelect"  :fit-input-width="true" placeholder="请输入"
            class="input-with-select">
            <template #append>
                <el-button :icon="Search"  @click="handleSelect"/>
            </template>
        </el-autocomplete>
    </div>
</template>

<script setup lang="ts">
import { searchRelationContent } from '@/utils/api'
import { inject, ref } from 'vue'
import { Location, Search } from '@element-plus/icons-vue'

interface LinkItem {
    value: string
    // link: string
    // company_name: string
}

const searchInput: any = inject('searchInput')

const links = ref<LinkItem[]>([])

// const loadAll = () => {
//     return [
//         { value: 'vue', link: 'https://github.com/vuejs/vue' },
//         { value: 'element', link: 'https://github.com/ElemeFE/element' },
//         { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
//         { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
//         { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
//         { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
//         { value: 'babel', link: 'https://github.com/babel/babel' },
//     ]
// }

let timeout: any
const querySearchAsync: any = async (queryString: string, cb: (arg: any) => void) => {
    if (queryString) {
        await searchRelationContent(queryString).then(resp => {
            links.value = resp.data
            // console.log('resp.data', resp.searchContent)
            // console.log('links.value', links.value)
        })

        // const results = queryString
        //     ? links.value.filter(createFilter(queryString))
        //     : links.value

        clearTimeout(timeout)
        timeout = setTimeout(() => {
            cb(links.value)
        }, 3000 * Math.random())
    }

}

// const createFilter = (queryString: string) => {
//     return (links: LinkItem) => {
//         return (
//             links.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
//         )
//     }
// }

const handleSelect: any = (item: LinkItem) => {
    console.log(item)
}

// onMounted(() => {
//     // links.value = loadAll()
// })

</script>

<style scoped></style>