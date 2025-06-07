<script setup lang="ts">
import AppHeader from './components/layouts/AppHeader.vue'
import AppMain from './components/layouts/AppMain.vue'
</script>

<template>
  <AppHeader />
  <AppMain />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
