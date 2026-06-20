<template>
  <div
    class="flex gap-2"
    :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
  >
    <!-- BOT ICON -->
    <div
      v-if="message.role === 'assistant'"
      class="w-8 h-8 rounded-full bg-purple-500 text-white flex items-center justify-center"
    >
      ✨
    </div>

    <!-- MESSAGE -->
    <div
      class="max-w-[75%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap"
      :class="
        message.role === 'user'
          ? 'bg-purple-600 text-white rounded-br-sm'
          : 'bg-white text-gray-900 rounded-bl-sm'
      "
    >
      {{ message.content }}
    </div>

    <!-- USER ICON -->
    <div
      v-if="message.role === 'user'"
      class="w-8 h-8 rounded-full bg-purple-400 text-white flex items-center justify-center"
    >
      👤
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: Object,
});
</script>
