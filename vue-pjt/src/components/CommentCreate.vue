<template>
  <div>
    <h5>댓글 작성하기</h5>
    <form @submit.prevent="createComment">
      <textarea
        v-model="content"
        class="form-control"
        rows="1"
        placeholder="댓글을 입력하세요"
      ></textarea>
      <button type="submit" class="btn btn-primary mt-2">작성하기</button>
    </form>
  </div>

  <div>
    <h5>댓글 목록</h5>
    <div v-if="comments.length">
      <div v-for="(comment, index) in comments" :key="comment.id">
        <CommentListItem
          :comment="comment"
          @edit="editComment(comment.id)"
          @deleteSuccess="loadComments"/>
        <CommentEdit
          v-if="isEditing(comment.id)"
          :comment="comment"
          @cancelEdit="cancelEdit"
          :onUpdate="(updatedComment) => handleUpdate(index, updatedComment)"
        />
      </div>
    </div>
    <div v-else>
      <p>댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import CommentListItem from "@/components/CommentListItem.vue";
import CommentEdit from "@/components/CommentEdit.vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const store = useCounterStore();
const router = useRouter();

const props = defineProps({
  article: Object,
});

const content = ref("");
const comments = ref([]);
const editingCommentId = ref(null);

// 댓글 작성 함수
const createComment = function () {

  if(store.isLogin === false) {
    alert("로그인을 먼저 해주세요")
    router.push({name: "LogInView"})
  }

  else {
    axios({
      method: "post",
      url: `${store.BASE_URL}/api/v3/articles/${props.article.id}/comment/`,
      headers: store.header,
      data: {
        content: content.value,
      },
    })
      .then(() => {
        console.log("댓글 작성 성공!");
        content.value = "";
        loadComments();
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

// 댓글 목록 불러오기
const loadComments = function () {
  if (!props.article || !props.article.id) {
    return; // article이 아직 정의되지 않았으면 로드하지 않음
  }
  axios({
    method: "get",
    url: `${store.BASE_URL}/api/v3/articles/${props.article.id}/comment/`,
  })
    .then((res) => {
      console.log("댓글 목록 로드!");
      comments.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

// `article`이 정의된 후에 댓글 목록을 로드
watch(
  () => props.article,
  (newArticle) => {
    if (newArticle && newArticle.id) {
      loadComments();
    }
  },
  { immediate: true }
);

// 수정 중인 댓글 여부 확인
const isEditing = (commentId) => {
  return editingCommentId.value === commentId;
};

// 댓글 수정 시작
const editComment = (commentId) => {
  editingCommentId.value = commentId;
};

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null;
};

// 댓글 수정 완료 후 업데이트
const handleUpdate = (index, updatedComment) => {
  comments.value[index] = updatedComment;
  editingCommentId.value = null;
};
</script>
<style scoped>
/* 전체 컨테이너 */
.comments-container {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
h5 {
  /* font-size: 1.5rem; */
  font-weight: bold;
  color: #203359; /* 네이비 */
  margin-bottom: 20px;
}

/* 댓글 작성 폼 */
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

textarea {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-sizing: border-box;
  background-color: #f9f9f9;
  resize: none; /* 크기 조정 방지 */
}

textarea::placeholder {
  color: #aaa;
}

/* 작성 버튼 */
button[type="submit"] {
  width: 150px;
  align-self: flex-end;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #203359;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #0d1a2e; /* 더 짙은 네이비 */
}

/* 댓글 목록 */
.comments {
  margin-top: 20px;
}

.comment-item {
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9; /* 연한 회색 배경 */
  border: 1px solid #e0e0e0; /* 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  display: flex;
  flex-direction: column;
  gap: 10px; /* 요소 간 간격 */
}

.comment-item:hover {
  transform: translateY(-3px); /* 살짝 들어올리기 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* 호버 효과 */
}

/* 댓글 내용 */
.comment-item p {
  font-size: 1rem;
  color: #555; /* 중간 회색 */
  margin: 0;
}

.comment-item p.author {
  font-weight: bold;
  color: #203359; /* 네이비 */
}

.comment-item p.date {
  font-size: 0.9rem;
  color: #6c757d; /* 회색 */
}

/* 수정 및 삭제 버튼 */
.comment-item button {
  padding: 5px 10px;
  font-size: 0.9rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.comment-item button.btn-secondary {
  background-color: #6c757d; /* 회색 */
  color: #fff;
  border: none;
}

.comment-item button.btn-secondary:hover {
  background-color: #5a6268; /* 더 짙은 회색 */
}

.comment-item button.btn-danger {
  background-color: #dc3545; /* 빨간색 */
  color: #fff;
  border: none;
}

.comment-item button.btn-danger:hover {
  background-color: #a71d2a; /* 더 짙은 빨간색 */
}

/* 빈 댓글 메시지 */
.comments-empty {
  text-align: center;
  font-size: 1rem;
  color: #aaa;
  margin-top: 20px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .comments-container {
    padding: 15px;
  }

  h4 {
    font-size: 1.3rem;
  }

  textarea {
    font-size: 0.9rem;
  }

  button {
    width: 100%;
    align-self: center;
  }

  .comment-item p {
    font-size: 0.9rem;
  }
}
</style>
