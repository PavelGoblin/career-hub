# AgenticShield - AI Agent Security Auditor

## Project Overview
- **Project name**: AgenticShield
- **Type**: Single-page React webapp
- **Core functionality**: A 5-step wizard that collects AI agent security details, sends them to Anthropic Claude API for analysis, and displays a security report with risk scores and mitigation recommendations
- **Target users**: Security engineers, AI developers, DevOps teams auditing AI agents

---

## UI/UX Specification

### Layout Structure

**Page Sections**:
1. **Header**: Logo/title, dark themed
2. **Progress Bar**: 5-step stepper showing current step
3. **Main Content Area**: Dynamic based on current step
4. **Navigation Footer**: Back/Next buttons
5. **Report View**: Full results display after scan

**Responsive Breakpoints**:
- Mobile: < 640px (single column, stacked elements)
- Tablet: 640px - 1024px (adjusted spacing)
- Desktop: > 1024px (centered content max-width 800px)

### Visual Design

**Color Palette**:
- Background Primary: `#0a0a0f` (near-black)
- Background Secondary: `#12121a` (dark card)
- Background Tertiary: `#1a1a25` (elevated surfaces)
- Border: `#2a2a3a` (subtle borders)
- Text Primary: `#e4e4e7` (zinc-200)
- Text Secondary: `#a1a1aa` (zinc-400)
- Text Muted: `#71717a` (zinc-500)
- Accent Primary: `#06b6d4` (cyan-500)
- Accent Hover: `#22d3ee` (cyan-400)
- Danger: `#ef4444` (red-500)
- Warning: `#f59e0b` (amber-500)
- Success: `#22c55e` (green-500)
- Info: `#3b82f6` (blue-500)

**Typography**:
- Font Family: `JetBrains Mono` for headings, `Inter` for body (via Google Fonts)
- Heading 1: 32px, font-weight 700
- Heading 2: 24px, font-weight 600
- Heading 3: 18px, font-weight 600
- Body: 14px, font-weight 400
- Small: 12px, font-weight 400

**Spacing System**:
- Base unit: 4px
- Padding: 16px (cards), 24px (containers)
- Gap: 8px (small), 16px (medium), 24px (large)
- Border radius: 8px (buttons), 12px (cards), 16px (modals)

**Visual Effects**:
- Card shadows: `0 4px 24px rgba(0, 0, 0, 0.5)`
- Glow effect on cyan elements: `0 0 20px rgba(6, 182, 212, 0.3)`
- Smooth transitions: 200ms ease-in-out
- Subtle gradient on header: linear-gradient to right with cyan accent

### Components

**1. Progress Stepper**
- 5 circular steps connected by lines
- States: completed (cyan fill), current (cyan ring), pending (gray ring)
- Step labels below each circle

**2. Text Input**
- Dark background (#12121a)
- Border on focus (cyan)
- Placeholder text in muted color

**3. Textarea**
- Same styling as text input
- Resize vertical only
- Min height 120px

**4. Chip Select (Single & Multi)**
- Pill-shaped buttons
- Unselected: dark bg, gray border
- Selected: cyan bg, cyan text
- Hover: lighter bg

**5. Buttons**
- Primary: cyan bg, dark text, hover glow
- Secondary: transparent, cyan border
- Disabled: gray, reduced opacity

**6. Loading Spinner**
- Cyan rotating ring
- "Analyzing..." text below

**7. Threat Cards**
- Left border color based on severity (red/amber/green)
- Card background with shadow
- Tag pills for OWASP and MITRE

**8. Risk Score Display**
- Large number (64px) with glow
- Badge pill (HIGH/MEDIUM/LOW)
- Animated counter

---

## Functionality Specification

### Core Features

**Step 1 - Agent Basics**:
- Text input for agent name (required)
- Single-select chips for agent type:
  - Chatbot, Code Agent, Research Agent, Data Analyst, Workflow Automator, Multi-Agent System, Other

**Step 2 - Agent Description**:
- Textarea for detailed description (what the agent does)
- Placeholder: "Describe the agent's purpose, architecture, and main functions..."

**Step 3 - Tools/Capabilities**:
- Multi-select chips (can select multiple):
  - Web Search, Code Execution, File Read/Write, Database Access, Email/Calendar, API Calls, Shell/Terminal, Image Generation, Memory/Vector DB, External Plugins

**Step 4 - Input Handling**:
- Textarea for input processing description
- Placeholder: "How does the agent receive and process user input? Describe data flow..."

**Step 5 - Trust Scope**:
- Multi-select chips:
  - Processes untrusted user input
  - Has admin/root privileges
  - Accesses PII
  - Calls third-party APIs
  - Spawns sub-agents
  - Runs in multi-tenant env
  - Has internet access
  - Can modify production systems

**Navigation**:
- Back button: disabled on step 1
- Next button: validates current step before proceeding
- "Run Security Scan" appears after step 5

**API Integration**:
- Endpoint: https://api.anthropic.com/v1/messages
- Model: claude-sonnet-4-20250514
- System prompt: "You are an expert AI security auditor..."
- Max tokens: 4096
- Temperature: 0.7

**Report Display**:
- Overall risk score (1-10)
- Risk level badge
- Executive summary
- Array of threat objects
- Each threat: id, name, severity, description, mitre, mitigation

**Error Handling**:
- API error: show error message with retry button
- Validation error: highlight required fields

**Reset**:
- "New Scan" button resets all state to step 1

### User Interactions
- Click chip to select/deselect
- Type in text fields
- Navigate with buttons
- Scroll through report
- Click "New Scan" to reset

---

## Acceptance Criteria

1. ✓ All 5 steps render correctly with proper inputs
2. ✓ Progress stepper shows current step accurately
3. ✓ Chip selection works (single for types, multi for others)
4. ✓ Next button validates before proceeding
5. ✓ Back button navigates to previous step
6. ✓ API call triggers on "Run Security Scan"
7. ✓ Loading state shows during API call
8. ✓ Error state displays on API failure with retry option
9. ✓ Report displays all risk information correctly
10. ✓ Threat cards have correct severity colors
11. ✓ "New Scan" resets entire wizard
12. ✓ Dark theme consistently applied
13. ✓ Mobile responsive layout works
14. ✓ No form tags used (onClick handlers only)