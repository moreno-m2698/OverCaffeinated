<script setup lang="ts">
import IndexView from "../../views/index/IndexView.vue";
import LoginView from "../../views/login/LoginView.vue";

import { useAuthStore } from "../../stores/auth";

const store = useAuthStore();

</script>

<template>
  <IndexView />
  <LoginView />
</template>