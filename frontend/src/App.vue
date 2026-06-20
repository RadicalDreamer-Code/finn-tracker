<template>
  <AppLayout>
    <RouterView />
  </AppLayout>
  <Toast position="bottom-right" />
</template>

<script setup lang="ts">
import Toast from 'primevue/toast'
import AppLayout from '@/components/layout/AppLayout.vue'
</script>
