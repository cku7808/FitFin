<template>
    <div>
      <select name="selectBank" id="selectBank" v-model="selectedBank" @change="handleBankChange" class="form-select" aria-label="Default select example">
        <option value="" disabled selected>은행 선택</option>
        <option value="all" selected>전체</option>
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
          <button class="btn" style="background-color: #203359;">
            <RouterLink 
                :to="{ name: 'SavingProductDetail', params: { id: data.id }, query: { bank: selectedBank } }" style="text-decoration: none; color: white; font-size: 14px;">
                상세 정보
            </RouterLink>
          </button>
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
        url: `${store.BASE_URL}/api/v2/saving-products/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
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
.data-wrapper {
  border: solid 1px #79F297;
  border-radius: 10px;
}
</style>