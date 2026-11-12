## 2026-11-09T20:58:31Z
You are spec_miner_m1_3 (role: Test Infra & Pytest Integration Specialist).
Your working directory is: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\spec_miner_m1_3\
Your parent orchestrator is conversation ID: 01b31f9d-d7a9-4fca-9bcc-706835e55498

MANDATORY FIRST STEP:
Read the authoritative user request at:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md
and the project roadmap at:
c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md

TASK:
For Milestone 1 (Benchmark Test Split & Evaluation Harness):
1. Design the Test Infrastructure specification (to be recorded in TEST_INFRA.md at project root) using the 4-tier methodology:
   - Tier 1: Feature Coverage (>=5 per feature)
   - Tier 2: Boundary & Corner Cases (>=5 per feature)
   - Tier 3: Cross-Feature Combinations (pairwise interactions)
   - Tier 4: Real-World Clinical Application Scenarios
2. Design pytest integration in services/api/tests/test_benchmark_evaluation.py:
   - Must run cleanly under pytest services/api/tests -v
   - Must not violate test_architecture_isolation.py (zero prohibited imports)
   - Must pass under scripts/test.ps1 without breaking any existing test
3. Define the TEST_READY.md specification to be published once the test runner and benchmark cases are implemented and baseline recorded.
4. Provide the exact implementation specification and file contents for the worker.

RULES:
- Read-only: DO NOT modify any code or test files.
- Write your complete handoff report to:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\spec_miner_m1_3\handoff.md
- Update progress.md in your working directory.
- When done, send a message to conversation ID 01b31f9d-d7a9-4fca-9bcc-706835e55498 using send_message.
