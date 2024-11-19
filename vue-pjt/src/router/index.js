import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MainView from '@/views/MainView.vue'
import KakaoLogin from '@/components/KakaoLogin.vue'
import CompareProductView from '@/views/CompareProductView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import BankPosView from '@/views/BankPosView.vue'
import CommunityView from '@/views/CommunityView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CartView from '@/views/CartView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/kakaologin',
      name: 'KakaoLogin',
      component: KakaoLogin,
    },
    {
      path: '/compareproduct',
      name: 'CompareProductView',
      component: CompareProductView,
    },
    {
      path: '/exchangerate',
      name: 'ExchangeRateView',
      component: ExchangeRateView,
    },
    {
      path: '/bankpos',
      name: 'BankPosView',
      component: BankPosView,
    },
    {
      path: '/community',
      name: 'CommunityView',
      component: CommunityView,
    },
    {
      path: '/mypage',
      name: 'MyPageView',
      component: MyPageView,
    },
    {
      path: '/cart',
      name: 'CartView',
      component: CartView,
    },
  ],
})

export default router
