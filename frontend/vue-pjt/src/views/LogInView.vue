<template>
    <div class="col-12 d-flex justify-content-center flex-column align-items-center pt-lg-5" style="font-family: 'S-CoreDream-3Light';">
      <div>
        <div class="fs-2 d-flex align-items-center">
          <span class="pe-2 poppins-bold mb-1">나에게 Fit한 Finance,</span>
          <img src="/logo/Logo2.png" width="94" height="31"><br>
        </div>
        <p class="fs-6 text-center mb-4">손 쉬운 금융 생활을 위해 로그인을 해주세요</p>
      </div>
      <div class="col-4">
        <form @submit.prevent="logIn">
          <div class="form-floating mb-3">
            <input type="text" id="username" v-model.trim="username" placeholder="ID"
              class="login-form form-control poppins-regular ps-4 mb-2"/>
            <label for="username">ID</label>
          </div>
          <div class="form-floating mb-3">
            <input type="password" id="password" v-model.trim="password" placeholder="Password"
              class="login-form form-control poppins-regular ps-4 mb-4"/>
            <label for="password">Password</label>
          </div>
          <button type="submit" class="btn login-box form-control text-light fs-6 mb-4 border-none">로그인 하기</button>
        </form>
        <img src="/login/line.png" class="w-100">
      </div>
      <br>
      <KakaoLogin @kakaoLogin="handleKakaoLoginSuccess" />
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useCounterStore } from "@/stores/counter";
  import KakaoLogin from "@/components/KakaoLogin.vue";
  import axios from "axios";

  
  // 상태 관리
  const store = useCounterStore();
  const username = ref(null);
  const password = ref(null);
  
  // 일반 로그인 처리 함수
  const logIn = () => {
    const payload = {
      username: username.value,
      password: password.value,
    };
    store.logIn(payload);
  };
  
  // 카카오 로그인 성공 처리 함수
  const handleKakaoLoginSuccess = (email) => {
    const userEmail = email
    store.socialLogIn(userEmail)
  };
  </script>
  
  <style scoped>
  @font-face {
     font-family: 'S-CoreDream-3Light';
     src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
     font-weight: normal;
     font-style: normal;
}
  .login-form {
    box-sizing: border-box;
    height: 70px;

    border: 1px solid #ccc;
    border-radius: 20px;
  }
  .poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
  .poppins-regular {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
  .login-box {
    border-radius: 20px;
    background-color: #203359;
    height: 70px;
  }
  .poppins-semibold {
    font-family: "Poppins", sans-serif;
    font-weight: 600;
    font-style: normal;
  }
  input:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
    background-color: transparent !important;
  }
  .btn:focus {
    border:none !important;
    box-shadow: none !important;
    background-color: #203359 !important;
  }

  input:active {
    background-color: inherit !important; 
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
  }
  .btn:active {
    border:none !important;
    box-shadow: none !important;
    background-color: #203359 !important;
  }
  .btn:hover {
    border:none !important;
    background-color: #203359 !important;
    outline: none !important;
    transform: none !important;
  }

 
  </style>
  