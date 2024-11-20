<template>
    <div>
      <form>
        <label for="selectBank">은행 선택 : </label>
        <select name="selectBank" id="selectBank" v-model="selectedBank" @change="handleBankChange">
          <option value="" selected>전체</option>
          <option :value="bank" v-for="bank in uniqueBanks" :key="bank">
            {{ bank }}
          </option>
        </select>
      </form>
      <ul v-for="data in filteredDatas" :key="data.id">
        <li>금융 회사명 : {{ data.kor_co_nm }}</li>
        <li>금융 상품명 : {{ data.fin_prdt_nm }}</li>
        <RouterLink 
            :to="{ name: 'DepositProductDetail', params: { id: data.id }, query: { bank: selectedBank } }">
            상품 상세 정보
        </RouterLink>

        <hr />
      </ul>
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
  return selectedBank.value
    ? datas.value.filter((data) => data.kor_co_nm === selectedBank.value)
    : datas.value;
});

const handleBankChange = () => {
  router.push({ query: { bank: selectedBank.value } })
};

</script>

<style scoped>

</style>