<template>
    <div>
        <h1>예적금 비교 페이지</h1>
        <div>
            <ul>
                <li>금융 상품 코드: {{ data.fin_prdt_cd }}</li>
                <li>금융 회사명: {{ data.kor_co_nm }}</li>
                <li>금융 상품명: {{ data.fin_prdt_nm }}</li>
                <li>기타 유의사항: {{ data.etc_note }}</li>
                <li>가입 제한: {{ data.join_deny }}</li>
                <li>가입 대상: {{ data.join_member }}</li>
                <li>가입 방법: {{ data.join_way }}</li>
                <hr>
            </ul>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
const route = useRoute()
const data = ref({})

const loadDepositDetailProduct = function (id) {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/finances/product-list/${id}/`,
    })
    .then((res) => {
        console.log(res.data)
        data.value = res.data
        console.log(data.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadDepositDetailProduct(route.params.id)
})

</script>

<style scoped>

</style>