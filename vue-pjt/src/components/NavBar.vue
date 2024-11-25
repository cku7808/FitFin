<template>
    <div>
        <nav class="navbar navbar-expand-lg">
            <div class="container-fluid position-relative d-flex">
                <!-- 로고와 토글 버튼 -->
                <div class="d-flex align-items-center">
                    <RouterLink :to="{ name: 'MainView'}">
                        <img src="/logo/Logo.png" alt="FitFin Logo" width="110" height="49" class="me-2">
                    </RouterLink>
                    <button
                        class="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                        >
                        <span class="navbar-toggler-icon"></span>
                    </button>
                </div>

                <!-- 로그인/로그아웃 버튼 -->
                <div class="position-absolute top-0 end-0 d-flex align-items-center mt-2">
                    <ul class="navbar-nav d-flex flex-row" v-if="store.isLogin">
                        <li class="nav-item">
                            <a @click="store.logOut()" style="cursor: pointer;">
                            <img src="/navbar/Logout.png" alt="Logout" width="80" height="19" class="me-2">
                            </a>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'MyPageView'}">
                            <img src="/navbar/Mypage.png" alt="Mypage" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'CartView'}">
                            <img src="/navbar/Cart.png" alt="Cart" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                    <ul class="navbar-nav d-flex flex-row" v-else>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'SignUpView'}">
                            <img src="/navbar/Signup.png" alt="Signup" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'LogInView'}">
                            <img src="/navbar/Login.png" alt="Login" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                </div>

                <!-- 메뉴 -->
                <div class="collapse navbar-collapse" id="navbarSupportedContent" style="font-family: 'S-CoreDream-3Light';">
                    <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <RouterLink :to="{ name: 'DepositSavingView'}" class="text-decoration-none text-black nav-link">예적금 상품 비교</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink :to="{ name: 'ExchangeRateView'}" class="text-decoration-none text-black nav-link">환율 계산</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink :to="{ name: 'BankPosView'}" class="text-decoration-none text-black nav-link">내 주변 은행</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink :to="{ name: 'ArticleList'}" class="text-decoration-none text-black nav-link">커뮤니티</RouterLink>
                    </li>
                    </ul>
                </div>
                </div>

        </nav>

    </div>
    <RouterView></RouterView>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
const store = useCounterStore()
</script>

<style scoped>
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.poppins-medium {
  font-family: "Poppins", sans-serif;
  font-weight: 500;
  font-style: normal;
}
html {
    min-width: 470px;
}
</style>