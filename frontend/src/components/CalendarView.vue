<template>
  <FullCalendar :options="calendarOptions" />
  <Tooltip :visible="tooltip.visible" :style="tooltip.style" :data="tooltip.data" />
</template>

<script setup>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { ref, onMounted } from 'vue'
import Tooltip from "./Tooltip.vue";

const tooltip = ref({
  visible: false,
  style: {
    position: 'absolute',
    top: '0px',
    left: '0px',
  },
  data: {
    medicine_name: '',
    pet_name: '',
    dosage: '',
    timing: [],
    notify: false,
  },
})

// ツールチップ表示
const eventMouseEnter = (info) => {
  tooltip.value.visible = true
  tooltip.value.data = info.event.extendedProps
  tooltip.value.style.top = info.jsEvent.pageY + 10 + 'px'
  tooltip.value.style.left = info.jsEvent.pageX + 10 + 'px'
}
// ツールチップ非表示
const eventMouseLeave = () => {
  tooltip.value.visible = false
}

// カレンダーの設定
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  events: [],
  eventMouseEnter,
  eventMouseLeave
})

// 投薬スケジュールを取得
const fetchSchedule = async () => {
  try {
    const res = await fetch('http://localhost:8000/schedule')
    const data = await res.json()

    calendarOptions.value.events = data.map(item => ({
      title: `${item.medicine_name}（${item.timing.join("・")}）`,
      start: item.date,
      extendedProps: {
        medicine_name: item.medicine_name,
        pet_name: item.pet_name,
        dosage: item.dosage,
        timing: item.timing,
      },
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
