<template>
  <div class="detail" v-if="experiment">
    <router-link to="/experiments" class="back">&larr; Back</router-link>
    <h1>{{ experiment.name }}</h1>
    <div class="grid">
      <div class="info-card">
        <h3>Details</h3>
        <dl>
          <dt>Kind</dt><dd>{{ experiment.kind }}</dd>
          <dt>Status</dt><dd><span :class="`badge ${experiment.status.toLowerCase()}`">{{ experiment.status }}</span></dd>
          <dt>Verdict</dt><dd><span :class="`badge ${(experiment.verdict || '').toLowerCase()}`">{{ experiment.verdict || 'N/A' }}</span></dd>
          <dt>Started</dt><dd>{{ experiment.started || 'N/A' }}</dd>
          <dt>Duration</dt><dd>{{ experiment.duration || 'N/A' }}</dd>
        </dl>
      </div>
    </div>
  </div>
  <div v-else class="loading"><p>Loading...</p></div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useChaosStore } from "../api/store";

const route = useRoute();
const store = useChaosStore();
const experiment = ref(null);

onMounted(async () => {
  await store.fetchExperiments();
  experiment.value = store.experiments.find((e) => e.name === route.params.name) || null;
});
</script>

<style scoped>
.back { color: #38bdf8; text-decoration: none; display: inline-block; margin-bottom: 1rem; }
.back:hover { text-decoration: underline; }
h1 { margin-bottom: 1.5rem; color: #f8fafc; }
.grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
.info-card { background: #1e293b; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #334155; }
.info-card h3 { color: #e2e8f0; margin-bottom: 1rem; }
dl dt { color: #64748b; font-size: 0.75rem; text-transform: uppercase; margin-top: 0.75rem; }
dl dd { color: #cbd5e1; }
.badge { padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 600; }
.badge.completed { background: #22c55e20; color: #22c55e; }
.badge.running { background: #f59e0b20; color: #f59e0b; }
.badge.fail { background: #ef444420; color: #ef4444; }
.badge.pass { background: #22c55e20; color: #22c55e; }
.loading { text-align: center; padding: 4rem; color: #64748b; }
</style>
