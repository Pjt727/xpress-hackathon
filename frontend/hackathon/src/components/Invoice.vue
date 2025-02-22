<template>
  <div
    class="absolute inset-0 flex items-center justify-center bg-gray-100 p-6"
    v-if="!invoiceView"
  >
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-xl p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">
        Invoice Generator
      </h1>

      <!-- PDF Upload Section -->
      <div
        v-if="!invoiceGenerated"
        class="mb-8 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
      >
        <i class="fas fa-file-upload text-4xl text-gray-400 mb-4"></i>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">
          Drag & Drop PDF here
        </h3>
        <p class="text-sm text-gray-500 mb-4">or</p>
        <input
          type="file"
          id="fileInput"
          accept="application/pdf"
          class="hidden"
          @change="handleFileUpload"
        />
        <button
          @click="openFileInput"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Choose File
        </button>
        <p class="text-sm text-gray-500 mt-2">Maximum file size: 10MB</p>
      </div>

      <!-- Invoice Details Preview with Editable Fields -->
      <div v-if="invoiceGenerated" class="bg-gray-50 rounded-lg p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Invoice Details</h2>
        <button
          @click="toggleEdit"
          class="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {{ isEditing ? "Save" : "Edit" }}
        </button>
        <div class="grid md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-500">From</h3>
              <input
                v-if="isEditing"
                v-model="invoice.from.name"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-800">{{ invoice.from.name }}</p>
              <input
                v-if="isEditing"
                v-model="invoice.from.address"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-600">{{ invoice.from.address }}</p>
              <input
                v-if="isEditing"
                v-model="invoice.from.email"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-600">{{ invoice.from.email }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Invoice Number</h3>
              <input
                v-if="isEditing"
                v-model="invoice.number"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-800">{{ invoice.number }}</p>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-500">To</h3>
              <input
                v-if="isEditing"
                v-model="invoice.to.name"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-800">{{ invoice.to.name }}</p>
              <input
                v-if="isEditing"
                v-model="invoice.to.address"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-600">{{ invoice.to.address }}</p>
              <input
                v-if="isEditing"
                v-model="invoice.to.email"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-600">{{ invoice.to.email }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Date</h3>
              <input
                v-if="isEditing"
                v-model="invoice.date"
                type="date"
                class="border p-2 w-full rounded"
              />
              <p v-else class="text-gray-800">{{ invoice.date }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="invoiceGenerated" class="flex justify-end space-x-4 mt-6">
        <button
          @click="resetForm"
          class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300 transition duration-200"
        >
          Clear
        </button>
        <button
          @click="toggleInvoiceView"
          class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition duration-200"
        >
          Generate Invoice
        </button>
      </div>
    </div>
  </div>

  <InvoiceView v-if="invoiceView" />
</template>

<script setup>
import { ref } from "vue";
import InvoiceView from "./InvoiceView.vue";

const invoiceGenerated = ref(false);
const invoiceView = ref(false);
const isEditing = ref(false);

const invoice = ref({
  from: {
    name: "Tech Solutions Inc.",
    address: "123 Business Ave",
    email: "contact@techsolutions.com",
  },
  number: "#INV-2024-001",
  to: {
    name: "Client Company LLC",
    address: "456 Client Street",
    email: "billing@clientcompany.com",
  },
  date: "2024-01-15",
});

const openFileInput = () => {
  document.getElementById("fileInput").click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  if (file.type !== "application/pdf") {
    alert("Please upload a PDF file");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    alert("File size exceeds 10MB limit");
    return;
  }
  // Simulating processing delay
  setTimeout(() => {
    invoiceGenerated.value = true;
  }, 1000);
};

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
};

const toggleInvoiceView = () => {
  invoiceView.value = true;
};

const resetForm = () => {
  invoiceGenerated.value = false;
  invoiceView.value = false;
};
</script>

<style>
body {
  font-family: "Inter", sans-serif;
  background-color: #f8f9fa;
  color: #333;
  margin: 0;
}
</style>
