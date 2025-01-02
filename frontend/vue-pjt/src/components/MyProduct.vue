<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님의 가입상품</span>
        </h2>
        
        <div class="d-flex col-8 profile-container score-dream">
            <div class="profile-block">
                <h6 class="score-dream-bold">가입 상품 관리</h6>
                <br>
                
                <ul class="product-list">
                    <h6>예금 상품</h6>
                    <!-- :key="index"  -->

                    <li v-if="deposits && deposits.length === 0" class="no-product-message"> 가입된 상품이 없습니다. </li>

                    <li v-for="myproduct in deposits" class="product-item" :key="'myproduct.product_id'+'&'+'myproduct.option_id'">
                    <span
                        class="product-name"
                        :title="'[' + myproduct.product_bank + '] ' + myproduct.product_name + ' (' + myproduct.option_trm + '개월)'">
                        [{{ myproduct.product_bank }}] {{ myproduct.product_name }} ({{ myproduct.option_trm }}개월)
                    </span>
                    <div class="product-actions">
                        <button class="action-btn" @click="viewDetails(myproduct.product_id)">
                        <i class="icon-search">🔍</i>
                        </button>
                        <button class="action-btn" @click="removeProduct(myproduct.product_code, myproduct.option_id)">
                        <i class="icon-delete">❌</i>
                        </button>
                    </div>
                    </li>
                </ul>

            </div>
            
            <div class="vertical-divider"></div>
            
            <div class="profile-block">
                <h6 class="score-dream-bold">금리 비교</h6>
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
                    <li v-if="savings && savings.length === 0" class="no-product-message"> 가입된 상품이 없습니다. </li>

                    <li v-for="myproduct in savings" class="product-item" :key="'myproduct.product_id'+'&'+'myproduct.option_id'">
                    <span
                        class="product-name"
                        :title="'[' + myproduct.product_bank + '] ' + myproduct.product_name + ' (' + myproduct.option_trm + '개월)'">
                        [{{ myproduct.product_bank }}] {{ myproduct.product_name }} ({{ myproduct.option_trm }}개월)
                    </span>
                    <div class="product-actions">
                        <button class="action-btn" @click="viewDetails(myproduct.product_id)">
                        <i class="icon-search">🔍</i>
                        </button>
                        <button class="action-btn" @click="removeProduct(myproduct.product_code, myproduct.option_id)">
                        <i class="icon-delete">❌</i>
                        </button>
                    </div>
                    </li>
                </ul>                
            </div>

            <div class="vertical-divider"></div>

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

const viewDetails = (id) => {
    router.push({ name: "DepositProductDetail", params: {id: id}});
  };
const removeProduct = (product_id, option_id) => {
    if (confirm('상품을 해지하시겠습니까?')){

        axios({
            method: 'post',
            url: `${store.BASE_URL}/api/v1/delete_products/`,
            headers: store.header,
            data: {
                product_id: product_id,
                option_id: option_id,
            },
        })
        .then((res) => {
            console.log(res.data)
            loadMyProduct()
        })
        .catch((err) => {
            console.log(err)
        })
    }
  };

// 나의 상품 정보
const loadMyProduct = function () {
    axios({
        method: 'get',
        url: `${store.BASE_URL}/api/v2/load-my-products/`,
        headers: store.header,
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
            label: "저축 금리",
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
            label: "저축 금리",
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
  overflow: hidden;
  position: relative; /* 툴팁 위치 조정을 위해 추가 */
}

.product-name {
  font-size: 1rem;
  color: #333;
  white-space: nowrap; /* 텍스트를 한 줄로 유지 */
  overflow: hidden; /* 텍스트가 넘치면 숨김 처리 */
  text-overflow: ellipsis; /* 넘친 텍스트는 ...으로 표시 */
  max-width: 70%; /* 최대 너비 설정 */
  position: relative; /* 툴팁을 위한 상대 위치 설정 */
  font-family: 'S-CoreDream-3Light';
}

.product-name:hover::after {
  content: attr(title); /* span의 title 속성 값을 툴팁으로 표시 */
  position: absolute;
  bottom: 100%; /* 상단에 표시 */
  left: 0;
  background: rgba(0, 0, 0, 0.8); /* 툴팁 배경색 */
  color: #fff; /* 툴팁 글자색 */
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.8rem;
  font-family: 'S-CoreDream-3Light';
  white-space: nowrap; /* 툴팁 텍스트 한 줄 유지 */
  z-index: 10;
  transform: translateY(-5px); /* 살짝 띄움 */
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease-in-out;
}

.product-name:hover::after {
  opacity: 1;
  visibility: visible;
  font-family: 'S-CoreDream-3Light';
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
  font-style: normal;
}

.action-btn:hover {
  color: #007bff; /* 아이콘에 호버 효과 */
}

.icon-search {
  font-size: 1.2rem;
  font-style: normal;
}

.icon-delete {
  font-size: 1.2rem;
  color: #ff4d4f;
  font-style: normal;
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

.no-product-message {
  display: flex; /* Flexbox를 사용 */
  justify-content: center; /* 가로 방향 가운데 정렬 */
  align-items: center; /* 세로 방향 가운데 정렬 */
  height: 100px; /* 적절한 높이 설정 */
  font-size: 1rem;
  color: black;
  text-align: center; /* 텍스트 가운데 정렬 */
  font-style: italic;
}
</style>