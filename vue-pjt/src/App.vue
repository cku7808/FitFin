<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'SignUpView'}">SignUp</RouterLink> | 
      <RouterLink :to="{ name: 'LogInView'}">LogIn</RouterLink>
    </nav>
  </header>
  <RouterView></RouterView>
</template>

<style scoped>

</style>
