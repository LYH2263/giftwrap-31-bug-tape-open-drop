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
    <p class="hint" data-list-pin="tape">列表优先钉写入摘要；详情走开放投影。</p>
    <p class="hint">列表钉写入摘要（tape_on / tape_m）；详情走开放视图字段。</p>
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
