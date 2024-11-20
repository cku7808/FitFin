<template>
    <div>
        <h1>환율 계산 페이지</h1>
        <div>
            
            
            <p>환전 단위 선택:</p>
            <select v-model="leftselectedCountry">
                <option v-for="country in datas" :key="country.id" :value="country">
                    {{ country.cur_con }} {{ country.cur_unit }}
                </option>
            </select>
            
            
            <input
                v-model.number="leftMoneyInput"
                @input = 'calculateRightFromLeft'
                type="number">
            <p>입력 금액: {{ leftMoneyInput || 0}} {{ leftselectedCountry?.cur_nm || ''}}</p>
            <p>환전 금액: {{ leftMoneyInput || 0}} {{ leftselectedCountry?.cur_nm || ''}}</p>

            <hr>

            <p>환전 단위 선택:</p>
            <select v-model="rightselectedCountry">
                <option v-for="country in datas" :key="country.id" :value="country">
                    {{ country.cur_con }} {{ country.cur_unit }}
                </option>
            </select>

            <input
                v-model="rightMoneyInput"
                @input="calculateLeftFromRight"
                type="number">
            <p>입력 금액: {{ rightMoneyInput || 0}} {{ rightselectedCountry?.cur_nm || '' }}</p>
            <p>환전 금액: {{ rightMoneyInput || 0}} {{ rightselectedCountry?.cur_nm || '' }}</p>
          

        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { onMounted } from 'vue';


// 환율 관련 상태 변수
const leftMoneyInput = ref('')  // 금액 입력
const leftselectedCountry = ref(null)  // 통화 선택
const rightMoneyInput = ref('')
const rightselectedCountry = ref(null)
// const states = ['송금 받으실 때', '송금 보내실 때', '매매 기준율']

// 환율 계산 함수
const calculateRightFromLeft = () => {
    // console.log('calculate!!!')
    if (!leftselectedCountry.value || !rightselectedCountry.value) {
        rightMoneyInput.value = 0;
        return;
    }
    const leftRate = parseFloat(leftselectedCountry.value.deal_bas_r.replace(/,/g, "")) || 1;
    const rightRate = parseFloat(rightselectedCountry.value.deal_bas_r.replace(/,/g, "")) || 1;
    const inputAmount = parseFloat(leftMoneyInput.value) || 0;
    if (inputAmount===0) {
        rightMoneyInput.value = 0;
        return;
    }
    // 오른쪽 금액 계산
    rightMoneyInput.value = ((inputAmount * leftRate) / rightRate).toFixed(2) || 0;
};
  
const calculateLeftFromRight = () => {
    if (!leftselectedCountry.value || !rightselectedCountry.value) {
        leftMoneyInput.value = 0;
        return;
    }
    const leftRate = parseFloat(leftselectedCountry.value.deal_bas_r.replace(/,/g, "")) || 1;
    const rightRate = parseFloat(rightselectedCountry.value.deal_bas_r.replace(/,/g, "")) || 1;
    const inputAmount = parseFloat(rightMoneyInput.value) || 0;
    if (inputAmount===0) {
        leftMoneyInput.value = 0;
        return;
    }
    // 왼쪽 금액 계산
    leftMoneyInput.value = ((inputAmount * rightRate) / leftRate).toFixed(2);
};


// 데이터 로드
const BASE_URL = 'http://127.0.0.1:8000'
const datas = ref([])
const loadEchangeRate = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/api/v2/load-exchangerate/`,
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
    loadEchangeRate()
})

</script>

<style scoped>

</style>