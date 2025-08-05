<template>
  <FullCalendar :options="calendarOptions" />
</template>

<script setup>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import {onMounted, ref} from 'vue'

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  events: []
})

// 投薬データを取得
const fetchMedicines = async () => {
  try {
    const res = await fetch('http://localhost:8000/medicines/schedule')
    const data = await res.json()

    calendarOptions.value.events = data.map(item => ({
      title: `${item.name}（${item.timing.join("・")}）`,
      start: item.date
    }))
  } catch (error) {
    console.error('カレンダーデータの取得に失敗:', error)
  }
}

onMounted(async () => {
  await fetchMedicines()
})
</script>

<style scoped>
</style>
