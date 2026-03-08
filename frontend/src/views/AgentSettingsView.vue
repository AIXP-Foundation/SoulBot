<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAgentStore } from '@/stores/agent'
import type { AisopInfo } from '@/types'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const props = defineProps<{ name: string }>()
const router = useRouter()
const agentStore = useAgentStore()

const aisops = ref<AisopInfo[]>([])
const libraryAisops = ref<AisopInfo[]>([])
const loading = ref(true)
const expandedGroups = ref<Set<string>>(new Set())
const expandedLibGroups = ref<Set<string>>(new Set())
const deleteTarget = ref<AisopInfo | null>(null)
const deleteGroupTarget = ref<string | null>(null)

onMounted(async () => {
  try {
    const [agentData, libData] = await Promise.all([
      agentStore.loadAisops(props.name).catch(() => [] as AisopInfo[]),
      agentStore.loadAisopLibrary().catch(() => [] as AisopInfo[]),
    ])
    aisops.value = agentData
    libraryAisops.value = libData
  } catch {
    aisops.value = []
    libraryAisops.value = []
  }
  loading.value = false
})

// Split into ungrouped (flat) and grouped
const ungrouped = computed(() => aisops.value.filter(a => !a.group))
const groups = computed(() => {
  const map = new Map<string, AisopInfo[]>()
  for (const a of aisops.value) {
    if (a.group) {
      if (!map.has(a.group)) map.set(a.group, [])
      map.get(a.group)!.push(a)
    }
  }
  // Sort each group: main.aisop.json first, rest alphabetical
  for (const [, items] of map) {
    items.sort((a, b) => {
      const aMain = a.path.endsWith('/main.aisop.json') ? 0 : 1
      const bMain = b.path.endsWith('/main.aisop.json') ? 0 : 1
      return aMain - bMain || a.path.localeCompare(b.path)
    })
  }
  return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]))
})

// Library: filter out groups already present in agent, then group
const libraryGroups = computed(() => {
  const agentGroupNames = new Set(aisops.value.filter(a => a.group).map(a => a.group!))
  const agentNames = new Set(aisops.value.map(a => a.name))
  const filtered = libraryAisops.value.filter(a => {
    if (a.group && agentGroupNames.has(a.group)) return false
    if (agentNames.has(a.name)) return false
    return true
  })
  const map = new Map<string, AisopInfo[]>()
  for (const a of filtered) {
    const key = a.group || '_flat'
    if (!map.has(key)) map.set(key, [])
    map.get(key)!.push(a)
  }
  for (const [, items] of map) {
    items.sort((a, b) => {
      const aMain = a.path.endsWith('/main.aisop.json') ? 0 : 1
      const bMain = b.path.endsWith('/main.aisop.json') ? 0 : 1
      return aMain - bMain || a.path.localeCompare(b.path)
    })
  }
  return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]))
})

function toggleLibGroup(group: string) {
  if (expandedLibGroups.value.has(group)) {
    expandedLibGroups.value.delete(group)
  } else {
    expandedLibGroups.value.add(group)
  }
}

function isMain(item: AisopInfo): boolean {
  return item.path.split('/').pop() === 'main.aisop.json'
}

function toggleGroup(group: string) {
  if (expandedGroups.value.has(group)) {
    expandedGroups.value.delete(group)
  } else {
    expandedGroups.value.add(group)
  }
}

async function handleAddFromLibrary(group: string) {
  try {
    await agentStore.addAisopFromLibrary(props.name, group)
    // Refresh both lists
    const [agentData, libData] = await Promise.all([
      agentStore.loadAisops(props.name).catch(() => [] as AisopInfo[]),
      agentStore.loadAisopLibrary().catch(() => [] as AisopInfo[]),
    ])
    aisops.value = agentData
    libraryAisops.value = libData
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : String(e))
  }
}

async function handleDelete() {
  if (!deleteTarget.value) return
  const path = deleteTarget.value.path
  deleteTarget.value = null
  try {
    await agentStore.deleteAisop(props.name, path)
    aisops.value = aisops.value.filter(a => a.path !== path)
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : String(e))
  }
}

async function handleDeleteGroup() {
  if (!deleteGroupTarget.value) return
  const group = deleteGroupTarget.value
  deleteGroupTarget.value = null
  try {
    await agentStore.deleteAisop(props.name, `aisop/${group}`)
    aisops.value = aisops.value.filter(a => a.group !== group)
    expandedGroups.value.delete(group)
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : String(e))
  }
}

function goBack() {
  router.push({ name: 'agents' })
}
</script>

<template>
  <div class="settings-page">
    <div class="page-header">
      <button class="btn-back" @click="goBack">&larr; Agents</button>
      <h2>{{ name }}</h2>
      <span class="header-label">Settings</span>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <template v-else>
      <div class="section">
        <div class="section-header">
          <h3>AISOP Files</h3>
          <span class="badge">{{ ungrouped.filter(a => !isMain(a)).length + groups.length }}</span>
        </div>

        <div v-if="aisops.length === 0" class="empty-state">
          No AISOP files found in this agent.
        </div>

        <div v-else class="aisop-list">
          <!-- Ungrouped (flat) files first -->
          <div v-for="item in ungrouped" :key="item.path" class="aisop-card">
            <div class="aisop-header">
              <div class="aisop-header-left">
                <span class="aisop-filename">{{ item.path.split('/').pop() }}</span>
                <button
                  v-if="!isMain(item)"
                  class="btn-text-delete"
                  @click="deleteTarget = item"
                >Delete</button>
              </div>
              <span v-if="item.version" class="aisop-version">v{{ item.version }}</span>
            </div>
            <div class="aisop-name">{{ item.name }}</div>
            <div v-if="item.summary" class="aisop-summary">{{ item.summary }}</div>
            <div v-if="item.tools.length > 0" class="aisop-tools">
              <span v-for="tool in item.tools" :key="tool" class="tool-tag">{{ tool }}</span>
            </div>
          </div>

          <!-- Grouped files -->
          <div v-for="[group, items] in groups" :key="group" class="aisop-group">
            <div class="group-header">
              <button class="group-toggle" @click="toggleGroup(group)">
                <span class="toggle-icon">{{ expandedGroups.has(group) ? '&#9662;' : '&#9656;' }}</span>
                <span class="group-name">{{ group }}</span>
                <span class="group-count">({{ items.length }})</span>
              </button>
              <button
                class="btn-text-delete"
                @click="deleteGroupTarget = group"
              >Delete</button>
            </div>
            <div v-if="expandedGroups.has(group)" class="group-items">
              <div v-for="item in items" :key="item.path" class="aisop-card">
                <div class="aisop-header">
                  <span class="aisop-filename">{{ item.path.split('/').pop() }}</span>
                  <span v-if="item.version" class="aisop-version">v{{ item.version }}</span>
                </div>
                <div class="aisop-name">{{ item.name }}</div>
                <div v-if="item.summary" class="aisop-summary">{{ item.summary }}</div>
                <div v-if="item.tools.length > 0" class="aisop-tools">
                  <span v-for="tool in item.tools" :key="tool" class="tool-tag">{{ tool }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AISOP Library -->
      <div v-if="libraryGroups.length > 0" class="section">
        <div class="section-header">
          <h3>AISOP Library</h3>
          <span class="badge">{{ libraryGroups.filter(([g]) => g !== '_flat').length + libraryGroups.filter(([g]) => g === '_flat').reduce((n, [, items]) => n + items.filter(a => !isMain(a)).length, 0) }}</span>
        </div>

        <div class="aisop-list">
          <div v-for="[group, items] in libraryGroups" :key="'lib-' + group" class="aisop-group">
            <div v-if="group !== '_flat'" class="group-header">
              <button class="group-toggle" @click="toggleLibGroup(group)">
                <span class="toggle-icon">{{ expandedLibGroups.has(group) ? '&#9662;' : '&#9656;' }}</span>
                <span class="group-name">{{ group }}</span>
                <span class="group-count">({{ items.length }})</span>
              </button>
              <button
                class="btn-text-add"
                @click="handleAddFromLibrary(group)"
              >Add</button>
            </div>
            <!-- Flat library items -->
            <template v-if="group === '_flat'">
              <div v-for="item in items" :key="item.path" class="aisop-card lib-card">
                <div class="aisop-header">
                  <span class="aisop-filename">{{ item.path.split('/').pop() }}</span>
                  <span v-if="item.version" class="aisop-version">v{{ item.version }}</span>
                </div>
                <div class="aisop-name">{{ item.name }}</div>
                <div v-if="item.summary" class="aisop-summary">{{ item.summary }}</div>
                <div v-if="item.tools.length > 0" class="aisop-tools">
                  <span v-for="tool in item.tools" :key="tool" class="tool-tag">{{ tool }}</span>
                </div>
              </div>
            </template>
            <!-- Grouped library items -->
            <div v-else-if="expandedLibGroups.has(group)" class="group-items">
              <div v-for="item in items" :key="item.path" class="aisop-card lib-card">
                <div class="aisop-header">
                  <span class="aisop-filename">{{ item.path.split('/').pop() }}</span>
                  <span v-if="item.version" class="aisop-version">v{{ item.version }}</span>
                </div>
                <div class="aisop-name">{{ item.name }}</div>
                <div v-if="item.summary" class="aisop-summary">{{ item.summary }}</div>
                <div v-if="item.tools.length > 0" class="aisop-tools">
                  <span v-for="tool in item.tools" :key="tool" class="tool-tag">{{ tool }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <ConfirmDialog
      v-if="deleteTarget"
      title="Delete AISOP File"
      :message="`Delete '${deleteTarget.path.split('/').pop()}'? This cannot be undone.`"
      confirmText="Delete"
      confirmVariant="danger"
      @confirm="handleDelete"
      @cancel="deleteTarget = null"
    />

    <ConfirmDialog
      v-if="deleteGroupTarget"
      title="Delete AISOP Group"
      :message="`Delete entire folder '${deleteGroupTarget}' and all AISOP files inside? This cannot be undone.`"
      confirmText="Delete Folder"
      confirmVariant="danger"
      @confirm="handleDeleteGroup"
      @cancel="deleteGroupTarget = null"
    />
  </div>
</template>

<style scoped>
.settings-page {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

.btn-back {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  font-family: var(--font);
}
.btn-back:hover {
  color: var(--accent);
  border-color: var(--accent);
}

.page-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--accent);
}

.header-label {
  font-size: 14px;
  color: var(--text-muted);
}

.loading {
  color: var(--text-muted);
  padding: 40px;
  text-align: center;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
}

.empty-state {
  color: var(--text-muted);
  font-size: 13px;
  padding: 24px;
  text-align: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.aisop-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.aisop-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
}

.aisop-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.aisop-header-left {
  display: flex;
  align-items: center;
  gap: 6px;
}

.aisop-filename {
  font-size: 13px;
  font-family: var(--mono);
  color: var(--accent);
  font-weight: 600;
}

.aisop-version {
  font-size: 11px;
  color: var(--text-muted);
  background: var(--accent-bg);
  padding: 1px 8px;
  border-radius: 8px;
}

.btn-text-delete {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 12px;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  opacity: 0.6;
  transition: opacity 0.15s, color 0.15s;
  font-family: var(--font);
}
.btn-text-delete:hover {
  opacity: 1;
  color: var(--error);
  background: rgba(239, 83, 80, 0.1);
}

.aisop-name {
  font-size: 13px;
  color: var(--text);
  margin-bottom: 2px;
}

.aisop-summary {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 6px;
  line-height: 1.4;
}

.aisop-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tool-tag {
  font-size: 10px;
  padding: 1px 6px;
  background: var(--tool-bg);
  color: var(--text-muted);
  border-radius: 6px;
}

.aisop-group {
  margin-top: 4px;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 4px;
}

.group-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--text);
  cursor: pointer;
  padding: 8px 4px;
  font-size: 14px;
  font-family: var(--font);
  text-align: left;
}
.group-toggle:hover {
  color: var(--accent);
}

.toggle-icon {
  font-size: 12px;
  width: 14px;
  text-align: center;
}

.group-name {
  font-weight: 600;
  font-family: var(--mono);
  font-size: 13px;
}

.group-count {
  color: var(--text-muted);
  font-size: 12px;
}

.group-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-left: 20px;
  padding-top: 6px;
}

.btn-text-add {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 12px;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  opacity: 0.6;
  transition: opacity 0.15s, color 0.15s;
  font-family: var(--font);
}
.btn-text-add:hover {
  opacity: 1;
  color: var(--accent);
  background: var(--accent-bg);
}

.lib-card {
  opacity: 0.75;
}
.lib-card:hover {
  opacity: 1;
}
</style>
