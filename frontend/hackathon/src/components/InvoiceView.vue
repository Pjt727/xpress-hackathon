<template>
  <div class="min-h-screen p-6 bg-gray-50 flex items-center justify-center">
    <div class="container max-w-4xl mx-auto bg-white rounded-lg">
      <div class="p-8" ref="pdfContent">
        <div class="flex justify-between items-start">
          <div>
            <img
              src="https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=150"
              alt="Company Logo"
              class="h-16 w-auto mb-4"
            />
            <h2 class="text-2xl font-bold text-gray-800">
              {{ invoiceData.from.name }}
            </h2>
            <p class="text-sm text-gray-600">{{ invoiceData.from.address }}</p>
            <p class="text-sm text-gray-600">{{ invoiceData.from.email }}</p>
          </div>
          <div class="text-right">
            <h1 class="text-4xl font-bold text-gray-800">INVOICE</h1>
            <div class="mt-4">
              <p class="text-sm text-gray-600">
                Invoice #: {{ invoiceData.number }}
              </p>
              <p class="text-sm text-gray-600">Date: {{ invoiceData.date }}</p>
            </div>
          </div>
        </div>

        <div class="mt-8">
          <h3 class="text-lg font-bold text-gray-700">Bill To:</h3>
          <div class="mt-2">
            <p class="text-gray-700">{{ invoiceData.to.name }}</p>
            <p class="text-gray-600">{{ invoiceData.to.address }}</p>
            <p class="text-gray-600">{{ invoiceData.to.email }}</p>
          </div>
        </div>
        <div class="mt-8">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-100">
                <th class="text-left py-3 px-4 text-gray-700">Description</th>
                <th class="text-center py-3 px-4 text-gray-700">Qty</th>
                <th class="text-right py-3 px-4 text-gray-700">Rate</th>
                <th class="text-right py-3 px-4 text-gray-700">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b hover:bg-gray-50">
                <td class="py-4 px-4">Web Development Services</td>
                <td class="text-center py-4 px-4">1</td>
                <td class="text-right py-4 px-4">$2,000.00</td>
                <td class="text-right py-4 px-4">$2,000.00</td>
              </tr>
              <tr class="border-b hover:bg-gray-50">
                <td class="py-4 px-4">UI/UX Design</td>
                <td class="text-center py-4 px-4">1</td>
                <td class="text-right py-4 px-4">$1,500.00</td>
                <td class="text-right py-4 px-4">$1,500.00</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-8 flex justify-end">
          <div class="w-1/3">
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Subtotal:</span>
              <span class="text-gray-800">$3,500.00</span>
            </div>
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Tax (10%):</span>
              <span class="text-gray-800">$350.00</span>
            </div>
            <div class="flex justify-between mb-2 pt-2 border-t">
              <span class="font-bold text-gray-700">Total:</span>
              <span class="font-bold text-blue-600">$3,850.00</span>
            </div>
          </div>
        </div>

        <div class="mt-12">
          <h4 class="text-lg font-bold text-gray-700 mb-4">
            Terms & Conditions
          </h4>
          <p class="text-sm text-gray-600">
            Payment is due within 15 days of invoice date. Please include
            invoice number on your payment.
          </p>
        </div>

        <div class="mt-8 flex justify-end space-x-4 print-hidden print:hidden">
          <button
            @click="printInvoice"
            class="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Print/Download PDF
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from "vue";
import { jsPDF } from "jspdf";

const props = defineProps({
  invoiceData: Object,
});

const printInvoice = () => {
  window.print();
};
</script>

<style>
body {
  font-family: "Inter", sans-serif;
  background-color: #f8f9fa;
  color: #333;
  margin: 0;
}

@media print {
  .print-hidden {
    display: none !important;
  }
}
</style>
