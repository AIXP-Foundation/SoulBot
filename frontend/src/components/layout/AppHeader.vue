<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

const { theme, toggle } = useTheme()
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <button class="theme-toggle" @click="toggle" :title="theme === 'dark' ? 'Switch to light' : 'Switch to dark'">
        {{ theme === 'dark' ? '☀️' : '🌙' }}
      </button>
      <a href="https://www.soulbot.dev" target="_blank" class="logo-link"><h1 class="logo">SoulBot.dev</h1></a>
      <span class="version">WebUI</span>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 16px;
  height: var(--header-height);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo {
  font-size: 16px;
  font-weight: 700;
  color: var(--accent);
}

.version {
  font-size: 11px;
  color: var(--text-muted);
  padding: 1px 6px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
}

.theme-toggle {
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 4px 8px;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
}
.logo-link {
  text-decoration: none;
  color: inherit;
}

.theme-toggle:hover {
  background: var(--bg-card);
}
</style>
