import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api, apiPost, apiDelete } from '@/composables/useApi'
import type { AgentInfo, AisopInfo, TemplateInfo } from '@/types'

export const useAgentStore = defineStore('agent', () => {
  const agents = ref<string[]>([])
  const currentAgent = ref<string | null>(localStorage.getItem('soulbot:lastAgent'))
  const agentInfo = ref<Record<string, AgentInfo>>({})
  const templates = ref<TemplateInfo[]>([])

  async function loadAgents() {
    agents.value = await api<string[]>('/list-apps')
    // Restore last agent; fallback to first if not found
    if (currentAgent.value && !agents.value.includes(currentAgent.value)) {
      currentAgent.value = null
    }
    if (!currentAgent.value && agents.value.length > 0) {
      selectAgent(agents.value[0]!)
    }
  }

  async function loadAgentInfo(name: string) {
    if (!agentInfo.value[name]) {
      agentInfo.value[name] = await api<AgentInfo>(`/apps/${name}`)
    }
    return agentInfo.value[name]
  }

  async function loadTemplates() {
    templates.value = await api<TemplateInfo[]>('/templates')
  }

  async function createAgent(name: string, template: string) {
    await apiPost('/agents/create', { name, template })
    // Refresh agent list and load info for the new agent
    await loadAgents()
    agentInfo.value[name] = await api<AgentInfo>(`/apps/${name}`)
  }

  async function deleteAgent(name: string) {
    await apiDelete(`/agents/${name}`)
    // Clear cached info
    delete agentInfo.value[name]
    // Refresh list
    await loadAgents()
  }

  async function loadAisops(agentName: string): Promise<AisopInfo[]> {
    return api<AisopInfo[]>(`/agents/${agentName}/aisops`)
  }

  async function loadAisips(agentName: string): Promise<AisopInfo[]> {
    return api<AisopInfo[]>(`/agents/${agentName}/aisips`)
  }

  async function deleteAisop(agentName: string, path: string) {
    await apiPost(`/agents/${agentName}/aisops/delete`, { path })
  }

  async function loadAisopLibrary(): Promise<AisopInfo[]> {
    return api<AisopInfo[]>('/aisop-library')
  }

  async function addAisopFromLibrary(agentName: string, group: string) {
    await apiPost(`/agents/${agentName}/aisops/add-from-library`, { group })
  }

  function selectAgent(name: string) {
    currentAgent.value = name
    localStorage.setItem('soulbot:lastAgent', name)
  }

  return {
    agents,
    currentAgent,
    agentInfo,
    templates,
    loadAgents,
    loadAgentInfo,
    loadTemplates,
    createAgent,
    deleteAgent,
    loadAisops,
    loadAisips,
    deleteAisop,
    loadAisopLibrary,
    addAisopFromLibrary,
    selectAgent,
  }
})
