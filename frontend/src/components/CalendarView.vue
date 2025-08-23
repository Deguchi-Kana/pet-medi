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

// 色のキャッシュ（同じペットIDには常に同じ色を返す）
const colorCache = new Map()

// 美しい色のパレット（緑ベースと相性のいい色）
const beautifulColors = [
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
  '#0891b2',  // シアン
  '#7c2d12',  // 茶色
  '#dc2626',  // 赤
  '#16a34a',  // 緑
  '#15803d',  // 深緑
  '#9333ea',  // 紫
  '#be185d',  // ピンク
  '#ca8a04',  // 黄色
  '#0d9488',  // ティール
]

// ランダムな色を生成する関数
const generateRandomColor = () => {
  // 美しい色パレットからランダムに選択
  const randomIndex = Math.floor(Math.random() * beautifulColors.length)
  return beautifulColors[randomIndex]
}

// ペットIDごとの色を生成する関数
const generatePetColors = (pets) => {
  const petColors = {}
  
  // 各ペットにランダムな色を割り当て（既存の色がある場合は再利用）
  pets.forEach(pet => {
    if (colorCache.has(pet.id)) {
      // 既存の色を再利用
      petColors[pet.id] = colorCache.get(pet.id)
    } else {
      // 新しい色を生成してキャッシュに保存
      const newColor = generateRandomColor()
      colorCache.set(pet.id, newColor)
      petColors[pet.id] = newColor
    }
  })
  
  console.log('生成された色マッピング:', petColors) // デバッグ用
  console.log('色キャッシュ:', Object.fromEntries(colorCache)) // デバッグ用
  return petColors
}

// ペット情報を取得
const pets = ref([])
const petColors = ref({})

const fetchPets = async () => {
  try {
    console.log('ペット情報の取得を開始...') // デバッグ用
    const response = await fetch('http://localhost:8000/pets')
    console.log('ペットAPIレスポンス:', response) // デバッグ用
    
    if (response.ok) {
      const petsData = await response.json()
      console.log('取得したペット情報（生データ）:', petsData) // デバッグ用
      
      // 各ペットのIDを確認
      petsData.forEach(pet => {
        console.log(`ペット: ${pet.name}, ID: ${pet.id}`) // デバッグ用
      })
      
      pets.value = petsData
      console.log('取得したペット情報:', pets.value) // デバッグ用
      console.log('ペット数:', pets.value.length) // デバッグ用
      
      // ペット数に応じて色を生成
      petColors.value = generatePetColors(pets.value)
      console.log('ペット情報取得完了:', pets.value) // デバッグ用
      console.log('色マッピング生成完了:', petColors.value) // デバッグ用
      
      // ペット情報取得完了後にスケジュールを取得
      await fetchSchedule()
    } else {
      console.error('ペットAPIエラー:', response.status, response.statusText) // デバッグ用
    }
  } catch (error) {
    console.error('ペット情報の取得に失敗しました:', error)
  }
}

// ペットIDに応じた色を取得
const getPetColor = (petId) => {
  console.log(`getPetColor呼び出し: petId=${petId}, petColors=`, petColors.value) // デバッグ用
  
  if (!petId) {
    console.log('petIdが未定義、デフォルト色を返す') // デバッグ用
    return '#6b7280' // デフォルトはグレー
  }
  
  const color = petColors.value[petId]
  console.log(`petId ${petId} の色: ${color}`) // デバッグ用
  
  if (!color) {
    console.log(`petId ${petId} の色が見つからない、デフォルト色を返す`) // デバッグ用
    return '#6b7280'
  }
  
  return color
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
      console.log(`処理中のアイテム:`, item) // デバッグ用
      console.log(`item.pet_id: ${item.pet_id}, 型: ${typeof item.pet_id}`) // デバッグ用
      
      // pet_idを数値に変換
      let petId = item.pet_id
      if (typeof petId === 'string') {
        petId = parseInt(petId, 10)
        console.log(`pet_idを数値に変換: ${item.pet_id} → ${petId}`) // デバッグ用
      }
      
      const petColor = getPetColor(petId)
      console.log(`イベント: ${item.medicine_name}, ペットID: ${petId}, 色: ${petColor}`) // デバッグ用
      
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
          pet_id: petId,
          dosage: item.dosage,
          timing: timing,
        },
      }
    })
    
    console.log('生成されたカレンダーイベント:', calendarOptions.value.events) // デバッグ用
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
