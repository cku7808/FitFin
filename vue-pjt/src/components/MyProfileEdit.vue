<template>
    <div class="d-flex align-items-center justify-content-center flex-column">
      <h2 class="poppins-bold mb-5">
        <span class="text-highlight">{{ userInfo.username }}</span>
        <span>님의 프로필 수정</span>
      </h2>
  
      <div class="d-flex col-8">
        <!-- 좌측: 프로필 사진과 수정하기 버튼 -->
        <div class="profile-left">
          <input type="file" @change="onImageChange" class="image-upload m-3 form-control" />
          <img class="profile-image" :src="profileImageUrl" alt="프로필 사진" />
          
          <button type="submit" class="profile-btn">저장하기</button>
        </div>
  
        <!-- 우측: 상단 네모 박스 3개와 하단 입력 폼 -->
        <div class="profile-right">
          <!-- 우측 상단: 네모 박스 3개 -->
          <div class="d-flex justify-content-center mb-4">
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
  
          <!-- 우측 하단: 입력 폼 -->
          <div class="form-container">
            <form @submit.prevent="editProfile">
                <table class="profile-table">
                <tbody>
                        <tr>
                        <td class="font-weight-bold">이메일</td>
                        <td>{{ userInfo.email }}</td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="age">나이</label></td>
                        <td><input type="number" id="age" v-model="userInfo.age" class="form-control" /></td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="job">직업</label></td>
                        <td><input type="text" id="job" v-model="userInfo.job" class="form-control" /></td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="family">부양가족</label></td>
                        <td><input type="number" id="family" v-model="userInfo.family" class="form-control" /></td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="spending">소비성향</label></td>
                        <td><input type="text" id="spending" v-model="userInfo.spending" class="form-control" /></td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="income">소득수준</label></td>
                        <td><input type="text" id="income" v-model="userInfo.income" class="form-control" /></td>
                        </tr>
                        <tr>
                        <td class="font-weight-bold"><label for="asset">자산</label></td>
                        <td><input type="text" id="asset" v-model="userInfo.asset" class="form-control" /></td>
                        </tr>
                </tbody>
            </table>
              
            </form>
          </div>
        </div>
      </div>
      <div class="col-8 d-flex justify-content-end"><button type="submit" class="withdrawal-btn" @click="deleteAccount">회원탈퇴</button></div>
    </div>
      <br>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { useCounterStore } from '@/stores/counter';
  
  const router = useRouter();
  const store = useCounterStore();
  const userInfo = computed(() => store.userInfo);
  const profileImageUrl = ref('/profile/profile.png'); // 기본 프로필 이미지
  
  // 이미지 변경 핸들러
  const onImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      profileImageUrl.value = URL.createObjectURL(file);
    }
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
  
  // 프로필 저장 핸들러
  const editProfile = () => {
    axios({
        method: 'post',
        url: `${store.BASE_URL}/api/v1/userinfo/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
        data: {
            product_id: product_id.value,
            option_id: option_id,
            option_id: option_id,
            option_id: option_id,
            option_id: option_id,
            option_id: option_id,
            option_id: option_id,
        },
    })
    .then((res) => {
        console.log(res.data)
        store.loadUserInfo(store.accessToken)
    })
    .catch((err) => {
        console.log(err)
    })
}

// 회원탈퇴
const deleteAccount = () => {
  if (confirm("정말로 회원탈퇴 하시겠습니까?")){
    axios({
        method: 'delete',
        url: `${store.BASE_URL}/api/v1/userinfo/`,
        headers: {
            Authorization: `Bearer ${store.accessToken}`, // JWT Access Token 포함
        },
    })
    .then((res) => {
        store.logOut()
    })
    .catch((err) => {
        console.log(err)
    })}
  }
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
    border-radius: 50%;
    margin-bottom: 20px;
  }
  

  
  /* 우측 상단: 네모 박스 3개 */
  .profile-right {
    display: flex;
    flex-direction: column;
    width: 50%;
  }
  
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
  
  /* 우측 하단: 입력 폼 */
  .form-container {
    padding: 10px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-control {
    width: 100%;
    padding: 8px;
    border: 1px solid #D7D5D5;
    border-radius: 5px;
  }
    /* 이미지 업로드 */
  .image-upload {
    width: 50%;
    text-align: center;
  }
  /* 글씨 */
  .poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }
  
  .text-highlight {
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
/* 회원 탈퇴 버튼 */
.withdrawal-btn{
  width: 120px;
  height: 40px;
  background-color: white;
  border: none;
  border-radius: 20px;
  margin-right: 10px;
}


/* 우측 하단: 테이블 */
.table-container {
  padding: 20px;
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

  </style>
  