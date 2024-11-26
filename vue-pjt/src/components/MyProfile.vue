<template>
    <div class="d-flex align-items-center justify-content-center flex-column score-dream">
        
        <h2 class="mb-5 score-dream-bold">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님의 프로필</span>
        </h2>

        <div class="d-flex col-8">
            <!-- 좌측: 프로필 사진과 수정하기 버튼 -->
            <div class="profile-left">
                <img class="profile-image" src="/profile/profile.png" alt="프로필 사진">
                <button class="profile-btn" type="button" @click="editProfile">
                    프로필 수정
                </button>
            </div>

            <!-- 우측: 상단 네모 박스 3개와 하단 테이블 -->
            <div class="profile-right">
                <!-- 우측 상단: 네모 박스 3개 -->
                <div class="d-flex justify-content-center mb-4 align-items-center">
                    <div class="stat-box">
                        <div>{{ daysSinceJoined }}</div>
                        <div>함께한지</div>
                    </div>
                    <div class="stat-box">
                        <div>{{ postsCount }}</div>
                        <div>게시글</div>
                    </div>
                    <div class="stat-box">
                        <div>{{ likesCount }}</div>
                        <div>좋아요</div>
                    </div>
                </div>

                <!-- 테이블 -->
                <div class="table-container">
                    <table class="profile-table">
                    <tbody>
                        <tr>
                        <td class="font-weight-bold">이메일</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">나이</td>
                        <td>{{ userInfo.age }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">직업</td>
                        <td>{{ userInfo.job }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">혼인여부</td>
                        <td>{{ is_married }}</td>
                        </tr>
                        <!-- <tr>
                        <td class="font-weight-bold">소비 성향</td>
                        <td>{{ userInfo.email }}</td>
                        </tr> -->
                        <tr>
                        <td class="font-weight-bold">소득수준</td>
                        <td>{{ userInfo.income }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">자산</td>
                        <td>{{ userInfo.assets }}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const router = useRouter();
const store = useCounterStore();
const userInfo = computed(() => store.userInfo);

// 프로필 수정 페이지로 이동
const editProfile = () => {
  router.push({ name: "MyProfileEdit" });
};

// 가입 날짜 계산
const daysSinceJoined = computed(() => {
  if (!userInfo.value.date_joined) return 0;
  const joinedDate = new Date(userInfo.value.date_joined);
  const today = new Date();
  const timeDifference = today - joinedDate;
  const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  return daysDifference;
});

// 게시글 및 좋아요 수 (예시로 고정값 사용)
const postsCount = 10;
const likesCount = 15;

onMounted(() => {
    // 프로필 바뀌거나, 상품 등록시 인포 바꾸도록 수정 
  store.loadUserInfo(store.accessToken)
})
const is_married = ref(userInfo.value.is_married); // 초기값 설정
console.log(userInfo.value)
// userInfo.value.is_married 값에 따라 초기화
if (userInfo.value.is_married === true) {
    is_married.value = "기혼";
} else if (userInfo.value.is_married === false) {
    is_married.value = "미혼";
}

</script>

<style scoped>
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.score-dream {
  font-family: 'S-CoreDream-3Light';
}
.score-dream-bold {
  font-family: 'S-CoreDream-3Light';
  font-weight: bold;
}
/* 좌측: 프로필 사진과 수정하기 버튼 */
.profile-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  padding: 20px;
}
/* 프로필 이미지 */
.profile-image {
  width: 70%;
  /* height: 100px; */
  border-radius: 50%;
  margin-bottom: 20px;
}

/* 우측 상단: 네모 박스 3개 */
.profile-right {
  display: flex;
  flex-direction: column;
  width: 50%;
}
/* 각 박스 요소 */
.stat-box {
  width: 25%;
  height: 125px;
  border: 1px solid #D7D5D5;
  padding: 15px;
  text-align: center;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 우측 하단: 테이블 */
.table-container {
  padding: 10px;
}
.profile-table {
  width: 100%;
  border-collapse: collapse;
}
.profile-table th,
.profile-table td {
  padding: 12px;
  border-bottom: 1px solid #D7D5D5;
  text-align: left;
}

/* 글씨 */
.poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
.text-highlight{
    color: #79F297;
}

/* 프로필 수정 버튼 */
.profile-btn{
    width: 120px;
    height: 40px;
    background-color: #203359;
    border: none;
    color: white;
    border-radius: 20px;
}
</style>