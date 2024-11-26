<template>
    <div class="d-flex align-items-center justify-content-center flex-column score-dream">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님에게 맞는 상품 </span>
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
        <ul>
          <li v-for="(result, index) in results" :key="index">{{ result }}</li>
        </ul>
      </div>
      <div v-else-if="searched" class="no-results">최소 한 개 이상의 조건을 설정해주세요.</div>
    </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from "@/stores/counter";

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
</style>