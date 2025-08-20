import { ref } from "vue";
import { defineStore } from "pinia";

type User = {
  id: number;
  username: string;
  caffeine: number;
  lastObservation: number;
};

export const useAuthStore = defineStore("auth", () => {
  // --- State ---
  const user = ref<User | null>(null);

  // --- Actions ---
  function login(username: string, password: string) {
    // For testing: mock user login
    if (import.meta.env.MODE === "development") {
      if (username === "janedoe" && password === "secret") {
        user.value = {
          id: 1,
          username,
          caffeine: 200,
          lastObservation: Date.now(),
        };
        console.log("Mock user logged in:", user.value);
        return true;
      }
      
      console.log("Failed to log in mock user")
      return false;
    }

    // TODO: Replace with real API call for production
    console.log("Would send credentials to backend:", { username, password });
    return false;
  }

  function logout() {
    user.value = null;
    console.log("User logged out");
  }

  // --- Getters ---
  const isAuthenticated = () => user.value !== null;

  return {
    user,
    login,
    logout,
    isAuthenticated,
  };
});