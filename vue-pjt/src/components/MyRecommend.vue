<template>
    <div class="d-flex align-items-center justify-content-center flex-column score-dream">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님에게 맞는 상품 </span>
        </h2>
        
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const userInfo = computed(() => store.userInfo);

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
</style>