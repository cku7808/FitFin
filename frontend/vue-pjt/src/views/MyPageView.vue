<template>

    <div class="d-flex justify-content-center my-4 score-dream-bold">
        <!-- 메뉴 -->
        <nav class="poppins-medium">
            <router-link :to="{ name: 'MyProfile' }"
            :class="[ isActiveRoute(['MyProfile', 'MyProfileEdit']) ? 'text-highlight' : 'text-black', 'text-decoration-none', 'score-dream']">
            회원 정보
            </router-link>
            <span class="separator"> | </span>
            <router-link :to="{ name: 'MyProduct' }"
            :class="[ isActiveRoute(['MyProduct']) ? 'text-highlight' : 'text-black', 'text-decoration-none', 'score-dream']">
            가입 상품
            </router-link>
            <span class="separator"> | </span>
            <router-link :to="{ name: 'MyRecommend' }"
            :class="[ isActiveRoute(['MyRecommend']) ? 'text-highlight' : 'text-black', 'text-decoration-none', 'score-dream']">
            상품 추천
            </router-link>
        </nav>
    </div>

    <router-view />

</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const isActiveRoute = (routeNames) => {
  return routeNames.includes(route.name);
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
.poppins-medium {
  font-family: "Poppins", sans-serif;
  font-weight: 500;
  font-style: normal;
}
.text-highlight{
    color: #79F297;
    font-weight: bold;
}
.separator {
  padding: 0 10px; /* 좌우로 10px의 패딩을 추가하여 공백을 만듭니다 */
}
</style>