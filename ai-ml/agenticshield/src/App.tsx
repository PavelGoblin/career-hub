import { useState } from 'react'

const AGENT_TYPES = [
  'Chatbot', 'Code Agent', 'Research Agent', 'Data Analyst',
  'Workflow Automator', 'Multi-Agent System', 'Other'
]

const TOOLS = [
  'Web Search', 'Code Execution', 'File Read/Write', 'Database Access',
  'Email/Calendar', 'API Calls', 'Shell/Terminal', 'Image Generation',
  'Memory/Vector DB', 'External Plugins'
]

const TRUST_SCOPE = [
  'Processes untrusted user input', 'Has admin/root privileges',
  'Accesses PII', 'Calls third-party APIs', 'Spawns sub-agents',
  'Runs in multi-tenant env', 'Has internet access', 'Can modify production systems'
]

const STEPS = [
  { label: 'Agent Basics', icon: '1' },
  { label: 'Description', icon: '2' },
  { label: 'Capabilities', icon: '3' },
  { label: 'Input Handling', icon: '4' },
  { label: 'Trust Scope', icon: '5' }
]

const API_KEY = 'sk-ant-api03-YOUR_API_KEY_HERE'

interface Threat {
  id: string
  name: string
  severity: 'HIGH' | 'MEDIUM' | 'LOW'
  description: string
  mitre: string
  mitigation: string
}

interface Report {
  risk_score: number
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW'
  summary: string
  threats: Threat[]
}

function App() {
  const [step, setStep] = useState(1)
  const [agentName, setAgentName] = useState('')
  const [agentType, setAgentType] = useState('')
  const [description, setDescription] = useState('')
  const [tools, setTools] = useState<string[]>([])
  const [inputHandling, setInputHandling] = useState('')
  const [trustScope, setTrustScope] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [report, setReport] = useState<Report | null>(null)

  const handleToolToggle = (tool: string) => {
    setTools(prev => prev.includes(tool) ? prev.filter(t => t !== tool) : [...prev, tool])
  }

  const handleTrustToggle = (item: string) => {
    setTrustScope(prev => prev.includes(item) ? prev.filter(t => t !== item) : [...prev, item])
  }

  const canProceed = () => {
    if (step === 1) return agentName.trim() && agentType
    if (step === 2) return description.trim()
    if (step === 3) return tools.length > 0
    if (step === 4) return inputHandling.trim()
    if (step === 5) return trustScope.length > 0
    return true
  }

  const runScan = async () => {
    setLoading(true)
    setError('')

    const userMessage = `Analyze this AI agent for security vulnerabilities:

Agent Name: ${agentName}
Agent Type: ${agentType}
Description: ${description}
Tools/Capabilities: ${tools.join(', ')}
Input Handling: ${inputHandling}
Trust Scope: ${trustScope.join(', ')}

Provide a JSON response with:
{
  "risk_score": <1-10>,
  "risk_level": "<HIGH|MEDIUM|LOW>",
  "summary": "<2-3 sentence executive summary>",
  "threats": [
    {
      "id": "<LLM01–LLM10>",
      "name": "<threat name>",
      "severity": "<HIGH|MEDIUM|LOW>",
      "description": "<agent-specific vulnerability>",
      "mitre": "<MITRE ATLAS technique e.g. AML.T0051>",
      "mitigation": "<concrete fix specific to this agent>"
    }
  ]
}`

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': API_KEY,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 4096,
          temperature: 0.7,
          system: 'You are an expert AI security auditor. Analyze AI agent workflows for OWASP LLM Top 10 and MITRE ATLAS vulnerabilities. Return ONLY valid JSON, no markdown, no backticks.',
          messages: [{ role: 'user', content: userMessage }]
        })
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const data = await response.json()
      const content = data.content?.[0]?.text || ''

      const jsonMatch = content.match(/\{[\s\S]*\}/)
      if (!jsonMatch) {
        throw new Error('Invalid response format')
      }

      const parsed = JSON.parse(jsonMatch[0])
      setReport(parsed)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run security scan')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setStep(1)
    setAgentName('')
    setAgentType('')
    setDescription('')
    setTools([])
    setInputHandling('')
    setTrustScope([])
    setReport(null)
    setError('')
  }

  const getSeverityColor = (severity: string) => {
    if (severity === 'HIGH') return 'border-l-red-500 bg-red-500/10'
    if (severity === 'MEDIUM') return 'border-l-amber-500 bg-amber-500/10'
    return 'border-l-green-500 bg-green-500/10'
  }

  const getSeverityPill = (severity: string) => {
    if (severity === 'HIGH') return 'bg-red-500/20 text-red-400 border-red-500/30'
    if (severity === 'MEDIUM') return 'bg-amber-500/20 text-amber-400 border-amber-500/30'
    return 'bg-green-500/20 text-green-400 border-green-500/30'
  }

  const getRiskBadge = (level: string) => {
    if (level === 'HIGH') return 'bg-red-500/20 text-red-400 border border-red-500/30'
    if (level === 'MEDIUM') return 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
    return 'bg-green-500/20 text-green-400 border border-green-500/30'
  }

  if (report) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] p-4 md:p-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold font-mono text-cyan-400 mb-2">
              Security Report
            </h1>
            <p className="text-zinc-400">Analysis for: {agentName}</p>
          </div>

          <div className="bg-[#12121a] rounded-xl p-6 md:p-8 border border-[#2a2a3a] mb-6">
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="text-center">
                <div className="text-7xl font-bold font-mono text-cyan-400 drop-shadow-[0_0_20px_rgba(6,182,212,0.5)]">
                  {report.risk_score}
                  <span className="text-3xl text-zinc-500">/10</span>
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getRiskBadge(report.risk_level)}`}>
                  {report.risk_level} RISK
                </span>
                <p className="mt-4 text-zinc-300 leading-relaxed">{report.summary}</p>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-xl font-semibold text-zinc-200 mb-4">Identified Threats</h2>
            <div className="space-y-4">
              {report.threats.map((threat, idx) => (
                <div
                  key={idx}
                  className={`bg-[#12121a] rounded-lg p-5 border border-[#2a2a3a] border-l-4 ${getSeverityColor(threat.severity)}`}
                >
                  <div className="flex flex-wrap items-center gap-3 mb-3">
                    <span className="px-2 py-1 rounded text-xs font-mono bg-cyan-500/20 text-cyan-400">
                      {threat.id}
                    </span>
                    <span className="font-semibold text-zinc-200">{threat.name}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityPill(threat.severity)}`}>
                      {threat.severity}
                    </span>
                    <span className="px-2 py-1 rounded text-xs font-mono bg-purple-500/20 text-purple-400">
                      {threat.mitre}
                    </span>
                  </div>
                  <p className="text-zinc-400 text-sm mb-4">{threat.description}</p>
                  <div className="bg-[#1a1a25] rounded-lg p-4 border border-[#2a2a3a]">
                    <p className="text-xs text-zinc-500 uppercase tracking-wide mb-2">Mitigation</p>
                    <p className="text-zinc-300 text-sm">{threat.mitigation}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={reset}
              className="px-6 py-3 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/30 transition-all font-medium"
            >
              New Scan
            </button>
            <button
              className="px-6 py-3 rounded-lg bg-[#1a1a25] text-zinc-300 border border-[#2a2a3a] hover:bg-[#2a2a3a] transition-all font-medium"
            >
              Get Remediation Plan
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <header className="bg-gradient-to-r from-[#0a0a0f] via-[#12121a] to-[#0a0a0f] border-b border-[#2a2a3a] py-4 px-4">
        <div className="max-w-3xl mx-auto flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center border border-cyan-500/30">
            <svg className="w-6 h-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h1 className="text-xl font-bold font-mono text-zinc-100">
            Agentic<span className="text-cyan-400">Shield</span>
          </h1>
        </div>
      </header>

      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          {STEPS.map((s, idx) => (
            <div key={idx} className="flex items-center flex-1">
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-mono text-sm font-semibold transition-all ${
                    idx + 1 < step
                      ? 'bg-cyan-500 text-[#0a0a0f]'
                      : idx + 1 === step
                      ? 'bg-cyan-500/20 text-cyan-400 border-2 border-cyan-500'
                      : 'bg-[#1a1a25] text-zinc-500 border border-[#2a2a3a]'
                  }`}
                >
                  {idx + 1 < step ? '✓' : s.icon}
                </div>
                <span className="text-xs mt-2 text-zinc-500 hidden sm:block">{s.label}</span>
              </div>
              {idx < STEPS.length - 1 && (
                <div className={`flex-1 h-0.5 mx-2 ${idx + 1 < step ? 'bg-cyan-500' : 'bg-[#2a2a3a]'}`} />
              )}
            </div>
          ))}
        </div>

        <div className="bg-[#12121a] rounded-xl p-6 md:p-8 border border-[#2a2a3a]">
          {step === 1 && (
            <div>
              <h2 className="text-xl font-semibold text-zinc-100 mb-6">Agent Basics</h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm text-zinc-400 mb-2">Agent Name *</label>
                  <input
                    type="text"
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    placeholder="e.g., CodeAssist Pro"
                    className="w-full bg-[#1a1a25] border border-[#2a2a3a] rounded-lg px-4 py-3 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-cyan-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm text-zinc-400 mb-3">Agent Type *</label>
                  <div className="flex flex-wrap gap-2">
                    {AGENT_TYPES.map((type) => (
                      <button
                        key={type}
                        onClick={() => setAgentType(type)}
                        className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                          agentType === type
                            ? 'bg-cyan-500 text-[#0a0a0f]'
                            : 'bg-[#1a1a25] text-zinc-400 border border-[#2a2a3a] hover:border-zinc-500'
                        }`}
                      >
                        {type}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-xl font-semibold text-zinc-100 mb-6">Agent Description</h2>
              <div>
                <label className="block text-sm text-zinc-400 mb-2">
                  What does this agent do? *
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe the agent's purpose, architecture, and main functions..."
                  rows={5}
                  className="w-full bg-[#1a1a25] border border-[#2a2a3a] rounded-lg px-4 py-3 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-cyan-500 transition-colors resize-y min-h-[120px]"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h2 className="text-xl font-semibold text-zinc-100 mb-6">Tools & Capabilities</h2>
              <div className="flex flex-wrap gap-2">
                {TOOLS.map((tool) => (
                  <button
                    key={tool}
                    onClick={() => handleToolToggle(tool)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                      tools.includes(tool)
                        ? 'bg-cyan-500 text-[#0a0a0f]'
                        : 'bg-[#1a1a25] text-zinc-400 border border-[#2a2a3a] hover:border-zinc-500'
                    }`}
                  >
                    {tool}
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 4 && (
            <div>
              <h2 className="text-xl font-semibold text-zinc-100 mb-6">Input Handling</h2>
              <div>
                <label className="block text-sm text-zinc-400 mb-2">
                  How does the agent receive and process user input? *
                </label>
                <textarea
                  value={inputHandling}
                  onChange={(e) => setInputHandling(e.target.value)}
                  placeholder="Describe the data flow, input validation, sanitization, and how user requests are handled..."
                  rows={5}
                  className="w-full bg-[#1a1a25] border border-[#2a2a3a] rounded-lg px-4 py-3 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-cyan-500 transition-colors resize-y min-h-[120px]"
                />
              </div>
            </div>
          )}

          {step === 5 && (
            <div>
              <h2 className="text-xl font-semibold text-zinc-100 mb-6">Trust Scope</h2>
              <p className="text-sm text-zinc-400 mb-4">Select all that apply:</p>
              <div className="flex flex-wrap gap-2">
                {TRUST_SCOPE.map((item) => (
                  <button
                    key={item}
                    onClick={() => handleTrustToggle(item)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all text-left ${
                      trustScope.includes(item)
                        ? 'bg-cyan-500 text-[#0a0a0f]'
                        : 'bg-[#1a1a25] text-zinc-400 border border-[#2a2a3a] hover:border-zinc-500'
                    }`}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          )}

          {loading && (
            <div className="mt-8 text-center py-8">
              <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mx-auto mb-4" />
              <p className="text-zinc-400">Analyzing security posture...</p>
            </div>
          )}

          {error && (
            <div className="mt-6 bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <p className="text-red-400 mb-3">{error}</p>
              <button
                onClick={runScan}
                className="px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
              >
                Retry
              </button>
            </div>
          )}

          {!loading && !error && (
            <div className="flex justify-between mt-8 pt-6 border-t border-[#2a2a3a]">
              <button
                onClick={() => setStep(step - 1)}
                disabled={step === 1}
                className={`px-6 py-3 rounded-lg font-medium transition-all ${
                  step === 1
                    ? 'text-zinc-600 cursor-not-allowed'
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-[#1a1a25]'
                }`}
              >
                Back
              </button>

              {step < 5 ? (
                <button
                  onClick={() => setStep(step + 1)}
                  disabled={!canProceed()}
                  className={`px-6 py-3 rounded-lg font-medium transition-all ${
                    canProceed()
                      ? 'bg-cyan-500 text-[#0a0a0f] hover:bg-cyan-400 hover:shadow-[0_0_20px_rgba(6,182,212,0.4)]'
                      : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'
                  }`}
                >
                  Next
                </button>
              ) : (
                <button
                  onClick={runScan}
                  disabled={!canProceed()}
                  className={`px-6 py-3 rounded-lg font-medium transition-all ${
                    canProceed()
                      ? 'bg-cyan-500 text-[#0a0a0f] hover:bg-cyan-400 hover:shadow-[0_0_20px_rgba(6,182,212,0.4)]'
                      : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'
                  }`}
                >
                  Run Security Scan
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App