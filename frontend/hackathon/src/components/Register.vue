<template>
  <div
    class="absolute inset-0 flex items-center justify-center bg-gray-100 text-gray-900"
  >
    <div
      class="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg border border-gray-300"
    >
      <h2 class="text-2xl font-bold text-center mb-6">Register</h2>
      <form @submit.prevent="handleSubmit" class="w-full">
        <div class="mb-4">
          <label class="block text-sm font-medium">First Name</label>
          <input
            type="text"
            v-model="firstName"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium">Last Name</label>
          <input
            type="text"
            v-model="lastName"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
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
            v-model="password"
            class="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
            required
          />
        </div>
        <button
          type="submit"
          class="mt-2 w-full py-2 text-white bg-gray-800 rounded-lg hover:bg-gray-900 focus:ring-2 focus:ring-gray-500"
        >
          Register
        </button>
      </form>
      <p class="text-center text-sm mt-6">
        Already have an account?
        <RouterLink to="/login" class="text-gray-600 hover:text-gray-900"
          >Login</RouterLink
        >
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterComponent",
  data() {
    return {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      console.log("Registering user:", {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
        password: this.password,
      });
    },
  },
};
</script>
