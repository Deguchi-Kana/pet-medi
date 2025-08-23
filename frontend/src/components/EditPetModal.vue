<template>
  <div class="modal-overlay" v-if="visible" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          <span class="modal-icon">✏️</span>
          ペット情報の編集
        </h3>
        <button @click="$emit('close')" class="close-btn" title="閉じる">✕</button>
      </div>

      <div class="modal-body">
        <form @submit.prevent="submit" class="edit-form">
          <div class="form-group">
            <label for="edit-pet-name" class="form-label">
              <span class="label-icon">🐕</span>
              ペットの名前
            </label>
            <input 
              id="edit-pet-name"
              v-model="form.name" 
              type="text"
              placeholder="例: ポチ、タマ" 
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-pet-species" class="form-label">
              <span class="label-icon">🐾</span>
              種類
            </label>
            <select id="edit-pet-species" v-model="form.species" class="form-select" required>
              <option value="">種類を選択してください</option>
              <option value="dog">犬</option>
              <option value="cat">猫</option>
              <option value="bird">鳥</option>
              <option value="rabbit">うさぎ</option>
              <option value="hamster">ハムスター</option>
              <option value="fish">魚</option>
              <option value="turtle">カメ</option>
              <option value="snake">ヘビ</option>
              <option value="other">その他</option>
            </select>
          </div>

          <div class="form-group">
            <label for="edit-pet-birthdate" class="form-label">
              <span class="label-icon">🎂</span>
              誕生日
            </label>
            <input 
              id="edit-pet-birthdate"
              type="date" 
              v-model="form.birthdate" 
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="edit-pet-weight" class="form-label">
              <span class="label-icon">⚖️</span>
              体重 (kg)
            </label>
            <input 
              id="edit-pet-weight"
              v-model="form.weight" 
              type="number"
              step="0.1"
              min="0"
              placeholder="例: 5.2" 
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="edit-pet-notes" class="form-label">
              <span class="label-icon">📝</span>
              メモ
            </label>
            <textarea 
              id="edit-pet-notes"
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
  pet: Object
})
const emit = defineEmits(['update', 'close'])

const form = reactive({
  id: null,
  name: '',
  species: '',
  birthdate: '',
  weight: '',
  notes: ''
})

watch(
    () => props.pet,
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
@import '../styles/EditPetModal.scss';
</style>
