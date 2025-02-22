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
            type="email"
            v-model="email"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium">Password</label>
          <input
            type="password"
            v-modecdl="password"
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
export default {
  name: "LoginComponent",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      console.log("Logging in with:", {
        email: this.email,
        password: this.password,
      });
    },
  },
};
</script>
