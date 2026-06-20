import { createRouter, createWebHistory } from 'vue-router'
import WatchlistView from '@/views/WatchlistView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import HistoryView from '@/views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { name: 'watchlist' },
    },
    {
      path: '/watchlist',
      name: 'watchlist',
      component: WatchlistView,
    },
    {
      path: '/stock/:symbol',
      name: 'stock',
      component: StockDetailView,
      props: true,
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView,
    },
  ],
})

export default router
