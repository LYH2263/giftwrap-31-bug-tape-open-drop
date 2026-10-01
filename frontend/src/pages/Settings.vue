<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const s = ref({})
const allowance = ref('')
const err = ref('')
const saved = ref(false)
const busy = ref(false)

async function load() {
  s.value = await getJSON('/api/settings')
  allowance.value = s.value.tape_allowance_m ?? ''
}

onMounted(load)

async function saveAllowance() {
  err.value = ''
  saved.value = false
  const v = Number(allowance.value)
  if (!Number.isFinite(v) || v < 0) {
    err.value = '默认胶带余量须为不小于 0 的数字（米）'
    return
  }
  busy.value = true
  try {
    s.value = await putJSON('/api/settings', { tape_allowance_m: v })
    allowance.value = s.value.tape_allowance_m
    saved.value = true
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>设置</h1>
    <p class="lede">折边系数只读展示；封口胶带的默认余量（米）可在此调整，仅影响之后的试算与写入，不改历史用纸档。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <p v-if="saved" class="pill">已保存</p>
    <ul class="item-list">
      <li>
        <span>折边系数 overlap</span>
        <span class="meta">{{ s.overlap }}</span>
      </li>
      <li>
        <span>胶带默认余量 tape_allowance_m（m）</span>
        <span class="meta settings-edit">
          <input class="allowance" type="number" step="0.05" min="0" v-model="allowance">
          <button :disabled="busy" @click="saveAllowance">保存</button>
        </span>
      </li>
    </ul>
  </div>
</template>
