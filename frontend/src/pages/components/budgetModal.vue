<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0 bg-black/40" @click="$emit('close')" />
    <div class="relative w-full max-w-sm rounded-lg bg-white p-4 shadow-lg">
      <div class="mb-3 flex justify-between">
        <h3 class="font-semibold">{{ title }}</h3>
        <button class="text-gray-400" @click="$emit('close')">✕</button>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String });
</script>
