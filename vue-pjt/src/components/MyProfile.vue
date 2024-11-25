<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
        
        <h2 class="poppins-bold mb-5">
            <span class="text-highlight">{{ userInfo.username }}</span>
            <span>님의 프로필</span>
        </h2>

        <div class="d-flex col-8">
            <!-- 좌측: 프로필 사진과 수정하기 버튼 -->
            <div class="profile-left">
                <!-- <img class="profile-image" :src="profileImageUrl" alt="프로필 사진" /> -->
                <img class="profile-image" src="/profile/profile.png" alt="프로필 사진">
                <button class="profile-btn" type="button" @click="editProfile">
                    프로필 수정
                </button>
            </div>

            <!-- 우측: 상단 네모 박스 3개와 하단 테이블 -->
            <div class="profile-right">
                <!-- 우측 상단: 네모 박스 3개 -->
                <div class="d-flex justify-content-center mb-4">
                    <div class="stat-box">
                        <div>{{ daysSinceJoined }}</div>
                        <div>함께한지</div>
                    </div>
                    <div class="stat-box">
                        <div>{{  }}</div>
                        <div>게시글</div>
                    </div>
                    <div class="stat-box">
                        <div>{{  }}</div>
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
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">직업</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">부양 가족</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">소비 성향</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">소득 수준</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold">자신</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
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

onMounted(() => {
    // 프로필 바뀌거나, 상품 등록시 인포 바꾸도록 수정 
  store.loadUserInfo(store.accessToken)
})

</script>

<style scoped>
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
  width: 25%;  /* 고정된 너비로 설정 */
  height: 125px; /* 고정된 높이로 설정 */
  border: 1px solid #D7D5D5;
  padding: 15px;
  text-align: center;
  font-weight: bold;
  flex-direction: column;
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
    background-color: white;
    border: 1.5px solid #79F297;
    border-radius: 20px;
}
</style>