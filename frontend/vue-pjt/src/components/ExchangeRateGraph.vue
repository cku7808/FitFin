<template>
    <div class="card p-3" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title fs-5 coredream-regular">{{ todaydata.cur_con }} {{ todaydata.cur_unit }}</h5>
      <p class="card-text mb-1 fs-4 coredream-bold">{{ todaydata.deal_bas_r }}</p>
      <p :class="{
      'card-text': true,
      'fs-5': true,
      'positive': parseFloat(todaydata.yesterday_per) > 0,
      'negative': parseFloat(todaydata.yesterday_per) < 0,
      }"
      class="coredream-regular">
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

.positive {
    color: red; /* 양수일 때 */
}
.negative {
color: blue; /* 음수일 때 */
}
</style>