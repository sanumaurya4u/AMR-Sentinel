"""AST Import Isolation Test for AMR Sentinel Deterministic Rules Engine.

Ensures that services/api/app/engine/ never imports HTTP, DB, AI/LLM, or OS environment modules.
"""
import ast
from pathlib import Path

PROHIBITED_MODULES = {
    # Network / HTTP
    "requests", "httpx", "urllib", "aiohttp", "socket", "http",
    # AI / LLM SDKs
    "google", "google.genai", "openai", "anthropic", "langchain", "llama_index",
    # Database / ORM
    "sqlalchemy", "asyncpg", "psycopg2", "psycopg", "supabase", "sqlite3",
    # Process / Environment execution
    "subprocess",
}

ENGINE_DIR = Path(__file__).parent.parent / "app" / "engine"


def test_engine_directory_exists():
    """Verify that the engine directory exists."""
    assert ENGINE_DIR.exists() and ENGINE_DIR.is_dir()


def test_no_prohibited_imports_in_engine():
    """Inspect all Python AST nodes in app/engine to forbid external dependencies."""
    violations = []

    for py_file in ENGINE_DIR.glob("**/*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(py_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_pkg = alias.name.split(".")[0]
                    if root_pkg in PROHIBITED_MODULES or alias.name in PROHIBITED_MODULES:
                        violations.append((py_file.name, node.lineno, alias.name))

            elif isinstance(node, ast.ImportFrom) and node.module:
                root_pkg = node.module.split(".")[0]
                if root_pkg in PROHIBITED_MODULES or node.module in PROHIBITED_MODULES:
                    violations.append((py_file.name, node.lineno, node.module))

    assert not violations, f"Architectural Isolation Violation! Forbidden imports in engine: {violations}"
