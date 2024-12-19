<template>
  <div class="coredream-regular">
    <h4 class="coredream-bold">게시글 상세보기</h4>
    <div class="coredream-regular" v-if="article">

      <p>제목 : {{ article.title }}</p>
      <p>내용 : {{ article.content }}</p>
      <p>작성자 : {{ article.user }}</p>
      <p>작성일 : {{ article.created_at.slice(0,10) }}</p>
      <p>수정일 : {{ article.updated_at.slice(0,10) }}</p>

      <!-- 좋아요 버튼 -->
      <button class="button-small" @click="toggleLike">
        <span v-if="article.like_users.includes(userInfo?.id || -1)">❤️</span>
        <span v-else>🤍</span>
        <!-- 좋아요 -->
        <span>&nbsp;{{ article.like_counts }}</span>
      </button>

      <!-- 수정 버튼 -->
      <button type="button" class="button-small" v-if="isPostedUser" @click="editArticle">
        수정
      </button>
      
      <!-- 삭제 버튼 -->
      <button type="button" class="button-small" v-if="isPostedUser" @click="deleteArticle">
        삭제
      </button>

    </div>

    <CommentCreate
    :article="article"/>

  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import CommentCreate from "@/components/CommentCreate.vue";
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute();
const router = useRouter();
const article = ref(null);
const userInfo = computed(() => store.userInfo);
const isPostedUser = ref(false)

// 게시글 상세 정보 로드 함수
const loadArticleDetail = function () {
  axios({
    method: 'get',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
  })
  .then((res) => {
    article.value = res.data
    // console.log(article.value.user)
    
    if (article.value.user === store.userInfo?.username || ''){
      isPostedUser.value = true
      console.log('일치합니다')
    }
    
    console.log('게시글 상세 정보 로드 성공!')
    console.log(res.data)
  })
  .catch((err) => {
    console.log(err)
  })
}

// 컴포넌트가 마운트되면 게시글 상세 정보 로드
onMounted(() => {
  loadArticleDetail();
});

// 좋아요 상태 변경
const toggleLike = function () {

  if(store.isLogin === false) {
    alert("로그인을 먼저 해주세요")
    router.push({name: "LogInView"})
  }
  
  else {
    axios({
      method: 'post',
      url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/like/`,
      headers: store.header,
    })
    .then((res) => {
      console.log('좋아요 성공!')
      loadArticleDetail();    // (!!! 이게 맞나?)
    })
    .catch((err) => {
      console.log(err)
    })
  }
}

// 게시글 수정
const editArticle = () => {
  router.push({ name: "ArticleEdit", params: { id: route.params.id } });
};

// 게시글 삭제 함수
const deleteArticle = function () {
  if (confirm('게시글을 삭제하시겠습니까?')){

    axios({
      method: 'delete',
      url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
      headers: store.header,
    })
      .then((res) => {
        console.log('게시글 삭제 성공!')
        router.push({ name: "ArticleList" });
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
/* 폰트 */
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.coredream-bold {
font-family: 'S-CoreDream-3Light';
font-weight: bold;
font-style: normal;
}

.coredream-regular {
font-family: 'S-CoreDream-3Light';
font-weight: 400;
font-style: normal;
}

.coredream-semibold {
font-family: 'S-CoreDream-3Light';
font-weight: 600;
font-style: normal;
}


/* 전체 컨테이너 */
div {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

/* 제목 */
h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #203359; /* 네이비 색상 */
  margin-bottom: 20px;
}

/* 게시글 정보 */
p {
  font-size: 1rem;
  line-height: 1.5;
  color: #333;
  margin-bottom: 15px;
}

/* 좋아요 삭제 수정 버튼 */
.button-small {
  padding: 10px 15px;
  background-color: #203359;
  color: #fff;
  border: none;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.button-small:hover {
  background-color: #0d1a2e;
  color: #fff;
}


/* 반응형 디자인 (!!!) */
@media (max-width: 768px) {
  div {
    padding: 15px;
  }

  h1 {
    font-size: 1.8rem;
  }

  p {
    font-size: 0.9rem;
  }

  .button-small {
    font-size: 0.9rem;
    padding: 8px 12px;
  }
}
</style>
