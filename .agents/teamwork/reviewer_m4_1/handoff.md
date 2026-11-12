# Handoff Report: Milestone 4 Independent Quality & Adversarial Review

## Review Summary

**Verdict**: **REQUEST_CHANGES**
**Overall Risk Assessment**: **MEDIUM-HIGH** (Flawed metric math and compound token over-extraction distort benchmark evaluation and baseline comparison).

---

## 1. Observation

### 1.1 Automated Verification Command Results
All automated quality gates were executed independently:

1. **Benchmark Evaluation Script Execution**:
   ```powershell
   .venv\Scripts\python.exe scripts/evaluate_agent.py --cases services/api/tests/data/benchmark_cases.json --compare-baseline
   ```
   **Observed Output**:
   ```
   ==================================================================
     AMR Sentinel AI — Benchmark Evaluation Runner
     Cases: services\api\tests\data\benchmark_cases.json
   ==================================================================
   [ExtractionAdapter] Cloud extraction failed, falling back to local heuristics: Gemini API returned status 404

   --- Summary Metrics ---
   Total Cases: 30
   Age Accuracy:        100.0%
   Gender Accuracy:     90.0%
   Pregnancy Accuracy:  93.33%
   eGFR Accuracy:       100.0%
   Drug Precision:      97.06%
   Drug Recall:         110.0%
   Drug F1 Score:       103.12%
   Indication Accuracy: 93.33%
   Audit Concordance:   96.67%
   Rule Jaccard:        95.0%

   >> OVERALL QUALITY SCORE: 96.64 / 100 <<

   ==================================================================
     BASELINE COMPARISON REPORT (Pre-Enhancement vs Post-Enhancement)
   ==================================================================
   Metric                         Baseline        Current         Delta          
   ---------------------------------------------------------------------------
   Age Accuracy                   96.67%          100.0%          +3.33%         
   Gender Accuracy                100.0%          90.0%           -10.0%         
   Pregnancy Accuracy             93.33%          93.33%          0.0%           
   eGFR Accuracy                  100.0%          100.0%          0.0%           
   Drug Precision                 100.0%          97.06%          -2.94%         
   Drug Recall                    100.0%          110.0%          +10.0%         
   Drug F1 Score                  100.0%          103.12%         +3.12%         
   Indication Accuracy            23.33%          93.33%          +70.0%         
   Audit Status Concordance       60.0%           96.67%          +36.67%        
   Mean Rule Jaccard              58.33%          95.0%           +36.67%        
   ---------------------------------------------------------------------------
   OVERALL QUALITY SCORE          81.9%           96.64%          +14.74%        
   ==================================================================
   ```

2. **Ruff Linter**:
   ```powershell
   .venv\Scripts\ruff.exe check services/api
   ```
   **Observed Output**: `All checks passed!`

3. **Pytest Suite**:
   ```powershell
   $env:PYTHONPATH = "services/api"; .venv\Scripts\pytest.exe services/api/tests -v
   ```
   **Observed Output**: `47 passed, 1 warning in 5.48s` (24 existing tests + 23 new benchmark tests).

4. **Quality Gates Script (`scripts/test.ps1`)**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/test.ps1
   ```
   **Observed Output**:
   - `[1/4] Running Ruff linter... All checks passed!`
   - `[2/4] Running AST Isolation & Pytest Suite... 47 passed, 1 warning in 5.82s`
   - `[3/4] Running TypeScript Strict Type-Check... tsc --noEmit (0 errors)`
   - `All Quality Gates Passed Successfully!`

---

## 2. Findings

### [Critical] Finding 1: Mathematically Impossible Metric Calculation (Drug Recall = 110.0%, Drug F1 = 103.12%)
- **What**: The evaluation script reports `Drug Recall: 110.0%` and `Drug F1 Score: 103.12%`. In probability, statistics, and machine learning, precision, recall, and F1 are strictly bounded in the closed interval $[0.0, 1.0]$ ($0\% \text{ to } 100\%$). A recall $> 100\%$ violates mathematical invariants.
- **Where**: `scripts/evaluate_agent.py`, lines 21–35 (`compute_token_f1`), and lines 114–116 (`all_pred_drugs.extend(ext_drugs)`).
- **Why**:
  In `scripts/evaluate_agent.py`:
  ```python
  def compute_token_f1(pred_tokens: list[str], truth_tokens: list[str]) -> tuple[float, float, float]:
      p_set = [t.lower().strip() for t in pred_tokens if t]
      t_set = [t.lower().strip() for t in truth_tokens if t]
      ...
      tp = sum(1 for p in p_set if p in t_set)
      precision = tp / len(p_set) if p_set else 0.0
      recall = tp / len(t_set) if t_set else 0.0
      f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
      return precision, recall, f1
  ```
  `all_pred_drugs` flattens all predictions across all 30 cases into one 34-element list, and `all_truth_drugs` flattens all ground-truth drugs into one 30-element list.
  The expression `tp = sum(1 for p in p_set if p in t_set)` performs a Python `in` membership check on the list `t_set`. It does not perform multiset intersection or consume matched ground-truth tokens. Because `p in t_set` is `True` for any drug that appears *anywhere* in the 30 ground truth cases, duplicate predictions or extra predictions repeatedly count as true positives.
  With 34 predictions, 33 matched some drug in `t_set`, resulting in $TP = 33$.
  Since $|t\_set| = 30$, $Recall = 33 / 30 = 1.10 = 110.0\%$, and $F1 = 1.03125 = 103.12\%$.

- **Forensic Impact on Baseline Data**:
  When evaluating `baseline_evaluation_results.json`, 17 out of 30 cases had WRONG drug predictions (defaulting to `Amoxicillin` when truth was `Doxycycline`, `Nitrofurantoin`, `Amikacin`, `Paracetamol`, etc.). However, because "Amoxicillin" was present in `t_set` from other cases, ALL 17 wrong predictions evaluated `p in t_set == True`. Consequently, the baseline falsely reported **100.0% Drug Precision, 100.0% Drug Recall, and 100.0% Drug F1** despite being wrong on 17/30 cases! (Actual baseline macro F1 was only 43.33%).
- **Suggestion**:
  1. In `scripts/evaluate_agent.py`, calculate drug precision, recall, and F1 using `collections.Counter` multiset intersection or per-case macro averaging:
     ```python
     from collections import Counter
     p_counts = Counter(t.lower().strip() for t in pred_tokens if t)
     t_counts = Counter(t.lower().strip() for t in truth_tokens if t)
     tp = sum((p_counts & t_counts).values())
     precision = tp / sum(p_counts.values()) if p_counts else 0.0
     recall = tp / sum(t_counts.values()) if t_counts else 0.0
     f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
     ```
  2. Re-record `services/api/tests/data/baseline_evaluation_results.json` with the mathematically valid calculation so the comparative delta report reflects reality (Baseline Macro F1: ~43.3% vs Current: ~96.1%).

---

### [Major] Finding 2: Compound FDC Substring Over-Extraction in `ExtractionAdapter`
- **What**: In fixed-dose combination (FDC) prescriptions, `ExtractionAdapter._extract_with_local_heuristics` extracts the compound drug AND duplicate individual component drugs, tripling the prescription line count.
- **Where**: `services/api/app/extraction/adapter.py`, lines 319–364 (`BRAND_MAPPINGS` scanning loop).
- **Why**:
  In `adapter.py`:
  - `BENCH_15` ("Tab Cefixime + Azithromycin 200mg+250mg"): Extracts `['Cefixime + Azithromycin', 'Azithromycin', 'Cefixime']` (3 drugs instead of 1).
  - `BENCH_16` ("Tab Ofloxacin + Ornidazole 200mg+500mg"): Extracts `['Ofloxacin + Ornidazole', 'Ofloxacin']` (2 drugs instead of 1).
  - `BENCH_17` ("Cap Amoxicillin + Flucloxacillin 500mg+500mg"): Extracts `['Amoxicillin + Flucloxacillin', 'Amoxicillin']` (2 drugs instead of 1).
  When a multi-word compound is matched, the matched string is not masked or consumed. As the loop continues iterating down `BRAND_MAPPINGS`, single tokens like `azithromycin`, `cefixime`, `ofloxacin`, and `amoxicillin` match again against the same text, creating spurious extra prescription lines.
- **Suggestion**:
  When a brand/generic token is matched in `lowered`, mask out the matched substring so sub-tokens are not matched again:
  ```python
  if token in lowered:
      if generic not in matched_drugs_seen:
          matched_drugs_seen.add(generic)
          lowered = lowered.replace(token, " " * len(token))
          ...
  ```
  This immediately eliminates the duplicate lines for BENCH_15, 16, and 17, producing exact 1:1 drug extractions across all 30 benchmark cases.

---

### [Minor] Finding 3: Incomplete Unit Test Assertions for `compute_token_f1`
- **What**: `services/api/tests/test_benchmark_evaluation.py` lines 151–204 includes 5 unit tests for `compute_token_f1`, but all test fixtures utilize balanced lists without duplicates, failing to catch the multiset bug.
- **Where**: `services/api/tests/test_benchmark_evaluation.py`, lines 171–179.
- **Why**:
  Testing `pred = ["Amoxicillin", "Clavulanate"]` vs `truth = ["Amoxicillin", "Paracetamol"]` yields $P=0.5, R=0.5, F1=0.5$ under both the buggy and correct formulations. Adding a test for `pred = ["Amoxicillin", "Amoxicillin"]` vs `truth = ["Amoxicillin"]` exposes the bug immediately (asserting $P=0.5, R=1.0, F1 \le 1.0$).
- **Suggestion**:
  Add a unit test in `test_benchmark_evaluation.py` explicitly asserting that duplicate predictions never yield $R > 1.0$ or $F1 > 1.0$.

---

## 3. Adversarial Stress-Test & Integrity Check

### 3.1 Integrity Violation Audit
- **Hardcoded test results in source code**: **PASS / NO VIOLATION DETECTED**.
  - Inspected `ExtractionAdapter`: uses generalized regex, token extraction, and clinical dictionary lookups. No hardcoded case IDs (`BENCH_01`, etc.) or input-to-output maps found in `adapter.py`.
- **Dummy or facade implementations**: **PASS / NO VIOLATION DETECTED**.
  - `AMRKnowledgeService` loads real CSVs (`guidelines.csv`, `who_aware_antibiotics.csv`, `icmr_surveillance_pages.csv`).
  - AST isolation in `services/api/app/engine/` is authentic (0 prohibited network/AI imports).
- **Fabricated verification outputs or logs**: **PASS / NO VIOLATION DETECTED**.
  - All test commands, pytest runs, and lint commands were executed independently in terminal; outputs matched worker claims.
- **Self-certifying work without genuine independent verification**: **REQUEST CHANGES**.
  - The worker attested that benchmark evaluation passed and met baseline, but accepted `Drug Recall: 110.0%` and `Drug F1 Score: 103.12%` without questioning mathematical validity.

### 3.2 Adversarial Attack Scenarios Tested

| Scenario | Input Tested | Predicted Behavior | Actual Behavior | Result |
|---|---|---|---|---|
| **Duplicate Prediction Inflation** | `compute_token_f1(["Amoxicillin"] * 5, ["Amoxicillin"])` | $P \le 1.0, R \le 1.0, F1 \le 1.0$ | $P=1.0, R=5.0, F1=1.666$ | **FAIL (Exceeds upper bound)** |
| **Compound Substring Overlap** | `"Tab Cefixime + Azithromycin 200mg+250mg"` | 1 line: `Cefixime + Azithromycin` | 3 lines: `['Cefixime + Azithromycin', 'Azithromycin', 'Cefixime']` | **FAIL (Over-extracted)** |
| **Deterministic Engine AST Isolation** | AST parse of all `.py` files in `app/engine/` | 0 AI/network imports | 0 prohibited imports found | **PASS** |
| **Pediatric Contraindication Gate** | `BENCH_01` (8yo child + Ciprofloxacin) | Status: `NEEDS_URGENT_REVIEW` | Status: `NEEDS_URGENT_REVIEW` | **PASS** |
| **Allergy Gate** | `BENCH_12` (Penicillin allergy + Amoxicillin) | Status: `NEEDS_URGENT_REVIEW` | Status: `NEEDS_URGENT_REVIEW` | **PASS** |
| **False Negative Urgent Invariant** | All 8 `NEEDS_URGENT_REVIEW` cases | 0 cases downgrade to `NO_RULE_TRIGGERED` | 0 cases downgrade | **PASS** |

---

## 4. Logic Chain

1. **Premise 1**: Metric evaluations must adhere to the definitions of mathematical statistics. Precision $P = TP / (TP + FP)$, Recall $R = TP / (TP + FN)$, and F1 Score $2PR / (P + R)$ are bounded in $[0.0, 1.0]$.
2. **Observation**: `scripts/evaluate_agent.py` outputs `Drug Recall: 110.0%` and `Drug F1 Score: 103.12%`.
3. **Trace**: `tp = sum(1 for p in p_set if p in t_set)` treats `t_set` as a lookup list rather than a multiset. Because `all_pred_drugs` has 34 elements (due to Finding 2) and `all_truth_drugs` has 30 elements, $TP$ was calculated as 33, exceeding $|t\_set| = 30$.
4. **Impact**: This bug masked baseline performance (crediting baseline with 100% Drug F1 when 17/30 cases were wrong) and generated an invalid comparative evaluation report.
5. **Conclusion**: Milestone 4 cannot be approved until `compute_token_f1` is replaced with valid multiset overlap, compound token over-extraction in `adapter.py` is resolved, and baseline comparison numbers are re-recorded accurately.

---

## 5. Caveats

- The Two-Layer Safety Architecture and AST isolation in `services/api/app/engine/` are fully verified and intact.
- The 47 tests in pytest and `scripts/test.ps1` pass with 100% success.
- The extraction quality on demographic fields (`age_accuracy: 100%`, `pregnancy_accuracy: 93.3%`, `egfr_accuracy: 100%`) and indication classification (`93.33%`) are genuinely strong and verified.
- The issue is isolated to metric calculation math in `scripts/evaluate_agent.py`, compound token masking in `adapter.py`, and the resulting baseline artifact.

---

## 6. Conclusion & Required Actions

**Verdict**: **REQUEST_CHANGES**

### Required Remediations for Worker:
1. **Fix `compute_token_f1` in `scripts/evaluate_agent.py`**:
   Use `collections.Counter(p_set) & collections.Counter(t_set)` so true positives are bounded by ground truth length, ensuring $P, R, F1 \in [0.0, 1.0]$.
2. **Fix compound token extraction in `ExtractionAdapter`**:
   In `services/api/app/extraction/adapter.py`, mask out matched tokens (`lowered = lowered.replace(token, ' ' * len(token))`) so compound drugs like `Cefixime + Azithromycin` do not generate duplicate `Azithromycin` and `Cefixime` lines.
3. **Add Boundary Test in `services/api/tests/test_benchmark_evaluation.py`**:
   Add a test asserting that duplicate prediction tokens never produce $R > 1.0$ or $F1 > 1.0$.
4. **Re-record Baseline & Run Evaluation**:
   Re-record baseline results (`--record-baseline`) with the corrected metric calculation and re-run comparison to display authentic, mathematically valid precision, recall, and F1 scores.

---

## 7. Verification Method

Once changes are applied:
1. Run evaluation script:
   ```powershell
   .venv\Scripts\python.exe scripts/evaluate_agent.py --cases services/api/tests/data/benchmark_cases.json --compare-baseline
   ```
   *Expected Outcome*: Drug Recall $\le 100.0\%$, Drug F1 $\le 100.0\%$, Drug Precision $\le 100.0\%$, with 0 spurious extra drugs.
2. Run pytest suite:
   ```powershell
   $env:PYTHONPATH = "services/api"; .venv\Scripts\pytest.exe services/api/tests -v
   ```
   *Expected Outcome*: All 47+ tests pass.
3. Run project quality gates:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/test.ps1
   ```
   *Expected Outcome*: Exit code 0, all gates pass cleanly.
