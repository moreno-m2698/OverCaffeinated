import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import IndexView from "../views/index/IndexView.vue";
import LoginView from "../views/login/LoginView.vue";

const routes = [
    {
        path: "/", component: IndexView
    },
    {
        path: "/login", component: LoginView, meta: { guestOnly: true } 
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore()
    if (auth.loading) await auth.fetchUser();

    if (to.meta.requiresAuth && !auth.user) {
        next("/login")
    } else if (to.meta.guestOnly && auth.user) {
        next("/dashboard");
    } else {
        next()
    }
})

export default router