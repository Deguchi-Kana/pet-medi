<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-content">
      <h3>お薬情報の編集</h3>
      <input v-model="form.name" placeholder="名前" class="input" />
      <input v-model="form.species" placeholder="種類" class="input" />
      <div>
        <label for="birthdate">誕生日</label>
        <input type="date" id="birthdate" v-model="form.birthdate" />
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
  pet: Object
})
const emit = defineEmits(['update', 'close'])

const form = reactive({
  id: null,
  name: '',
  species: '',
  birthdate: ''
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
