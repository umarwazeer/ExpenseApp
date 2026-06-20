src/pages/components/settings/CurrencySelector.vue
<template>
  <q-select dense :dark="dark" v-model="model" :options="currencyOptions" emit-value map-options />
</template>

<script setup>
import { computed } from 'vue'


const props = defineProps({
  modelValue: { type: String, default: 'USD' },
  dark: { type: Boolean, default: false }
});
const emit = defineEmits(['update:modelValue','change']);

const currencyOptions = [
  { label: 'USD', value: 'USD' },
  { label: 'EUR', value: 'EUR' },
  { label: 'PKR', value: 'PKR' },
  { label: 'INR', value: 'INR' }
];

const model = computed({
  get: () => props.modelValue,
  set: (v) => { emit('update:modelValue', v); emit('change', v); }
});
</script>
