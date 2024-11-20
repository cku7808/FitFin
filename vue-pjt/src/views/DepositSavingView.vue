<template>
    <div>
      <h1>예적금 금리 비교 페이지</h1>
      <fieldset>
          <input type="radio" id="deposit" name="productType" value="deposit" v-model="productType" checked />
          <label for="deposit">예금 상품 보기</label>&nbsp

          <input type="radio" id="saving" name="productType" value="saving" v-model="productType"/>
          <label for="saving">적금 상품 보기</label>
      </fieldset>
      <div v-if="productType === 'deposit'">
        <h3>예금 상품</h3>
        <DepositProduct></DepositProduct>
      </div>
      <div v-else>
        <h3>적금 상품</h3>
        <SavingProduct></SavingProduct>
      </div>
    </div>
</template>

<script setup>
import DepositProduct from '@/components/DepositProduct.vue';
import SavingProduct from '@/components/SavingProduct.vue';
import { ref } from 'vue';

const productType = ref('deposit')
</script>

<style scoped>

</style>