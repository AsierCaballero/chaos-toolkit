<template>
  <div class="experiments">
    <h1>Experiments</h1>
    <div class="toolbar">
      <input v-model="search" placeholder="Search experiments..." class="search" />
      <select v-model="filter" class="filter">
        <option value="">All</option>
        <option value="Pass">Passed</option>
        <option value="Fail">Failed</option>
        <option value="Running">Running</option>
      </select>
    </div>
    <table>
      <thead>
        <tr>
          <th @click="sort('name')">Name</th>
          <th @click="sort('kind')">Kind</th>
          <th @click="sort('status')">Status</th>
          <th @click="sort('verdict')">Verdict</th>
          <th @click="sort('age')">Age</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="exp in filtered" :key="exp.name">
          <td><router-link :to="`/experiments/${exp.name}`">{{ exp.name }}</router-link></td>
          <td>{{ exp.kind }}</td>
          <td><span :class="`badge ${exp.status.toLowerCase()}`">{{ exp.status }}</span></td>
          <td><span :class="`badge ${(exp.verdict || '').toLowerCase()}`">{{ exp.verdict || 'N/A' }}</span></td>
          <td>{{ exp.age }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useChaosStore } from "../api/store";

const store = useChaosStore();
const search = ref("");
const filter = ref("");
const sortKey = ref("name");
const sortDir = ref(1);

const filtered = computed(() => {
  let list = [...store.experiments];
  if (search.value) {
    const q = search.value.toLowerCase();
    list = list.filter((e) => e.name.toLowerCase().includes(q));
  }
  if (filter.value) {
    list = list.filter((e) => (e.verdict || e.status) === filter.value);
  }
  list.sort((a, b) => {
    const av = (a[sortKey.value] || "").toString().toLowerCase();
    const bv = (b[sortKey.value] || "").toString().toLowerCase();
    return av.localeCompare(bv) * sortDir.value;
  });
  return list;
});

function sort(key) {
  if (sortKey.value === key) sortDir.value *= -1;
  else { sortKey.value = key; sortDir.value = 1; }
}

onMounted(() => store.fetchExperiments());
</script>

<style scoped>
h1 { margin-bottom: 1.5rem; color: #f8fafc; }
.toolbar { display: flex; gap: 1rem; margin-bottom: 1rem; }
.search, .filter { padding: 0.5rem 1rem; border-radius: 0.375rem; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; }
.search { flex: 1; }
table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 0.5rem; overflow: hidden; }
th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #334155; color: #cbd5e1; }
th { background: #1e293b; color: #64748b; font-size: 0.75rem; text-transform: uppercase; cursor: pointer; user-select: none; }
th:hover { color: #94a3b8; }
td a { color: #38bdf8; text-decoration: none; }
.badge { padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 600; }
.badge.completed { background: #22c55e20; color: #22c55e; }
.badge.running { background: #f59e0b20; color: #f59e0b; }
.badge.fail { background: #ef444420; color: #ef4444; }
.badge.pass { background: #22c55e20; color: #22c55e; }
</style>
