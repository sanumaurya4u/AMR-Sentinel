## 2026-11-09T20:44:17Z
You are explorer_survey_3 (role: Test Suites & Clinical Rules Spec Miner).
Your working directory is: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_3\
Your parent orchestrator is conversation ID: 01b31f9d-d7a9-4fca-9bcc-706835e55498

MANDATORY FIRST STEP:
Read the authoritative user request at:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md

TASK:
Conduct a thorough, read-only investigation of tests and clinical audit rules:
1. Examine all existing test suites in services/api/tests and scripts/test.ps1 (and any other test files).
2. Determine how tests are structured, how pytest is configured, what environment or dependencies are needed, and what tests currently exist.
3. Investigate the deterministic clinical rules engine (audit core):
   - What rules exist? (e.g., dosage limits, allergy checks, contraindicated drugs, drug interactions, pathogen-drug mismatches, AWaRe classification).
   - What contracts and safety boundaries guarantee that the deterministic core remains authoritative and cannot be bypassed or weakened by the AI agent?
4. Determine the requirements and specifications for an automated evaluation script:
   - What metrics should it compute? (e.g., field-level extraction accuracy, precision/recall/F1 on medications, dosages, frequencies, indication matching, clinical recommendation appropriateness).
   - How should baseline vs enhanced agent performance be compared and reported?
5. Identify any existing baseline test commands and verify that all criteria in R2, R3, and Acceptance Criteria can be tested cleanly.

RULES:
- Read-only: DO NOT modify any code or test files.
- Document all findings with exact file paths, line numbers, test names, and rule definitions.
- Write your complete handoff report to:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_3\handoff.md
- Update your progress in:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_survey_3\progress.md
- When done, send a message to your parent orchestrator (conversation ID: 01b31f9d-d7a9-4fca-9bcc-706835e55498) using send_message with a summary and confirmation of handoff.md.
