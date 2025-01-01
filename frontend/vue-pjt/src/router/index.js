import { createRouter, createWebHistory } from 'vue-router'

import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import KakaoLogin from '@/components/KakaoLogin.vue'

import MainView from '@/views/MainView.vue'

import ExchangeRateView from '@/views/ExchangeRateView.vue'

import BankPosView from '@/views/BankPosView.vue'

import CommunityView from '@/views/CommunityView.vue'

import MyPageView from '@/views/MyPageView.vue'

import CartView from '@/views/CartView.vue'

import DepositSavingView from '@/views/DepositSavingView.vue'
import DepositProduct from '@/components/DepositProduct.vue'
import DepositProductDetail from '@/components/DepositProductDetail.vue'
import SavingProduct from '@/components/SavingProduct.vue'
import SavingProductDetail from '@/components/SavingProductDetail.vue'

import ArticleList from '@/components/ArticleList.vue'
import ArticleDetail from '@/components/ArticleDetail.vue'
import ArticleCreate from '@/components/ArticleCreate.vue'
import ArticleEdit from '@/components/ArticleEdit.vue'

import MyProfile from '@/components/MyProfile.vue'
import MyProfileEdit from '@/components/MyProfileEdit.vue'
import MyProduct from '@/components/MyProduct.vue'
import MyRecommend from '@/components/MyRecommend.vue'

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
      path: '/depositsavingproducts',
      name: 'DepositSavingView',
      component: DepositSavingView,
    },
    {
      path: '/depositproduct',
      name: 'DepositProduct',
      component: DepositProduct,
    },
    {
      path: '/depositproduct/:id',
      name: 'DepositProductDetail',
      component: DepositProductDetail,
    },
    {
      path: '/savingproduct',
      name: 'SavingProduct',
      component: SavingProduct,
    },
    {
      path: '/savingproduct/:id',
      name: 'SavingProductDetail',
      component: SavingProductDetail,
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
      children: [
        { path: "", name:'ArticleList', component: ArticleList },
        { path: ":id", name:'ArticleDetail', component: ArticleDetail, props: true },
        { path: "create", name:'ArticleCreate', component: ArticleCreate },
        { path: ":id/edit", name:'ArticleEdit', component: ArticleEdit },
      ],
    },
    {
      path: '/mypage',
      name: 'MyPageView',
      component: MyPageView,
      children: [
        { path: "", name:'MyProfile', component: MyProfile },
        { path: "editprofile", name:'MyProfileEdit', component: MyProfileEdit },
        { path: "product", name:'MyProduct', component: MyProduct },
        { path: "recommend", name:'MyRecommend', component: MyRecommend },
      ],
    },
    {
      path: '/cart',
      name: 'CartView',
      component: CartView,
    },
  ],
})

export default router
