import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
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
    })
    .catch(err => {
      console.log(err)
    })
  }
  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
    .then(res => {
      console.log('로그인 완료')
      token.value = res.data.key
    })
    .catch(err => {
      console.log(err)
    })
  }
  return { API_URL, signUp, logIn, token }
}, { persist: true })
