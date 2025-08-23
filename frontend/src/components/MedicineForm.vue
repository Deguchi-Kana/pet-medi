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
.medicine-form-container {
  width: 100%;
}

.medicine-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  font-weight: 600;
  color: var(--gray-700);
  font-size: var(--font-size-base);
}

.label-icon {
  font-size: var(--font-size-lg);
}

.form-input,
.form-select,
.form-textarea {
  padding: var(--spacing-3);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius);
  font-size: var(--font-size-base);
  transition: var(--transition);
  background: var(--white);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-green);
  box-shadow: 0 0 0 3px rgb(74 222 128 / 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-help {
  color: var(--gray-500);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-1);
}

/* タイミングチェックボックス */
.timing-checkboxes {
  display: flex;
  gap: var(--spacing-4);
  flex-wrap: wrap;
}

.timing-checkbox {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  cursor: pointer;
  position: relative;
}

.timing-checkbox input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius);
  background: var(--white);
  transition: var(--transition);
  position: relative;
}

.timing-checkbox input[type="checkbox"]:checked + .checkmark {
  background: var(--primary-green);
  border-color: var(--primary-green);
}

.timing-checkbox input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--white);
  font-size: var(--font-size-sm);
  font-weight: bold;
}

.timing-text {
  font-weight: 500;
  color: var(--gray-700);
}

/* 期間入力 */
.duration-input {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.duration-unit {
  color: var(--gray-600);
  font-weight: 500;
  white-space: nowrap;
}

/* 通知トグル */
.notify-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--gray-300);
  transition: var(--transition);
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: var(--white);
  transition: var(--transition);
  border-radius: 50%;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: var(--primary-green);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.notify-text {
  font-weight: 500;
  color: var(--gray-700);
}

.form-actions {
  display: flex;
  gap: var(--spacing-4);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-6);
  border-top: 1px solid var(--gray-200);
}

.submit-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-4);
  font-size: var(--font-size-base);
  font-weight: 600;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-icon,
.reset-icon {
  font-size: var(--font-size-lg);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 成功メッセージ */
.success-message {
  background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
  color: var(--white);
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  text-align: center;
  margin-top: var(--spacing-6);
  animation: slideIn 0.3s ease-out;
}

.success-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-3);
}

.success-title {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-2);
  font-weight: 600;
}

.success-text {
  font-size: var(--font-size-base);
  opacity: 0.9;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .timing-checkboxes {
    flex-direction: column;
    gap: var(--spacing-3);
  }

  .form-actions {
    flex-direction: column;
    gap: var(--spacing-3);
  }

  .submit-btn {
    order: 1;
  }

  .duration-input {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-2);
  }

  .duration-unit {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .medicine-form {
    gap: var(--spacing-4);
  }

  .form-actions {
    margin-top: var(--spacing-4);
    padding-top: var(--spacing-4);
  }
}
</style>