<template>
    <div>
        <div class="col-12 d-flex justify-content-center flex-column align-items-center my-5">
        <div class="d-flex justify-content-center">
            <h2 class="fs-2 coredream-bold">
                <span class="text-highlight">환율</span>
                계산하기
            </h2>
        </div>
        </div>

        <!-- 환율 변환 -->
        <div class="col-12 d-flex align-items-center justify-content-center mb-5">

            <div class="col-2">            
                <select
                    v-model="leftselectedCountry"
                    @change = 'calculateLeftFromRight'
                    class="form-select fs-6 coredream-regular">
                    <option v-for="country in datas" :key="country.id" :value="country">
                        {{ country.cur_con }} {{ country.cur_unit }}
                    </option>
                </select>
            
                <div class="login-form py-2 px-4 mt-2">
                <input
                    v-model.number="leftMoneyInput"
                    @input = 'calculateRightFromLeft'
                    type="number"
                    class="fs-5 text-end p-1 no-border coredream-semibold">
                <div class="fs-6 text-end mt-1 coredream-regular">{{ leftMoneyInput || 0}} {{ leftselectedCountry?.cur_nm || ''}}</div>
                </div>
           </div>

           <img src="@/assets/images/exchangerate/arrows.png" width="50" height="50" class="mx-3"><br>

            <div class="col-2">
                <select 
                    v-model="rightselectedCountry"
                    @change = 'calculateRightFromLeft'
                    class="form-select fs-6 coredream-regular">
                    <option v-for="country in datas" :key="country.id" :value="country">
                        {{ country.cur_con }} {{ country.cur_unit }}
                    </option>
                </select>

                <div class="login-form py-2 px-4 mt-2">
                <input
                    v-model="rightMoneyInput"
                    @input="calculateLeftFromRight"
                    type="number"
                    class="fs-5 text-end p-1 no-border coredream-semibold">
                <div class="fs-6 text-end mt-1 coredream-regular">{{ rightMoneyInput || 0}} {{ rightselectedCountry?.cur_nm || '' }}</div>
                </div>
            </div>

        </div>
        <br>
        <!-- 그래프 로드 (캐러셀)-->

            <div class="d-flex align-items-center justify-content-center">
                <div id="carouselExampleRide" class="carousel slide">
                    <div class="container-fluid d-flex justify-content-center">
                        <div class="carousel-inner w-75">
                            
                            <div
                                v-for="group in groupedCards"
                                :key="group.id"
                                :class="['carousel-item', { active: group.id === activeSlide }]"
                            >
                                <div class="container">
                                    <div class="row justify-content-center align-items-center g-2">
                                    <div
                                        class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center"
                                        v-for="todaydata in group.todaydatagroup"
                                        :key="todaydata?.id || todaydata"
                                    >
                                        <div v-if="String(todaydata).includes('null')">
                                            <div class="empty-box"></div>
                                        </div>
                                        <div v-else>
                                            <ExchangeRateGraph :todaydata="todaydata" />
                                        </div>
                                        
                                    </div>
                                    </div>
                                </div>
                            
                            </div>
                        
                        </div>
                    </div>

                    <div class="d-flex justify-content-center mb-3">
                        <div class="col-8 d-flex justify-content-center my-3 coredream-regular">
                            * 영업일 기준 7일 정보를 제공합니다. (영업일 11시 이후 업데이트)
                        </div>
                    </div>
                    

                    <div class="coustom-carousel-indicators coredream-regular fs-5">                     
                        <button
                            type="button"
                            data-bs-target="#carouselExampleRide"
                            data-bs-slide="prev"
                            class="coredream-semibold"
                            @click="setActiveSlide(activeSlide - 1 < 1 ? totalSlides : activeSlide - 1)"
                        >
                            <span class="carousel-control-prev-icon" aria-hidden="true"><</span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        
                        <button
                            v-for="number in totalSlides"
                            :key="`indicator-${number}`"
                            type="button"
                            data-bs-target="#carouselExampleRide"
                            :data-bs-slide-to="number-1"
                            class="coredream-semibold"
                            :class="{ active: number === activeSlide }"
                            @click="setActiveSlide(number)"
                            :aria-current="number === activeSlide ? 'true' : null"
                            :aria-label="`Slide ${number}`"                            
                        >
                        {{ number }}
                        </button>

                        <button
                            type="button"
                            data-bs-target="#carouselExampleRide"
                            data-bs-slide="next"
                            class="coredream-semibold"
                            @click="setActiveSlide(activeSlide + 1 > totalSlides ? 1 : activeSlide + 1)"
                        >
                            <span class="carousel-control-next-icon" aria-hidden="true">></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                        
                    </div>
                </div>
            </div>

    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { onMounted } from 'vue';
import router from "@/router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
if(store.isLogin === false) {
  alert("로그인을 먼저 해주세요")
  router.push({name: "LogInView"})
}

import ExchangeRateGraph from '@/components/ExchangeRateGraph.vue';


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
const datas = ref([])
const loadEchangeRate = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-exchangerate/`,
        headers: store.header,
    })
    .then((res) => {
        console.log(res.data)
        datas.value = res.data
        setDefaultCountries()
    })
    .catch((err) => {
        console.log(err)
    })
}
const todaydatas = ref([])
const loadTodayEchangeRate = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-today-exchangerate/`,
        headers: store.header,
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

// 데이트 그룹화
const groupedCards = computed(() => {
  const groups = [];
  let id = 1;
  let null_id = 1;
  for (let i = 0; i < todaydatas.value.length; i += 6) {
    const group = todaydatas.value.slice(i, i + 6);
    while (group.length < 6) {
      group.push('null_'+toString(null_id++)); // 부족한 항목을 null로 채움
    }
    groups.push({id: id++, todaydatagroup: group});
  }
  return groups;
});
// 총 슬라이드 개수
const totalSlides = computed(() => groupedCards.value.length);
// 현재 활성 슬라이드 ID
const activeSlide = ref(1);
// 슬라이드 선택 함수
const setActiveSlide = (id) => {
  activeSlide.value = id;
};

</script>

<style scoped>
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.coredream-bold {
font-family: 'S-CoreDream-3Light';
font-weight: bold;
font-style: normal;
}

.coredream-regular {
font-family: 'S-CoreDream-3Light';
font-weight: 400;
font-style: normal;
}

.coredream-semibold {
font-family: 'S-CoreDream-3Light';
font-weight: 600;
font-style: normal;
}




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
    border: 1px solid #ccc;
    border-radius: 20px;
}

/* input 화살표 없애기 */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance:none;
  margin: 0;
}

input:focus {
    outline: none; /* 기본 브라우저 검은색 테두리 제거 */
  }

/* 테두리 없애기 */
.no-border {
  width: 100%;
  border-width: 0;
}

/* 캐러셀 */
.coustom-carousel-indicators {
    position: relative;
    display: flex;
    justify-content: center;
    gap: 8px;
    /* margin-top: 10px; */
    margin-bottom: 40px;
}
.coustom-carousel-indicators button {
    width: 50px;
    height: 50px;
    background-color: white; 
    border: none; 
    color: #ccc;
}
.coustom-carousel-indicators button.active {
    color: #79F297; 
}
.carousel-control-next:active {
  background-color: #79F297; /* 클릭 시 색상 */
}


.form-select {
  border-radius: 20px; /* 둥근 모서리 */
  background-color: #f9f9f9; /* 배경색 */
  border: 1px solid #ccc; /* 테두리 색상 */
  padding: 10px 30px; /* 내부 여백 */
  transition: all 0.3s ease; /* 전환 효과 */
}

/* 선택 시 활성화된 상태 */
.form-select:focus {
  border-color: #79F297; /* 선택 시 테두리 색상 */
  box-shadow: 0 0 5px rgba(121, 242, 151, 0.8); /* 선택 시 그림자 효과 */
  outline: none; /* 기본 브라우저 아웃라인 제거 */
}
.text-highlight{
    color: #79F297;
}
</style>