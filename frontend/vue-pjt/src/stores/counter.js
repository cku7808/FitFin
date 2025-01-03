import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const BASE_URL = 'https://django-backend-service-579042790724.asia-northeast1.run.app'
  const accessToken = ref(null);
  const refreshToken = ref(null);
  const router = useRouter()

  const isLogin = computed(() => {
    return accessToken.value === null ? false : true
  })

  const signUp = function (payload) {
    const { 
      username, email, password1, password2,
      income, assets, is_married, job, age, credit

     } = payload 

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2,
        income, assets, is_married, job, age, credit
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
        accessToken.value = res.data.key;

        loadUserInfo(header.value)
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
        loadUserInfo(header.value)
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
  const loginType = computed(() => {
    return refreshToken.value === null ? 'general' : 'social'
  })

// console.log(isLogin.value)

const header = computed(() => {
  if (isLogin.value === true & loginType.value === 'general') {
    return {Authorization: `Token ${accessToken.value}`}
  } else {
    return {Authorization: `Bearer ${accessToken.value}`}
  }
})

  // 사용자 정보
const userInfo = ref(null)
const loadUserInfo = (header) => {
  axios({
        method: 'get',
        url: `${BASE_URL}/api/v1/userinfo/`,
        headers: header
  })
  .then((res) => {
      console.log(res.data)
      userInfo.value = res.data
  })
  .catch((err) => {
      console.log(err)
  })
}

  return { BASE_URL, logIn, socialLogIn, accessToken, refreshToken, signUp, isLogin, logOut, userInfo, loadUserInfo, header };
}, { persist: true });

