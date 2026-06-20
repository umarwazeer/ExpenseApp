<!-- src/pages/components/settings/LanguageSelector.vue -->
<template>
  <q-select dense :dark="dark" v-model="model" :options="options" emit-value map-options />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: 'en' },
  dark: { type: Boolean, default: false }
});
const emit = defineEmits(['update:modelValue','change']);

const options = [
  { label: 'English', value: 'en' },
  { label: 'Urdu', value: 'ur' },
  { label: 'Spanish', value: 'es' }
];

const model = computed({
  get: () => props.modelValue,
  set: (v) => { emit('update:modelValue', v); emit('change', v); }
});
</script>
