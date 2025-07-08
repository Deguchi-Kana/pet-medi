<template>
  <div class="medicine-form">
    <h2 class="text-xl font-bold mb-4">お薬の登録</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="name" class="block text-sm font-medium">薬名</label>
        <input id="name" v-model="form.name" type="text" class="border rounded w-full p-2" />
      </div>

      <div>
        <label for="amount" class="block text-sm font-medium">分量</label>
        <select id="amount" v-model="form.amount" class="border rounded w-full p-2">
          <option value="1錠">1錠</option>
          <option value="0.5錠">1/2錠</option>
          <option value="1包">1包</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium">投薬時間</label>
        <label><input type="checkbox" value="朝" v-model="form.times" /> 朝</label>
        <label><input type="checkbox" value="昼" v-model="form.times" /> 昼</label>
        <label><input type="checkbox" value="夜" v-model="form.times" /> 夜</label>
      </div>

      <div>
        <label>
          <input type="checkbox" v-model="form.notify" />
          通知をONにする
        </label>
      </div>

      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        登録
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  amount: '1錠',
  times: [],
  notify: false
})

function handleSubmit() {
  console.log('登録内容:', form)
  alert('仮登録完了！開発中✨')
}
</script>
