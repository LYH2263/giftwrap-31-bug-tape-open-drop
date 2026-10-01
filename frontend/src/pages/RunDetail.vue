<script setup>
// 详情与列表同钉：直接展示写入时落库的 tape_on / tape_m / 余量，不按当前默认重算。

import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档详情</h1>
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <p class="lede">
        {{ run.box_name ?? '（盒型已删除）' }} · 落库于 {{ new Date(run.created_at).toLocaleString() }}
      </p>
      <ul class="item-list">
        <li>
          <span>用纸面积 paper_m2</span>
          <span class="meta">{{ run.result?.paper_m2 ?? '—' }} m²</span>
        </li>
        <li>
          <span>封口胶带 tape_m</span>
          <span class="meta">
            {{ run.result?.tape_on ? `${run.result.tape_m} m（含余量 ${run.result.tape_allowance_m} m）` : '未计胶带' }}
          </span>
        </li>
        <li>
          <span>十字丝带 ribbon_m</span>
          <span class="meta">{{ run.result?.ribbon?.ribbon_m ?? '—' }} m</span>
        </li>
        <li>
          <span>折边系数 overlap</span>
          <span class="meta">{{ run.overlap }}</span>
        </li>
        <li v-if="run.note">
          <span>备注</span>
          <span class="meta">{{ run.note }}</span>
        </li>
      </ul>
      <p class="stat-line"><router-link to="/history">← 返回用纸档</router-link></p>
    </template>
  </div>
</template>
