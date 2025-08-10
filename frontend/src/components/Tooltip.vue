<template>
  <div v-if="visible" :style="style" class="tooltip">
    <p><strong>薬名:</strong> {{ data.medicine_name }}</p>
    <p><strong>ペット:</strong> {{ data.pet_name }}</p>
    <p><strong>用量:</strong> {{ data.dosage }}</p>
    <p><strong>タイミング:</strong> {{ data.timing.join('・') }}</p>
  </div>
</template>

<script setup>
import { toRefs } from 'vue'

const props = defineProps({
  visible: Boolean,
  style: Object,
  data: {
    type: Object,
    default: () => ({
      medicine_name: '',
      pet_name: '',
      dosage: '',
      timing: [],
      notify: false,
    }),
  },
})
const { visible, style, data } = toRefs(props)
</script>

<style scoped>
.tooltip {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  padding: 8px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  pointer-events: none;
  z-index: 1000;
  white-space: nowrap;
}
</style>
