<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
        
        <h2 class="poppins-bold mb-5">
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