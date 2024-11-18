import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const router = useRouter()

  const signUp = function (payload) {
    const { username, email, password1, password2 } = payload 

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2
      }
    })
    .then(res => {
      console.log('회원가입 완료')
      router.push({name:'LogInView'})
    })
    .catch(err => {
      console.log(err)
    })
  }
  const logIn = (payload) => {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password },
    })
      .then((res) => {
        console.log('로그인 완료');
        console.log(res.data)
        accessToken.value = res.data.accessToken;
        refreshToken.value = res.data.refreshToken;
        router.push({ name: 'MainView' });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  // 소셜 로그인
  const socialLogIn = (email) => {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/social_login/`,
      data: { email },
    })
      .then((res) => {
        console.log('소셜 로그인 완료');
        accessToken.value = res.data.access;
        refreshToken.value = res.data.refresh;
        router.push({ name: 'MainView' });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return { API_URL, logIn, socialLogIn, accessToken, refreshToken };
}, { persist: true });

