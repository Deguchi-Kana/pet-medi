<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-content">
      <h3>お薬情報の編集</h3>
      <input v-model="form.name" placeholder="薬名" class="input" />
      <select v-model="form.dosage" class="input">
        <option>1錠</option>
        <option>1/2錠</option>
        <option>1/3錠</option>
        <option>1/4錠</option>
        <option>1包</option>
      </select>
      <div class="checkbox-group">
        <label><input type="checkbox" v-model="form.timing" value="朝" /> 朝</label>
        <label><input type="checkbox" v-model="form.timing" value="昼" /> 昼</label>
        <label><input type="checkbox" v-model="form.timing" value="夜" /> 夜</label>
      </div>
      <label><input type="checkbox" v-model="form.notify" /> 通知ON</label>
      <div>
        <label for="start-date">開始日</label>
        <input type="date" id="start-date" v-model="form.start_date" />
      </div>
      <div>
        <input type="number" id="duration" placeholder="日数" v-model="form.duration_days" />日分
      </div>
      <div class="buttons">
        <button @click="submit" class="save">保存</button>
        <button @click="$emit('close')" class="cancel">キャンセル</button>
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
  duration_days: ''
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
