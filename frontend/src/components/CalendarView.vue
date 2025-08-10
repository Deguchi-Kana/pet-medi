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

// 投薬スケジュールを取得
const fetchSchedule = async () => {
  try {
    const res = await fetch('http://localhost:8000/schedule')
    const data = await res.json()

    calendarOptions.value.events = data.map(item => ({
      title: `${item.medicine_name}（${item.timing.join("・")}）`,
      start: item.date
    }))
  } catch (error) {
    console.error('カレンダーデータの取得に失敗:', error)
  }
}

onMounted(async () => {
  await fetchSchedule()
})
</script>

<style scoped>
</style>
