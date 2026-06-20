<template>
  <q-card flat bordered class="q-pa-md">
    <div class="row items-center justify-between">
      <div>
        <div class="text-caption text-grey">{{ title }}</div>
        <div class="text-h6 text-weight-bold">₹{{ value }}</div>
      </div>
      <q-icon :name="icon" :color="color" size="32px" />
    </div>
  </q-card>
</template>

<script setup>
defineProps({
  title: String,
  value: Number,
  icon: String,
  color: String
})
</script>
