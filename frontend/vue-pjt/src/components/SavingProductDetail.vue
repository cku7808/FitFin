<template>
    <div>
        <div class="d-flex align-items-center justify-content-center flex-column col-12">
            <h2 class="score-dream-bold my-4">상품 상세 정보</h2>
            <div class="col-8 border rounded p-4">
                <div class="d-flex align-items-center justify-content-between mb-4 score-dream">
                    <div class="d-flex align-items-center ">
                        <img :src="`/banklogo/${data.kor_co_nm}.png`" :alt="selectedBank" width="50" height="50" class="me-3">
                        <li style="line-height: 20px; font-size: 18px;" class="fw-bold d-flex">{{ data.kor_co_nm }}&nbsp&nbsp
                            <span class="fw-normal text-secondary" style="font-size: 16px;">{{ data.fin_prdt_nm }}</span>
                        </li>
                    </div>
                    <button class="btn" style="background-color: #203359;">
                        <RouterLink :to="{ name: 'DepositSavingView', query: { bank: route.query.bank } }" style="text-decoration: none; color: white; font-size: 14px;">
                            뒤로 가기
                        </RouterLink>
                    </button>
                </div>
                <hr style="background:#6C757D; height:1px; border:0; margin-bottom: 0px;">
                <div class="p-2 score-dream">
                    <ul class="ps-0">
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                금융 상품 코드: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.fin_prdt_cd }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                금융 회사명: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.kor_co_nm }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                금융 상품명: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.fin_prdt_nm }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                가입 제한: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.join_deny }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                가입 대상: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.join_member }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold">
                                가입 방법: &nbsp
                                <span class="fw-normal" style="font-size: 14px;">{{ data.join_way }}</span>
                            </li>
                        </div>
                        <div class="d-flex align-items-center bg-light-subtle m-2 p-2 rounded-3">
                            <img src="/etc/check.png" :alt="selectedBank" width="30" height="30" class="me-3">
                            <li style="line-height: 20px; font-size: 14px;" class="d-flex fw-semibold flex-column">
                                유의 사항
                                <div class="etc-note fw-normal my-1">{{ data.etc_note }}</div>
                            </li>
                        </div>
                    </ul>
                </div>
            </div>
            <hr style="background:#6C757D; height:1px; border:0;">
            <div class="border rounded p-5 col-8">
                <div id="carouselExample" class="carousel slide d-flex justify-content-evenly " data-bs-ride="carousel">
                    <div data-bs-target="#carouselExample" data-bs-slide="prev" class="d-flex align-items-center me-2">
                        <img src="/carousel/back.png" alt="">
                    </div>
                    <div class="carousel-inner">
                        <div 
                            class="carousel-item" 
                            v-for="(chunk, chunkIndex) in chunkedOptions" 
                            :class="{ active: chunkIndex === 0 }" 
                            :key="chunkIndex">
                            <div class="row" :class="`row-cols-${currentColumns}`">
                                <div class="col d-flex justify-content-center" v-for="(option, index) in chunk" :key="index">
                                    <div class="card">
                                        <h5 class="card-header text-white text-center score-dream" style="background-color: #203359;">상품{{ (chunkIndex * chunkSize) + index + 1 }}</h5>
                                        <div class="card-body score-dream">
                                            <p class="card-text fw-semibold">저축 금리 유형명: <span class="fw-normal">{{ option.intr_rate_type_nm }}</span></p>
                                            <p class="card-text fw-semibold">저축 기간: <span class="fw-normal">{{ option.save_trm }}개월</span></p>
                                            <p class="card-text fw-semibold">저축 금리: <span class="fw-normal">{{ option.intr_rate }}%</span></p>
                                            <p class="card-text fw-semibold">최고 우대 금리: <span class="fw-normal">{{ option.intr_rate2 }}%</span></p>
                                            <br>
                                            <div class="d-flex justify-content-center">
                                                <button 
                                                    @click="signUpForSavingProduct(option.id)" 
                                                    v-if="store.isLogin"
                                                    class="btn me-1" style="background-color: #C2D2F2; font-size: 13px;"
                                                    >가입하기
                                                </button>
                                                <!-- <button 
                                                    @click="" 
                                                    v-if="store.isLogin"
                                                    class="btn ms-1" style="background-color: #C2D2F2; font-size: 13px;"
                                                    >장바구니
                                                </button> -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div data-bs-target="#carouselExample" data-bs-slide="next" class="d-flex align-items-center ms-2">
                        <img src="/carousel/front.png" alt="">
                    </div>
                </div>
            </div>
            <br>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { onBeforeUnmount, onMounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import router from '@/router';

const store = useCounterStore()
const route = useRoute()
const data = ref({})
const product_id = ref(null)
const options = ref([])

const loadSavingtDetailProduct = function (id) {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/saving-products/${id}/`,
        headers: store.header
    })
    .then((res) => {
        data.value = res.data
        product_id.value = data.value.fin_prdt_cd
        options.value = data.value.options
    })
    .catch((err) => {
        console.log(err)
        alert('로그인을 먼저 해주세요')
        router.push({name: 'LogInView'})
    })
}
onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
});
onMounted(() => {
    loadSavingtDetailProduct(route.params.id)
    window.addEventListener('resize', handleResize);
})

const signUpForSavingProduct = (option_id) => {
    if (confirm('해당 상품을 가입하시겠습니까?')){

        axios({
            method: 'post',
            url: `${store.BASE_URL}/api/v1/signup_products/`,
            headers: store.header,
            data: {
                product_id: product_id.value,
                option_id: option_id
            },
        })
        .then((res) => {
            console.log(res.data)
        })
        .catch((err) => {
            console.log(err)
        })
    }
}
const windowWidth = ref(window.innerWidth); // 현재 창 너비 저장

// 창 크기 변경 이벤트 핸들러
const handleResize = () => {
    windowWidth.value = window.innerWidth;
};

// 창 크기에 따라 chunkSize 동적으로 계산
const chunkSize = computed(() => {
    if (windowWidth.value >= 1400) return 5; // 대형 화면
    if (windowWidth.value >= 1290) return 4;  // 중형 화면
    if (windowWidth.value >= 992) return 3;  // 중형 화면
    if (windowWidth.value >= 768) return 2;  // 소형 화면
    return 1;                                // 모바일 화면
});

// 옵션을 chunkSize에 따라 나누기
const chunkedOptions = computed(() => {
    const chunks = [];
    for (let i = 0; i < options.value.length; i += chunkSize.value) {
        chunks.push(options.value.slice(i, i + chunkSize.value));
    }
    return chunks;
});

</script>

<style scoped>
 @font-face {
     font-family: 'S-CoreDream-3Light';
     src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
     font-weight: normal;
     font-style: normal;
}
.score-dream {
    font-family: 'S-CoreDream-3Light';
}
.score-dream-bold {
    font-family: 'S-CoreDream-3Light';
    font-weight: bold;
}
.poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }

.etc-note {
    white-space: pre-wrap;
    margin: 0px 20px;
}

.card-text {
    margin-bottom: 5px;
}
</style>