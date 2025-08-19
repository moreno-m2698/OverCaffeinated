import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"
import IndexView from "../views/index/IndexView.vue"
import LoginView from "../views/login/LoginView.vue"

const routes = [
  { path: "/", component: IndexView, meta: { requiresAuth: true } },
  { path: "/login", component: LoginView, meta: { guestOnly: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// global before guard
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // ensure we check auth at least once
  if (auth.loading) {
    await auth.fetchUser()
  }

  if (to.meta.requiresAuth && !auth.user) {
    // needs auth but no user → go login
    return next("/login")
  }

  if (to.meta.guestOnly && auth.user) {
    // logged in but trying to see login page → go home
    return next("/")
  }

  next()
})

export default router