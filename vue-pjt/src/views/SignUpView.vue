<template>
<div class="container mt-5 d-flex flex-column align-items-center">
    <div class="text-center">
        <img src="/logo/Logo2.png" width="120" height="40">
        <p class="mb-4 fs-4 poppins-regular">FitFin에 오신 것을 환영합니다!</p>
    </div>
    <div class="d-flex flex-column col-8">
        <form @submit.prevent="signUp">
            <div class="form-group mb-3">
                <div class="input-group">
                    <input type="text" id="username" class="form-control login-form poppins-regular rounded-4 col-10" v-model.trim="username" placeholder="아이디를 입력해주세요">
                    <button type="button" class="rounded-4 bt col-2 ms-3">중복 확인</button>
                </div>
            </div>
    
            <div class="form-group mb-3">
                <div class="input-group">
                    <input type="email" id="email" class="form-control login-form rounded-4 poppins-regular col-10" v-model.trim="email" placeholder="이메일을 입력해주세요">
                    <button type="button" class="rounded-4 bt col-2 ms-3">이메일 인증</button>
                </div>
            </div>
            <div class="form-group mb-3 d-flex gap-3">
                <div class="w-50">
                    <input type="password" id="password1" class="form-control login-form poppins-regular rounded-4" v-model.trim="password1" placeholder="비밀번호를 입력해주세요">
                </div>
        
                <div class="w-50">
                    <input type="password" id="password2" class="form-control login-form poppins-regular rounded-4" v-model.trim="password2" placeholder="비밀번호를 다시 입력해주세요">
                </div>
            </div>
            <div class="form-group mb-3 d-flex gap-3">
                <div class="w-50">
                    <label for="range" class="form-label">소득 수준을 입력해주세요</label>
                    <input type="range" id="range" class="form-range" v-model="income" min="0" max="1000000">
                    <p>{{ income }}</p>
                </div>
    
                <div class="w-50">
                    <label for="range" class="form-label">보유 자산 규모를 입력해주세요</label>
                    <input type="range" id="assets" class="form-range" v-model="assets" min="0" max="1000000">
                    <p>{{ assets }}</p>
                </div>
            </div>

            <!-- <div class="form-group mb-3">
                <div class="form-check">
                    <input type="radio" id="married" name="married" class="form-check-input poppins-regular rounded-4" v-model.trim="married">
                    <label for="married" class="form-check-label">기혼</label>
                </div>
                <div class="form-check">
                    <input type="radio" id="notmarried" name="married" class="form-check-input poppins-regular rounded-4" v-model.trim="married">
                    <label for="notmarried" class="form-check-label">미혼</label>
                </div>
            </div> -->

            <div class="form-check">
                <input class="form-check-input" type="radio" name="married" id="married">
                <label class="form-check-label" for="married">
                    기혼
                </label>
                </div>
                <div class="form-check">
                <input class="form-check-input" type="radio" name="married" id="notmarried" checked>
                <label class="form-check-label" for="notmarried">
                    미혼
                </label>
            </div>
    
            <div class="form-group mb-3">
                <input type="text" id="job" class="form-control login-form poppins-regular" v-model.trim="job" placeholder="직업을 입력해주세요">
            </div>
    
            <div class="form-group mb-3">
                <input type="number" id="age" class="form-control login-form poppins-regular" v-model.trim="age" placeholder="나이를 입력해주세요">
            </div>
    
            <div class="text-center">
                <input type="submit" value="회원가입" class="bt mt-3">
            </div>
        </form>
    </div>
</div>

</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

const email = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const income = ref(null)
const assets = ref(null)
const married = ref(null)
const job = ref(null)
const age = ref(null)

const signUp = function () {
    const payload = {
        email: email.value,
        username: username.value,
        password1: password1.value,
        password2: password2.value,
        income: income.value,
        assets: assets.value,
        is_married: married.value,
        job: job.value,
        age: age.value,
    }
    console.log(payload.value)
    store.signUp(payload)
}

</script>

<style scoped>
input:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
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
  .bt {
    background-color: #203359;
    color: white;
  }
</style>