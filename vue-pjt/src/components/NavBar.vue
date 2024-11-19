<template>
    <div>
        <nav class="navbar navbar-expand-lg">
            <!-- <div class="container-fluid">
                <div>
                    <RouterLink :to="{ name: 'MainView'}">
                        <img src="@/assets/images/logo/Logo.png" alt="Bootstrap" width="110" height="49" class="ms-2">
                    </RouterLink>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                </div>
                
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-4">
                        <li class="nav-item poppins-regular">
                            <RouterLink :to="{ name: 'CompareProductView'}" class="text-decoration-none text-black">예적금 상품 비교</RouterLink>&nbsp&nbsp
                        </li> 
                        <li class="nav-item poppins-regular">
                            <RouterLink :to="{ name: 'ExchangeRateView'}" class="text-decoration-none text-black">환율 계산</RouterLink>&nbsp&nbsp
                        </li>
                        <li class="nav-item poppins-regular">
                            <RouterLink :to="{ name: 'BankPosView'}" class="text-decoration-none text-black">내 주변 은행</RouterLink>&nbsp&nbsp
                        </li>
                        <li class="nav-item poppins-regular">
                            <RouterLink :to="{ name: 'CommunityView'}" class="text-decoration-none text-black">커뮤니티</RouterLink>
                        </li>
                    </ul>
                </div>

                <div class="navbar-expand-lg justify-content-end" id="navbarNavDropdown" v-if="store.isLogin">
                    <ul class="navbar-nav d-flex flex-row">
                        <li class="nav-item">
                            <a @click="store.logOut()" style="cursor: pointer;">
                                <img src="@/assets/images/navbar/Logout.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </a>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'SignUpView'}">
                                <img src="@/assets/images/navbar/Mypage.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'LogInView'}">
                                <img src="@/assets/images/navbar/Cart.png" alt="Bootstrap" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                </div>

                <div class="navbar-expand-lg justify-content-end" id="navbarNavDropdown" v-else>
                    <ul class="navbar-nav d-flex flex-row">
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'SignUpView'}">
                                <img src="@/assets/images/navbar/Signup.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'LogInView'}">
                                <img src="@/assets/images/navbar/Login.png" alt="Bootstrap" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                </div>
            </div> -->
        
            <div class="container-fluid position-relative d-flex">
                <!-- 로고와 토글 버튼 -->
                <div class="d-flex align-items-center">
                    <RouterLink :to="{ name: 'MainView'}">
                    <img src="@/assets/images/logo/Logo.png" alt="FitFin Logo" width="110" height="49" class="me-2">
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
                    <ul class="navbar-nav d-flex flex-row">
                    <li class="nav-item" v-if="store.isLogin">
                        <a @click="store.logOut()" style="cursor: pointer;">
                        <img src="@/assets/images/navbar/Logout.png" alt="Logout" width="80" height="19" class="me-2">
                        </a>
                    </li>
                    <li class="nav-item" v-if="store.isLogin">
                        <RouterLink :to="{ name: 'MyPageView'}">
                        <img src="@/assets/images/navbar/Mypage.png" alt="Mypage" width="80" height="19" class="me-2">
                        </RouterLink>
                    </li>
                    <li class="nav-item" v-if="store.isLogin">
                        <RouterLink :to="{ name: 'CartView'}">
                        <img src="@/assets/images/navbar/Cart.png" alt="Cart" width="80" height="19">
                        </RouterLink>
                    </li>
                    <li class="nav-item" v-else>
                        <RouterLink :to="{ name: 'SignUpView'}">
                        <img src="@/assets/images/navbar/Signup.png" alt="Signup" width="80" height="19" class="me-2">
                        </RouterLink>
                    </li>
                    <li class="nav-item" v-else>
                        <RouterLink :to="{ name: 'LogInView'}">
                        <img src="@/assets/images/navbar/Login.png" alt="Login" width="80" height="19">
                        </RouterLink>
                    </li>
                    </ul>
                </div>

                <!-- 메뉴 -->
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto">
                    <li class="nav-item poppins-regular">
                        <RouterLink :to="{ name: 'CompareProductView'}" class="text-decoration-none text-black nav-link">예적금 상품 비교</RouterLink>
                    </li>
                    <li class="nav-item poppins-regular">
                        <RouterLink :to="{ name: 'ExchangeRateView'}" class="text-decoration-none text-black nav-link">환율 계산</RouterLink>
                    </li>
                    <li class="nav-item poppins-regular">
                        <RouterLink :to="{ name: 'BankPosView'}" class="text-decoration-none text-black nav-link">내 주변 은행</RouterLink>
                    </li>
                    <li class="nav-item poppins-regular">
                        <RouterLink :to="{ name: 'CommunityView'}" class="text-decoration-none text-black nav-link">커뮤니티</RouterLink>
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
.poppins-regular {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
html {
    min-width: 470px;
}
</style>