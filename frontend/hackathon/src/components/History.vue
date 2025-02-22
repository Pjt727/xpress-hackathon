<template>
  <div class="container mx-auto px-4 py-8 bg-gray-50">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Invoice History</h1>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6">
      <div class="flex flex-col md:flex-row justify-between gap-4 mb-6">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search invoices..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      <!-- Invoice Table -->
      <div
        v-if="filteredInvoices.length > 0"
        class="overflow-x-auto rounded-lg border border-gray-200"
      >
        <table class="w-full table-auto">
          <thead>
            <tr class="bg-gray-100 text-left">
              <th class="px-6 py-3 text-gray-600 font-semibold">
                Invoice Number
              </th>
              <th class="px-6 py-3 text-gray-600 font-semibold">Date</th>
              <th class="px-6 py-3 text-gray-600 font-semibold">Client Name</th>
              <th class="px-6 py-3 text-gray-600 font-semibold">
                Total Amount
              </th>
              <th class="px-6 py-3 text-gray-600 font-semibold text-center">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="invoice in filteredInvoices"
              :key="invoice.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 text-gray-900">{{ invoice.number }}</td>
              <td class="px-6 py-4 text-gray-600">{{ invoice.date }}</td>
              <td class="px-6 py-4 text-gray-900">{{ invoice.client }}</td>
              <td class="px-6 py-4 text-gray-900 font-medium">
                ${{ invoice.amount }}
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-center gap-4">
                  <button
                    class="text-gray-600 hover:text-gray-800 font-medium"
                    @click="editInvoice(invoice)"
                  >
                    Edit
                  </button>
                  <button
                    class="text-blue-600 hover:text-blue-800 font-medium"
                    @click="viewInvoice(invoice)"
                  >
                    View
                  </button>
                  <button
                    class="text-gray-600 hover:text-gray-800 font-medium"
                    @click="downloadInvoice(invoice)"
                  >
                    Download
                  </button>
                  <button
                    class="text-red-600 hover:text-red-800 font-medium"
                    @click="deleteInvoice(invoice.id)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- No Invoices Found -->
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
          <h3 class="text-xl font-semibold mb-2">No Invoices Found</h3>
          <p class="text-gray-500">
            There are no invoices matching your search criteria.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

// Reactive data for invoices
const searchQuery = ref("");
const invoices = ref([
  {
    id: 1,
    number: "#INV-2024-001",
    date: "Jan 15, 2024",
    client: "Tech Solutions Inc.",
    amount: "2500.00",
  },
  {
    id: 2,
    number: "#INV-2024-002",
    date: "Jan 18, 2024",
    client: "Global Systems Ltd.",
    amount: "1800.00",
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

// Edit Invoice (Placeholder function)
const editInvoice = (invoice) => {
  console.log("Editing invoice:", invoice);
};

// View Invoice
const viewInvoice = (invoice) => {
  console.log("Viewing invoice:", invoice);
};

// Download Invoice
const downloadInvoice = (invoice) => {
  console.log("Downloading invoice:", invoice);
};

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
