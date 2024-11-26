<template>
    <div class="d-flex align-items-center justify-content-center flex-column score-dream">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님에게 맞는 대출 상품 </span>
        </h2>
        
    <div class="container">

      <!-- 버튼 그룹 -->
      <div class="button-grid">
        <button
          v-for="(button, index) in buttons"
          :key="index"
          class="filter-button"
          :class="{ active: button.active }"
          @click="toggleButton(index)"
        >
          <i :class="button.icon"></i>
          <img v-if=button.active :src="button.iconwhite" alt="아이콘" class="button-image">
          <img v-else=button.active :src="button.icon" alt="아이콘" class="button-image">
          <!-- <img :class="button.icon" src="/profile/profile.png" alt="프로필 사진"> -->
          <span>{{ button.label }}</span>
        </button>
      </div>

      <!-- 검색 및 초기화 -->
      <div class="action-buttons">
        <button class="reset-button" @click="resetFilters">초기화</button>
        <button class="search-button" @click="searchResults">검색</button>
      </div>

      <!-- 결과 -->
      <div class="results" v-if="results.length > 0">
        <div>선택하신 조건으로 상품이 추천되었습니다.</div>
        <!-- <ul>
          <li v-for="(result, index) in results" :key="index">{{ result }}</li>
        </ul> -->
      </div>
      <div v-else-if="searched" class="no-results">최소 한 개 이상의 조건을 설정해주세요.</div>
          
    </div>

    <!-- 추천 상품 카드 -->
    <div class="recommend-card-container">
      <div 
        class="recommend-card"
        v-for="recommenddata in recommendedloans"
        :key="recommenddata.id"
      >
        <RecommendProduct :recommenddata="recommenddata" />
      </div>
    </div>
    
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useCounterStore } from "@/stores/counter";
import RecommendProduct from '@/components/RecommendProduct.vue';

const store = useCounterStore();
const userInfo = computed(() => store.userInfo);

const buttons = ref([
      { label: "나이", active: false, icon: "/recommend/icon_hourglass.png", iconwhite: "/recommend/icon_hourglass_white.png" },
      { label: "혼인", active: false, icon: "/recommend/icon_diamond.png", iconwhite: "/recommend/icon_diamond_white.png" },
      { label: "직업", active: false, icon: "/recommend/icon_bag.png", iconwhite: "/recommend/icon_bag_white.png" },
      { label: "소득", active: false, icon: "/recommend/icon_money.png", iconwhite: "/recommend/icon_money_white.png" },
      { label: "자산", active: false, icon: "/recommend/icon_piggy.png", iconwhite: "/recommend/icon_piggy_white.png" },
      { label: "신용", active: false, icon: "/recommend/icon_note.png", iconwhite: "/recommend/icon_note_white.png" },
    ]);

const results = ref([]);
const searched = ref(false);

const toggleButton = (index) => {
  buttons.value[index].active = !buttons.value[index].active;
};

const resetFilters = () => {
  buttons.value.forEach((button) => (button.active = false));
  results.value = [];
  searched.value = false;
};

const searchResults = () => {
  // 예제: 활성화된 버튼 이름을 결과로 표시
  results.value = buttons.value
    .filter((button) => button.active)
    .map((button) => button.label);
  searched.value = true;
  console.log(results.value)
  recommendloan()
};

const recommendedloans = ref()
const recommendloan = () => {
  axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/recommend-loan-product/`,
        headers: store.header,
    }).then((res) => {
        console.log(res.data)
        recommendedloans.value = res.data.my_recommend_detail
    })
    .catch((err) => {
        console.log(err)
    })
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
/* 글씨 */
.poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
.text-highlight{
    color: #79F297;
}



.container {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr); /* 6개의 열로 나눔 */
  margin-bottom: 20px;
}

.filter-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px;
  border: 1px solid #D7D5D5;
  cursor: pointer;
  background-color: white;
  width: 100%;
  height: 100px;
  text-align: center;
  transition: background-color 0.3s, color 0.3s;
}

.filter-button.active {
  background-color: #203359;
  color: white;
  border-color: white;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.reset-button,
.search-button{
    width: 100px;
    height: 40px;
    border-radius: 20px;
    cursor: pointer;
}

.reset-button {
  background-color: white;
  border: 1px solid #203359;
  color: black;
}

.search-button {
  background-color: #203359;
  color: white;
  border: none;
}

.results {
  margin-top: 20px;
  font-size: 1rem;
}

.no-results {
  margin-top: 20px;
  font-size: 1rem;
}
.button-image {
  width: 40px; /* 이미지 크기 */
  height: 40px;
  margin-bottom: 5px;
}


/* 추천 상품 카드 */
.recommend-card-container {
  display: flex;
  flex-wrap: wrap; /* 여러 줄로 배치 */
  justify-content: center; /* 가로 가운데 정렬 */
  align-items: center; /* 세로 가운데 정렬 */
  gap: 20px; /* 카드 간격 */
  margin-top: 30px; /* 상단 여백 */
}

.recommend-card {
  display: flex;
  flex-direction: column; /* 내부 요소를 세로로 정렬 */
  justify-content: space-between; /* 요소 간 간격 고르게 분배 */
  align-items: center; /* 가로 가운데 정렬 */
  width: 300px; /* 고정된 너비 */
  height: 300px; /* 고정된 높이 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  border-radius: 10px; /* 둥근 모서리 */
  background-color: #fff; /* 배경색 */
  padding: 15px; /* 내부 여백 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 호버 애니메이션 */
}

.recommend-card img {
  max-width: 100%; /* 이미지 크기를 카드에 맞게 조정 */
  max-height: 100%; /* 이미지 최대 높이 제한 */
  object-fit: cover; /* 이미지가 카드에 꽉 차도록 조정 */
}

.recommend-card:hover {
  transform: scale(1.2); /* 호버 시 살짝 확대 */
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15); /* 더 강한 그림자 */
}

</style>