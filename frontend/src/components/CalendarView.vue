<template>
  <!-- ペット色の凡例 -->
  <div class="calendar-legend">
    <h4 class="legend-title">ペット別色分け</h4>
    <div class="legend-items">
      <div v-for="pet in pets" :key="pet.id" class="legend-item">
        <div class="legend-color" :style="{ backgroundColor: getPetColor(pet.id) }"></div>
        <span class="legend-label">{{ pet.name }}</span>
      </div>
    </div>
  </div>

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

// ペットIDごとの色を生成する関数
const generatePetColors = (petCount) => {
  const colors = [
    '#3b82f6',  // 青
    '#8b5cf6',  // 紫
    '#06b6d4',  // シアン
    '#f59e0b',  // オレンジ
    '#ef4444',  // 赤
    '#10b981',  // 緑
    '#059669',  // 深緑
    '#7c3aed',  // 深紫
    '#ec4899',  // ピンク
    '#84cc16',  // ライム
    '#f97316',  // オレンジ
    '#06b6d4',  // シアン
    '#8b5cf6',  // 紫
    '#3b82f6',  // 青
    '#ef4444',  // 赤
  ]
  
  const petColors = {}
  for (let i = 0; i < petCount; i++) {
    petColors[i + 1] = colors[i % colors.length]
  }
  return petColors
}

// ペット情報を取得
const pets = ref([])
const petColors = ref({})

const fetchPets = async () => {
  try {
    const response = await fetch('http://localhost:8000/pets')
    if (response.ok) {
      pets.value = await response.json()
      // ペット数に応じて色を生成
      petColors.value = generatePetColors(pets.value.length)
      console.log('ペット情報取得完了:', pets.value) // デバッグ用
      console.log('色マッピング生成完了:', petColors.value) // デバッグ用
      
      // ペット情報取得完了後にスケジュールを取得
      await fetchSchedule()
    }
  } catch (error) {
    console.error('ペット情報の取得に失敗しました:', error)
  }
}

// ペットIDに応じた色を取得
const getPetColor = (petId) => {
  if (!petId) return '#6b7280' // デフォルトはグレー
  return petColors.value[petId] || '#6b7280'
}

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
  eventMouseLeave,
  eventColor: '#10b981', // デフォルト色（緑）
  eventTextColor: '#ffffff',
  eventDisplay: 'block',
  height: 'auto',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,dayGridWeek'
  },
  locale: 'ja',
  buttonText: {
    today: '今日',
    month: '月',
    week: '週'
  }
})

// 投薬スケジュールを取得
const fetchSchedule = async () => {
  try {
    const res = await fetch('http://localhost:8000/schedule')
    const data = await res.json()
    
    console.log('スケジュールデータ:', data) // デバッグ用
    console.log('ペット情報:', pets.value) // デバッグ用
    console.log('ペット色マッピング:', petColors.value) // デバッグ用

    calendarOptions.value.events = data.map(item => {
      const petColor = getPetColor(item.pet_id)
      console.log(`イベント: ${item.medicine_name}, ペットID: ${item.pet_id}, 色: ${petColor}`) // デバッグ用
      
      // timingフィールドの安全な処理
      let timing = []
      if (item.timing) {
        if (Array.isArray(item.timing)) {
          timing = item.timing
        } else if (typeof item.timing === 'string') {
          // カンマ区切りの文字列を配列に分割
          timing = item.timing.split(',').map(t => t.trim()).filter(t => t)
        }
      }
      
      const timingText = timing.length > 0 ? timing.join("・") : "時間未定"
      
      return {
        title: `${item.medicine_name}（${timingText}）`,
        start: item.date,
        backgroundColor: petColor,
        borderColor: petColor,
        textColor: '#ffffff',
        extendedProps: {
          medicine_name: item.medicine_name,
          pet_name: item.pet_name,
          pet_id: item.pet_id,
          dosage: item.dosage,
          timing: timing,
        },
      }
    })
  } catch (error) {
    console.error('カレンダーデータの取得に失敗:', error)
  }
}

onMounted(async () => {
  await fetchPets()
  // fetchScheduleはfetchPets内で呼び出されるため、ここでは呼び出さない
})
</script>

<style scoped>
/* カレンダー凡例 */
.calendar-legend {
  background: var(--white);
  border: 1px solid var(--border-green);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-4);
  box-shadow: var(--shadow-sm);
}

.legend-title {
  color: var(--gray-800);
  margin: 0 0 var(--spacing-3) 0;
  font-size: var(--font-size-base);
  font-weight: 600;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: var(--radius);
  border: 1px solid var(--gray-200);
}

.legend-label {
  font-size: var(--font-size-sm);
  color: var(--gray-700);
  font-weight: 500;
}

/* FullCalendarのスタイル */
:deep(.fc-event) {
  border-radius: 6px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

:deep(.fc-event:hover) {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
  transition: all 0.2s ease;
}

:deep(.fc-toolbar-title) {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--gray-800);
}

:deep(.fc-button-primary) {
  background-color: var(--primary-green);
  border-color: var(--primary-green);
  color: white;
}

:deep(.fc-button-primary:hover) {
  background-color: var(--primary-green-dark);
  border-color: var(--primary-green-dark);
}

:deep(.fc-button-primary:focus) {
  box-shadow: 0 0 0 3px rgb(74 222 128 / 0.3);
}

:deep(.fc-today-button) {
  background-color: var(--accent-green);
  border-color: var(--accent-green);
  color: var(--gray-800);
}

:deep(.fc-today-button:hover) {
  background-color: var(--secondary-green);
  border-color: var(--secondary-green);
}

:deep(.fc-day-today) {
  background-color: rgba(74, 222, 128, 0.1) !important;
}

:deep(.fc-daygrid-day-number) {
  font-weight: 500;
  color: var(--gray-700);
}

:deep(.fc-daygrid-day.fc-day-today .fc-daygrid-day-number) {
  background-color: var(--primary-green);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 2px;
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .legend-items {
    gap: var(--spacing-2);
  }
  
  .legend-item {
    font-size: var(--font-size-xs);
  }
  
  .legend-color {
    width: 14px;
    height: 14px;
  }
}
</style>
