<template>
    <div class="d-flex justify-content-center">
        <div id="carouselExampleRide" class="carousel slide d-flex flex-column justify-content-center col-8 mt-3" data-bs-ride="carousel">
            <div class="container-fluid d-flex justify-content-center">
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <RouterLink :to="{ name: 'MyPageView'}">
                            <img src="/carousel/carousel1.png" class="d-block w-100 rounded" alt="Slide 1">
                        </RouterLink>
                    </div>
                    <div class="carousel-item">
                        <RouterLink :to="{ name: 'DepositSavingView'}">
                            <img src="/carousel/carousel2.png" class="d-block w-100 rounded" alt="Slide 2">
                        </RouterLink>
                    </div>
                    <div class="carousel-item">
                        <RouterLink :to="{ name: 'ExchangeRateView'}">
                            <img src="/carousel/carousel3.png" class="d-block w-100 rounded" alt="Slide 3">
                        </RouterLink>
                    </div>
                </div>
            </div>

            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleRide" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleRide" data-bs-slide-to="1" aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleRide" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>
            <br>
            <div class="d-flex justify-content-evenly align-items-start">
                <!-- 환율 정보 -->
                <ExchangeRate></ExchangeRate>
                <!-- 예적금 best -->
                <BestProduct></BestProduct>
            </div>
            <br>
        </div>
    </div>
</template>

<script setup>
import BestProduct from '@/components/BestProduct.vue';
import ExchangeRate from '@/components/ExchangeRate.vue';
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
.carousel-indicators {
    position: relative;
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 20px;
}

.carousel-indicators button {
    width: 10px;
    height: 10px;
    border-radius: 50%; 
    background-color: #ccc; 
    border: none; 
    transition: background-color 0.3s ease, width 0.3s ease;; 
}

.carousel-indicators button.active {
    background-color: #79F297; 
    width:25px;
    border-radius: 20px;
}

</style>