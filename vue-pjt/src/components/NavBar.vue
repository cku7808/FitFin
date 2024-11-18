<template>
    <div>
        <nav class="navbar navbar-expand-lg" v-if="store.isLogin">
            <div class="container-fluid">
                <RouterLink :to="{ name: 'MainView'}">
                    <img src="@/assets/images/logo.png" alt="Bootstrap" width="110" height="50" class="ms-2">
                </RouterLink>

                <div class="navbar-expand-lg justify-content-end" id="navbarNavDropdown">
                    <ul class="navbar-nav d-flex flex-row">
                        <li class="nav-item">
                            <a @click="store.logOut()" style="cursor: pointer;">
                                <img src="@/assets/images/navbar/Logout.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </a>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'SignUpView'}">
                                <img src="@/assets/images/navbar/Mypage.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'LogInView'}">
                                <img src="@/assets/images/navbar/Cart.png" alt="Bootstrap" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <nav class="navbar navbar-expand-lg" v-else>
            <div class="container-fluid">
                <RouterLink :to="{ name: 'MainView'}">
                    <img src="@/assets/images/logo.png" alt="Bootstrap" width="110" height="50" class="ms-2">
                </RouterLink>

                <div class="navbar-expand-lg justify-content-end" id="navbarNavDropdown">
                    <ul class="navbar-nav d-flex flex-row">
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'SignUpView'}">
                                <img src="@/assets/images/navbar/Signup.png" alt="Bootstrap" width="80" height="19" class="me-2">
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink :to="{ name: 'LogInView'}">
                                <img src="@/assets/images/navbar/Login.png" alt="Bootstrap" width="80" height="19">
                            </RouterLink>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

    </div>
    <RouterView></RouterView>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
const store = useCounterStore()
</script>

<style scoped>

</style>