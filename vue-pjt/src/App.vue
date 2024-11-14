<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'SignUpView'}">SignUp</RouterLink>
    </nav>
  </header>
  <RouterView></RouterView>
</template>

<style scoped>

</style>
