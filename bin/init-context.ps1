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

    [string]$AddMcp,
    [string]$RemoveMcp,
    [switch]$ListMcp,
    [string]$Preset,
    [Alias("runner")]
    [string]$Runtime,
    [string]$Command,
    [string]$Args,
    [string]$Url,
    [string]$Env,
    [string]$EnvVar,

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
init-context - Autonomous Context, Instruction & Tool Manager for AI Coding Agents

USAGE:
    init-context [-TargetDir <path>] [OPTIONS]

OPTIONS (RULES & SKILLS):
    -NewRule, -r <name>    Scaffold a new agent rule (.agents/rules/<name>.md)
    -NewSkill, -s <name>   Scaffold a new skill (.agents/skills/<name>/SKILL.md)
    -Global, -g            Create the rule or skill globally for all projects
    -Force, -f             Overwrite existing files
    -DryRun, -d            Preview generated files without writing to disk
    -Help, -h              Show this help message

OPTIONS (MCP TOOLING):
    -AddMcp <name>         Add or update an MCP server configuration
    -RemoveMcp <name>      Remove an MCP server from configuration
    -ListMcp               List all active MCP server tools
    -Preset <preset>       Preset template (sqlite, git, fetch, time, duckdb, postgres, github, filesystem, brave)
    -Runtime, -runner <cmd> Package runner for stdio tools: uvx (Python) or npx (Node)
    -Command <cmd>         Executable command for stdio server (e.g. npx, uvx, python)
    -Args <args>           Arguments to pass to command
    -Url <url>             Streamable HTTP endpoint URL for remote MCP server
    -Env <key=val,...>     Environment variables (e.g. 'GITHUB_TOKEN=xyz')

EXAMPLES:
    init-context
    init-context -NewRule code-standards
    init-context -NewSkill deploy-docker
    init-context -AddMcp sqlite
    init-context -AddMcp github -Global
    init-context -ListMcp

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
version: 1.0.0
description: Describe what this skill accomplishes and the specific keywords or conditions under which the agent should activate it.
triggers: ["$CleanSkillName"]
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

# ------------------------------------------------------------------------------
# Action 3: List MCP Servers
# ------------------------------------------------------------------------------
if ($ListMcp) {
    if ($Global) {
        $McpFile = Join-Path $HOME ".gemini\config\mcp_config.json"
        $ScopeLabel = "GLOBAL (~/.gemini/config/mcp_config.json)"
    } else {
        $McpFile = Join-Path $TargetDir ".gemini\mcp_config.json"
        if (-not (Test-Path $McpFile)) {
            $McpFile = Join-Path $TargetDir ".agents\mcp_config.json"
        }
        $ScopeLabel = "LOCAL ($McpFile)"
    }

    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "🔌 Registered MCP Servers: $ScopeLabel" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Cyan

    if (-not (Test-Path $McpFile)) {
        Write-Host "   [!] No MCP configuration found at: $McpFile" -ForegroundColor Yellow
        Write-Host "   Run 'init-context -AddMcp <name>' to register an MCP tool."
        Write-Host ""
        exit 0
    }

    try {
        $json = Get-Content -Path $McpFile -Raw | ConvertFrom-Json
        $servers = $json.mcpServers
        if (-not $servers -or ($servers.psobject.properties.Count -eq 0)) {
            Write-Host "   No MCP servers registered." -ForegroundColor Yellow
        } else {
            Write-Host ("   {0,-20} {1,-8} {2}" -f "NAME", "TYPE", "ENDPOINT / COMMAND") -ForegroundColor Cyan
            Write-Host ("   " + ("-" * 60))
            foreach ($prop in $servers.psobject.properties) {
                $name = $prop.Name
                $cfg = $prop.Value
                if ($cfg.url) {
                    Write-Host ("   {0,-20} {1,-8} {2}" -f $name, "http", $cfg.url)
                } elseif ($cfg.command) {
                    $cmdStr = $cfg.command + " " + ($cfg.args -join " ")
                    if ($cmdStr.Length -gt 40) { $cmdStr = $cmdStr.Substring(0, 37) + "..." }
                    Write-Host ("   {0,-20} {1,-8} {2}" -f $name, "stdio", $cmdStr)
                }
            }
        }
    } catch {
        Write-Host "   Error parsing MCP file: $_" -ForegroundColor Red
    }
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

# ------------------------------------------------------------------------------
# Action 4: Remove MCP Server
# ------------------------------------------------------------------------------
if ($RemoveMcp) {
    if ($Global) {
        $McpFiles = @(Join-Path $HOME ".gemini\config\mcp_config.json", Join-Path $HOME ".gemini\config\plugins\auto-context\mcp_config.json")
        $ScopeLabel = "GLOBAL"
    } else {
        $McpFiles = @(Join-Path $TargetDir ".gemini\mcp_config.json", Join-Path $TargetDir ".agents\mcp_config.json")
        $ScopeLabel = "LOCAL"
    }

    $found = $false
    foreach ($f in $McpFiles) {
        if (Test-Path $f) {
            try {
                $json = Get-Content -Path $f -Raw | ConvertFrom-Json
                if ($json.mcpServers -and $json.mcpServers.$RemoveMcp) {
                    $json.mcpServers.PSObject.Properties.Remove($RemoveMcp)
                    $json | ConvertTo-Json -Depth 10 | Set-Content -Path $f -Encoding UTF8
                    $found = $true
                }
            } catch {}
        }
    }

    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    if ($found) {
        Write-Host "🗑️  Removed MCP Server: $RemoveMcp ($ScopeLabel)" -ForegroundColor Green
    } else {
        Write-Host "[!] MCP Server '$RemoveMcp' was not found in $ScopeLabel configuration." -ForegroundColor Yellow
    }
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

# ------------------------------------------------------------------------------
# Action 5: Add or Update MCP Server (Secure Secret-Handling via .env / Env Vars)
# ------------------------------------------------------------------------------
if ($AddMcp) {
    $ServerName = ($AddMcp.ToLower() -replace '[ _]', '-')
    $ChosenPreset = if ($Preset) { $Preset } else { $ServerName }

    $CmdVal = ""
    $ArgsArr = @()
    $EnvObj = @{}
    $UrlVal = ""
    $SecureVarName = ""
    $EnvPlaceholder = ""
    $RawSecretPassed = ""

    # Determine runtime preference (uvx vs npx)
    $RunnerVal = $Runtime
    if (-not $RunnerVal) {
        if ($ChosenPreset -in @("duckdb", "time")) {
            $RunnerVal = "uvx"
        } else {
            $hasPython = (Test-Path (Join-Path $TargetDir "pyproject.toml")) -or (Test-Path (Join-Path $TargetDir "requirements.txt")) -or (Test-Path (Join-Path $TargetDir "Pipfile"))
            if ($hasPython -and (Get-Command "uvx" -ErrorAction SilentlyContinue)) {
                $RunnerVal = "uvx"
            } else {
                $RunnerVal = "npx"
            }
        }
    }

    if ($ChosenPreset -eq "sqlite") {
        $dbPath = if ($Args) { $Args } else { "database.db" }
        if ($RunnerVal -eq "uvx" -or $RunnerVal -eq "python") {
            $CmdVal = "uvx"
            $ArgsArr = @("mcp-server-sqlite", "--db-path", $dbPath)
        } else {
            $CmdVal = "npx"
            $ArgsArr = @("-y", "@modelcontextprotocol/server-sqlite", $dbPath)
        }
    } elseif ($ChosenPreset -eq "git") {
        $repoPath = if ($Args) { $Args } else { $TargetDir }
        if ($RunnerVal -eq "uvx" -or $RunnerVal -eq "python") {
            $CmdVal = "uvx"
            $ArgsArr = @("mcp-server-git", "--repository", $repoPath)
        } else {
            $CmdVal = "npx"
            $ArgsArr = @("-y", "@modelcontextprotocol/server-git", $repoPath)
        }
    } elseif ($ChosenPreset -eq "duckdb") {
        $CmdVal = "uvx"
        $dbPath = if ($Args) { $Args } else { "database.duckdb" }
        $ArgsArr = @("duckdb-mcp", "--db-path", $dbPath)
    } elseif ($ChosenPreset -eq "time") {
        $CmdVal = "uvx"
        $ArgsArr = @("mcp-server-time")
    } elseif ($ChosenPreset -eq "fetch") {
        if ($RunnerVal -eq "uvx" -or $RunnerVal -eq "python") {
            $CmdVal = "uvx"
            $ArgsArr = @("mcp-server-fetch")
        } else {
            $CmdVal = "npx"
            $ArgsArr = @("-y", "@modelcontextprotocol/server-fetch")
        }
    } elseif ($ChosenPreset -in @("postgres", "postgresql")) {
        $CmdVal = "npx"
        $SecureVarName = if ($EnvVar) { $EnvVar } else { "DATABASE_URL" }
        $EnvPlaceholder = "postgresql://username:password@localhost:5432/mydb"
        if ($Args -and ($Args -like "postgres*")) { $RawSecretPassed = $Args }
        $ArgsArr = @("-y", "@modelcontextprotocol/server-postgres", "`${$SecureVarName}")
    } elseif ($ChosenPreset -eq "github") {
        $CmdVal = "npx"
        $ArgsArr = @("-y", "@modelcontextprotocol/server-github")
        $SecureVarName = if ($EnvVar) { $EnvVar } else { "GITHUB_PERSONAL_ACCESS_TOKEN" }
        $EnvPlaceholder = "ghp_yourPersonalAccessTokenHere"
        if ($Args) { $RawSecretPassed = $Args }
        $EnvObj["GITHUB_PERSONAL_ACCESS_TOKEN"] = "`${$SecureVarName}"
    } elseif ($ChosenPreset -eq "filesystem") {
        $CmdVal = "npx"
        $dirPath = if ($Args) { $Args } else { $TargetDir }
        $ArgsArr = @("-y", "@modelcontextprotocol/server-filesystem", $dirPath)
    } elseif ($ChosenPreset -in @("brave", "brave-search")) {
        $CmdVal = "npx"
        $ArgsArr = @("-y", "@modelcontextprotocol/server-brave-search")
        $SecureVarName = if ($EnvVar) { $EnvVar } else { "BRAVE_API_KEY" }
        $EnvPlaceholder = "your_brave_api_key_here"
        if ($Args) { $RawSecretPassed = $Args }
        $EnvObj["BRAVE_API_KEY"] = "`${$SecureVarName}"
    } elseif ($Url) {
        $UrlVal = $Url
    } elseif ($Command) {
        $CmdVal = $Command
        if ($Args) { $ArgsArr = $Args -split " " }
        if ($EnvVar) {
            $SecureVarName = $EnvVar
            $EnvPlaceholder = "your_${SecureVarName}_secret_here"
            $EnvObj[$SecureVarName] = "`${$SecureVarName}"
        }
    } else {
        if ($RunnerVal -eq "uvx" -or $RunnerVal -eq "python") {
            $CmdVal = "uvx"
            $ArgsArr = @("mcp-server-$ServerName")
        } else {
            $CmdVal = "npx"
            $ArgsArr = @("-y", "@modelcontextprotocol/server-$ServerName")
        }
        if ($EnvVar) {
            $SecureVarName = $EnvVar
            $EnvPlaceholder = "your_${SecureVarName}_secret_here"
            $EnvObj[$SecureVarName] = "`${$SecureVarName}"
        }
    }

    if ($Env) {
        foreach ($item in ($Env -split ",")) {
            if ($item -match "=") {
                $parts = $item -split "=", 2
                $EnvObj[$parts[0].Trim()] = $parts[1].Trim()
            }
        }
    }

    # Secret-handling .env and .gitignore
    if ($SecureVarName -and -not $Global) {
        $DotEnv = Join-Path $TargetDir ".env"
        $DotEnvExample = Join-Path $TargetDir ".env.example"
        $GitIgnore = Join-Path $TargetDir ".gitignore"

        if (-not (Test-Path $DotEnvExample)) {
            Set-Content -Path $DotEnvExample -Value "$SecureVarName=$EnvPlaceholder" -Encoding UTF8
            Write-Host "   [✓] Added placeholder to: .env.example" -ForegroundColor Green
        } else {
            $exContent = Get-Content -Path $DotEnvExample -Raw -ErrorAction SilentlyContinue
            if ($exContent -notmatch "^$SecureVarName=") {
                Add-Content -Path $DotEnvExample -Value "$SecureVarName=$EnvPlaceholder"
                Write-Host "   [✓] Added placeholder to: .env.example" -ForegroundColor Green
            }
        }

        if ($RawSecretPassed) {
            Add-Content -Path $DotEnv -Value "$SecureVarName=$RawSecretPassed"
            Write-Host "   [🔒 Security Hardening] Raw secret safely saved to .env." -ForegroundColor Yellow
            Write-Host "       Plaintext secret was NOT stored in mcp_config.json." -ForegroundColor Yellow
        }

        if (Test-Path $GitIgnore) {
            $giContent = Get-Content -Path $GitIgnore -Raw -ErrorAction SilentlyContinue
            if ($giContent -notmatch "\.env") {
                Add-Content -Path $GitIgnore -Value "`n# Security: Environment secrets`n.env`n.env.local`n.env.*.local"
                Write-Host "   [✓] Protected .env from Git in: .gitignore" -ForegroundColor Green
            }
        } else {
            Set-Content -Path $GitIgnore -Value "# Security: Environment secrets`n.env`n.env.local`n.env.*.local`nnode_modules/" -Encoding UTF8
            Write-Host "   [✓] Created .gitignore with .env protection." -ForegroundColor Green
        }
    }

    if ($Global) {
        $TargetDirs = @(Join-Path $HOME ".gemini\config", Join-Path $HOME ".gemini\config\plugins\auto-context")
        $ScopeLabel = "GLOBAL (~/.gemini/config/mcp_config.json)"
    } else {
        $TargetDirs = @(Join-Path $TargetDir ".gemini", Join-Path $TargetDir ".agents")
        $ScopeLabel = "LOCAL ($TargetDir/.gemini/mcp_config.json)"
    }

    foreach ($d in $TargetDirs) {
        if (-not (Test-Path $d)) {
            New-Item -ItemType Directory -Path $d -Force | Out-Null
        }
        $cfgPath = Join-Path $d "mcp_config.json"
        $data = [PSCustomObject]@{ mcpServers = [PSCustomObject]@{} }

        if (Test-Path $cfgPath) {
            try {
                $existing = Get-Content -Path $cfgPath -Raw | ConvertFrom-Json
                if ($existing.mcpServers) { $data = $existing }
            } catch {}
        }

        $serverCfg = [ordered]@{}
        if ($UrlVal) {
            $serverCfg["url"] = $UrlVal
        } else {
            $serverCfg["command"] = $CmdVal
            if ($ArgsArr.Count -gt 0) { $serverCfg["args"] = $ArgsArr }
            if ($EnvObj.Count -gt 0) { $serverCfg["env"] = $EnvObj }
        }

        $data.mcpServers | Add-Member -MemberType NoteProperty -Name $ServerName -Value ([PSCustomObject]$serverCfg) -Force
        $data | ConvertTo-Json -Depth 10 | Set-Content -Path $cfgPath -Encoding UTF8
    }

    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "🔌 MCP Server Configured Successfully!" -ForegroundColor Green
    Write-Host "   Server Name: $ServerName" -ForegroundColor Yellow
    Write-Host "   Scope:       $ScopeLabel" -ForegroundColor Cyan
    if ($UrlVal) {
        Write-Host "   Transport:   Streamable HTTP ($UrlVal)" -ForegroundColor Green
    } else {
        Write-Host "   Transport:   Stdio ($CmdVal)" -ForegroundColor Green
        if ($RunnerVal) {
            Write-Host "   Runtime:     $RunnerVal" -ForegroundColor Magenta
        }
        Write-Host "   Arguments:   $($ArgsArr -join ' ')" -ForegroundColor Yellow
        if ($EnvObj.Count -gt 0) {
            Write-Host "   Environment: $(($EnvObj.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ', ')" -ForegroundColor Cyan
        }
    }
    if ($SecureVarName) {
        Write-Host "   🔒 Secret Safety: Token referenced via `${$SecureVarName} (stored in .env / env vars)" -ForegroundColor Green
    }
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "   [i] Session Notice: Host clients (Antigravity, Cursor, Claude Desktop) discover MCP tools at session start." -ForegroundColor Yellow
    Write-Host "       Reload window or start a new chat to activate native MCP tool calls." -ForegroundColor Yellow
    Write-Host "       For immediate mid-flight execution in this session, use CLI tools (e.g. sqlite3, gh, curl)." -ForegroundColor White
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

5. **Local Sandbox Test Credentials (`context.local.md`)**:
   - For local dev logins, automated browser testing, and mock fixtures, inspect and update `context.local.md`.
   - Never store real production secrets or payment tokens in markdown files. Real secrets belong in `.env`.
   - Ensure `context.local.md` is strictly git-ignored.

6. **Two-Tier Progressive Disclosure**:
   - Never load full `SKILL.md` bodies into the initial context. Use Section 5 of `context.md` for routing.
   - Dynamically load specific skills via `read_file` only when a user prompt matches their triggers.
'@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($RuleFile, $RuleContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: .agents\rules\maintain_context.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: .agents\rules\maintain_context.md (use -Force to overwrite)" -ForegroundColor Yellow
}

# 2b. .agents/rules/security-boundaries.md
$SecRuleFile = Join-Path $ProjectDir ".agents\rules\security-boundaries.md"
if (-not (Test-Path $SecRuleFile) -or $Force) {
    $SecRuleContent = @"
---
name: security-boundaries
description: Enforces zero plaintext secrets in Git, strict .env protection, and isolated mock data in context.local.md.
trigger: always_on
---

# Rule: Security Boundaries & Secret Safety

## Objective
Prevent credential leakage, indirect prompt injection, and unauthorized network exposure across all code, configuration files, and git commits.

## Guidelines & Constraints
1. **Zero Hardcoded Secrets:**
   - API keys, tokens, database passwords, and private keys must NEVER be hardcoded into source code, committed configs, or git history.
   - All runtime secrets must be loaded via `.env` or system environment variables.
2. **Local Sandbox Test Data Isolation (`context.local.md`):**
   - Only dummy/mock credentials (e.g. `admin@test.local`) belong in `context.local.md`.
   - Real production credentials or live payment keys are strictly prohibited in markdown files.
   - `context.local.md` must remain strictly git-ignored.
3. **Public Exposure Boundaries:**
   - Raw database and internal service ports must bind to `127.0.0.1` unless encapsulated by secure tunneling.
"@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($SecRuleFile, $SecRuleContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: .agents\rules\security-boundaries.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: .agents\rules\security-boundaries.md" -ForegroundColor Yellow
}

# 2c. .agents/rules/code-standards.md
$CodeRuleFile = Join-Path $ProjectDir ".agents\rules\code-standards.md"
if (-not (Test-Path $CodeRuleFile) -or $Force) {
    $CodeRuleContent = @"
---
name: code-standards
description: Enforces clean code principles, DRY architecture, early return patterns, and defensive error handling.
trigger: always_on
---

# Rule: Code Quality & Architecture Standards

## Objective
Maintain readable, maintainable, modular, and type-safe codebases with clear error handling.

## Guidelines & Constraints
1. **Defensive Coding & Early Return:**
   - Prefer guard clauses and early returns to reduce nested indentation.
   - Always validate inputs and handle edge cases at the beginning of functions.
2. **Clean Code & Self-Documenting Logic:**
   - Keep functions focused on a single responsibility (SRP).
   - Write descriptive variable and function names; avoid cryptic abbreviations.
   - Preserve existing comments and docstrings.
3. **Structured Error Handling:**
   - Never suppress exceptions with empty `catch` or `except` blocks.
   - Log actionable error messages that include relevant context (e.g. invalid inputs, resource identifiers).
4. **Conventional Git Commits:**
   - Write semantic commit messages (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
"@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($CodeRuleFile, $CodeRuleContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: .agents\rules\code-standards.md" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: .agents\rules\code-standards.md" -ForegroundColor Yellow
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

### 5. Local Sandbox Credentials & Dummy Test Fixtures (``context.local.md``)
- **Inspection Mandate:** When testing local dev servers, performing browser automation (Playwright/Puppeteer), or authenticating API endpoints, ALWAYS read ``context.local.md`` first before prompting the user for credentials.
- **Strict Mock Boundary:** ONLY store dummy test credentials, mock accounts (\`admin@test.local\`), seed users, and local dev ports in ``context.local.md``.
- **Zero Real Secrets:** Real production secrets, payment keys, or personal tokens MUST NEVER be stored in ``context.local.md`` or ``context.md``; reference them via \`.env\` or system environment variables.
- **Git Protection:** Ensure ``context.local.md`` remains strictly ignored by Git (\`.gitignore\`).

### 6. Two-Tier Progressive Disclosure Protocol (Token Optimization)
- **Initial Boot Budget:** NEVER read full \`SKILL.md\` files into the initial context. Use Section 5 of \`context.md\` for lightweight routing (< 800 tokens).
- **Dynamic On-Demand Loading:** Only when a user prompt matches a skill's triggers (e.g. "docker", "rebase", "diagnostics", "browser"), dynamically inspect the file using \`read_file\`.
- **Zero Session Bloat:** Once the task concludes, do not keep the full skill body in persistent memory.
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

> 🔒 **Local Sandbox Isolation:** Mock test logins, seed users, and local dev ports are stored in [``context.local.md``](file://$ProjectDir/context.local.md) (strictly protected by ``.gitignore``). Real secrets reside exclusively in ``.env``.

| Property | Value / Setting | Description |
| :--- | :--- | :--- |
| **Project Name** | ``$ProjectName`` | Active project identifier |
| **Environment** | Development / Production | Current runtime environment |
| **Base Port** | TBD | Application listening port |
| **API Endpoints** | TBD | Service URL / Domains |
| **Secrets / Keys** | Secured in Vault | Credentials, API tokens, passwords |
| **Test Fixtures** | ``context.local.md`` | Local dummy test credentials (git-ignored) |

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
│   ├── rules/
│   │   ├── code-standards.md
│   │   ├── maintain_context.md
│   │   └── security-boundaries.md
│   └── skills/
│       ├── browser-testing/
│       ├── docker-ops/
│       ├── git-workflow/
│       └── server-diagnostics/
├── AGENTS.md
├── GEMINI.md
├── context.local.md
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

## 5. Skills & Progressive Disclosure Catalog

> 💡 **Progressive Disclosure Protocol:** Agents must NOT read full \`SKILL.md\` files upfront. When user prompts match any triggers, dynamically inspect the skill file using \`read_file\`.

| Skill | Version | Purpose & Scope | Triggers | Location |
| :--- | :---: | :--- | :--- | :--- |
| **\`docker-ops\`** | 1.0.0 | Production Dockerfile & Compose orchestration | \`docker\`, \`container\`, \`compose\` | [SKILL.md](file://$ProjectDir/.agents/skills/docker-ops/SKILL.md) |
| **\`git-workflow\`** | 1.0.0 | Conventional commits & merge conflict resolution | \`git\`, \`commit\`, \`branch\`, \`rebase\` | [SKILL.md](file://$ProjectDir/.agents/skills/git-workflow/SKILL.md) |
| **\`server-diagnostics\`** | 1.0.0 | System health, RAM/swap, CPU, ports & sockets | \`health\`, \`ram\`, \`cpu\`, \`swap\`, \`port\` | [SKILL.md](file://$ProjectDir/.agents/skills/server-diagnostics/SKILL.md) |
| **\`browser-testing\`** | 1.0.0 | UI testing & mock logins using \`context.local.md\` | \`browser\`, \`playwright\`, \`puppeteer\`, \`ui-test\` | [SKILL.md](file://$ProjectDir/.agents/skills/browser-testing/SKILL.md) |

---

## 6. Autonomous Documentation Policy
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

# 6. context.local.md (Local Sandbox & Dummy Test Fixtures Vault)
$LocalVaultFile = Join-Path $ProjectDir "context.local.md"
if (-not (Test-Path $LocalVaultFile) -or $Force) {
    $LocalVaultContent = @"
# ⚠️ LOCAL SANDBOX & DUMMY TEST FIXTURES ONLY
# ==============================================================================
# SECURITY GUARDRAIL:
# DO NOT STORE REAL PRODUCTION SECRETS, PAYMENT KEYS, OR LIVE PASSWORDS HERE.
# This file is strictly for mock logins, seed users, localhost ports, and dev test data.
# Real secrets MUST stay in .env (protected by system environment variables).
#
# GIT STATUS: STRICTLY GIT-IGNORED (*.local.md, context.local.md)
# ==============================================================================

> **Project:** ``$ProjectName``  
> **Purpose:** Local mock credentials & test logins for AI browser testing and dev automation.  
> **Notice to AI Assistant:** Check this file before asking user for test login credentials. Never commit this file to Git.

---

## 1. Local Dev Endpoints & Test Ports

| Service | Local URL / Port | Status / Description |
| :--- | :--- | :--- |
| **Frontend Web** | ``http://localhost:3000`` | Dev server |
| **Backend API** | ``http://localhost:8000`` | Local API endpoint |
| **Local Mock DB** | ``localhost:5432`` / ``database.db`` | Non-production dev database |

---

## 2. Seed Accounts & Dummy Test Logins (Browser Automation)

Use these mock accounts when performing automated UI testing, Playwright / Puppeteer workflows, or manual verification.

| Role | Username / Email | Mock Password | Notes / Permissions |
| :--- | :--- | :--- | :--- |
| **Super Admin** | ``admin@test.local`` | ``adminpass123`` | Full admin privileges |
| **Standard User** | ``user@test.local`` | ``userpass123`` | Default user permissions |
| **Guest / Demo** | ``guest@test.local`` | ``guestpass123`` | Read-only access |

---

## 3. Local Mock Tokens & Test Headers

\`\`\`http
Authorization: Bearer dev-mock-token-12345
X-Test-Bypass: true
\`\`\`

---

## 4. Local Test Notes & Scratch Data
<!-- AI and developer can jot temporary test notes, cookie values, or scratch session tokens here -->
- Test session initialized: $DateNow
"@
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($LocalVaultFile, $LocalVaultContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "  [✓] Generated: context.local.md (Local Sandbox Vault)" -ForegroundColor Green
} else {
    Write-Host "  [*] Preserved: context.local.md" -ForegroundColor Yellow
}

# 7. Default Starter Skills Library (Two-Tier Progressive Disclosure)
$StarterSkills = @("docker-ops", "git-workflow", "server-diagnostics", "browser-testing")
foreach ($s in $StarterSkills) {
    $sDir = Join-Path $ProjectDir ".agents\skills\$s"
    $sFile = Join-Path $sDir "SKILL.md"
    if (-not (Test-Path $sFile) -or $Force) {
        if (-not $DryRun) {
            if (-not (Test-Path $sDir)) { New-Item -ItemType Directory -Path $sDir -Force | Out-Null }
            $content = ""
            if ($s -eq "docker-ops") {
                $content = @"
---
name: docker-ops
version: 1.0.0
description: Production multi-stage Dockerfile and Compose setup, container diagnostics, cleanup, and logging.
triggers: ["docker", "container", "compose", "dockerfile", "entrypoint"]
---

# Skill: Docker Operations & Container Management

## Overview
Standard operating procedures for containerizing applications, writing secure multi-stage Dockerfiles, managing docker-compose stacks, and diagnosing container failures.

## When to Activate
- When creating or modifying Dockerfile or docker-compose.yml.
- When diagnosing crashed, restarting, or unhealthy containers.
- When cleaning up dangling images, unused volumes, or container build cache.

## Workflows & Procedures
1. Multi-Stage Builds: Separate build environment from lean production runtime.
2. Non-Root Users: Run container processes as non-root (USER appuser).
3. Secret Decoupling: Reference secrets dynamically via .env (`${VAR_NAME}`).
4. Resource Bounds: Limit CPU and memory in compose configurations.
"@
            } elseif ($s -eq "git-workflow") {
                $content = @"
---
name: git-workflow
version: 1.0.0
description: Conventional commit standards, branch management, safe rebasing, and merge conflict resolution.
triggers: ["git", "commit", "branch", "pr", "pull-request", "merge", "conflict", "rebase"]
---

# Skill: Git Workflow & Release Management

## Overview
Standard procedures for feature branching, atomic conventional commits, interactive rebasing, merge conflict resolution, and safe remote synchronization.

## When to Activate
- When staging, committing, or pushing code changes to remote repositories.
- When creating pull requests, managing feature branches, or tagging releases.
- When resolving git merge or rebase conflicts.

## Workflows & Procedures
1. Conventional Commits: Use feat:, fix:, docs:, refactor:, chore: prefixes.
2. Safe Rebasing: Always rebase against main branch (git fetch origin && git rebase origin/main).
3. Conflict Resolution: Inspect conflict markers, decide ours vs theirs, resolve, test, and continue.
"@
            } elseif ($s -eq "server-diagnostics") {
                $content = @"
---
name: server-diagnostics
version: 1.0.0
description: Real-time system health checks, RAM/swap usage, CPU load, open ports, and network connectivity diagnostics.
triggers: ["health", "ram", "cpu", "swap", "diagnostics", "server", "port", "disk", "uptime"]
---

# Skill: Server Diagnostics & Resource Health

## Overview
Comprehensive runbook for assessing server stability, inspecting hardware memory buffers, verifying swap allocation, auditing listening network ports, and monitoring active background processes.

## When to Activate
- When experiencing system slowdowns, high latency, or OOM kill events.
- When checking server resource headroom before running heavy builds or containers.
- When verifying open ports, firewall status, or Cloudflare tunnel connectivity.

## Workflows & Procedures
1. RAM & Swap: free -h (alert if available memory < 200MB).
2. CPU & Load: uptime, ps aux --sort=-%cpu | head -n 6.
3. Disk & Inodes: df -h /, df -i /.
4. Ports: sudo ss -tulpn.
"@
            } elseif ($s -eq "browser-testing") {
                $content = @"
---
name: browser-testing
version: 1.0.0
description: Automated web UI verification, Playwright/Puppeteer automation, and dev endpoint testing using context.local.md.
triggers: ["browser", "playwright", "puppeteer", "ui-test", "login-test", "headless", "screenshot"]
---

# Skill: Browser Testing & Local UI Verification

## Overview
Automated procedures for conducting browser testing, verifying web UI flows, performing login checks using mock fixtures from context.local.md, and preventing credential amnesia.

## When to Activate
- When verifying frontend web pages, UI components, forms, or authentication flows.
- When running Playwright, Puppeteer, or Chrome DevTools automated actions.
- When capturing screenshots or checking console errors on local dev servers.

## Workflows & Procedures
1. Read context.local.md for mock accounts (admin@test.local) and local ports.
2. Launch test automation script or browser action.
3. Capture error screenshots in local scratch directory if assertions fail.
"@
            }
            [System.IO.File]::WriteAllText($sFile, $content, [System.Text.Encoding]::UTF8)
        }
        Write-Host "  [✓] Generated: .agents\skills\$s\SKILL.md (Two-Tier Progressive)" -ForegroundColor Green
    } else {
        Write-Host "  [*] Preserved: .agents\skills\$s\SKILL.md" -ForegroundColor Yellow
    }
}

# 8. Gitignore Hardening for context.local.md and .env
$GitIgnoreFile = Join-Path $ProjectDir ".gitignore"
if (-not $DryRun) {
    if (-not (Test-Path $GitIgnoreFile)) {
        $GiContent = @"
# Security: Local AI sandbox vault (dummy test logins & secrets)
context.local.md
*.local.md

# Security: Environment secrets
.env
.env.local
.env.*.local
node_modules/
"@
        Set-Content -Path $GitIgnoreFile -Value $GiContent -Encoding UTF8
        Write-Host "  [✓] Generated: .gitignore (protected context.local.md & .env)" -ForegroundColor Green
    } else {
        $giRaw = Get-Content -Path $GitIgnoreFile -Raw -ErrorAction SilentlyContinue
        if ($giRaw -notmatch "context\.local\.md") {
            Add-Content -Path $GitIgnoreFile -Value "`n# Security: Local AI sandbox vault (dummy test logins & secrets)`ncontext.local.md`n*.local.md"
            Write-Host "  [✓] Hardened: .gitignore with context.local.md protection" -ForegroundColor Green
        }
    }
}

# 9. Git
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

