<template>
  <div class="container mx-auto px-4 py-8 bg-gray-50">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Download</h1>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6">
      <div class="flex items-center gap-4 mb-6">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search invoices..."
          class="flex-grow px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <router-link
          to="/invoice"
          class="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Add
        </router-link>
      </div>

      <!-- File Table -->
      <div
        v-if="filteredFiles.length > 0"
        class="overflow-x-auto rounded-lg border border-gray-200"
      >
        <table class="w-full table-auto">
          <thead>
            <tr class="bg-gray-100 text-left">
              <th class="px-6 py-3 text-gray-600 font-semibold">File Name</th>
              <th class="px-6 py-3 text-gray-600 font-semibold text-center">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="(file, index) in filteredFiles"
              :key="index"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 text-gray-900">{{ file }}</td>
              <td class="px-6 py-4 text-center">
                <button
                  class="text-blue-600 hover:text-blue-800 font-medium"
                  @click="downloadInvoice(file)"
                >
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- No Files Found -->
      <div v-else class="bg-white p-12 text-center mt-8">
        <div class="text-gray-400">
          <svg
            class="w-16 h-16 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            ></path>
          </svg>
          <h3 class="text-xl font-semibold mb-2">No Files Found</h3>
          <p class="text-gray-500">
            There are no files matching your search criteria.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Reactive data for invoices
const searchQuery = ref("");
const invoices = ref([
  {
    id: 0,
    number: "#INV-2024-000",
    date: "Jan 25, 2014",
    client: "Tech Inc.",
    amount: "250.00",
    is_settled: false,
    is_outgoing: true,
  },
  {
    id: 1,
    number: "#INV-2024-001",
    date: "Jan 15, 2024",
    client: "Tech Solutions Inc.",
    amount: "2500.00",
    is_settled: true,
    is_outgoing: true,
  },
  {
    id: 2,
    number: "#INV-2024-002",
    date: "Jan 18, 2024",
    client: "Global Systems Ltd.",
    amount: "1800.00",
    is_settled: false,
    is_outgoing: false,
  },
]);

// Computed property for filtering invoices
const filteredInvoices = computed(() => {
  if (!searchQuery.value) return invoices.value;
  return invoices.value.filter(
    (invoice) =>
      invoice.number.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      invoice.client.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// View Invoice
const viewInvoice = (invoice) => {
  console.log("Viewing invoice:", invoice);
};

const files = ref([]);

const fetchFiles = async () => {
  try {
    const response = await axios.get(`${domainName}/invoice-uploads`, {
      withCredentials: true,
    });

    console.log("API Response:", response.data);
    if (response.data && Array.isArray(response.data)) {
      files.value = response.data;
      console.log("Files retrieved:", files.value);
    } else {
      console.warn("No files found.");
    }
  } catch (error) {
    console.error("Error fetching invoice files:", error);
  }
};

const filteredFiles = computed(() => {
  if (!searchQuery.value) return files.value;
  return files.value.filter((file) =>
    file.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const downloadInvoice = async (file) => {
  try {
    const fileUrl = `${domainName}/${file}`;
    console.log("Downloading from:", fileUrl);

    const response = await fetch(fileUrl, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to download file");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = file.split("/").pop();
    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    console.log("File downloaded successfully!");
  } catch (error) {
    console.error("Error downloading file:", error);
  }
};

onMounted(fetchFiles);

// Delete Invoice
const deleteInvoice = (id) => {
  invoices.value = invoices.value.filter((invoice) => invoice.id !== id);
};
</script>

<style>
body {
  font-family: "Inter", sans-serif;
  background-color: #f8f9fa;
  color: #333;
}
</style>
