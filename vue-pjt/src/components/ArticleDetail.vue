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

const BASE_URL = "http://127.0.0.1:8000";
const route = useRoute();
const router = useRouter();
const article = ref(null);

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
const deleteArticle = async () => {
  try {
    await axios.delete(`${BASE_URL}/api/v3/articles/${route.params.id}/`);
    console.log("게시글 삭제 성공!");
  } catch (error) {
    console.error("게시글 삭제 중 오류 발생:", error);
    throw error; // 에러 발생 시 이후 동작 중단
  }
};

// 게시글 상세 정보 로드 함수
const loadArticleDetail = async () => {
  try {
    const response = await axios.get(
      `${BASE_URL}/api/v3/articles/${route.params.id}/`
    );
    article.value = response.data;
  } catch (error) {
    console.error("게시글 상세 로드 중 오류 발생:", error);
  }
};

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


// 좋아요 상태 변경
const toggleLike = async () => {
  try {
    // 서버로 POST 요청을 보내 좋아요 상태를 변경
    await axios.post(`${BASE_URL}/articles/${props.article.id}/like/`);
    liked.value = !liked.value; // 좋아요 상태 반전
    likeCount.value += liked.value ? 1 : -1; // 좋아요 개수 반영
  } catch (error) {
    console.error('좋아요 상태 변경 중 오류 발생:', error);
    alert('좋아요 변경에 실패했습니다. 다시 시도해주세요.');
  }
};
</script>

<style>
/* 필요에 따라 추가 스타일링 */
</style>
