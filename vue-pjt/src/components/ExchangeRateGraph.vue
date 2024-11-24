<template>
    <div class="card p-3" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title fs-5">{{ todaydata.cur_con }} {{ todaydata.cur_unit }}</h5>
      <p class="card-text mb-1 fs-4 poppins-semibold">{{ todaydata.deal_bas_r }}</p>
      <p :class="{
      'card-text': true,
      'fs-5': true,
      'positive': parseFloat(todaydata.yesterday_per) > 0,
      'negative': parseFloat(todaydata.yesterday_per) < 0,
      }">
        {{ todaydata.yesterday_diff }}  {{ todaydata.yesterday_per }}%
      </p>
    </div>
    <img :src="BASE_URL+todaydata.img" class="card-img-top" alt="todaydata.img">
  </div>
</template>

<script setup>
defineProps({
    todaydata: Object
})
const BASE_URL = 'http://127.0.0.1:8000'
</script>

<style scoped>
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