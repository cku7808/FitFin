<template>
  <div>
    <form @submit.prevent="updateComment">
      <textarea v-model="updatedContent" class="form-control" rows="3"></textarea>
      <button type="submit" class="btn btn-success mt-2">수정하기</button>
      <button type="button" class="btn btn-secondary mt-2" @click="$emit('cancelEdit')">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";
import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";
const props = defineProps({
  comment: Object,
  onUpdate: Function,
});

const updatedContent = ref(props.comment.content);

const updateComment = async () => {
  try {
    await axios.put(`${BASE_URL}/api/v3/articles/${props.comment.article}/comment/${props.comment.id}/`, {
      content: updatedContent.value,
    });
    alert("댓글 수정 성공!");
    props.onUpdate({ ...props.comment, content: updatedContent.value });
  } catch (error) {
    console.error("댓글 수정 중 오류 발생:", error);
    alert("댓글 수정에 실패했습니다. 다시 시도해주세요.");
  }
};
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>
