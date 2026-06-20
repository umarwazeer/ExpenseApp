<template>
  <q-toggle dense v-model="value" @update:model-value="onToggle" />
</template>

<script setup>
import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';

const props = defineProps({
  modelValue: { type: Boolean, default: false }
});
const emit = defineEmits(['update:modelValue']);

const $q = useQuasar();
const value = ref(props.modelValue);

watch(() => props.modelValue, (v) => value.value = v);

function onToggle(v) {
  emit('update:modelValue', v);
  // Also apply to Quasar dark
  $q.dark.set(v);
  // you might also persist via store in parent
}
</script>
