<template>
    <div class="col-12 d-flex justify-content-center flex-column align-items-center">
      <div>
        <div class="fs-2 d-flex align-items-center">
          <span class="pe-2">나에게 Fit한 Finance,</span>
          <img src="@/assets/images/logo/Logo2.png" width="94" height="31"><br>
        </div>
        <p class="fs-6">손 쉬운 금융 생활을 위해 로그인을 해주세요</p>
      </div>
      <div class="">
        <form @submit.prevent="logIn">
          <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력해주세요." 
            class="login-form login-box col-12"
          /><br />
          <input type="password" id="password" v-model.trim="password" placeholder="비밀번호를 입력해주세요."
            class="login-form pw-box col-12"
          /><br />
    
          <input type="submit" value="Log In" />
        </form>
      </div>
  
      <KakaoLogin @kakaoLogin="handleKakaoLoginSuccess" />
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useCounterStore } from "@/stores/counter";
  import KakaoLogin from "@/components/KakaoLogin.vue";
  import axios from "axios";

  const BASE_URL = 'http://127.0.0.1:8000'
  
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
  .login-form {
    box-sizing: border-box;
    height: 80px;

    border: 1px solid #79F297;
    border-radius: 20px;
  }


 
  </style>
  