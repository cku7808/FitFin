<template>
  <div class="comment-item">
    <!-- 댓글 내용 -->
    <span class="comment-content">
      <strong>{{ comment.author }}</strong>: {{ comment.content }}
    </span>
    <!-- 수정 및 삭제 버튼 -->
    <span class="comment-actions">
      <button class="btn btn-secondary btn-sm" @click="$emit('edit')">수정</button>
      <button class="btn btn-danger btn-sm" @click="deleteComment">삭제</button>
    </span>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const store = useCounterStore();
const props = defineProps({
  comment: Object, // 댓글 정보
});
const emit = defineEmits(["edit", "deleteSuccess"]);

const deleteComment = function () {
  if (confirm('댓글을 삭제하시겠습니까?')){

    axios({
      method: "delete",
      url: `${store.BASE_URL}/api/v3/articles/${props.comment.article}/comment/${props.comment.id}/`,
      headers: store.header,
    })
      .then(() => {
        console.log("댓글 삭제 성공!");
        emit("deleteSuccess"); // 삭제 성공 시 부모 컴포넌트에 알림
      })
      .catch((err) => {
        console.log(err);
      });
  };
  }
</script>

<style scoped>
/* 댓글 아이템 컨테이너 */
.comment-item {
  display: flex; /* Flexbox 사용 */
  justify-content: space-between; /* 좌우로 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  width: 100%; /* 컨테이너 전체 너비 */
}

/* 댓글 내용 스타일 */
.comment-content {
  flex: 1; /* 댓글 내용이 가용 공간을 차지 */
  font-size: 1rem;
  color: #333;
  margin-right: 20px; /* 버튼과의 간격 */
  text-align: left; /* 텍스트 좌측 정렬 */
}

/* 버튼 그룹 스타일 */
.comment-actions {
  display: flex; /* 버튼을 가로로 정렬 */
  gap: 10px; /* 버튼 간 간격 */
}

/* 버튼 스타일 */
button {
  font-size: 0.85rem;
  padding: 5px 10px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

button.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

button.btn-secondary:hover {
  background-color: #5a6268;
}

button.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
}

button.btn-danger:hover {
  background-color: #c82333;
}
</style>
