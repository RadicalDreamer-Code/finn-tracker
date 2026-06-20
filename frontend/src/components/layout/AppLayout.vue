<template>
  <div class="app-layout">
    <WatchlistSidebar />
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import WatchlistSidebar from '@/components/sidebar/WatchlistSidebar.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--p-surface-ground);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
