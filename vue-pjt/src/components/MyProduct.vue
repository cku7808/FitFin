<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
        
        <h2 class="poppins-bold mb-5">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님의 가입상품</span>
        </h2>

        <div class="d-flex col-8 profile-container">
            <div class="profile-block">
                <div>가입 상품 관리</div>
            </div>
            <div class="vertical-divider"></div>
            <div class="profile-block">
                <div>금리 비교</div>
            </div>
        </div>

    </div>

    <div>
        {{ userInfo.registered_ptcd }}
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const userInfo = computed(() => store.userInfo);
</script>

<style scoped>
/* 블록 */
.profile-container {
  height: 300px; /* 부모 컨테이너의 높이를 설정하여 세로선이 잘 보이게 함 */
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
</style>