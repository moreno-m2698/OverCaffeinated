<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const error = ref("");

const handleLogin = async () => {
  try {
    await auth.login(username.value, password.value); // call store method
    router.push("/"); // redirect to Home after login
  } catch (err: any) {
    error.value = err.message || "Login failed";
  }
};
</script>

<template>
    <h1>Login</h1>

    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="Enter username"
        />
      </div>

      <div>
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Enter password"
        />
      </div>

      <button type="submit">Login</button>
    </form>

    <p v-if="error" style="color:red;">{{ error }}</p>
</template>