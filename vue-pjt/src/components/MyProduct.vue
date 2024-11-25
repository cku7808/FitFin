<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님의 가입상품</span>
        </h2>
        
        <div class="d-flex col-8 profile-container score-dream">
            <div class="profile-block">
                <div>가입 상품 관리</div>
                <br>
                
                <ul class="product-list">
                    <h6>예금 상품</h6>
                    <!-- :key="index"  -->
                    <li v-for="myproduct in deposits" class="product-item">
                        <span class="product-name">[{{ myproduct.product_bank }}] {{ myproduct.product_name }}</span>
                        <div class="product-actions">
                        <button class="action-btn" @click="viewDetails(product)">
                            <i class="icon-search">🔍</i>
                        </button>
                        <button class="action-btn" @click="removeProduct(product)">
                            <i class="icon-delete">❌</i>
                        </button>
                        </div>
                    </li>
                </ul>

            </div>
            
            <div class="vertical-divider"></div>
            
            <div class="profile-block">
                <div>금리 비교</div>
                <br>

                <!-- 오른쪽 금리 비교 그래프 -->
                <div class="chart-section mt-4">
                    <canvas id="depositChart"></canvas>
                </div>
            
            </div>
            
            
        </div>
        
        <div class="d-flex col-8 profile-container score-dream">
            <div class="profile-block">
                <ul class="product-list">
                    <h6>적금 상품</h6>
                    <!-- :key="index"  -->
                    <li v-for="myproduct in savings" class="product-item">
                        <span class="product-name">[{{ myproduct.product_bank }}] {{ myproduct.product_name }}</span>
                        <div class="product-actions">
                        <button class="action-btn" @click="viewDetails(product)">
                            <i class="icon-search">🔍</i>
                        </button>
                        <button class="action-btn" @click="removeProduct(product)">
                            <i class="icon-delete">❌</i>
                        </button>
                        </div>
                    </li>
                </ul>                
            </div>
            <div class="profile-block">
                <!-- 오른쪽 금리 비교 그래프 -->
                <div class="chart-section mt-4">
                    <canvas id="savingChart"></canvas>
                </div>
            </div>                        
        </div>
    
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';
import { useCounterStore } from "@/stores/counter";
import Chart from "chart.js/auto";

import { useRouter } from 'vue-router';
const router = useRouter();


const store = useCounterStore();
const userInfo = computed(() => store.userInfo);
const myproducts = ref()
const deposits = ref()
const savings = ref()

const viewDetails = () => {
  };
const removeProduct = () => {
  };

// 나의 상품 정보
const loadMyProduct = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-my-products/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
    })
    .then((res) => {
        console.log(res.data)
        myproducts.value = res.data.my_product_detail
        deposits.value = myproducts.value.filter(product => product.type === '예금');
        savings.value = myproducts.value.filter(product => product.type === '적금');
        renderdepositChart()
        rendersavingChart()
    })
    .catch((err) => {
        console.log(err)
    })
}

// 그래프
const renderdepositChart = () => {
    const ctx = document.getElementById("depositChart").getContext("2d");

    // 데이터 구성
    const labels = deposits.value.map((product) => product.product_name);
    const baseRates = deposits.value.map((product) => product.option_rate);
    const maxRates = deposits.value.map((product) => product.option_maxrate);

    new Chart(ctx, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [
        {
            label: "기본 금리",
            data: baseRates,
            backgroundColor: "rgba(194, 210, 242, 1)",
            borderColor: "rgba(194, 210, 242, 1)",
            borderWidth: 1,
        },
        {
            label: "최고 금리",
            data: maxRates,
            backgroundColor: "rgba(32, 51, 89, 1)",
            borderColor: "rgba(32, 51, 89, 1)",
            borderWidth: 1,
        },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
            position: "bottom",
        },
        tooltip: {
            callbacks: {
            label: function (tooltipItem) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw}%`;
            },
            },
        },
        },
        scales: {
        y: {
            beginAtZero: true,
            title: {
            display: true,
            text: "금리 (%)",
            },
        },
        },
    },
    });
};
const rendersavingChart = () => {
    const ctx = document.getElementById("savingChart").getContext("2d");

    // 데이터 구성
    const labels = savings.value.map((product) => product.product_name);
    const baseRates = savings.value.map((product) => product.option_rate);
    const maxRates = savings.value.map((product) => product.option_maxrate);

    new Chart(ctx, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [
        {
            label: "기본 금리",
            data: baseRates,
            backgroundColor: "rgba(194, 210, 242, 1)",
            borderColor: "rgba(194, 210, 242, 1)",
            borderWidth: 1,
        },
        {
            label: "최고 금리",
            data: maxRates,
            backgroundColor: "rgba(32, 51, 89, 1)",
            borderColor: "rgba(32, 51, 89, 1)",
            borderWidth: 1,
        },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
            position: "bottom",
        },
        tooltip: {
            callbacks: {
            label: function (tooltipItem) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw}%`;
            },
            },
        },
        },
        scales: {
        y: {
            beginAtZero: true,
            title: {
            display: true,
            text: "금리 (%)",
            },
        },
        },
    },
    });
};


onMounted(() => {
    loadMyProduct();
})


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
/* 블록 */
.profile-container {
  height: 100%; 
}
.profile-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  padding: 10px;
}
/* 세로선 */
.vertical-divider {
  width: 2px;
  background-color: #d7d5d5;
  height: 100%;
  margin: 0 10px;
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


/* GPT */

.product-list {
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
}

.product-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 30px;
  background-color: #fff;
  overflow: hidden; /* 텍스트가 넘치지 않도록 설정 */
}

.product-name {
  font-size: 1rem;
  color: #333;
  white-space: nowrap; /* 텍스트를 한 줄로 유지 */
  overflow: hidden; /* 텍스트가 넘치면 숨김 처리 */
  text-overflow: ellipsis; /* 넘친 텍스트는 ...으로 표시 */
  max-width: 70%; /* 최대 너비 설정 */
}

.product-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.action-btn:hover {
  color: #007bff; /* 아이콘에 호버 효과 */
}

.icon-search {
  font-size: 1.2rem;
}

.icon-delete {
  font-size: 1.2rem;
  color: #ff4d4f;
}

.icon-delete:hover {
  color: #d43535; /* 삭제 아이콘 호버 색상 */
}
.chart-section {
  width: 100%; /* 차트가 박스 내에서 꽉 차도록 설정 */
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.chart-section canvas {
  width: 80%;
}
</style>