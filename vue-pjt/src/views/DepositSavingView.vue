<template>
    <div class="d-flex align-items-center justify-content-center flex-column col-12" v-if="store.isLogin">
      <h2 class="score-dream-bold">
        예적금 
        <span class="text-highlight">금리</span>
        비교하기
      </h2><br>
      <div class="col-8 d-flex justify-content-start score-dream">
        <div class="col-8 folder-tabs">
          <button
            class="tab-button"
            :class="{ active: productType === 'deposit' }"
            @click="productType = 'deposit'"
          >
            예금 상품 보기
          </button>
          <button
            class="tab-button"
            :class="{ active: productType === 'saving' }"
            @click="productType = 'saving'"
          >
            적금 상품 보기
          </button>
        </div>
      </div>

      <div class="col-8 border rounded-bottom rounded-end p-4">
        <DepositProduct v-if="productType === 'deposit'"></DepositProduct>
        <SavingProduct v-else></SavingProduct>
      </div>
      <br>

    </div>
</template>

<script setup>
import DepositProduct from '@/components/DepositProduct.vue';
import SavingProduct from '@/components/SavingProduct.vue';
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import router from '@/router';

const store = useCounterStore()
const productType = ref('deposit')

if(store.isLogin === false) {
  alert("로그인을 먼저 해주세요")
  router.push({name: "LogInView"})
}
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
.selected {
  color: #79F297; /* 원하는 색상 */
  font-weight: bold; /* 글씨를 두껍게 설정 */
}
.poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
  .folder-tabs {
  display: flex;
  justify-content: flex-start;

}

.tab-button {
  background: #f4f4f4; /* 비활성화 상태 배경 */
  border: 1px solid #ddd;
  border-bottom: none; /* 하단 경계선 제거 */
  border-radius: 10px 10px 0 0; /* 상단 모서리 둥글게 */
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  color: #555;
  margin-right: 5px;
  z-index: 1; /* 탭이 콘텐츠 위로 올라오게 */
  position: relative;
}

.tab-button:last-child {
  margin-right: 0; /* 마지막 탭 간격 제거 */
}

.tab-button.active {
  background: #ffffff; /* 활성화 상태 배경 */
  color: #000; /* 활성화 상태 글자색 */
  font-weight: bold;
  z-index: 2; /* 활성화된 탭을 가장 위로 */
}

.folder-content {
  border: 1px solid #ddd; /* 콘텐츠 경계선 */
  border-radius: 0 0 10px 10px; /* 하단 모서리 둥글게 */
  background: #ffffff;
  padding: 20px;
  z-index: 0;
}
.text-highlight{
    color: #79F297;
}
</style>