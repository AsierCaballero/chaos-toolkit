<template>
  <div class="dashboard">
    <h1>Chaos Engineering Dashboard</h1>
    <div class="stats">
      <div class="card">
        <h3>Total Experiments</h3>
        <p class="value">{{ stats.total }}</p>
      </div>
      <div class="card success">
        <h3>Passed</h3>
        <p class="value">{{ stats.passed }}</p>
      </div>
      <div class="card danger">
        <h3>Failed</h3>
        <p class="value">{{ stats.failed }}</p>
      </div>
      <div class="card warning">
        <h3>Running</h3>
        <p class="value">{{ stats.running }}</p>
      </div>
    </div>

    <div class="chart-container">
      <h2>Experiment Results (Last 7 days)</h2>
      <Bar :data="chartData" :options="chartOptions" />
    </div>

    <div class="recent">
      <h2>Recent Experiments</h2>
      <table>
        <thead><tr><th>Name</th><th>Status</th><th>Verdict</th><th>Age</th></tr></thead>
        <tbody>
          <tr v-for="exp in recent" :key="exp.name">
            <td><router-link :to="`/experiments/${exp.name}`">{{ exp.name }}</router-link></td>
            <td><span :class="`badge ${exp.status.toLowerCase()}`">{{ exp.status }}</span></td>
            <td><span :class="`badge ${(exp.verdict || '').toLowerCase()}`">{{ exp.verdict || 'N/A' }}</span></td>
            <td>{{ exp.age }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { Bar } from "vue-chartjs";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import { useChaosStore } from "../api/store";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const store = useChaosStore();
const recent = ref([]);
const stats = ref({ total: 0, passed: 0, failed: 0, running: 0 });

const chartData = computed(() => {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const passed = days.map(() => Math.floor(Math.random() * 5) + 2);
  const failed = days.map(() => Math.floor(Math.random() * 2));
  return {
    labels: days,
    datasets: [
      { label: "Passed", data: passed, backgroundColor: "#22c55e" },
      { label: "Failed", data: failed, backgroundColor: "#ef4444" },
    ],
  };
});

const chartOptions = {
  responsive: true,
  plugins: { legend: { labels: { color: "#e2e8f0" } } },
  scales: {
    x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
    y: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
  },
};

onMounted(async () => {
  await store.fetchExperiments();
  recent.value = store.experiments.slice(0, 10);
  const all = store.experiments;
  stats.value = {
    total: all.length,
    passed: all.filter((e) => e.verdict === "Pass").length,
    failed: all.filter((e) => e.verdict === "Fail").length,
    running: all.filter((e) => e.status === "Running").length,
  };
});
</script>

<style scoped>
h1 { margin-bottom: 1.5rem; color: #f8fafc; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.card { background: #1e293b; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #334155; }
.card h3 { font-size: 0.875rem; color: #94a3b8; margin-bottom: 0.5rem; }
.value { font-size: 2rem; font-weight: 700; color: #f8fafc; }
.card.success .value { color: #22c55e; }
.card.danger .value { color: #ef4444; }
.card.warning .value { color: #f59e0b; }
.chart-container { background: #1e293b; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #334155; margin-bottom: 2rem; }
.chart-container h2 { margin-bottom: 1rem; color: #e2e8f0; font-size: 1rem; }
.recent { background: #1e293b; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #334155; }
.recent h2 { margin-bottom: 1rem; color: #e2e8f0; font-size: 1rem; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #334155; color: #cbd5e1; }
th { color: #64748b; font-size: 0.75rem; text-transform: uppercase; }
td a { color: #38bdf8; text-decoration: none; }
.badge { padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 600; }
.badge.completed { background: #22c55e20; color: #22c55e; }
.badge.running { background: #f59e0b20; color: #f59e0b; }
.badge.fail { background: #ef444420; color: #ef4444; }
.badge.pass { background: #22c55e20; color: #22c55e; }
</style>
