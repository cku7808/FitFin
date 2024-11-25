import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const router = useRouter()

  const isLogin = computed(() => {
    return accessToken.value === null ? false : true
  })

  const signUp = function (payload) {
    const { 
      username, email, password1, password2,
      income, assets, is_married, job, age

     } = payload 

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2,
        income, assets, is_married, job, age
      }
    })
    .then(res => {
      console.log('회원가입 완료')
      router.push({name:'LogInView'})
    })
    .catch(err => {
      console.log(err)
      alert('회원가입 실패')
    })
  }
  
  const logIn = (payload) => {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/login/`,
      data: { username, password },
    })
      .then((res) => {
        console.log('로그인 완료');
        console.log(res.data)
        accessToken.value = res.data.access;
        refreshToken.value = res.data.refresh;
        loadUserInfo(res.data.access)
        router.push({ name: 'MainView' });
      })
      .catch((err) => {
        console.error(err);
        alert('로그인 실패 : 가입되지 않은 회원이거나 비밀번호가 일치하지 않습니다')
      });
  };

  // 소셜 로그인
  const socialLogIn = (email) => {
    axios({
      method: 'post',
      url: `${BASE_URL}/api/v1/social_login/`,
      data: { email },
    })
      .then((res) => {
        console.log('소셜 로그인 완료');
        accessToken.value = res.data.access;
        refreshToken.value = res.data.refresh;
        loadUserInfo(res.data.access)
        router.push({ name: 'MainView' });
      })
      .catch((err) => {
        console.error(err);
        alert('가입되지 않은 사용자입니다.')
        router.push({name: 'SignUpView'})
      });
  };

  const logOut = function () {
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        accessToken.value = null
        refreshToken.value = null
        userInfo.value = null
        router.push({ name: 'MainView' })
        alert('로그아웃되었습니다.')
      })
      .catch((err) => {
        console.log(err)
      })
  };

  // 사용자 정보
  const userInfo = ref(null)
  const loadUserInfo = (token) => {
    axios({
        method: 'get',
        url: `${BASE_URL}/api/v1/userinfo/`,
        headers: {
            Authorization: `Bearer ${token}`, // JWT Access Token 포함
        },
    })
    .then((res) => {
        console.log(res.data)
        userInfo.value = res.data
    })
    .catch((err) => {
        console.log(err)
    })
}


  return { BASE_URL, logIn, socialLogIn, accessToken, refreshToken, signUp, isLogin, logOut, userInfo, loadUserInfo };
}, { persist: true });

