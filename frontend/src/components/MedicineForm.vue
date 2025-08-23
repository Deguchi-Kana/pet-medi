<template>
  <div class="medicine-form-container">
    <form @submit.prevent="submitForm" class="medicine-form">
      <div class="form-group">
        <label for="medicine-name" class="form-label">
          <span class="label-icon">💊</span>
          薬の名前
        </label>
        <input 
          id="medicine-name"
          v-model="form.name" 
          type="text"
          placeholder="例: フィラリア薬、アモキシシリン" 
          class="form-input"
          required
        />
      </div>

      <div class="form-group">
        <label for="medicine-dosage" class="form-label">
          <span class="label-icon">📏</span>
          投薬量
        </label>
        <select id="medicine-dosage" v-model="form.dosage" class="form-select" required>
          <option value="">投薬量を選択してください</option>
          <option value="1錠">1錠</option>
          <option value="1/2錠">1/2錠</option>
          <option value="1/3錠">1/3錠</option>
          <option value="1/4錠">1/4錠</option>
          <option value="1包">1包</option>
          <option value="2錠">2錠</option>
          <option value="3錠">3錠</option>
          <option value="5ml">5ml</option>
          <option value="10ml">10ml</option>
          <option value="その他">その他</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">⏰</span>
          投薬タイミング
        </label>
        <div class="timing-checkboxes">
          <label class="timing-checkbox">
            <input type="checkbox" v-model="form.timing" value="朝" />
            <span class="checkmark"></span>
            <span class="timing-text">朝</span>
          </label>
          <label class="timing-checkbox">
            <input type="checkbox" v-model="form.timing" value="昼" />
            <span class="checkmark"></span>
            <span class="timing-text">昼</span>
          </label>
          <label class="timing-checkbox">
            <input type="checkbox" v-model="form.timing" value="夜" />
            <span class="checkmark"></span>
            <span class="timing-text">夜</span>
          </label>
        </div>
        <small class="form-help">複数選択可能です</small>
      </div>

      <div class="form-group">
        <label for="medicine-pet" class="form-label">
          <span class="label-icon">🐕</span>
          対象ペット
        </label>
        <select id="medicine-pet" v-model="form.pet_id" class="form-select" required>
          <option value="">ペットを選択してください</option>
          <option v-for="pet in pets" :key="pet.id" :value="pet.id">
            {{ pet.name }} ({{ getPetSpeciesName(pet.species) }})
          </option>
        </select>
        <small class="form-help">先にペットを登録してください</small>
      </div>

      <div class="form-group">
        <label for="medicine-start-date" class="form-label">
          <span class="label-icon">📅</span>
          開始日
        </label>
        <input 
          id="medicine-start-date"
          type="date" 
          v-model="form.start_date" 
          class="form-input"
          required
        />
      </div>

      <div class="form-group">
        <label for="medicine-duration" class="form-label">
          <span class="label-icon">⏳</span>
          投薬期間
        </label>
        <div class="duration-input">
          <input 
            id="medicine-duration"
            type="number" 
            v-model="form.duration_days" 
            placeholder="例: 7" 
            class="form-input"
            min="1"
            required
          />
          <span class="duration-unit">日分</span>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">🔔</span>
          通知設定
        </label>
        <div class="notify-toggle">
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.notify" />
            <span class="toggle-slider"></span>
          </label>
          <span class="notify-text">{{ form.notify ? '通知ON' : '通知OFF' }}</span>
        </div>
        <small class="form-help">投薬時間になったら通知を受け取ります</small>
      </div>

      <div class="form-group">
        <label for="medicine-notes" class="form-label">
          <span class="label-icon">📝</span>
          メモ
        </label>
        <textarea 
          id="medicine-notes"
          v-model="form.notes" 
          placeholder="特記事項があれば入力してください" 
          class="form-textarea"
          rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary submit-btn" :disabled="isSubmitting || !canSubmit">
          <span v-if="isSubmitting" class="loading-spinner"></span>
          <span v-else class="submit-icon">✅</span>
          {{ isSubmitting ? '登録中...' : '薬を登録' }}
        </button>
        <button type="button" @click="resetForm" class="btn btn-secondary">
          <span class="reset-icon">🔄</span>
          リセット
        </button>
      </div>
    </form>

    <!-- 成功メッセージ -->
    <div v-if="showSuccess" class="success-message">
      <div class="success-icon">🎉</div>
      <h4 class="success-title">登録完了！</h4>
      <p class="success-text">{{ form.name }}の登録が完了しました</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const form = ref({
  name: '',
  dosage: '',
  pet_id: '',
  timing: [],
  notify: false,
  start_date: '',
  duration_days: '',
  notes: ''
})

const pets = ref([])
const isSubmitting = ref(false)
const showSuccess = ref(false)

// ペット情報の取得
const fetchPets = async () => {
  try {
    const response = await fetch('http://localhost:8000/pets')
    if (response.ok) {
      pets.value = await response.json()
    }
  } catch (error) {
    console.error('ペット情報の取得に失敗しました:', error)
  }
}

onMounted(fetchPets)

// ペットの種類名を取得
const getPetSpeciesName = (species) => {
  const speciesMap = {
    'dog': '犬',
    'cat': '猫',
    'bird': '鳥',
    'rabbit': 'うさぎ',
    'hamster': 'ハムスター',
    'fish': '魚',
    'turtle': 'カメ',
    'snake': 'ヘビ',
    'other': 'その他'
  }
  return speciesMap[species] || species
}

// フォームの送信可否をチェック
const canSubmit = computed(() => {
  return form.value.name && 
         form.value.dosage && 
         form.value.pet_id && 
         form.value.timing.length > 0 && 
         form.value.start_date && 
         form.value.duration_days
})

// 薬の登録
const submitForm = async () => {
  if (isSubmitting.value || !canSubmit.value) return
  
  isSubmitting.value = true
  
  try {
    const response = await fetch('http://localhost:8000/medicines', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) throw new Error('登録に失敗しました')

    const data = await response.json()
    console.log('登録成功:', data)
    
    // 成功メッセージを表示
    showSuccess.value = true
    
    // フォームをリセット
    resetForm()
    
    // 3秒後に成功メッセージを非表示
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
    
  } catch (error) {
    console.error(error)
    alert('登録に失敗しました')
  } finally {
    isSubmitting.value = false
  }
}

// フォームをリセット
const resetForm = () => {
  form.value = {
    name: '',
    dosage: '',
    pet_id: '',
    timing: [],
    notify: false,
    start_date: '',
    duration_days: '',
    notes: ''
  }
}
</script>

<style scoped>
@import '../styles/MedicineForm.scss';
</style>