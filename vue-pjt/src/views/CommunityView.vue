<template>
    <div>
        <div class="col-12 d-flex justify-content-center flex-column align-items-center my-5">
        <div class="d-flex justify-content-center">
            <h2 class="fs-2 coredream-bold">
                <span class="text-highlight">정보 공유</span>
                게시판
            </h2>
        </div>
        </div>
        <router-view />
    </div>
</template>

<script setup>
</script>

<style scoped>
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.coredream-bold {
font-family: 'S-CoreDream-3Light';
font-weight: bold;
font-style: normal;
}
.text-highlight{
    color: #79F297;
}
</style>