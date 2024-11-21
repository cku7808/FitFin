<template>
    <div class="d-flex align-items-center justify-content-center flex-column col-12">
      <h2 class="poppins-bold">예적금 금리 비교 페이지</h2>
      <fieldset class="">
          <input type="radio" id="deposit" name="productType" value="deposit" class="btn-check" v-model="productType" checked />
          <label for="deposit" :class="{ selected: productType === 'deposit' }">예금 상품 보기</label>&nbsp

          <input type="radio" id="saving" name="productType" value="saving" class="btn-check" v-model="productType"/>
          <label for="saving" :class="{ selected: productType === 'saving' }">적금 상품 보기</label>
      </fieldset>
      <DepositProduct v-if="productType === 'deposit'" class="col-6"></DepositProduct>
      <SavingProduct v-else class="col-6"></SavingProduct>

    </div>
</template>

<script setup>
import DepositProduct from '@/components/DepositProduct.vue';
import SavingProduct from '@/components/SavingProduct.vue';
import { ref } from 'vue';

const productType = ref('deposit')
</script>

<style scoped>
.selected {
  color: #79F297; /* 원하는 색상 */
  font-weight: bold; /* 글씨를 두껍게 설정 */
}
.poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
</style>