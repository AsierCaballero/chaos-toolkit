<template>
  <div class="app">
    <nav class="nav">
      <router-link to="/" class="logo">Chaos Dashboard</router-link>
      <div class="links">
        <router-link to="/">Dashboard</router-link>
        <router-link to="/experiments">Experiments</router-link>
      </div>
    </nav>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; }
.app { min-height: 100vh; }
.nav { display: flex; align-items: center; justify-content: space-between; padding: 1rem 2rem; background: #1e293b; border-bottom: 1px solid #334155; }
.logo { font-size: 1.25rem; font-weight: 700; color: #38bdf8; text-decoration: none; }
.links { display: flex; gap: 1.5rem; }
.links a { color: #94a3b8; text-decoration: none; font-size: 0.875rem; transition: color 0.2s; }
.links a:hover, .links a.router-link-active { color: #38bdf8; }
.main { padding: 2rem; max-width: 1200px; margin: 0 auto; }
</style>
