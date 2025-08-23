<template>
  <div class="modal-overlay" v-if="visible" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          <span class="modal-icon">💊</span>
          薬情報の編集
        </h3>
        <button @click="$emit('close')" class="close-btn" title="閉じる">✕</button>
      </div>

      <div class="modal-body">
        <form @submit.prevent="submit" class="edit-form">
          <div class="form-group">
            <label for="edit-medicine-name" class="form-label">
              <span class="label-icon">💊</span>
              薬の名前
            </label>
            <input 
              id="edit-medicine-name"
              v-model="form.name" 
              type="text"
              placeholder="例: フィラリア薬、アモキシシリン" 
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-medicine-dosage" class="form-label">
              <span class="label-icon">📏</span>
              投薬量
            </label>
            <select id="edit-medicine-dosage" v-model="form.dosage" class="form-select" required>
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
            <label for="edit-medicine-start-date" class="form-label">
              <span class="label-icon">📅</span>
              開始日
            </label>
            <input 
              id="edit-medicine-start-date"
              type="date" 
              v-model="form.start_date" 
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-medicine-duration" class="form-label">
              <span class="label-icon">⏳</span>
              投薬期間
            </label>
            <div class="duration-input">
              <input 
                id="edit-medicine-duration"
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
            <label for="edit-medicine-notes" class="form-label">
              <span class="label-icon">📝</span>
              メモ
            </label>
            <textarea 
              id="edit-medicine-notes"
              v-model="form.notes" 
              placeholder="特記事項があれば入力してください" 
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary save-btn">
              <span class="save-icon">💾</span>
              保存
            </button>
            <button type="button" @click="$emit('close')" class="btn btn-secondary cancel-btn">
              <span class="cancel-icon">❌</span>
              キャンセル
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  medicine: Object
})
const emit = defineEmits(['update', 'close'])

const form = reactive({
  id: null,
  name: '',
  dosage: '',
  timing: [],
  notify: false,
  pet_id: 1,
  start_date: '',
  duration_days: '',
  notes: ''
})

watch(
    () => props.medicine,
    (val) => {
      if (val) Object.assign(form, val)
    },
    { immediate: true }
)

const submit = () => {
  emit('update', { ...form })
}
</script>

<style scoped>
@import '../styles/EditMedicineModal.scss';
</style>
