<template>
    <div class="card">
      <div class="card-body">
        <!-- 은행 이름 -->
        <h5 class="card-title">{{ recommenddata.product_bank }}</h5>
        
        <!-- 상품 이름 -->
        <p 
          class="card-text product-name" 
          :style="{ fontSize: baseFontSize + 'px' }">
          {{ recommenddata.product_name }}
        </p>
        
        <!-- 금리 정보 -->
        <p class="card-text interest-rate">
          나의 예상 금리: {{ recommenddata.crdt_my }}%<br />
          평균 금리: {{ recommenddata.crdt_avg }}%
        </p>
        
        <!-- 은행 로고 -->
        <img 
          :src="`/banklogo2/${recommenddata.product_bank}.png`" 
          class="card-img-top bank-logo" 
          alt="은행 로고"
        />
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

defineProps({
  recommenddata: Object,
});

// 기본 폰트 크기와 카드 너비 설정
const baseFontSize = 20; // 기본 폰트 크기 (픽셀 단위)
const cardWidth = 250; // 카드 너비 (픽셀 단위)

// 텍스트 길이에 따라 폰트 크기 계산
// 안전하게 recommenddata와 product_name을 확인하고 계산
// const calculatedFontSize = computed(() => {
//   if (!recommenddata || !recommenddata.product_name) {
//     return baseFontSize; // recommenddata가 없거나 product_name이 없는 경우 기본 폰트 크기 반환
//   }
//   const nameLength = recommenddata.product_name.length; // 상품 이름 길이
//   if (nameLength <= 20) {
//     return baseFontSize; // 길이가 짧으면 기본 폰트 크기 유지
//   }
//   const scaleFactor = 1 - (nameLength - 20) * 0.05; // 길이가 길수록 폰트 크기 축소
//   return Math.max(baseFontSize * scaleFactor, 12); // 최소 폰트 크기 12px 보장
// });

</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 요소 간 간격 고르게 분배 */
  align-items: center; /* 가로 중앙 정렬 */
  width: 270px; /* 고정 카드 너비 */
  height: 270px; /* 고정 카드 높이 */
  padding: 10px;
  border-radius: 10px; /* 둥근 모서리 */
  background-color: #fff; /* 흰 배경 */
  overflow: hidden; /* 내용 넘침 방지 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card-body {
  flex: 1; /* 카드의 높이에 맞춤 */
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  justify-content: space-between; /* 상하 간격 균등 분배 */
  align-items: center; /* 가운데 정렬 */
  gap: 10px;
}

.card-title {
  font-size: 1.4rem; /* 제목 폰트 크기 */
  font-weight: bold;
  margin: 0;
}

.product-name {
  font-weight: 600;
  line-height: 1.2;
  margin: 10px 0;
  white-space: nowrap; /* 줄바꿈 방지 */
  overflow: hidden; /* 넘치는 부분 숨김 */
  text-align: center; /* 중앙 정렬 */
}

.interest-rate {
  font-size: 1rem; /* 금리 정보 폰트 크기 */
  line-height: 1.5;
  margin: 10px 0;
}

.bank-logo {
  max-width: 190px;
  height: auto;
  margin-top: 10px;
  object-fit: contain;
}

</style>
