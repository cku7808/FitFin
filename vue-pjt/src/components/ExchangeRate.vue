<template>
    <div class="d-flex flex-column score-dream col-5">
        <h3 class="score-dream-bold mb-0">환율 최고 증감율</h3>
        <hr>
        <div class="d-flex">
            <div class="card p-3 me-2 w-50">
                <div class="card-body">
                    <h5 class="card-title fs-5">{{ max_rate_data.cur_con }} {{ max_rate_data.cur_unit }}</h5>
                    <p class="card-text mb-1 fs-4 poppins-semibold">{{ max_rate_data.deal_bas_r }}</p>
                    <p :class="{
                        'card-text': true,
                        'fs-5': true,
                        'positive': parseFloat(max_rate_data.yesterday_per) > 0,
                        'negative': parseFloat(max_rate_data.yesterday_per) < 0,
                        }">
                            {{ max_rate_data.yesterday_diff }}  {{ max_rate_data.yesterday_per }}%
                    </p>
                </div>
                <img :src="store.BASE_URL+max_rate_data.img" class="card-img-top" alt="todaydata.img">
            </div>
            <div class="card p-3 ms-2 w-50">
                <div class="card-body">
                    <h5 class="card-title fs-5">{{ min_rate_data.cur_con }} {{ min_rate_data.cur_unit }}</h5>
                    <p class="card-text mb-1 fs-4 poppins-semibold">{{ min_rate_data.deal_bas_r }}</p>
                    <p :class="{
                        'card-text': true,
                        'fs-5': true,
                        'positive': parseFloat(min_rate_data.yesterday_per) > 0,
                        'negative': parseFloat(min_rate_data.yesterday_per) < 0,
                        }">
                            {{ min_rate_data.yesterday_diff }}  {{ min_rate_data.yesterday_per }}%
                    </p>
                </div>
                <img :src="store.BASE_URL+min_rate_data.img" class="card-img-top" alt="todaydata.img">
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const min_rate_data = ref({})
const max_rate_data = ref({})
const store = useCounterStore()

const load_max_currency = () => {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-max-exchangerate/`,
    })
    .then((res) => {
        max_rate_data.value = res.data
        console.log(max_rate_data.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
const load_min_currency = () => {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-min-exchangerate/`,
    })
    .then((res) => {
        min_rate_data.value = res.data
    })
    .catch((err) => {
        console.log(err)
    })
}

onMounted(() => {
    load_max_currency()
    load_min_currency()

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
.poppins-semibold {
font-family: "Poppins", sans-serif;
font-weight: 600;
font-style: normal;
}
.positive {
    color: red; /* 양수일 때 */
}
.negative {
color: blue; /* 음수일 때 */
}
</style>