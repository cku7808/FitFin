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
                <ul v-for="(option, index) in data.options">
                   <li>{{ index+1 }} 번째 옵션</li>
                   <li>저축 금리 유형명: {{ option.intr_rate_type_nm }}</li> 
                   <li>저축 기간: {{ option.save_trm }}</li> 
                   <li>저축 금리: {{ option.intr_rate }}</li> 
                   <li>최고 우대 금리: {{ option.intr_rate2 }}</li> 
                   <button @click="signUpForDepositProduct(option.id)" v-if="store.isLogin">가입하기</button>
                   <hr>
                </ul>
                <RouterLink :to="{ name: 'DepositSavingView', query: { bank: route.query.bank } }">
                    뒤로 가기
                </RouterLink>
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
import router from '@/router';

const store = useCounterStore()
const route = useRoute()
const data = ref([])
const product_id = ref(null)

const loadDepositDetailProduct = function (id) {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/deposit-products/${id}/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
    })
    .then((res) => {
        data.value = res.data
        product_id.value = data.value.fin_prdt_cd
    })
    .catch((err) => {
        console.log(err)
        alert('로그인을 먼저 해주세요')
        router.push({name: 'LogInView'})
    })
}
onMounted(() => {
    loadDepositDetailProduct(route.params.id)
})

const signUpForDepositProduct = (option_id) => {
    axios({
        method: 'post',
        url: `${store.BASE_URL}/api/v1/signup_products/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
        data: {
            product_id: product_id.value,
            option_id: option_id,
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