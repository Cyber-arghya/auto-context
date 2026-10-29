<#
.SYNOPSIS
    Autonomous Context & Instruction Manager for AI Coding Assistants.
.DESCRIPTION
    Scaffolds and activates continuous context.md maintenance, credentials tracking,
    and error-solution logging for Antigravity, Cursor, Claude Code, Copilot, and Windsurf.
.PARAMETER TargetDir
    The target project directory. Defaults to current directory ($PWD).
.PARAMETER Force
    Overwrite existing context.md and rule files.
.PARAMETER DryRun
    Preview actions without writing any files to disk.
.EXAMPLE
    init-context
    init-context -Force
    init-context "C:\Projects\MyApp"
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetDir = (Get-Location).Path,

    [Alias("r")]
    [string]$NewRule,

    [Alias("s")]
    [string]$NewSkill,

    [Alias("g")]
    [switch]$Global,

    [Alias("f")]
    [switch]$Force,

    [Alias("d")]
    [switch]$DryRun,

    [Alias("h")]
    [switch]$Help
)

$Version = "1.0.0"

if ($Help) {
    Write-Host @"
init-context - Autonomous Context & Instruction Manager for AI Coding Agents

USAGE:
    init-context [-TargetDir <path>] [OPTIONS]

OPTIONS:
    -NewRule, -r <name>    Scaffold a new agent rule (.agents/rules/<name>.md)
    -NewSkill, -s <name>   Scaffold a new skill (.agents/skills/<name>/SKILL.md)
    -Global, -g            Create the rule or skill globally for all projects
    -Force, -f             Overwrite existing files
    -DryRun, -d            Preview generated files without writing to disk
    -Help, -h              Show this help message

EXAMPLES:
    init-context
    init-context -NewRule code-standards
    init-context -NewSkill deploy-docker
    init-context -NewSkill security-audit -Global

DOCUMENTATION:
    https://github.com/Cyber-arghya/auto-context
"@
    exit 0
}

# ------------------------------------------------------------------------------
# Action 1: Scaffold a New Rule
# ------------------------------------------------------------------------------
if ($NewRule) {
    $CleanRuleName = ($NewRule.ToLower() -replace '[ _]', '-') -replace '\.md$', ''
    $RuleTitle = (Get-Culture).TextInfo.ToTitleCase($CleanRuleName.Replace('-', ' '))

    if ($Global) {
        $DestDir = Join-Path $HOME ".gemini\config\plugins\auto-context\rules"
        $ScopeLabel = "GLOBAL Plugin (~/.gemini/config/plugins/auto-context/rules)"
    } else {
        $DestDir = Join-Path $TargetDir ".agents\rules"
        $ScopeLabel = "LOCAL Project ($DestDir)"
    }

    $DestFile = Join-Path $DestDir "$CleanRuleName.md"

    if ((Test-Path $DestFile) -and -not $Force) {
        Write-Host "[!] Rule already exists at: $DestFile" -ForegroundColor Yellow
        Write-Host "    Use -Force to overwrite." -ForegroundColor Cyan
        exit 1
    }

    if ($DryRun) {
        Write-Host "[!] Dry-run: Would create rule at: $DestFile" -ForegroundColor Yellow
        exit 0
    }

    if (-not (Test-Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    }

    $RuleTemplate = @"
---
name: $CleanRuleName
description: Rule guidelines and constraints for $CleanRuleName. Explain when and how the agent should apply this rule.
trigger: always_on
---

# Rule: $RuleTitle

## Objective
Define the goal and purpose of this rule.

## Guidelines & Constraints
- **Constraint 1:** Specific coding standards, naming conventions, or prohibited patterns.
- **Constraint 2:** Security protocols, credential management, or access boundaries.
- **Constraint 3:** Testing or documentation requirements.

## Enforcement
AI coding agents (Antigravity, Cursor, Claude Code, Copilot) operating in this workspace must adhere strictly to these instructions.
"@

    [System.IO.File]::WriteAllText($DestFile, $RuleTemplate, [System.Text.Encoding]::UTF8)

    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "✨ New Rule Created Successfully!" -ForegroundColor Green
    Write-Host "   Name:   $CleanRuleName" -ForegroundColor Yellow
    Write-Host "   Scope:  $ScopeLabel" -ForegroundColor Cyan
    Write-Host "   File:   $DestFile" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

# ------------------------------------------------------------------------------
# Action 2: Scaffold a New Skill
# ------------------------------------------------------------------------------
if ($NewSkill) {
    $CleanSkillName = $NewSkill.ToLower() -replace '[ _]', '-'
    $SkillTitle = (Get-Culture).TextInfo.ToTitleCase($CleanSkillName.Replace('-', ' '))

    if ($Global) {
        $DestDir = Join-Path $HOME ".gemini\config\plugins\auto-context\skills\$CleanSkillName"
        $ScopeLabel = "GLOBAL Plugin (~/.gemini/config/plugins/auto-context/skills)"
    } else {
        $DestDir = Join-Path $TargetDir ".agents\skills\$CleanSkillName"
        $ScopeLabel = "LOCAL Project ($DestDir)"
    }

    $DestFile = Join-Path $DestDir "SKILL.md"

    if ((Test-Path $DestFile) -and -not $Force) {
        Write-Host "[!] Skill already exists at: $DestFile" -ForegroundColor Yellow
        Write-Host "    Use -Force to overwrite." -ForegroundColor Cyan
        exit 1
    }

    if ($DryRun) {
        Write-Host "[!] Dry-run: Would create skill at: $DestFile" -ForegroundColor Yellow
        exit 0
    }

    if (-not (Test-Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    }

    $SkillTemplate = @"
---
name: $CleanSkillName
description: Describe what this skill accomplishes and the specific keywords or conditions under which the agent should activate it.
---

# Skill: $SkillTitle

## Overview
Briefly summarize the procedure, workflows, or runbooks taught by this skill.

## When to Activate
- When the user asks to perform task X.
- When working on subsystem Y or diagnosing error Z.

## Workflow & Step-by-Step Instructions

### Step 1: Pre-flight & Checks
* Validate prerequisites, environment variables, or dependencies:
  ````bash
  # Check command
  ````

### Step 2: Core Execution
* Follow this exact procedure:
  ````bash
  # Execution command
  ````

### Step 3: Verification
* Verify the expected outcome:
  ````bash
  # Verification command
  ````

## Reference & Troubleshooting
* Common pitfalls and their solutions.
"@

    [System.IO.File]::WriteAllText($DestFile, $SkillTemplate, [System.Text.Encoding]::UTF8)

    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "🎯 New Skill Created Successfully!" -ForegroundColor Green
    Write-Host "   Name:   $CleanSkillName" -ForegroundColor Yellow
    Write-Host "   Scope:  $ScopeLabel" -ForegroundColor Cyan
    Write-Host "   File:   $DestFile" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

if (-not (Test-Path -Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$ProjectDir = (Resolve-Path $TargetDir).Path
$ProjectName = Split-Path -Leaf $ProjectDir
$DateNow = (Get-Date).ToString("yyyy-MM-dd")

# Detect Stack
$Stack = "General / Multi-stack"
$Framework = "Not detected"

if (Test-Path (Join-Path $ProjectDir "package.json")) {
    $Stack = "Node.js / JavaScript / TypeScript"
    $pkg = Get-Content (Join-Path $ProjectDir "package.json") -Raw -ErrorAction SilentlyContinue
    if ($pkg -match "next") { $Framework = "Next.js" }
    elseif ($pkg -match "react") { $Framework = "React" }
    elseif ($pkg -match "vue") { $Framework = "Vue.js" }
    elseif ($pkg -match "express") { $Framework = "Express.js" }
    elseif ($pkg -match "fastify") { $Framework = "Fastify" }
    elseif ($pkg -match "nest") { $Framework = "NestJS" }
}
elseif ((Test-Path (Join-Path $ProjectDir "requirements.txt")) -or (Test-Path (Join-Path $ProjectDir "pyproject.toml"))) {
    $Stack = "Python"
    if (Test-Path (Join-Path $ProjectDir "manage.py")) { $Framework = "Django" }
    else {
        $pyContent = Get-Content (Join-Path $ProjectDir "requirements.txt"), (Join-Path $ProjectDir "pyproject.toml") -Raw -ErrorAction SilentlyContinue
        if ($pyContent -match "fastapi") { $Framework = "FastAPI" }
        elseif ($pyContent -match "flask") { $Framework = "Flask" }
    }
}
elseif (Test-Path (Join-Path $ProjectDir "go.mod")) {
    $Stack = "Go (Golang)"
    $Framework = "Standard Go Modules"
}
elseif (Test-Path (Join-Path $ProjectDir "Cargo.toml")) {
    $Stack = "Rust"
    $Framework = "Cargo Package"
}
elseif ((Test-Path (Join-Path $ProjectDir "pom.xml")) -or (Test-Path (Join-Path $ProjectDir "build.gradle"))) {
    $Stack = "Java / Kotlin"
    $Framework = "Maven / Gradle"
}
elseif ((Test-Path (Join-Path $ProjectDir "docker-compose.yml")) -or (Test-Path (Join-Path $ProjectDir "Dockerfile"))) {
    $Stack = "Dockerized Container"
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "🚀 Auto-Context: Initializing Autonomous Context Manager" -ForegroundColor Green
Write-Host "   Target Project: $ProjectName ($ProjectDir)" -ForegroundColor Yellow
Write-Host "   Detected Stack: $Stack (Framework: $Framework)" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "[!] Dry-run mode: No files will be modified." -ForegroundColor Yellow
}

# 1. Rules directory
$RulesDir = Join-Path $ProjectDir ".agents\rules"
if (-not $DryRun -and -not (Test-Path $RulesDir)) {
    New-Item -ItemType Directory -Path $RulesDir -Force | Out-Null
}

# 2. .agents/rules/maintain_context.md
$RuleFile = Join-Path $RulesDir "maintain_context.md"
if (-not (Test-Path $RuleFile) -or $Force) {
    $RuleContent = @'
---
name: maintain_context
description: Mandates autonomous, continuous synchronization of context.md and proactive rule/skill learning on any repository or server configuration change without requiring user prompting.
trigger: always_on
---

# Autonomous Context Maintenance & Self-Evolution Rule

1. **Mandatory Synchronization**: Every agent working in this workspace MUST inspect and update `context.md` before finishing their turn whenever any of the following occur:
   - Script or configuration edits (environment variables, docker-compose, configs, network parameters).
   - Problem diagnosis, debugging steps, and technical solutions.
   - User credentials, tokens, secrets, or permissions changes.
   - Architectural decisions or operational runbooks.

2. **Autonomous Learning & Skill Crystallization**:
   - Whenever a new pattern, user preference, architectural guideline, or multi-step procedure is discovered or instructed:
     - Scaffolds a **Rule** (`init-context -r <name> [-g]`) if it is a constraint, coding standard, or guideline.
     - Scaffolds a **Skill** (`init-context -s <name> [-g]`) if it is a multi-step procedure or deployment runbook.
     - Populates the file with clear instructions and notifies the user.

3. **CLI Tool Availability**:
   - The agent has full access to run `init-context` directly via terminal:
     - `init-context`: Initialize/repair context.
     - `init-context -r <name> [-g]`: Create rule.
     - `init-context -s <name> [-g]`: Create skill.

4. **No User Reminder Needed**: The user must never need to ask the agent to update `context.md` or learn rules. This is a strict automated post-condition for all actions.
'@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($RuleFile, $RuleContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: .agents\rules\maintain_context.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: .agents\rules\maintain_context.md (use -Force to overwrite)" -ForegroundColor Yellow
}

# 3. GEMINI.md
$GeminiFile = Join-Path $ProjectDir "GEMINI.md"
if (-not (Test-Path $GeminiFile) -or $Force) {
    $GeminiContent = @"
# Standing Agent Rules for $ProjectName

## Critical Mandate: Autonomous ``context.md`` Synchronization & Self-Evolution
As an AI coding assistant working in this repository (``$ProjectDir``), you are **strictly mandated** to keep ``$ProjectDir/context.md`` continuously up to date and autonomously learn, persist, and crystallize new rules and skills. The user must **never** need to remind or instruct you.

### 1. Mandatory Post-Action Protocol
Whenever ANY of the following events occur in any session or conversation turn:
- A configuration file or script is created, edited, moved, or deleted.
- A problem, bug, or error is encountered and diagnosed.
- Credentials, tokens, user accounts, or security keys are generated or updated.
- Architectural decisions or operational steps are modified.

**You MUST immediately update ``$ProjectDir/context.md`` before finalizing your response.**

### 2. Autonomous Learning & Self-Evolution Protocol
Whenever you learn a new pattern, receive a correction, observe a coding preference, or resolve a complex repeatable problem:
1. **Identify the Type:**
   - **Rule:** If it is a constraint, coding standard, safety boundary, or architectural preference -> Create a Rule (\`init-context -r <name>\`).
   - **Skill:** If it is a multi-step procedure, deployment workflow, diagnosis runbook, or CLI sequence -> Create a Skill (\`init-context -s <name>\`).
2. **Scope Decision:**
   - **Project-Specific:** Save in \`.agents/rules/\` or \`.agents/skills/\`.
   - **Machine-Wide / Global:** If it applies to all projects, use \`--global\` (\`-g\`) to register in \`~/.gemini/config/plugins/auto-context/\`.
3. **Execution:**
   - Use the \`init-context\` CLI tool to scaffold the file.
   - Populate it with clear objectives, constraints, or step-by-step instructions.
   - Inform the user of the new rule or skill codified.

### 3. Tool Access: \`init-context\`
You have native access to run \`init-context\` via terminal commands:
- \`init-context\`: Scaffolds or repairs project context.
- \`init-context -r <rule-name> [-g]\`: Creates a new rule with frontmatter.
- \`init-context -s <skill-name> [-g]\`: Creates a new skill with frontmatter.

### 4. Required Content & Structure in ``context.md``
1. **Master Credentials & Configuration Vault (Section 1):** Keep all ports, IPs, secrets, tokens, and endpoints synchronized.
2. **Chronological Problem Log & Technical Solutions (Section 2):** Document symptom, root cause, exact commands/code used, and update Mermaid diagram.
3. **Architecture & Component Layout (Section 3):** Keep stack overview and directory maps accurate.
4. **Operations Runbook (Section 4):** Ensure 1-step reproduction instructions remain functional.
"@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($GeminiFile, $GeminiContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: GEMINI.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: GEMINI.md" -ForegroundColor Yellow
}

# 4. AGENTS.md
$AgentsFile = Join-Path $ProjectDir "AGENTS.md"
if (-not (Test-Path $AgentsFile) -or $Force) {
    if (-not $DryRun) {
        Copy-Item -Path $GeminiFile -Destination $AgentsFile -Force
    }
    Write-Host "  [✓] Generated: AGENTS.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: AGENTS.md" -ForegroundColor Yellow
}

# 5. context.md
$ContextFile = Join-Path $ProjectDir "context.md"
if (-not (Test-Path $ContextFile) -or $Force) {
    $ContextContent = @"
# $ProjectName — Master Architectural Context, Problem Log & Operations Manual

> **Last Updated:** $DateNow  
> **Project Directory:** ``$ProjectDir``  
> **Repository Name:** ``$ProjectName``  
> **Primary Stack:** $Stack ($Framework)  

---

## 1. Master Credentials & Configuration Vault

| Property | Value / Setting | Description |
| :--- | :--- | :--- |
| **Project Name** | ``$ProjectName`` | Active project identifier |
| **Environment** | Development / Production | Current runtime environment |
| **Base Port** | TBD | Application listening port |
| **API Endpoints** | TBD | Service URL / Domains |
| **Secrets / Keys** | Secured in Vault | Credentials, API tokens, passwords |

---

## 2. Chronological Problem Log & Technical Solutions

\`\`\`mermaid
flowchart TD
    Init["1. Project Initialized"] --> Ready["Ready for development"]
\`\`\`

| # | Symptom / Error Message | Root Cause | Exact CLI Solution & Code Patch |
| :-: | :--- | :--- | :--- |
| 1 | Initial setup | Clean repository initialization | Generated autonomous context framework |

---

## 3. System Architecture & Tech Stack

* **Primary Stack:** $Stack
* **Framework:** $Framework
* **Database / Cache:** TBD
* **Deployment Target:** TBD

```
$ProjectName/
├── .agents/
│   └── rules/maintain_context.md
├── AGENTS.md
├── GEMINI.md
└── context.md
```

---

## 4. Setup, Reproduction & Operations Runbook

### Prerequisites
* Operating System: Windows / Linux / WSL2 / macOS
* Runtime / Package Manager: TBD

### Quick Start
\`\`\`bash
# Setup instructions will be populated automatically by AI assistant
\`\`\`

---

## 5. Autonomous Documentation Policy
* Maintained automatically by AI assistants (Antigravity, Cursor, Claude Code, Copilot, Cline, Windsurf) on every code or configuration change.
* Governed by [\`GEMINI.md\`](file://$ProjectDir/GEMINI.md) and [\`.agents/rules/maintain_context.md\`](file://$ProjectDir/.agents/rules/maintain_context.md).
"@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($ContextFile, $ContextContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: context.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: context.md (existing context intact)" -ForegroundColor Yellow
}

# 6. Git
$GitDir = Join-Path $ProjectDir ".git"
if (-not (Test-Path $GitDir)) {
    if (-not $DryRun) {
        git init $ProjectDir 2>$null | Out-Null
    }
    Write-Host "  [✓] Initialized: Git repository" -ForegroundColor Green
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "🎉 Autonomous Context Management is now ACTIVE for: $ProjectName" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   Any AI assistant (Antigravity, Cursor, Claude Code, Copilot)" -ForegroundColor White
Write-Host "   operating in this workspace will now automatically maintain context.md." -ForegroundColor White
Write-Host ""

