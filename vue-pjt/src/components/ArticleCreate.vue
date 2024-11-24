<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const BASE_URL = 'http://127.0.0.1:8000'
const title = ref(null)
const content = ref(null)
const router = useRouter()
const newArticleId = ref(null)

// DRF로 게시글 생성 요청을 보내는 함수
const createArticle = function () {
  axios({
    method: 'post',
    url: `${BASE_URL}/api/v3/articles/`,
    data: {
      title: title.value,
      content: content.value
    }
  })
    .then((res) => {
      console.log('게시글 작성 성공!')
      newArticleId.value = res.data.articleid
      router.push({ name: 'ArticleDetail', params: { id: newArticleId.value } })
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style>

</style>
