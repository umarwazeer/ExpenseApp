<template>
  <div class="flex flex-col justify-between rounded-lg border bg-white p-3 shadow-sm lg:p-4">
    <p class="text-xs font-medium uppercase tracking-wide text-gray-500">
      {{ title }}
    </p>
    <p
      v-if="value !== null"
      class="mt-1 text-lg font-semibold text-gray-900 lg:text-xl"
    >
      {{ displayValue }}
    </p>
    <p
      v-else
      class="mt-1 text-sm font-medium text-gray-800"
    >
      {{ text }}
    </p>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  title: { type: String, required: true },
  value: { type: Number, default: null },
  text: { type: String, default: "" },
  currency: { type: Boolean, default: true }
});

const displayValue = computed(() => {
  if (props.value === null) return "";
  if (!props.currency) return props.value;
  return "₹" + props.value.toLocaleString("en-IN", { maximumFractionDigits: 0 });
});
</script>