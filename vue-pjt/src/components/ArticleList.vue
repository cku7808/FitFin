<template>
    <div>
        <h3>Article List</h3>
        <button type="button" class="btn btn-primary" @click="createarticle">작성하기</button>
        <hr>
        <ArticleListItem
        v-for="article in articlelist"
        :key="article.id"
        :article="article"/>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";


import ArticleListItem from '@/components/ArticleListItem.vue';

// 데이터 로드
const router = useRouter();
const BASE_URL = 'http://127.0.0.1:8000'
const articlelist = ref([])
const loadArticleList = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/api/v3/articles/`,
    })
    .then((res) => {
        articlelist.value = res.data
        console.log(articlelist.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadArticleList()
});


const createarticle = () => {
  router.push({ name: "ArticleCreate"});
}


</script>

<style scoped>

</style>    