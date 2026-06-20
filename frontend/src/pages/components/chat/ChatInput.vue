<template>
  <div class="p-3 bg-white border-t flex items-center gap-2">
    <input
      v-model="text"
      @keyup.enter="submit"
      placeholder="Ask about your finances..."
      class="flex-1 px-4 py-2 border rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
    />
    <button
      @click="submit"
      class="w-10 h-10 rounded-full bg-purple-600 text-white flex items-center justify-center"
    >
      ➤
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["send"]);
const text = ref("");

const submit = () => {
  if (!text.value.trim()) return;
  emit("send", text.value);
  text.value = "";
};
</script>
