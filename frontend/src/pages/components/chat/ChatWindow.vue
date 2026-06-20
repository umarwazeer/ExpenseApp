<template>
  <div ref="container" class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-100">
    <ChatMessage
      v-for="(msg, i) in messages"
      :key="i"
      :message="msg"
    />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import ChatMessage from "./ChatMessage.vue";

const props = defineProps({
  messages: Array,
});

const container = ref(null);

watch(
  () => props.messages.length,
  async () => {
    await nextTick();
    container.value.scrollTop = container.value.scrollHeight;
  }
);
</script>
