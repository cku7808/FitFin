<template>
  <div>
    <a id="custom-login-btn" @click="kakaoLogin()">
      <img
        src="/login/kakao.png"
        width="55"
        alt="카카오 로그인 버튼"
      />
    </a>
    <!-- <div @click="kakaoLogout()">로그아웃</div> -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    kakaoLogin() {
      window.Kakao.Auth.login({
        scope: "profile_nickname, account_email",
        success: this.getKakaoAccount,
      });
    },
    getKakaoAccount() {
      window.Kakao.API.request({
        url: "/v2/user/me",
        success: (res) => {
          const kakao_account = res.kakao_account;
          const email = kakao_account.email;

          //로그인처리구현
          this.$emit('kakaoLogin', email)
        },
        fail: (error) => {
          console.log(error);
        },
      });
    },
    kakaoLogout() {
      window.Kakao.Auth.logout((res) => {
        console.log(res);
      });
    },
  },
};
</script>