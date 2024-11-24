<template>
    <div>
      {{ article }}
      <h4>댓글 작성하기</h4>
      <form @submit.prevent="createComment">
        <textarea v-model="content" class="form-control" rows="3" placeholder="댓글을 입력하세요"></textarea>
        <button type="submit" class="btn btn-primary mt-2">작성하기</button>
      </form>
    </div>
  
    <div>
      <h4>댓글 목록</h4>
      <div v-if="comments.length">
        <div v-for="(comment, index) in comments" :key="comment.id">
          <CommentListItem
            v-if="!isEditing(comment.id)"
            :comment="comment"
            @edit="editComment(comment.id)"
          />
          <CommentEdit
            v-else
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
  
  const props = defineProps({
    article: Object,
  });
  
  const BASE_URL = "http://127.0.0.1:8000";
  const content = ref("");
  
  // 댓글 작성 함수
  const createComment = async () => {
    try {
      if (!content.value) {
        alert("댓글 내용을 입력해주세요.");
        return;
      }
      // props로 전달된 article 객체에서 id에 접근
      await axios.post(`${BASE_URL}/api/v3/articles/${props.article.id}/comment/`, {
        content: content.value,
      });
      content.value = ""; // 작성 후 폼 초기화
      alert("댓글 작성 성공!");
      loadComments(); // 댓글 작성 후 댓글 목록 갱신
    } catch (error) {
      console.error("댓글 작성 중 오류 발생:", error);
      alert("댓글 작성에 실패했습니다. 다시 시도해주세요.");
    }
  };
  
  const comments = ref([]);
  const editingCommentId = ref(null);
  
  // 댓글 목록 불러오기
  const loadComments = async () => {
    try {
      if (!props.article || !props.article.id) {
        return; // article이 아직 정의되지 않았으면 로드하지 않음
      }
      const response = await axios.get(`${BASE_URL}/api/v3/articles/${props.article.id}/comment/`);
      comments.value = response.data;
    } catch (error) {
      console.error("댓글 목록 로드 중 오류 발생:", error);
    }
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
  /* 필요에 따라 스타일 추가 */
  </style>
  