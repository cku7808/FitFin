<template>
  <div>
    <p><strong>{{ comment.author }}</strong>: {{ comment.content }}</p>
    <p class="text-muted">작성일: {{ comment.created_at }}</p>
    <button class="btn btn-secondary btn-sm" @click="$emit('edit')">수정</button>
    <button class="btn btn-danger btn-sm" @click="deleteComment">삭제</button>
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
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>
