<template>
    <div>
      <h1>환율 계산 페이지</h1>
      <div>
        <!-- 출발 통화 -->
        <p>환전 단위 선택 (출발):</p>
        <select v-model="leftselectedCountry">
          <option v-for="country in datas" :key="country.id" :value="country">
            {{ country.cur_nm }} ({{ country.cur_unit }})
          </option>
        </select>
  
        <p>출발 금액:</p>
        <input
          v-model.number="leftMoneyInput"
          @input="calculateRightFromLeft"
          type="number"
          placeholder="출발 금액 입력"
        />
  
        <!-- 대상 통화 -->
        <p>환전 단위 선택 (대상):</p>
        <select v-model="rightselectedCountry">
          <option v-for="country in datas" :key="country.id" :value="country">
            {{ country.cur_nm }} ({{ country.cur_unit }})
          </option>
        </select>
  
        <p>환전 금액:</p>
        <input
          v-model.number="rightMoneyInput"
          @input="calculateLeftFromRight"
          type="number"
          placeholder="환전 금액 입력"
        />
  
        <!-- 실시간 계산 결과 -->
        <p>
          {{ leftMoneyInput || 0 }} {{ leftselectedCountry?.cur_unit || '' }} →
          {{ rightMoneyInput || 0 }} {{ rightselectedCountry?.cur_unit || '' }}
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from "axios";
  import { ref, onMounted } from "vue";
  
  // 상태 변수
  const datas = ref([]); // 환율 데이터 배열
  const leftMoneyInput = ref(""); // 출발 금액
  const rightMoneyInput = ref(""); // 대상 금액
  const leftselectedCountry = ref(null); // 출발 통화 선택
  const rightselectedCountry = ref(null); // 대상 통화 선택
  
  // 환율 계산 함수
  const calculateRightFromLeft = () => {
    if (!leftselectedCountry.value || !rightselectedCountry.value) {
      rightMoneyInput.value = 0;
      return;
    }
  
    const leftRate = parseFloat(leftselectedCountry.value.tts.replace(/,/g, "")) || 1;
    const rightRate = parseFloat(rightselectedCountry.value.ttb.replace(/,/g, "")) || 1;
  
    
    const inputAmount = parseFloat(leftMoneyInput.value) || 0;
  
    // 오른쪽 금액 계산
    rightMoneyInput.value = ((inputAmount / leftRate) * rightRate).toFixed(2);
  };
  
  const calculateLeftFromRight = () => {
    if (!leftselectedCountry.value || !rightselectedCountry.value) {
      leftMoneyInput.value = 0;
      return;
    }
  
    const leftRate = parseFloat(leftselectedCountry.value.tts.replace(/,/g, "")) || 1;
    const rightRate = parseFloat(rightselectedCountry.value.ttb.replace(/,/g, "")) || 1;
  
    const inputAmount = parseFloat(rightMoneyInput.value) || 0;
  
    // 왼쪽 금액 계산
    leftMoneyInput.value = ((inputAmount * leftRate) / rightRate).toFixed(2);
  };
  
  // 데이터 로드 함수
  const store = useCounterStore();
  const loadExchangeRate = async () => {
    try {
      const response = await axios.get(`${store.BASE_URL}/api/v2/load-exchangerate/`);
      datas.value = response.data; // API에서 받은 데이터 저장
    } catch (error) {
      console.error("환율 데이터를 불러오는 중 오류 발생:", error);
    }
  };
  
  // 컴포넌트 마운트 시 데이터 로드
  onMounted(() => {
    loadExchangeRate();
  });
  </script>
  
  <style scoped>
  /* 간단한 스타일 */
  select,
  input {
    margin: 10px 0;
    padding: 8px;
    font-size: 16px;
  }
  p {
    margin: 5px 0;
  }
  </style>
  