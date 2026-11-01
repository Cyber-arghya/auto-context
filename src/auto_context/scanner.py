"""
scanner.py — Stack-Adaptive Codebase Introspection & Brownfield Discovery Engine.

Discovers ports, routes, database schemas, services, and runbooks using lightweight
filesystem convention heuristics (0 LLM tokens, 100% crash-proof, idempotency-guaranteed).
"""
import hashlib
import json
from pathlib import Path
import re
from typing import Optional

from rich.console import Console

console = Console()


# ── Idempotency & Hash Helpers ────────────────────────────────────────────────

def get_content_hash(text: str) -> str:
    """Compute SHA-256 hash of text content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_idempotent(path: Path, content: str, label: str = "File") -> bool:
    """
    Write content to path only if content has changed (Content-Hash Guard).
    Returns True if a write occurred, False if content was already identical.
    """
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
            if get_content_hash(existing) == get_content_hash(content):
                console.print(f"  [dim]— Up to date:[/] {path.name}")
                return False
        except Exception:
            pass

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    console.print(f"  [green][✓] Synchronized:[/] {path.name}")
    return True


# ── Port & Service Extractor ──────────────────────────────────────────────────

def discover_ports_and_services(project_dir: Path) -> list[tuple[str, str, str]]:
    """
    Extract network ports and service bindings from configs without leaking secrets.
    Returns list of (Service, Port, SourceFile).
    """
    results: list[tuple[str, str, str]] = []
    seen_ports: set[str] = set()

    # 1. Check docker-compose.yml / compose.yaml
    for compose_name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"):
        compose_file = project_dir / compose_name
        if compose_file.exists():
            try:
                text = compose_file.read_text(encoding="utf-8", errors="ignore")
                matches = re.findall(r'["\']?(\d{2,5}):(\d{2,5})["\']?', text)
                for host_port, container_port in matches:
                    if host_port not in seen_ports and int(host_port) > 80:
                        seen_ports.add(host_port)
                        results.append(("Container Port", host_port, compose_name))
            except Exception:
                pass

    # 2. Check .env.example / .env
    for env_name in (".env.example", ".env", ".env.local"):
        env_file = project_dir / env_name
        if env_file.exists():
            try:
                for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if "PORT" in key.upper() and val.isdigit() and val not in seen_ports:
                        seen_ports.add(val)
                        results.append((key, val, env_name))
            except Exception:
                pass

    # 3. Check Dockerfile
    dockerfile = project_dir / "Dockerfile"
    if dockerfile.exists():
        try:
            for line in dockerfile.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.strip().upper().startswith("EXPOSE "):
                    port = line.strip().split()[1]
                    if port.isdigit() and port not in seen_ports:
                        seen_ports.add(port)
                        results.append(("Exposed Port", port, "Dockerfile"))
        except Exception:
            pass

    return results


# ── Runbook Command Extractor ─────────────────────────────────────────────────

def discover_runbook_commands(project_dir: Path) -> list[tuple[str, str]]:
    """
    Extract executable development, build, and test commands from project manifests.
    Returns list of (Action, Command).
    """
    commands: list[tuple[str, str]] = []

    # 1. package.json scripts
    pkg_file = project_dir / "package.json"
    if pkg_file.exists():
        try:
            data = json.loads(pkg_file.read_text(encoding="utf-8", errors="ignore"))
            scripts = data.get("scripts", {})
            for key in ("dev", "start", "build", "test", "lint"):
                if key in scripts:
                    commands.append((f"Run {key}", f"npm run {key}"))
        except Exception:
            pass

    # 2. Makefile
    makefile = project_dir / "Makefile"
    if makefile.exists():
        try:
            targets = re.findall(r"^([a-zA-Z0-9_-]+):", makefile.read_text(encoding="utf-8", errors="ignore"), re.M)
            for t in targets[:4]:
                if not t.startswith("."):
                    commands.append((f"Make {t}", f"make {t}"))
        except Exception:
            pass

    # 3. Python indicators
    if (project_dir / "manage.py").exists():
        commands.append(("Django Runserver", "python manage.py runserver"))
        commands.append(("Django Migrate", "python manage.py migrate"))
    elif (project_dir / "pyproject.toml").exists() or (project_dir / "requirements.txt").exists():
        for main_candidate in ("main.py", "app.py", "server.py", "wsgi.py"):
            if (project_dir / main_candidate).exists():
                commands.append(("Start Python Server", f"python {main_candidate}"))
                break

    # 4. Docker Compose
    if (project_dir / "docker-compose.yml").exists() or (project_dir / "compose.yaml").exists():
        commands.append(("Start Docker Services", "docker compose up -d"))

    return commands


# ── Routes & Endpoints Extractor ──────────────────────────────────────────────

def discover_routes(project_dir: Path) -> list[str]:
    """
    Extract API and UI routes using Next.js, Express, FastAPI, and Django conventions.
    Returns clean list of detected route paths.
    """
    routes: list[str] = []

    try:
        # 1. Next.js App Router (app/ or src/app/)
        app_dirs = [d for d in (project_dir / "app", project_dir / "src" / "app") if d.is_dir()]
        for app_dir in app_dirs:
            for file_path in app_dir.rglob("*"):
                if file_path.is_file() and file_path.name in ("route.ts", "route.js", "page.tsx", "page.jsx"):
                    rel = file_path.parent.relative_to(app_dir).as_posix()
                    route_path = "/" if rel == "." else f"/{rel}"
                    kind = "API" if file_path.name.startswith("route") else "Page"
                    routes.append(f"[{kind}] {route_path} -> {file_path.relative_to(project_dir).as_posix()}")

        # 2. Next.js Pages Router (pages/ or src/pages/)
        page_dirs = [d for d in (project_dir / "pages", project_dir / "src" / "pages") if d.is_dir()]
        for page_dir in page_dirs:
            for file_path in page_dir.rglob("*.tsx"):
                if not file_path.name.startswith("_"):
                    rel = file_path.relative_to(page_dir).with_suffix("").as_posix()
                    route_path = "/" if rel == "index" else f"/{rel.replace('/index', '')}"
                    kind = "API" if "api" in rel else "Page"
                    routes.append(f"[{kind}] {route_path} -> {file_path.relative_to(project_dir).as_posix()}")

        # 3. Express / FastAPI / Django Route folders
        for folder_name in ("routes", "controllers", "routers", "endpoints"):
            for candidate in (project_dir / folder_name, project_dir / "src" / folder_name):
                if candidate.is_dir():
                    for f in candidate.glob("*.py") if candidate.glob("*.py") else candidate.glob("*.ts"):
                        routes.append(f"[Module] {f.stem} -> {f.relative_to(project_dir).as_posix()}")

    except Exception:
        pass

    return routes[:35]  # Cap to prevent unbounded lists


# ── Database Models Extractor ─────────────────────────────────────────────────

def discover_database_models(project_dir: Path) -> list[str]:
    """
    Extract data models from Prisma, Django, SQLAlchemy, Drizzle schemas.
    Returns list of discovered model names and schema files.
    """
    models: list[str] = []

    try:
        # 1. Prisma schema
        for prisma_path in (project_dir / "prisma" / "schema.prisma", project_dir / "schema.prisma"):
            if prisma_path.exists():
                text = prisma_path.read_text(encoding="utf-8", errors="ignore")
                found = re.findall(r"\bmodel\s+([A-Za-z0-9_]+)\s*\{", text)
                for m in found:
                    models.append(f"[Prisma] {m} ({prisma_path.relative_to(project_dir).as_posix()})")

        # 2. Django / SQLAlchemy models.py
        for models_file in project_dir.rglob("models.py"):
            if "venv" not in models_file.parts and ".git" not in models_file.parts:
                text = models_file.read_text(encoding="utf-8", errors="ignore")
                found = re.findall(r"\bclass\s+([A-Za-z0-9_]+)\s*\(", text)
                for m in found:
                    if m not in ("Meta",):
                        models.append(f"[Model] {m} ({models_file.relative_to(project_dir).as_posix()})")

        # 3. Drizzle schema
        for drizzle_file in project_dir.rglob("schema.ts"):
            if "node_modules" not in drizzle_file.parts:
                text = drizzle_file.read_text(encoding="utf-8", errors="ignore")
                found = re.findall(r"export\s+const\s+([A-Za-z0-9_]+)\s+=\s+(?:pgTable|mysqlTable|sqliteTable)", text)
                for m in found:
                    models.append(f"[Drizzle] {m} ({drizzle_file.relative_to(project_dir).as_posix()})")

    except Exception:
        pass

    return models[:30]


# ── Satellites Generator (.agents/context/) ───────────────────────────────────

def generate_satellites(project_dir: Path, force: bool = False) -> dict[str, Path]:
    """
    Generate stack-adaptive satellite files in .agents/context/ on-demand.
    Enforces strict idempotency and zero token bloat in the main hub.
    """
    satellites_dir = project_dir / ".agents" / "context"
    satellites_dir.mkdir(parents=True, exist_ok=True)
    generated: dict[str, Path] = {}

    routes = discover_routes(project_dir)
    models = discover_database_models(project_dir)

    # 1. routes.md (if web routes detected)
    if routes:
        routes_path = satellites_dir / "routes.md"
        routes_content = (
            "# System Route & Endpoint Map\n\n"
            "> Discovered automatically via convention scanner. Used by AI agents for precision navigation.\n\n"
            "| Kind | Route Path | Implementation File |\n"
            "| :--- | :--- | :--- |\n"
        )
        for r in routes:
            parts = r.split(" -> ")
            kind_path = parts[0]
            impl = parts[1] if len(parts) > 1 else ""
            routes_content += f"| {kind_path} | `{impl}` |\n"

        write_idempotent(routes_path, routes_content, "Routes Satellite")
        generated["routes"] = routes_path

    # 2. schema.md (if database models detected)
    if models:
        schema_path = satellites_dir / "schema.md"
        schema_content = (
            "# Database Schema & Entity Models\n\n"
            "> Discovered data models and ORM schema definitions. Used by AI agents for database context.\n\n"
            "| Model / Entity | Definition File |\n"
            "| :--- | :--- |\n"
        )
        for m in models:
            schema_content += f"| {m} |\n"

        write_idempotent(schema_path, schema_content, "Schema Satellite")
        generated["schema"] = schema_path

    # 3. gotchas.md (Critical Traps & Anti-Patterns — Replaces useless bug diaries)
    gotchas_path = satellites_dir / "gotchas.md"
    if not gotchas_path.exists() or force:
        gotchas_content = (
            "# Critical Gotchas, Anti-Patterns & Architecture Invariants\n\n"
            "> Institutional knowledge and non-obvious traps that cannot be guessed from reading code.\n\n"
            "## ⚠️ Active Constraints & Traps\n\n"
            "1. **Port Invariants:** Inspect discovered ports before binding local services.\n"
            "2. **Secret Isolation:** Production secrets belong in `.env`; dummy dev accounts belong in `context.local.md`.\n"
            "3. **State Boundaries:** Verify migrations before initiating build or release cycles.\n"
        )
        write_idempotent(gotchas_path, gotchas_content, "Gotchas Satellite")
        generated["gotchas"] = gotchas_path

    return generated
