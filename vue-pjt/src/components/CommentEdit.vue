<template>
  <div>
    <form @submit.prevent="updateComment">
      <textarea v-model="updatedContent" class="form-control" rows="1"></textarea>
      <button type="submit" class="btn btn-success mt-2">수정하기</button>
      <button type="button" class="btn btn-secondary mt-2" @click="$emit('cancelEdit')">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";
import axios from "axios";
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

const props = defineProps({
  comment: Object,
  onUpdate: Function,
});

const updatedContent = ref(props.comment.content);

const updateComment = function () {
  axios({
    method: 'put',
    url: `${store.BASE_URL}/api/v3/articles/${props.comment.article}/comment/${props.comment.id}/`,
    headers: store.header,
    data: {
      content: updatedContent.value,
    }
  })
    .then((res) => {
      console.log('댓글 수정 성공!');
      props.onUpdate({ ...props.comment, content: updatedContent.value });
    })
    .catch((err) => {
      console.log(err);
    })
}

</script>

<style scoped>
/* 전체 폼 */
form {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 요소 간 간격 */
  margin-top: 20px;
  background-color: #f9f9f9; /* 연한 배경색 */
  padding: 15px;
  border: 1px solid #e0e0e0; /* 테두리 */
  border-radius: 10px; /* 둥근 모서리 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

/* 수정 텍스트 영역 */
textarea {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-sizing: border-box;
  resize: none; /* 크기 조정 방지 */
  background-color: #fff;
}

/* 버튼 스타일 */
button {
  padding: 10px 15px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* 수정하기 버튼 */
button.btn-success {
  background-color: #28a745; /* 초록색 */
  color: #fff;
  border: none;
}

button.btn-success:hover {
  background-color: #218838; /* 더 짙은 초록색 */
}

/* 취소 버튼 */
button.btn-secondary {
  background-color: #6c757d; /* 회색 */
  color: #fff;
  border: none;
}

button.btn-secondary:hover {
  background-color: #5a6268; /* 더 짙은 회색 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  form {
    padding: 10px;
  }

  textarea {
    font-size: 0.9rem;
    padding: 10px;
  }

  button {
    font-size: 0.9rem;
    padding: 8px 12px;
  }
}
</style>

