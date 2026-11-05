"""AMR Sentinel Pure Python Deterministic Rules Engine.

CRITICAL ARCHITECTURAL CONSTRAINTS:
1. Zero network imports (no requests, httpx, aiohttp, urllib, socket).
2. Zero database/ORM imports (no sqlalchemy, psycopg, supabase).
3. Zero LLM / AI SDK imports (no google.genai, openai, anthropic, langchain).
4. Zero environment mutation or direct os.environ reads.
5. All calculations are pure, deterministic functions of confirmed input models.
"""
