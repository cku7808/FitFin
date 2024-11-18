<template>
    <div>
      <h1>Login page</h1>
      <form @submit.prevent="logIn">
        <label for="username">ID : </label>
        <input type="text" id="username" v-model.trim="username" /><br />
  
        <label for="password">Password : </label>
        <input type="password" id="password" v-model.trim="password" /><br />
  
        <input type="submit" value="Log In" />
      </form>
  
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
  /* 스타일링 필요시 추가 */
  </style>
  