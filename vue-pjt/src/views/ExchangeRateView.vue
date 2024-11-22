<template>
    <div>
        <div class="col-12 d-flex justify-content-center flex-column align-items-center py-lg-5">
        <div class="d-flex justify-content-center">
            <h1 class="fs-2 poppins-bold">환율 계산 페이지</h1>
        </div>
        </div>

        <!-- 환율 변환 -->
        <div class="col-12 d-flex align-items-center justify-content-center">

            <div class="col-4">            
            <select
                v-model="leftselectedCountry"
                @change = 'calculateLeftFromRight'
                class="form-select fs-6 poppins-regular">
                <option v-for="country in datas" :key="country.id" :value="country">
                    {{ country.cur_con }} {{ country.cur_unit }}
                </option>
            </select>
            
            <div class="login-form">
            <input
                v-model.number="leftMoneyInput"
                @input = 'calculateRightFromLeft'
                type="number"
                class="fs-5 text-end no-border poppins-bold">
            <div class="fs-6 text-end poppins-regular">{{ leftMoneyInput || 0}} {{ leftselectedCountry?.cur_nm || ''}}</div>
            </div>
           </div>

           <img src="@/assets/images/exchangerate/arrows.png" width="50" height="50"><br>

            <div class="col-4">
            <select 
                v-model="rightselectedCountry"
                @change = 'calculateRightFromLeft'
                class="form-select fs-6 poppins-regular">
                <option v-for="country in datas" :key="country.id" :value="country">
                    {{ country.cur_con }} {{ country.cur_unit }}
                </option>
            </select>
            <div class="login-form">
            <input
                v-model="rightMoneyInput"
                @input="calculateLeftFromRight"
                type="number"
                class="fs-5 text-end no-border poppins-bold">
            <div class="fs-6 text-end poppins-regular">{{ rightMoneyInput || 0}} {{ rightselectedCountry?.cur_nm || '' }}</div>
            </div>
            </div>

        </div>

        <!-- 그래프 로드 -->
        <div class="product-list">
            <div v-for="todaydata in todaydatas" :key="todaydata.id" class="product-card">
                <p>{{ todaydata.cur_con }}</p>
                <p>{{ todaydata.cur_unit }}</p>
                <p>{{ todaydata.deal_bas_r }}</p>
                <p>{{ todaydata.yesterday_diff }}</p>
                <p>{{ todaydata.yesterday_per }}</p>
                <img :src="BASE_URL+todaydata.img" alt="todaydata.img" class="product-img">
            </div>
            
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { onMounted } from 'vue';


// 환율 관련 상태 변수
// const leftfirstselected = datas.find((country) => country.cur_con === "미국")
// const rightirstselected = datas.find((country) => country.cur_con === "한국")


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
        // console.log(res.data)
        datas.value = res.data
        setDefaultCountries()
        // console.log(datas.value)
    })
    .catch((err) => {
        // console.log(err)
    })
}
const todaydatas = ref([])
const loadTodayEchangeRate = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/api/v2/load-today-exchangerate/`,
    })
    .then((res) => {
        // console.log(res.data)
        todaydatas.value = res.data
        // console.log(todaydatas.value)
    })
    .catch((err) => {
        // console.log(err)
    })
}

// 데이터 로드 후 기본값 설정
const setDefaultCountries = () => {
    const usaCountry = datas.value.find((country) => country.cur_con === "미국");
    // console.log(datas.value)
    const koreaCountry = datas.value.find((country) => country.cur_con === "한국");

    // 기본값 설정
    leftselectedCountry.value = usaCountry || null; // 미국 설정
    rightselectedCountry.value = koreaCountry || null; // 한국 설정

    // console.log(leftselectedCountry.value)
};

onMounted(() => {
    loadEchangeRate()
    loadTodayEchangeRate()
});



</script>

<style scoped>
.product-list{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.product-card{
    border: 1px solid black;
    width: 200px;
}
.product-img{
    width: 100%;
}


/* 고운 */
.login-form {
    box-sizing: border-box;
    height: 70px;

    border: 1px solid #ccc;
    border-radius: 20px;
  }
  .poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
  .poppins-regular {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
  .login-box {
    border-radius: 20px;
    background-color: #203359;
    height: 70px;
  }
  .poppins-semibold {
    font-family: "Poppins", sans-serif;
    font-weight: 600;
    font-style: normal;
  }
  input:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
  }
  .btn:focus {
    border:none !important;
    box-shadow: none !important;
    background-color: #203359 !important;
  }

  input:active {
    background-color: inherit !important; 
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
  }
  .btn:active {
    border:none !important;
    box-shadow: none !important;
    background-color: #203359 !important;
  }
  .btn:hover {
    border:none !important;
    background-color: #203359 !important;
    outline: none !important;
    transform: none !important;
  }


/* input 화살표 없애기 */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance:none;
  margin: 0;
}
/* 테두리 없애기 */
.no-border {
  width: 100%;
  border-width: 0;
}





</style>