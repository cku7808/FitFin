<template>
    <div>
      <h5>{{ article.id }}</h5>
      <p><RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">{{ article.title }}</RouterLink></p>
      <p>{{ article.content }}</p>
      
      <hr>
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'
  
  defineProps({
    article: Object
  })
  </script>
  