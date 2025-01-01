<template>
<div class="container mt-5 d-flex flex-column align-items-center" style="font-family: 'S-CoreDream-3Light'; font-weight: 500;">
    <div class="text-center">
        <img src="/logo/Logo2.png" width="120" height="40">
        <p class="mb-4 fs-5 mt-2">FitFin에 오신 것을 환영합니다!</p>
    </div>
    <div class="d-flex flex-column col-8">
        <form @submit.prevent="signUp">
            <div class="form-group mb-3">
                <div class="input-group">
                    <input type="text" id="username" class="form-control login-form poppins-regular rounded-4 col-10" v-model.trim="username" placeholder="아이디를 입력해주세요">
                    <button type="button" class="rounded-4 bt col-2 ms-3" @click="idCheck">중복 확인</button>
                </div>
            </div>
    
            <div class="form-group mb-3">
                <div class="input-group">
                    <input type="email" id="email" class="form-control login-form rounded-4 poppins-regular col-10" v-model.trim="email" placeholder="이메일을 입력해주세요">
                    <!-- <button type="button" class="rounded-4 bt col-2 ms-3">이메일 인증</button> -->
                </div>
            </div>
            <div class="form-group mb-3 d-flex gap-3 align-items-center">
                <div class="w-50">
                    <input type="password" id="password1" class="form-control login-form poppins-regular rounded-4" v-model.trim="password1" placeholder="비밀번호를 입력해주세요"
                    @input="checkPasswords">
                </div>
        
                <div class="w-50">
                    <input type="password" id="password2" class="form-control login-form poppins-regular rounded-4" v-model.trim="password2" placeholder="비밀번호를 다시 입력해주세요"
                    @input="checkPasswords">
                </div>
                <div id="password-feedback" class="feedback" aria-live="polite"></div>
            </div>

            <div class="form-group mb-3 d-flex gap-3">
                <!-- 소득 슬라이더 -->
                <div class="w-50">
                    <label for="income-range" class="form-label">소득 수준을 입력해주세요</label>
                    <div class="slider-container">
                        <input
                            type="range"
                            id="income-range"
                            class="form-range"
                            v-model="income"
                            :min="0"
                            :max="100000"
                            @input="updateThumbPosition('income', $event)"
                            ref="incomeSlider"
                        />
                        <!-- <div class="label" :style="{ right: '0px' }">
                            {{ formatNumber(income * 10000) }}원 ({{ convertToKorean(income * 10000) }})
                        </div> -->
                        <div class="label" :style="{ right: '0px' }">
                            {{ convertToKorean(income * 10000) }}
                        </div>
                    </div>
                </div>

                <!-- 자산 슬라이더 -->
                <div class="w-50">
                    <label for="assets-range" class="form-label">보유 자산 규모를 입력해주세요</label>
                    <div class="slider-container">
                        <input
                            type="range"
                            id="assets-range"
                            class="form-range"
                            v-model="assets"
                            :min="0"
                            :max="100000"
                            @input="updateThumbPosition('assets', $event)"
                            ref="assetsSlider"
                        />
                        <!-- <div class="label" :style="{ right: '0px' }">
                            {{ formatNumber(assets * 10000) }}원 ({{ convertToKorean(assets * 10000) }})
                        </div> -->
                        <div class="label" :style="{ right: '0px' }">
                            {{ convertToKorean(assets * 10000) }}
                        </div>
                    </div>
                </div>
            </div>



            <div class="wrap">
                <div class="radio_area w-50 me-2">
                    <input type="radio" name="married" id="married" value="true" v-model="married">
                    <label for="married"><span></span>기혼</label>  
                </div>
                <div class="radio_area w-50 ms-2">
                    <input type="radio" name="married" id="notmarried" value="false" v-model="married">
                    <label for="notmarried"><span></span>미혼</label>  
                </div>  
            </div>
            <br>
            <div class="form-group mb-3 d-flex">
                <select name="selectJob" id="selectJob" class="form-select form-control form-control login-form w-50 me-2" aria-label="Default select example" v-model.trim="job">
                    <option value="" disabled selected>직업을 선택해주세요</option>
                    <option value="무직">무직</option>
                    <option value="직장인">직장인</option>
                    <option value="공무원">공무원</option>
                    <option value="자영업자">자영업자</option>
                    <option value="주부">주부</option>
                </select>

                <div class="w-50 me-2">
                    <input type="number" id="age" class="form-control login-form poppins-regular" v-model="age" placeholder="나이를 입력해주세요">
                </div>
                
                <div class="w-50">
                    <input type="number" id="credit" class="form-control login-form poppins-regular" v-model="credit" placeholder="신용 점수를 입력해주세요">
                </div>
            </div>
    
            <div class="text-center">
                <input type="submit" value="회원가입" class="bt w-100 rounded-4 h-25" style="height: 70px !important;">
            </div>
        </form>
    </div>
</div>

</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';

const store = useCounterStore()

const email = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const income = ref(0)
const assets = ref(0)
const married = ref(false)
const job = ref('')
const age = ref(null)
const credit = ref(null)

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
        credit: credit.value
    }
    console.log(payload)
    store.signUp(payload)
}

const idCheck = () => {
    axios({
        method: 'post',
        url: `${store.BASE_URL}/api/v1/id_check/`,
        data: {
            username: username.value
        }
    })
    .then((res) => {
        console.log(res.data)
        alert("사용 가능한 ID 입니다")
    })
    .catch((err) => {
        console.log(err)
        alert("이미 존재하는 ID 입니다")
        username.value = ""
    })
}

// 숫자를 천 단위로 포맷
const formatNumber = (value) => {
    if (value === null || value === undefined) {
        return "0";
    }
    return Number(value).toLocaleString(); // 천 단위 콤마 추가
};

// 숫자를 한글 단위로 변환
const convertToKorean = (num) => {
    if (num === 0) return "0원";

    const units = ["", "만", "억", "조", "경"];
    let unitIndex = 0;
    let koreanNumber = "";

    while (num > 0) {
        const chunk = num % 10000; // 4자리씩 끊어서 처리
        if (chunk > 0) {
            koreanNumber = `${chunk}${units[unitIndex]} ${koreanNumber}`;
        }
        num = Math.floor(num / 10000);
        unitIndex++;
    }

    return koreanNumber.trim(); // 마지막 공백 제거
};

// 슬라이더 값을 업데이트
const updateThumbPosition = (type, event) => {
    const slider = type === "income" ? incomeSlider.value : assetsSlider.value;
    if (!slider) return;

    if (type === "income") {
        income.value = Number(event.target.value); // 슬라이더 값 반영
    } else if (type === "assets") {
        assets.value = Number(event.target.value); // 슬라이더 값 반영
    }
};

const checkPasswords = () => {
    const feedback = document.getElementById("password-feedback");
    // 초기 상태: 입력값이 없으면 feedback 숨기기
    if (password1.value === "" && password2.value === "") {
        feedback.innerHTML = "";
        feedback.classList.remove("visible");
        return;
    }

    // 입력값이 있을 때 feedback 표시
    feedback.classList.add("visible");

    // 비밀번호 일치 여부 확인
    if (password1.value === password2.value) {
        feedback.innerHTML = `
            <span><img src="/etc/check.png" width="30" height="30"> 비밀번호가 일치합니다</span>
        `;
        feedback.classList.remove("error");
        feedback.classList.add("success");
    } else {
        feedback.innerHTML = `
            <span><img src="/etc/red_check.png" width="30" height="30"> 비밀번호가 일치하지 않습니다</span>
        `;
        feedback.classList.remove("success");
        feedback.classList.add("error");
    }
};


</script>

<style scoped>
@font-face {
     font-family: 'S-CoreDream-3Light';
     src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
     font-weight: normal;
     font-style: normal;
}
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
  .form-select:focus {
    border: 1px solid #79F297 !important;
    box-shadow: none !important;
  }
  .form-select:active {
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
    border: none;
  }
  .form-group {
  display: flex;
  justify-content: space-between;
}

.slider-container {
  position: relative;
  width: 100%;
}

input[type="range"] {
  width: 100%;
  appearance: none;
  height: 8px;
  background: #e0e0e0;
  border-radius: 5px;
  outline: none;
  transition: background 0.3s;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 15px;
  height: 15px;
  background: #79F297;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 15px;
  height: 15px;
  background: #2d3e50;
  border-radius: 50%;
  cursor: pointer;
}

.label {
  position: absolute;
  top: -30px; /* 슬라이더 thumb 위에 위치 */
  background: #2d3e50;
  color: white;
  padding: 3px 8px;
  border-radius: 5px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none; /* 클릭 방지 */
  right: 0; /* 항상 오른쪽에 고정 */
}

.wrap {display:flex;flex-flow:row;justify-content: center;gap:5px;}

.wrap .radio_area label{cursor:pointer;display:flex;align-items:center;gap:15px;height:40px;padding:0 18px 0 15px;border-radius:30px;font-size:15px;font-weight:500;color:#999;background:#f2f2f2;transition:all .2s}
.wrap .radio_area label span{opacity:.3;display:flex;width:18px;height:18px;border:2px solid #2d3e50;border-radius:50%;transition:all .2s}
.wrap .radio_area label span:before{content:"";width:6px;height:6px;margin:auto;border-radius:50%;background:#2d3e50;transition:all .2s}
.wrap .radio_area label:hover{background:#e1e1e1}
.radio_area input[type=radio]{display:none}
.radio_area input[type=radio]:checked + label{color:#79F297;background:#2d3e50}
.radio_area input[type=radio]:checked + label span{opacity:1;border-color:#79F297}
.radio_area input[type=radio]:checked + label span:before{background:#79F297}

input {
    font-family: 'S-CoreDream-3Light';
}
input::placeholder {
    font-family: 'S-CoreDream-3Light';
}
.feedback {
    display: none; /* 초기에는 표시하지 않음 */
    font-size: 14px;
    margin-top: 5px;
    align-items: center;
    white-space: nowrap;
    justify-content: space-between;
    color: inherit; /* 부모 색상 상속 */
}

.feedback.visible {
    display: flex; /* 입력값이 있을 때 표시 */
    width: 32%; /* 입력 필드와 동일한 너비 */
}

.feedback .icon {
    margin-left: 8px; /* 아이콘과 텍스트 간의 간격 */
    flex-shrink: 0; /* 아이콘이 줄어들지 않도록 */
}


</style>