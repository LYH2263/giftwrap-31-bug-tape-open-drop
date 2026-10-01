<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const boxes = ref([])
const bid = ref(1)
const out = ref(null)
const err = ref('')
const busy = ref(false)
const tapeOn = ref(false)
const allowanceInput = ref('')
const defaultAllowance = ref(null)

onMounted(async () => {
  try {
    boxes.value = (await getJSON('/api/boxes')).items.filter((b) => b.data_quality === 'clean')
    if (boxes.value.length) bid.value = boxes.value[0].id
    defaultAllowance.value = Number((await getJSON('/api/settings')).tape_allowance_m)
  } catch (e) {
    err.value = String(e.message || e)
  }
})

function tapeParams() {
  const p = { tape: tapeOn.value }
  if (tapeOn.value && allowanceInput.value !== '') {
    const v = Number(allowanceInput.value)
    if (!Number.isFinite(v) || v < 0) {
      err.value = '胶带余量须为不小于 0 的数字（米）'
      return null
    }
    p.tape_allowance_m = v
  }
  return p
}

async function go(save) {
  err.value = ''
  const tp = tapeParams()
  if (!tp) return
  busy.value = true
  try {
    out.value = save
      ? await postJSON('/api/estimate', { box_id: bid.value, save: true, ...tp })
      : await getJSON(`/api/estimate?box_id=${bid.value}&tape=${tp.tape}`
        + (tp.tape_allowance_m !== undefined ? `&tape_allowance_m=${tp.tape_allowance_m}` : ''))
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先试算看面积与展开，确认后再写入用纸档。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <label class="tape-toggle">
        <input type="checkbox" v-model="tapeOn">
        封口胶带
      </label>
      <input
        class="allowance"
        type="number"
        step="0.05"
        min="0"
        :disabled="!tapeOn"
        v-model="allowanceInput"
        :placeholder="`余量，默认 ${defaultAllowance ?? 0.2} m`"
      >
      <button :disabled="busy" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy" @click="go(true)">写入用纸档</button>
    </div>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="figure">{{ out.paper_m2 }}<span>m²</span></div>
      <p class="stat-line" v-if="out.tape_on">
        封口胶带约 {{ out.tape_m }} m（含余量 {{ out.tape_allowance_m }} m）
      </p>
      <p class="stat-line stat-muted" v-else>未计胶带</p>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m
      </p>
      <BoxUnfold
        :l="out.box.length"
        :w="out.box.width"
        :h="out.box.height"
        :paper-m2="out.paper_m2"
      />
    </div>
  </div>
</template>
