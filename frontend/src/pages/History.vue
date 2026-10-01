<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const err = ref('')

onMounted(async () => {
  try {
    items.value = (await getJSON('/api/runs')).items
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档</h1>
    <p class="hint" data-list-pin="tape">列表与详情同钉写入值：胶带米数与面积按落库时展示。</p>
    <p class="hint">改默认余量或胶带开关后，旧编号仍按写入时的 tape_on / tape_m 展示，不重算。</p>
    <p class="lede">算纸页「写入用纸档」后的落库结果，按次保留盒名、用纸面积与胶带米数；点行查看详情。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <p v-else-if="!items.length" class="empty">还没有写入过。先去算纸试一单。</p>
    <ul v-else class="item-list">
      <li v-for="r in items" :key="r.id">
        <router-link class="run-link" :to="`/history/${r.id}`">
          <span>{{ r.box_name }}</span>
          <span class="meta">用纸 {{ r.result?.paper_m2 ?? '—' }} m²</span>
          <span class="meta">胶带 {{ r.result?.tape_on ? r.result.tape_m + ' m' : '—' }}</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>
