<template>
    <div>
        <h1>예적금 비교 페이지</h1>
        <div>
            <ul v-for="d in data">
                <li>{{ d }}</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';

const BASE_URL = 'http://127.0.0.1:8000'
const data = ref([])
const loadDepositProduct = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/finances/product-list/`,
    })
    .then((res) => {
        console.log(res.data)
        data.value.push(res.data)
        console.log(data.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadDepositProduct()
})

</script>

<style scoped>

</style>