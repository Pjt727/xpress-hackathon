<template>
  <div class="container mx-auto px-4 py-8 bg-gray-50">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Invoice History</h1>
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
              <th class="px-6 py-3 text-gray-600 font-semibold">
                External/Internal
              </th>
              <th class="px-6 py-3 text-gray-600 font-semibold">Paid</th>
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
              <td class="px-6 py-4 text-gray-900">
                {{ invoice.details.to.name }}
              </td>
              <td class="px-6 py-4 text-gray-900 font-medium">
                ${{ invoice.total_invoice_cost }}
              </td>
              <td class="px-6 py-4 text-gray-900 font-medium">
                {{ invoice.is_outgoing ? "External" : "Internal" }}
              </td>
              <td class="px-6 py-4 text-gray-900 font-medium">
                {{ invoice.is_settled ? "✔️" : "❌" }}
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-center gap-4">
                  <button
                    class="text-green-600 hover:text-green-800 font-medium"
                    @click="viewInvoice(invoice)"
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
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Reactive data for invoices
const searchQuery = ref("");
const invoices = ref([]); // We will fetch invoices from the backend

// Fetch invoices from the API
const fetchInvoices = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/invoice-uploads");
    invoices.value = response.data.map((invoice) => ({
      id: invoice.group_id,
      number: invoice.details[0]?.number || "Unknown", // Constructing invoice number based on group_id (or replace with your logic)
      date: invoice.details[0]?.date || "Unknown", // Date from details (replace with your field name)
      client: invoice.details[0]?.name || "Unknown", // Client name from details (replace with your field name)
      total_invoice_cost: invoice.total_invoice_cost,
      is_outgoing: invoice.is_outgoing,
      is_settled: invoice.is_settled,
    }));
  } catch (error) {
    console.error("Error fetching invoices:", error);
  }
};

// Fetch invoices when component is mounted
onMounted(() => {
  fetchInvoices();
});

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
