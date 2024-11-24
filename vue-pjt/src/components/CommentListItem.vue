<template>
  <div>
    <p><strong>{{ comment.author }}</strong>: {{ comment.content }}</p>
    <p class="text-muted">작성일: {{ comment.created_at }}</p>
    <button class="btn btn-secondary btn-sm" @click="$emit('edit')">수정</button>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  comment: Object,
});
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>
