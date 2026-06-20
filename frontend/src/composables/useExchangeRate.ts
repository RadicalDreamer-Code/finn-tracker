import { ref } from 'vue'

const rate = ref<number | null>(null)
const loading = ref(false)
const error = ref(false)

async function fetchRate() {
  if (rate.value !== null || loading.value) return
  loading.value = true
  try {
    const res = await fetch('https://api.frankfurter.dev/v1/latest?from=USD&to=EUR')
    const data = await res.json()
    rate.value = data.rates.EUR
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

fetchRate()

export function useExchangeRate() {
  return { rate, loading, error }
}
