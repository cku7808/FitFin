<template>
    <div class="d-flex flex-column score-dream col-5">
        <h3 class="score-dream-bold mb-0">예적금 Best</h3>
        <hr>
        <div class="d-flex">
            <div class="card p-3 me-2 w-50 d-flex flex-column" v-if="depositBest !== null">
                <div class="card-body d-flex flex-column justify-content-evenly">
                    <h5 class="card-title">{{ depositBest.kor_co_nm }}</h5>
                    <p class="card-text mb-1 fs-4 poppins-semibold">{{ depositBest.fin_prdt_nm }}</p>
                    <p :class="{
                        'card-text': true,
                        'fs-5': true}">
                            연 {{ depositBest.options[0].intr_rate2 }}%
                    </p>
                    <img :src="`/banklogo2/${depositBest.kor_co_nm}.png`" class="card-img-top" alt="todaydata.img">
                </div>
            </div>
            <div class="card p-3 ms-2 w-50 d-flex flex-column" v-if="savingBest !== null">
                <div class="card-body d-flex flex-column justify-content-evenly">
                    <h5 class="card-title fs-5">{{ savingBest.kor_co_nm }}</h5>
                    <p class="card-text mb-1 fs-4 poppins-semibold">{{ savingBest.fin_prdt_nm }}</p>
                    <p :class="{
                        'card-text': true,
                        'fs-5': true}">
                            연 {{ savingBest.options[0].intr_rate2 }}%
                    </p>
                    <div>
                        <img :src="`/banklogo2/${savingBest.kor_co_nm}.png`" class="card-img-top" alt="todaydata.img">
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
const depositData = ref(null)
const savingData = ref(null)
const depositBest = ref(null)
const savingBest = ref(null)

const loadDepositProduct = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/deposit-products/`,
    })
    .then((res) => {
        // console.log(res.data)
        depositData.value = res.data
        depositBest.value = depositData.value[0]
        for (let i=0; i<depositData.value.length; i++){
            if(depositData.value[i].options[0].intr_rate2 > depositBest.value.options[0].intr_rate2) {
                depositBest.value = depositData.value[i]
            }
        }
        console.log(depositBest.value.fin_prdt_nm)
    })
    .catch((err) => {
        console.log(err)
    })
}
const loadSavingProduct = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/saving-products/`,
    })
    .then((res) => {
        // console.log(res.data)
        savingData.value = res.data
        savingBest.value = savingData.value[0]
        for (let i=0; i<savingData.value.length; i++){
            if(savingData.value[i].options[0].intr_rate2 > savingBest.value.options[0].intr_rate2) {
                savingBest.value = savingData.value[i]
            }
        }
        
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadDepositProduct()
    loadSavingProduct()
})


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
.poppins-semibold {
font-family: "Poppins", sans-serif;
font-weight: 600;
font-style: normal;
}
</style>