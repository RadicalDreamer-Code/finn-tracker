<template>
  <div class="watchlist-view">
    <div class="view-header">
      <h1 class="view-title">Watchlist</h1>
      <div class="view-toolbar">
        <IconField class="filter-field">
          <InputIcon class="pi pi-search" />
          <InputText v-model="filterQuery" placeholder="Filter…" class="w-full" size="small" />
        </IconField>
        <Button icon="pi pi-plus" label="Add" size="small" @click="showDialog = true" />
      </div>
    </div>

    <div class="card-grid" v-if="!store.loading">
      <StockCard
        v-for="item in filteredEntries"
        :key="item.entry.symbol"
        :item="item"
        @select="openDetail"
        @remove="confirmRemove"
      />
      <div class="empty-state" v-if="filteredEntries.length === 0">
        <i class="pi pi-chart-line" />
        <span v-if="store.entries.length === 0">Add your first symbol</span>
        <span v-else>No match for "{{ filterQuery }}"</span>
      </div>
    </div>

    <div class="card-grid loading-state" v-else>
      <Skeleton v-for="n in 6" :key="n" height="3.5rem" border-radius="8px" />
    </div>

    <AddSymbolDialog v-model="showDialog" @add="handleAdd" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Skeleton from 'primevue/skeleton'
import { useToast } from 'primevue/usetoast'
import { useWatchlistStore } from '@/stores/watchlist'
import AddSymbolDialog from '@/components/AddSymbolDialog.vue'
import StockCard from '@/components/StockCard.vue'

const store = useWatchlistStore()
const router = useRouter()
const toast = useToast()
const showDialog = ref(false)
const filterQuery = ref('')

const filteredEntries = computed(() =>
  store.entries.filter((e) =>
    e.entry.symbol.toLowerCase().includes(filterQuery.value.toLowerCase()),
  ),
)

onMounted(() => store.fetchWatchlist())

function openDetail(symbol: string) {
  store.selectSymbol(symbol)
  router.push({ name: 'stock', params: { symbol } })
}

async function handleAdd(symbol: string) {
  try {
    await store.addSymbol(symbol)
    toast.add({ severity: 'success', summary: `${symbol} added`, life: 2500 })
  } catch {
    toast.add({ severity: 'error', summary: 'Already in watchlist', life: 2500 })
  }
}

async function confirmRemove(symbol: string) {
  try {
    await store.removeSymbol(symbol)
    toast.add({ severity: 'info', summary: `${symbol} removed`, life: 2000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Could not remove', life: 2000 })
  }
}
</script>

<style scoped>
.watchlist-view {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.view-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.view-toolbar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-field {
  width: 220px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.75rem;
}

.loading-state {
  gap: 0.75rem;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 3rem 1rem;
  color: var(--p-text-muted-color);
  font-size: 0.9rem;
  text-align: center;
}

.empty-state .pi {
  font-size: 2rem;
  opacity: 0.4;
}
</style>
