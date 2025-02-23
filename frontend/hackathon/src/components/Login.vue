<template>
  <div
    class="absolute inset-0 flex items-center justify-center bg-gray-100 text-gray-900"
  >
    <div
      class="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg border border-gray-300"
    >
      <h2 class="text-2xl font-bold text-center mb-6">Login</h2>
      <form @submit.prevent="handleSubmit" class="w-full">
        <div class="mb-4">
          <label class="block text-sm font-medium">Email</label>
          <input
            v-model="email"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium">Password</label>
          <input
            type="password"
            v-model="password"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>

        <button
          type="submit"
          class="mt-2 w-full py-2 text-white bg-gray-800 rounded-lg hover:bg-gray-900 focus:ring-2 focus:ring-gray-500"
        >
          Login
        </button>
      </form>
      <p class="text-center text-sm mt-6">
        Don't have an account?
        <RouterLink to="/register" class="text-gray-600 hover:text-gray-900"
          >Register</RouterLink
        >
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref } from "vue";

axios.defaults.withCredentials = true;

export default {
  name: "LoginComponent",
  setup() {
    const router = useRouter();
    const email = ref("");
    const password = ref("");

    const handleSubmit = async () => {
      console.log("Logging in with:", {
        email: email.value,
        password: password.value,
      });

      try {
        const response = await axios.post(
          `${domainName}/login`,
          {
          email: email.value,
          password: password.value,
          },
          {
            withCredentials: true,
          }
        );

        if (response.data.success) {
          console.log("Success!");
          alert("Success!");
          router.push("/history");
        } else {
          console.error("Failed:", response.data.message);
          alert("Failed: " + response.data.message);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Error!");
      }
    };

    return {
      email,
      password,
      handleSubmit,
    };
  },
};
</script>
