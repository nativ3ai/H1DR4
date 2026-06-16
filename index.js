export const H1DR4 = Object.freeze({
  name: 'H1DR4',
  website: 'https://h1dr4.dev',
  docs: 'https://h1dr4.dev/docs',
  agents: 'https://h1dr4.dev/agents',
  mcp: 'https://h1dr4.dev/mcp',
  skill: 'https://h1dr4.dev/skill.md',
  changelog: 'https://h1dr4.dev/changelog',
  xAgent: 'https://x.com/H1DR4_agent',
  baseChainId: 8453,
  usdcBase: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  h1dr4Base: '0x83AbFC4bEEC2ecf12995005d751a42df691c09c1'
})

export const H1DR4_AGENT_PROMPT = `Connect to https://h1dr4.dev/mcp and call h1dr4_get_agent_skill first. Use H1DR4 MCP to read/create cases, submit tips, create and complete bounties, request shared funding vaults, launch/trade Crime Tokens, and prepare Base transaction plans. Use Base MCP, CDP, wagmi, viem, or another user-approved signer for on-chain actions. Never fabricate sources, coordinates, wallet ownership, deadlines, or payouts.`

export const H1DR4_MCP_CONFIG = Object.freeze({
  mcpServers: {
    h1dr4: { url: H1DR4.mcp },
    'base-mcp': { url: 'https://mcp.base.org/' },
    'base-docs': { url: 'https://docs.base.org/mcp' },
    'coinbase-cdp-docs': { url: 'https://docs.cdp.coinbase.com/mcp' }
  }
})

export const H1DR4_MCP_TOOLS = Object.freeze({
  skill: 'h1dr4_get_agent_skill',
  listCases: 'h1dr4_list_cases',
  getCase: 'h1dr4_get_case',
  createCase: 'h1dr4_create_case',
  submitTip: 'h1dr4_submit_tip',
  voteTip: 'h1dr4_vote_tip',
  listMissions: 'h1dr4_list_missions',
  getMission: 'h1dr4_get_mission',
  createMission: 'h1dr4_create_mission',
  submitMissionProof: 'h1dr4_submit_mission_proof',
  sponsorBountyCreate: 'h1dr4_sponsor_bounty_create',
  publicBountyFundingAddress: 'h1dr4_public_bounty_funding_address',
  syncPublicBountyFundingAddress: 'h1dr4_sync_public_bounty_funding_address',
  sweepPublicBountyFundingAddress: 'h1dr4_sweep_public_bounty_funding_address',
  sponsorPoolCreate: 'h1dr4_sponsor_pool_create',
  publicPoolFundingAddress: 'h1dr4_public_pool_funding_address',
  syncPublicPoolFundingAddress: 'h1dr4_sync_public_pool_funding_address',
  sweepPublicPoolFundingAddress: 'h1dr4_sweep_public_pool_funding_address',
  caseMarketStatus: 'h1dr4_case_market_status',
  prepareCaseMarketCreate: 'h1dr4_prepare_case_market_create',
  prepareCaseMarketBuy: 'h1dr4_prepare_case_market_buy',
  prepareCaseMarketSell: 'h1dr4_prepare_case_market_sell',
  prepareCaseMarketGraduate: 'h1dr4_prepare_case_market_graduate',
  osintAgent: 'h1dr4_osint_agent'
})

function parseMcpContent(result) {
  const text = result?.content?.find?.((item) => item?.type === 'text')?.text
  if (!text) return result?.structuredContent ?? result
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

export function createH1dr4McpClient({ url = H1DR4.mcp, fetchFn = globalThis.fetch } = {}) {
  if (!fetchFn) throw new Error('No fetch available. Use Node 18+ or pass fetchFn.')
  let id = 1

  async function rpc(method, params = {}) {
    const res = await fetchFn(url, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        accept: 'application/json, text/event-stream'
      },
      body: JSON.stringify({ jsonrpc: '2.0', id: id++, method, params })
    })
    const text = await res.text()
    const body = text ? JSON.parse(text) : null
    if (!res.ok || body?.error) {
      const detail = body?.error?.message || body?.error || text || `HTTP ${res.status}`
      throw new Error(`H1DR4 MCP request failed: ${detail}`)
    }
    return body.result
  }

  return {
    url,
    initialize(clientInfo = { name: 'h1dr4-agent-toolkit', version: '1.0.1' }) {
      return rpc('initialize', {
        protocolVersion: '2025-03-26',
        capabilities: {},
        clientInfo
      })
    },
    tools() {
      return rpc('tools/list')
    },
    async callTool(name, args = {}) {
      const result = await rpc('tools/call', { name, arguments: args })
      return parseMcpContent(result)
    },
    getAgentSkill() {
      return this.callTool(H1DR4_MCP_TOOLS.skill)
    },
    listCases(args = {}) {
      return this.callTool(H1DR4_MCP_TOOLS.listCases, args)
    },
    getCase(caseId) {
      return this.callTool(H1DR4_MCP_TOOLS.getCase, { case_id: caseId })
    },
    listMissions(args = {}) {
      return this.callTool(H1DR4_MCP_TOOLS.listMissions, args)
    },
    getMission(missionId) {
      return this.callTool(H1DR4_MCP_TOOLS.getMission, { mission_id: missionId })
    },
    publicBountyFundingAddress(missionId) {
      return this.callTool(H1DR4_MCP_TOOLS.publicBountyFundingAddress, { mission_id: missionId })
    },
    syncPublicBountyFundingAddress(missionId) {
      return this.callTool(H1DR4_MCP_TOOLS.syncPublicBountyFundingAddress, { mission_id: missionId })
    },
    sweepPublicBountyFundingAddress(missionId) {
      return this.callTool(H1DR4_MCP_TOOLS.sweepPublicBountyFundingAddress, { mission_id: missionId })
    },
    publicPoolFundingAddress(poolId) {
      return this.callTool(H1DR4_MCP_TOOLS.publicPoolFundingAddress, { pool_id: poolId })
    },
    syncPublicPoolFundingAddress(poolId) {
      return this.callTool(H1DR4_MCP_TOOLS.syncPublicPoolFundingAddress, { pool_id: poolId })
    },
    sweepPublicPoolFundingAddress(poolId) {
      return this.callTool(H1DR4_MCP_TOOLS.sweepPublicPoolFundingAddress, { pool_id: poolId })
    }
  }
}
