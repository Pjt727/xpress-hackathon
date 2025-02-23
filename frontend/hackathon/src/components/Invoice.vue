<template>
  <div
    class="absolute inset-0 flex items-center justify-center bg-gray-100 p-6"
    v-if="!invoiceView"
  >
    <div
      class="w-full max-w-4xl bg-white rounded-lg shadow-xl p-8 overflow-hidden"
    >
      <h1 class="text-4xl font-bold text-gray-800 mb-8 text-center">
        Invoice Generator
      </h1>

      <!-- PDF Upload Section -->
      <div
        v-if="!invoiceGenerated"
        class="mb-10 border-2 border-dashed border-gray-300 rounded-lg p-10 text-center"
      >
        <i class="fas fa-file-upload text-5xl text-gray-400 mb-6"></i>
        <h3 class="text-xl font-semibold text-gray-700 mb-4">
          Drag & Drop PDF here
        </h3>
        <p class="text-sm text-gray-500 mb-6">or</p>
        <input
          type="file"
          id="fileInput"
          accept="application/pdf"
          class="hidden"
          @change="handleFileUpload"
        />
        <button
          @click="openFileInput"
          class="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Choose File
        </button>
        <p class="text-sm text-gray-500 mt-4">Maximum file size: 10MB</p>
      </div>

      <!-- Invoice Details Preview with Editable Fields -->
      <div
        v-if="invoiceGenerated"
        class="bg-gray-50 rounded-lg p-8 mb-8 max-h-[600px] overflow-y-auto"
      >
        <h2 class="text-2xl font-semibold mb-6">Invoice Details</h2>

        <div class="grid md:grid-cols-2 gap-8">
          <div class="space-y-6">
            <div>
              <h3 class="text-lg font-medium text-gray-600">From</h3>
              <input
                v-if="isEditing"
                v-model="invoice.from.name"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Name"
              />
              <p v-else class="text-gray-800 text-lg">
                {{ invoice.from.name }}
              </p>
              <input
                v-if="isEditing"
                v-model="invoice.from.address"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Address"
              />
              <p v-else class="text-gray-600 text-sm">
                {{ invoice.from.address }}
              </p>
              <input
                v-if="isEditing"
                v-model="invoice.from.email"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Email"
              />
              <p v-else class="text-gray-600 text-sm">
                {{ invoice.from.email }}
              </p>
            </div>
            <div>
              <h3 class="text-lg font-medium text-gray-600">Invoice Number</h3>
              <input
                v-if="isEditing"
                v-model="invoice.number"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Invoice Number"
              />
              <p v-else class="text-gray-800 text-lg">{{ invoice.number }}</p>
            </div>
          </div>
          <div class="space-y-6">
            <div>
              <h3 class="text-lg font-medium text-gray-600">To</h3>
              <input
                v-if="isEditing"
                v-model="invoice.to.name"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Name"
              />
              <p v-else class="text-gray-800 text-lg">{{ invoice.to.name }}</p>
              <input
                v-if="isEditing"
                v-model="invoice.to.address"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Address"
              />
              <p v-else class="text-gray-600 text-sm">
                {{ invoice.to.address }}
              </p>
              <input
                v-if="isEditing"
                v-model="invoice.to.email"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Email"
              />
              <p v-else class="text-gray-600 text-sm">{{ invoice.to.email }}</p>
            </div>
            <div>
              <h3 class="text-lg font-medium text-gray-600">Date</h3>
              <input
                v-if="isEditing"
                v-model="invoice.date"
                type="date"
                class="border mt-1 mb-1 border-gray-300 p-2 w-full rounded-lg text-sm"
                placeholder="Date"
              />
              <p v-else class="text-gray-800 text-lg">{{ invoice.date }}</p>
            </div>
          </div>
        </div>

        <!-- Products Table -->
        <div class="mt-8">
          <h3 class="text-xl font-medium text-gray-600 mb-4">Products</h3>
          <table
            class="min-w-full table-auto border-collapse border border-gray-300"
          >
            <thead>
              <tr>
                <th class="px-4 py-2 border border-gray-300">Description</th>
                <th class="px-4 py-2 border border-gray-300">Qty</th>
                <th class="px-4 py-2 border border-gray-300">Rate</th>
                <th class="px-4 py-2 border border-gray-300">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in invoice.products" :key="index">
                <td class="px-4 py-2 border border-gray-300">
                  <input
                    v-if="isEditing"
                    v-model="product.description"
                    class="border border-gray-300 p-2 w-full rounded-md text-sm"
                  />
                  <p v-else class="text-gray-800">{{ product.description }}</p>
                </td>
                <td class="px-4 py-2 border border-gray-300">
                  <input
                    v-if="isEditing"
                    v-model="product.qty"
                    type="number"
                    class="border border-gray-300 p-2 w-full rounded-md text-sm"
                  />
                  <p v-else class="text-gray-800">{{ product.qty }}</p>
                </td>
                <td class="px-4 py-2 border border-gray-300">
                  <input
                    v-if="isEditing"
                    v-model="product.rate"
                    type="number"
                    class="border border-gray-300 p-2 w-full rounded-md text-sm"
                  />
                  <p v-else class="text-gray-800">{{ product.rate }}</p>
                </td>
                <td class="px-4 py-2 border border-gray-300">
                  <p class="text-gray-800">{{ product.qty * product.rate }}</p>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Add Product Button -->
          <div class="justify-stretch">
            <button
              @click="addProduct"
              class="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-200"
            >
              Add Product
            </button>

            <!-- External/Internal Selection -->
            <tg class="ml-50 m-4">External/Internal </tg>
            <select
              v-model="invoice.externalInternal"
              class="rounded-md bg-white px-6 py-2 text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50"
            >
              <option value="" disabled selected></option>
              <option value="external">External</option>
              <option value="internal">Internal</option>
            </select>

            <!-- Paid/Unpaid Selection -->
            <tg class="m-4"> Paid </tg>
            <select
              v-model="invoice.paidStatus"
              class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50"
            >
              <option value="" disabled selected></option>
              <option value="paid">Paid</option>
              <option value="unpaid">Unpaid</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Buttons Section (Back, Edit/Save, Generate Invoice) -->
      <div v-if="invoiceGenerated" class="flex justify-between space-x-6 mt-8">
        <div class="justify-start space-x-6">
          <button
            @click="resetForm"
            class="bg-gray-200 text-gray-700 px-8 py-3 rounded-lg hover:bg-gray-300 transition duration-200"
          >
            Back
          </button>

          <!-- Edit/Save Button next to Back -->
          <button
            @click="toggleEdit"
            class="px-8 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-200"
          >
            {{ isEditing ? "Save" : "Edit" }}
          </button>
        </div>
        <div class="justify-start space-x-6">
          <button
            @click="saveInvoice"
            class="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            Save
          </button>

          <button
            @click="toggleInvoiceView"
            class="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 transition duration-200"
          >
            Generate Invoice
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Pass the edited invoice data to InvoiceView -->
  <InvoiceView v-if="invoiceView" :invoiceData="invoice" />
</template>
111
<script setup>
// Import relevant hooks and components
import { ref } from "vue";
import axios from "axios";
import InvoiceView from "./InvoiceView.vue";

// Define necessary state variables
const invoiceGenerated = ref(false);
const invoiceView = ref(false);
const isEditing = ref(false);

// Sample invoice data
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
  products: [
    { description: "Product 1", qty: 1, rate: 100 },
    { description: "Product 2", qty: 2, rate: 50 },
  ],
});

// Function for handling file upload
const openFileInput = () => {
  document.getElementById("fileInput").click();
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (file.type !== "application/pdf") {
    alert("Please upload a PDF file");
    console.log("Upload failed: Not a PDF file");
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    alert("File size exceeds 10MB limit");
    console.log("Upload failed: File too large");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${domainName}/invoice-upload`, {
      method: "POST",
      body: formData,
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const result = await response.json();
    console.log("Upload successful:", result);
    alert(result.message);

    invoiceGenerated.value = true;
  } catch (error) {
    console.error("Upload failed:", error);
    alert("File upload failed. Please try again.");
  }
};

// Toggle the edit state
const toggleEdit = () => {
  isEditing.value = !isEditing.value;
};

// Toggle the invoice view
const toggleInvoiceView = () => {
  invoiceView.value = true;
};

// Reset the form
const resetForm = () => {
  invoiceGenerated.value = false;
  invoiceView.value = false;
};

// Add a new product to the invoice
const addProduct = () => {
  invoice.value.products.push({ description: "", qty: 1, rate: 0 });
};

// Calculate the total invoice cost
const calculateTotalCost = () => {
  return invoice.value.products.reduce((total, product) => {
    return total + product.qty * product.rate;
  }, 0);
};

// Save the invoice to the database
// Save the invoice to the database
const saveInvoice = async () => {
  // Assign true/false based on selected values for Paid/Unpaid and External/Internal
  const isSettled = invoice.value.paidStatus === "paid"; // true if "Paid", false if "Unpaid"
  const isOutgoing = invoice.value.externalInternal === "external"; // true if "External", false if "Internal"

  const invoiceData = {
    group_id: 1,
    total_invoice_cost: invoice.value.products.reduce(
      (sum, product) => sum + product.qty * product.rate,
      0
    ),
    is_settled: isSettled,
    is_outgoing: isOutgoing,
    item: invoice.value.products.map((product) => ({
      description: product.description,
      qty: product.qty,
      rate: product.rate,
      amount: product.qty * product.rate,
    })),
    details: [
      {
        from: {
          name: invoice.value.from.name,
          address: invoice.value.from.address,
          email: invoice.value.from.email,
        },
        to: {
          name: invoice.value.to.name,
          address: invoice.value.to.address,
          email: invoice.value.to.email,
        },
        date: new Date(invoice.value.date).toISOString().split("T")[0],
        number: invoice.value.number,
      },
    ],
  };

  console.log("Sending invoiceData:", invoiceData);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/invoice",
      invoiceData
    );
    console.log("Invoice saved successfully:", response.data);
  } catch (error) {
    console.error("Error saving invoice:", error.response?.data || error);
  }
};
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
  background-color: #f8f9fa;
  color: #333;
  margin: 0;
}
</style>
