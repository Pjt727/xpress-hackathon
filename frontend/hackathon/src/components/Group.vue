<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Group Management</h1>
      <div class="flex gap-4">
        <button
          class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
          @click="showModal = true"
        >
          Create Group
        </button>
        <a
          href="/history"
          class="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition"
        >
          Go to Invoices History
        </a>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Group Name
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="group in groups"
              :key="group.id"
              class="hover:bg-gray-50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ group.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <button
                  class="text-red-600 hover:text-red-900"
                  @click="deleteGroup(group.id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center"
    >
      <div class="relative p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
            Create New Group
          </h3>
          <form @submit.prevent="addGroup" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Group Name</label
              >
              <input
                v-model="newGroup"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                placeholder="Enter group name"
              />
            </div>
            <div class="mt-5 flex justify-end gap-3">
              <button
                type="button"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
                @click="showModal = false"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                :disabled="isSubmitting"
              >
                Create Group
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const groups = ref([]);
const newGroup = ref("");
const showModal = ref(false);

const fetchGroups = async () => {
  try {
    const response = await axios.get(`${domainName}/groups`);
    groups.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Error fetching groups:", error);
    groups.value = [];
  }
};

const isSubmitting = ref(false);

const addGroup = async () => {
  if (newGroup.value.trim() && !isSubmitting.value) {
    isSubmitting.value = true;
    try {
      await axios.post(`${domainName}/groups`, {
        name: newGroup.value.trim(),
      });

      await fetchGroups();

      newGroup.value = "";
      showModal.value = false;
    } catch (error) {
      console.error("Error creating group:", error);
    } finally {
      isSubmitting.value = false;
    }
  }
};

const deleteGroup = async (id) => {
  try {
    const response = await axios.delete(`${domainName}/groups`, {
      headers: {
        "Content-Type": "application/json",
      },
      data: { id: String(id) },
      withCredentials: true,
    });

    if (response.data.success) {
      await fetchGroups();
    } else {
      console.error("Failed to delete:", response.data.message);
    }
  } catch (error) {
    console.error("Error deleting group:", error);
  }
};

onMounted(fetchGroups);
</script>
