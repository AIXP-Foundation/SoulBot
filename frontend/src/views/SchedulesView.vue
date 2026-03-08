<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/composables/useApi'
import type { ScheduleEntry } from '@/types'

const schedules = ref<ScheduleEntry[]>([])
const loading = ref(true)
const errorMsg = ref('')

onMounted(async () => {
  await loadSchedules()
})

async function loadSchedules() {
  loading.value = true
  errorMsg.value = ''
  try {
    schedules.value = await api<ScheduleEntry[]>('/schedule/list')
  } catch (e: unknown) {
    if (e instanceof Error && e.message.includes('404')) {
      errorMsg.value = 'Schedule service not available (no schedule_service configured)'
    } else {
      errorMsg.value = e instanceof Error ? e.message : String(e)
    }
    schedules.value = []
  } finally {
    loading.value = false
  }
}

function statusBadge(status: string): string {
  switch (status) {
    case 'active': return 'badge--success'
    case 'completed': return ''
    case 'paused': return 'badge--warning'
    case 'error': return 'badge--error'
    default: return ''
  }
}

function formatDate(ts: string | null): string {
  if (!ts) return '—'
  return new Date(ts).toLocaleString()
}
</script>

<template>
  <div class="schedules-page">
    <div class="page-header">
      <h2>Schedules</h2>
      <span class="badge">{{ schedules.length }}</span>
      <button class="btn-refresh" @click="loadSchedules">Refresh</button>
    </div>

    <div v-if="loading" class="loading">Loading schedules...</div>
    <div v-else-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

    <div v-else-if="schedules.length === 0" class="empty">No scheduled tasks</div>

    <div v-else class="schedule-table-wrap">
      <table class="schedule-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Status</th>
            <th>Agent</th>
            <th>Created</th>
            <th>Last Run</th>
            <th>Runs</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in schedules" :key="s.id">
            <td class="cell-id">{{ s.id }}</td>
            <td>{{ s.trigger_config?.type || '—' }}</td>
            <td><span class="badge" :class="statusBadge(s.status)">{{ s.status }}</span></td>
            <td>{{ s.from_agent }} → {{ s.to_agent }}</td>
            <td>{{ formatDate(s.created_at) }}</td>
            <td>{{ formatDate(s.last_run) }}</td>
            <td>{{ s.run_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.schedules-page {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 18px;
  font-weight: 600;
}

.btn-refresh {
  margin-left: auto;
  background: var(--bg-card);
  color: var(--accent);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
}
.btn-refresh:hover { background: var(--border); }

.loading, .empty {
  color: var(--text-muted);
  padding: 40px;
  text-align: center;
}

.error-msg {
  color: var(--error);
  padding: 16px;
  background: #2a1a1a;
  border-radius: var(--radius);
  font-size: 13px;
}

.schedule-table-wrap {
  overflow-x: auto;
}

.schedule-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.schedule-table th,
.schedule-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.schedule-table th {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  background: var(--bg-card);
}

.schedule-table tr:hover td {
  background: var(--accent-bg);
}

.cell-id {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--accent);
}
</style>
