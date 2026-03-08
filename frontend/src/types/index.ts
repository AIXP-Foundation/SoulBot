// SoulBot API types

export interface Session {
  id: string
  app_name: string
  user_id: string
  agent_name: string
  last_agent: string | null
  title: string | null
  created_at: number
  last_update_time: number
}

export interface SessionDetail extends Session {
  state: Record<string, unknown>
  events: AgentEvent[]
}

export interface AgentEvent {
  author: string
  timestamp?: number
  content?: {
    parts?: EventPart[]
  }
  actions?: {
    transfer_to_agent?: string
  }
  partial?: boolean
  error_code?: string
  error_message?: string
}

export interface EventPart {
  text?: string
  function_call?: {
    name: string
    args: Record<string, unknown>
  }
  function_response?: {
    name: string
    response: unknown
  }
}

export interface AgentInfo {
  name: string
  description: string
  sub_agents: string[]
}

export interface TemplateInfo {
  name: string
  description: string
}

export interface CreateAgentRequest {
  name: string
  template: string
}

export interface AisopInfo {
  path: string
  group: string | null
  name: string
  version: string
  summary: string
  protocol: string
  tools: string[]
}

export interface StoreProgram {
  name: string
  version: string
  pattern: string
  summary: string
  tools: string[]
  quality_grade: string
  quality_score: number
  trust_level: string
  module_count: number
  github_url: string
}

export interface ScheduleEntry {
  id: string
  trigger_config: {
    type: string
    delay?: number
    interval?: number
    cron?: string
  }
  status: string
  from_agent: string
  to_agent: string
  created_at: string
  last_run: string | null
  run_count: number
  last_result: string | null
  last_error: string | null
}
