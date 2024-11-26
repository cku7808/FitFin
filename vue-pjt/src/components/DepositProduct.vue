<template>
    <div class="score-dream">
      <select name="selectBank" id="selectBank" v-model="selectedBank" @change="handleBankChange" class="form-select" aria-label="Default select example">
        <option value="" disabled selected>은행 선택</option>
        <option value="all">전체</option>
        <option :value="bank" v-for="bank in uniqueBanks" :key="bank">
          {{ bank }}
        </option>
      </select><br>
      <div class="data-wrapper px-4 py-2 overflow-auto" style="max-height: 600px;">
          <ul v-for="data in filteredDatas" :key="data.id" class="bg-body-tertiary rounded-4 p-3 px-4 d-flex justify-content-between align-items-center mt-3" style="list-style: none;">
            <div class="d-flex align-items-center">
              <img :src="`/banklogo/${data.kor_co_nm}.png`" :alt="selectedBank" width="50" height="50" class="me-3">
              <li style="line-height: 20px;" class="fw-semibold d-flex flex-column">{{ data.kor_co_nm }}
                <span class="fw-normal text-secondary" style="font-size: 14px;">{{ data.fin_prdt_nm }}</span>
              </li>
            </div>
            <div class="d-flex flex-row align-items-center">
              <li style="font-size: 14px;" class="me-3 interest p-2">최고 우대 금리 : {{ data.options[0].intr_rate2 }}%</li>
              <button class="btn" style="background-color: #203359;">
                <RouterLink :to="{ name: 'DepositProductDetail', params: { id: data.id }, query: { bank: selectedBank } }" style="text-decoration: none; color: white; font-size: 14px; border-radius: 10px;">
                    상세 정보
                </RouterLink>
              </button>
            </div>
          </ul>
      </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { computed, ref } from 'vue';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
const datas = ref([])
const route = useRoute();
const router = useRouter();
const selectedBank = ref(route.query.bank || "");
const uniqueBanks = ref([]);

const loadDepositProduct = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/deposit-products/`,
        headers: store.header,
    })
    .then((res) => {
        datas.value = res.data
        const bankSet = new Set(res.data.map((data) => data.kor_co_nm));
        uniqueBanks.value = Array.from(bankSet);
    })
    .catch((err) => {
        console.log(err)
        alert('로그인을 먼저 해주세요')
        router.push({name: 'LogInView'})
    })
}

onMounted(() => {
    loadDepositProduct()    
})

const filteredDatas = computed(() => {
  if (selectedBank.value && selectedBank.value !== 'all') {
    return datas.value.filter((data) => data.kor_co_nm === selectedBank.value)
  }
  else {
    return datas.value
  }
});

const handleBankChange = () => {
  router.push({ query: { bank: selectedBank.value } })
};

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
.data-wrapper {
  border: solid 1px #79F297;
  border-radius: 10px;
}
.interest {
  background-color: white;
  border-radius: 10px;
  height: 30px;
  line-height: 14px;
}
</style>