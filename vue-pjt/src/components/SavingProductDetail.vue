<template>
    <div>
        <h1>상품 상세 정보 페이지</h1>
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
                <RouterLink :to="{ name: 'DepositSavingView', query: { bank: route.query.bank } }">
                    뒤로 가기
                </RouterLink>
                <button @click="signUpForSavingProduct">가입하기</button>
            </ul>
            
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';


const store = useCounterStore()
const route = useRoute()
const data = ref({})
const product_id = ref(null)

const loadDepositDetailProduct = function (id) {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/saving-products/${id}/`,
    })
    .then((res) => {
        data.value = res.data
        product_id.value = data.value.fin_prdt_cd
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadDepositDetailProduct(route.params.id)
})

const signUpForSavingProduct = () => {
    axios({
        method: 'post',
        url: `${store.BASE_URL}/api/v1/signup_products/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
        data: {
            product_id: product_id.value,
        },
    })
    .then((res) => {
        console.log(res.data)
    })
    .catch((err) => {
        console.log(err)
    })
}

</script>

<style scoped>

</style>