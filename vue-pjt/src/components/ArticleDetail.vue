<template>
  <div>
    <h1>Detail</h1>
    <div v-if="article">
      <p>게시글 번호 : {{ article.id }}</p>
      <p>제목 : {{ article.title }}</p>
      <p>내용 : {{ article.content }}</p>
      <p>작성일 : {{ article.created_at }}</p>
      <p>수정일 : {{ article.updated_at }}</p>

          <!-- 좋아요 버튼 -->
    <button @click="toggleLike" class="btn btn-outline-danger">
      <span v-if="liked">❤️</span>
      <span v-else>🤍</span>
      좋아요 ({{ likeCount }})
    </button>


      <!-- 삭제 버튼을 클릭하면 모달을 띄우도록 설정 -->
      <button
        id="openModalButton"
        type="button"
        class="btn btn-danger"
        data-bs-toggle="modal"
        data-bs-target="#deleteModal"
      >
        삭제
      </button>


      <button type="button" class="btn" @click="editArticle">
        수정
      </button>

      <!-- 삭제 모달 -->
      <div
        class="modal fade"
        id="deleteModal"
        data-bs-backdrop="static"
        tabindex="-1"
        aria-labelledby="deleteModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="deleteModalLabel">게시글 삭제</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                @click="focusTriggerButton"
              ></button>
            </div>
            <div class="modal-body">
              이 게시글을 정말 삭제하시겠습니까?
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
                @click="removeFocus"
              >
                취소
              </button>
              <!-- 모달 내 삭제 버튼 -->
              <button @click="handleDeleteAndRemoveFocus" type="button" class="btn btn-danger">
                삭제
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CommentCreate
    :article="article"/>

  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Modal } from "bootstrap"; // 부트스트랩 모달 사용을 위해 임포트
import CommentCreate from "@/components/CommentCreate.vue";
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute();
const router = useRouter();
const article = ref(null);
const liked = ref()

// 삭제와 포커스 제거를 함께 처리하는 함수
const handleDeleteAndRemoveFocus = async () => {
  await removeFocus();
  handleDelete();
};

// 삭제 버튼 클릭 시 호출되는 함수
const handleDelete = async () => {
  try {
    // 모달 닫기
    const modalElement = document.getElementById("deleteModal");
    const modalInstance = Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    }

    // 약간의 지연 시간 추가
    await new Promise((resolve) => setTimeout(resolve, 300));

    // 게시글 삭제 요청
    await deleteArticle();

    // 게시글 목록 페이지로 이동
    router.push({ name: "ArticleList" });
  } catch (error) {
    console.error("삭제 처리 중 오류:", error);
    alert("삭제에 실패했습니다. 다시 시도해주세요.");
  }
};

// 게시글 삭제 함수
const deleteArticle = function () {
  axios({
    method: 'delete',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
    headers: store.header,
  })
    .then((res) => {
      console.log('게시글 작성 성공!')
    })
    .catch((err) => {
      console.log(err)
    })
}

// 게시글 상세 정보 로드 함수
const loadArticleDetail = function () {
  axios({
    method: 'get',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
    headers: store.header,
  })
    .then((res) => {
      article.value = res.data
      console.log('게시글 작성 성공!')
    })
    .catch((err) => {
      console.log(err)
    })
}

// 포커스를 모달을 트리거했던 버튼으로 이동시키는 함수
const focusTriggerButton = () => {
  const openModalButton = document.getElementById("openModalButton");
  if (openModalButton) {
    openModalButton.focus();
  }
};

// 포커스를 제거하는 함수
const removeFocus = () => {
  document.activeElement.blur();
};

// 컴포넌트가 마운트되면 게시글 상세 정보 로드
onMounted(() => {
  loadArticleDetail();
});

// 게시글 수정
const editArticle = () => {
  router.push({ name: "ArticleEdit", params: { id: route.params.id } });
};


// 좋아요 상태 변경 (상태 변경 수정!!!!)
const toggleLike = function () {
  axios({
    method: 'post',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/like/`,
    headers: store.header,
  })
    .then((res) => {
      liked.value = !liked.value; // 좋아요 상태 반전
      likeCount.value += liked.value ? 1 : -1; // 좋아요 개수 반영
      console.log('좋아요 성공!')
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style scoped>
/* 전체 컨테이너 */
div {
  font-family: 'Arial', sans-serif;
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

/* 좋아요 버튼 */
.btn-outline-danger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  border: 2px solid #dc3545;
  background-color: transparent;
  color: #dc3545;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}

/* 삭제 버튼 */
.btn-danger {
  padding: 10px 15px;
  background-color: #dc3545;
  color: #fff;
  border: none;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.btn-danger:hover {
  background-color: #a71d2a;
}

/* 수정 버튼 */
.btn {
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

.btn:hover {
  background-color: #0d1a2e;
}

/* 모달 스타일 */
.modal-content {
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.modal-header {
  background-color: #203359;
  color: #fff;
  border-bottom: none;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.modal-body {
  font-size: 1rem;
  color: #555;
}

.modal-footer .btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.modal-footer .btn-secondary:hover {
  background-color: #5a6268;
}

.modal-footer .btn-danger {
  background-color: #dc3545;
  color: #fff;
  border: none;
}

.modal-footer .btn-danger:hover {
  background-color: #a71d2a;
}

/* 반응형 디자인 */
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

  .btn,
  .btn-danger,
  .btn-outline-danger {
    font-size: 0.9rem;
    padding: 8px 12px;
  }
}
</style>
