<template>
    <div>
        <h1>예적금 비교 페이지</h1>
        <div>
            <ul v-for="data in datas">
                <li>금융 회사명 : {{ data.kor_co_nm }}</li>
                <li>금융 상품명 : {{ data.fin_prdt_nm }}</li>
                <RouterLink :to="{name:'CompareProductDetailView', params:{id: data.fin_prdt_cd}}" >상품 상세 정보</RouterLink>
                <hr>
            </ul>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';
import CompareProductDetailView from './CompareProductDetailView.vue';
import { RouterLink } from 'vue-router';

const BASE_URL = 'http://127.0.0.1:8000'
const datas = ref([])
const loadDepositProduct = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/finances/product-list/`,
    })
    .then((res) => {
        console.log(res.data)
        datas.value = res.data
        console.log(datas.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadDepositProduct()
})

</script>

<style scoped>

</style>