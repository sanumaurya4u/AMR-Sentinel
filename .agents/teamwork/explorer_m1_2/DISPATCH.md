## 2026-11-09T20:58:14Z
From: 01b31f9d-d7a9-4fca-9bcc-706835e55498
Role: Evaluation Runner Specialist

You are explorer_m1_2 (role: Evaluation Runner Specialist).
Your working directory is: c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\explorer_m1_2\
Your parent orchestrator is conversation ID: 01b31f9d-d7a9-4fca-9bcc-706835e55498

MANDATORY FIRST STEP:
Read the authoritative user request at:
c:\Seva Sankalp Hackathon\AMR Sentinel\.agents\teamwork\ORIGINAL_REQUEST.md
and the project roadmap at:
c:\Seva Sankalp Hackathon\AMR Sentinel\PROJECT.md

TASK:
For Milestone 1 (Benchmark Test Split & Evaluation Harness):
1. Design the architecture and algorithms for the automated evaluation script (scripts/evaluate_agent.py) and pytest integration (services/api/tests/test_benchmark_evaluation.py).
2. Detail the exact metrics formulation:
   - Demographic field accuracy (age, gender, pregnancy, eGFR, allergies Jaccard/F1)
   - Indication code exact match accuracy
   - Medication extraction accuracy (Drug resolution Precision, Recall, F1 against canonical drug names)
   - Dose, Frequency, Duration match accuracy
   - Downstream clinical audit concordance (% of cases where extracted draft audited by DeterministicAuditEngine yields identical status to ground truth)
   - Safety-critical false negative rate (cases requiring URGENT_REVIEW mis-extracted as clean NO_RULE_TRIGGERED)
3. Detail how the script executes across:
   - Live Gemini cloud API mode (when GEMINI_API_KEY is configured)
   - Local offline fallback mode (when key is absent or offline)
   - Baseline recording mode: saving baseline metrics to services/api/tests/data/baseline_evaluation_results.json
4. Ensure the evaluation script outputs:
   - JSON summary file with structured scores
   - Markdown comparison table showing Baseline vs Enhanced scores
5. Provide complete code specification and step-by-step implementation guide for the worker.
