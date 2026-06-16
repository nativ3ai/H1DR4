import { createH1dr4McpClient } from '../index.js'

const h1dr4 = createH1dr4McpClient()
await h1dr4.initialize({ name: 'h1dr4-public-smoke', version: '1.0.1' })
const tools = await h1dr4.tools()
console.log((tools.tools || []).map((tool) => tool.name).join('\n'))
