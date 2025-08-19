import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "axios"

axios.defaults.withCredentials = true

export const useAuthStore = defineStore("auth", () => {
  type User = {
    id: number
    username: string
    lastObservation: number
    caffeine: number
  }

  const user = ref<User | null>(null)
  const loading = ref(true)

  // Helper to generate a mock user in dev
  function createMockUser(): User {
    const today = new Date()
    today.setUTCHours(0, 0, 0, 0)

    return {
      id: 1,
      username: "janedoe",
      lastObservation: today.valueOf(),
      caffeine: 200
    }
  }

  async function fetchUser() {
    loading.value = true
    if (import.meta.env.MODE === "development") {
      user.value = createMockUser()
      loading.value = false
    } else {
      try {
        const res = await axios.get("/users/me")
        user.value = res.data
      } catch {
        user.value = null
      } finally {
        loading.value = false
      }
    }
  }

  async function logout() {
    if (import.meta.env.MODE !== "development") {
      await axios.post("/logout")
    }
    user.value = null
  }

  return { user, loading, fetchUser, logout }
})