import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

// Views
import IndexView from "../views/index/IndexView.vue";
import LoginView from "../views/login/LoginView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: IndexView,
    meta: { requiresAuth: true }, // only accessible if logged in
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, _, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated()) {
    next({ name: "Login" });
  } else if (to.name === "Login" && auth.isAuthenticated()) {
    next({ name: "Home" });
  } else {
    next();
  }
});

export default router;