<template>
  <Dialog
    v-model:visible="visible"
    header="Add Symbol"
    modal
    :style="{ width: '420px' }"
    @hide="reset"
  >
    <div class="search-wrapper">
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="query"
          placeholder="Search symbol or company…"
          class="w-full"
          autofocus
          @input="onInput"
        />
      </IconField>
    </div>

    <div class="results" v-if="results.length > 0">
      <div
        v-for="result in results"
        :key="result.symbol"
        class="result-item"
        @click="select(result.symbol)"
      >
        <div class="result-symbol">{{ result.symbol }}</div>
        <div class="result-desc">{{ result.description }}</div>
        <Tag :value="result.type" severity="secondary" class="result-type" />
      </div>
    </div>

    <div class="empty" v-else-if="query.length >= 1 && !searching">
      <i class="pi pi-search" />
      <span>No results for "{{ query }}"</span>
    </div>

    <div class="searching" v-if="searching">
      <ProgressSpinner style="width: 24px; height: 24px" />
    </div>

    <template #footer>
      <Button label="Cancel" text severity="secondary" @click="visible = false" />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'
import { stocksApi } from '@/api/stocks'
import type { SymbolSearchResult } from '@/types'

const visible = defineModel<boolean>({ required: true })
const emit = defineEmits<{ add: [symbol: string] }>()

const query = ref('')
const results = ref<SymbolSearchResult[]>([])
const searching = ref(false)
let debounceTimer: ReturnType<typeof setTimeout>

async function onInput() {
  clearTimeout(debounceTimer)
  if (query.value.length < 1) {
    results.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    searching.value = true
    try {
      results.value = await stocksApi.search(query.value)
    } finally {
      searching.value = false
    }
  }, 300)
}

function select(symbol: string) {
  emit('add', symbol)
  visible.value = false
}

function reset() {
  query.value = ''
  results.value = []
}
</script>

<style scoped>
.search-wrapper {
  margin-bottom: 0.75rem;
}

.results {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.result-item:hover {
  background: var(--p-surface-100);
}

.result-symbol {
  font-weight: 600;
  font-size: 0.875rem;
  min-width: 72px;
  color: var(--p-text-color);
}

.result-desc {
  flex: 1;
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-type {
  font-size: 0.65rem;
  padding: 1px 5px;
  flex-shrink: 0;
}

.empty {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
  color: var(--p-text-muted-color);
  font-size: 0.875rem;
}

.searching {
  display: flex;
  justify-content: center;
  padding: 0.75rem 0;
}
</style>
