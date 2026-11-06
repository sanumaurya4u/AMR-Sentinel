import os
import subprocess
import shutil
import pymupdf

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AMR Sentinel AI - Clinician & Practitioner Operational Manual</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 7mm 9mm 7mm 9mm;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: #0f172a;
      background: #ffffff;
      line-height: 1.40;
      font-size: 9.6pt;
    }

    .page {
      page-break-after: always;
      break-after: page;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 283mm;
      max-height: 283mm;
      overflow: hidden;
      padding: 0;
      position: relative;
    }

    .page:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }

    /* Header styling */
    .page-header {
      border-bottom: 2.5px solid #0d9488;
      padding-bottom: 4px;
      margin-bottom: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }

    .header-logo-group {
      display: flex;
      align-items: center;
      gap: 9px;
    }

    .logo-svg {
      width: 30px;
      height: 30px;
      fill: #0d9488;
      flex-shrink: 0;
    }

    .header-titles h1 {
      font-size: 13.5pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.3px;
      line-height: 1.15;
    }

    .header-titles p {
      font-size: 7.6pt;
      color: #64748b;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .header-meta {
      text-align: right;
    }

    .header-badge {
      display: inline-block;
      background: #f0fdfa;
      border: 1.5px solid #99f6e4;
      color: #0f766e;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 7.6pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .header-submeta {
      font-size: 7pt;
      color: #64748b;
      margin-top: 1px;
      font-weight: 600;
    }

    /* Footer styling */
    .page-footer {
      border-top: 1.5px solid #cbd5e1;
      padding-top: 4px;
      margin-top: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.5pt;
      color: #475569;
      flex-shrink: 0;
    }

    .page-footer .lead-text {
      font-weight: 800;
      color: #0f766e;
    }

    /* Main page body */
    .page-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
      justify-content: space-between;
    }

    /* Section Headings */
    h2 {
      font-size: 11pt;
      font-weight: 800;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 6px;
      border-left: 3.5px solid #0d9488;
      padding-left: 7px;
      margin-top: 1px;
      margin-bottom: 2px;
      letter-spacing: -0.2px;
    }

    h3 {
      font-size: 9.8pt;
      font-weight: 800;
      color: #1e293b;
      margin-bottom: 1px;
    }

    p {
      color: #334155;
      font-size: 9.1pt;
      line-height: 1.36;
    }

    /* Hero Banner for Page 1 */
    .hero-box {
      background: linear-gradient(135deg, #042f2e 0%, #0f766e 100%);
      color: #ffffff;
      padding: 9px 12px;
      border-radius: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1px;
      border: 1px solid #115e59;
    }

    .hero-content h1 {
      font-size: 14.5pt;
      font-weight: 900;
      letter-spacing: -0.4px;
      line-height: 1.15;
      margin-bottom: 2px;
    }

    .hero-content p {
      color: #ccfbf1;
      font-size: 8.8pt;
      line-height: 1.32;
      max-width: 530px;
    }

    .hero-badges {
      display: flex;
      flex-direction: column;
      gap: 3px;
      align-items: flex-end;
    }

    .hero-tag {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.35);
      color: #ffffff;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 7.2pt;
      font-weight: 700;
      white-space: nowrap;
    }

    /* Cards & Grids */
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }

    .card {
      border: 1.2px solid #cbd5e1;
      background: #ffffff;
      border-radius: 5px;
      padding: 6px 9px;
    }

    .card-accent {
      background: #f8fafc;
      border-color: #cbd5e1;
    }

    .card-title {
      font-size: 9.2pt;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    /* Architecture Box */
    .arch-container {
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-radius: 5px;
      padding: 6px 9px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .arch-step {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 4px 8px;
    }

    .arch-step.layer-1 { border-left: 4px solid #0284c7; }
    .arch-step.layer-2 { border-left: 4px solid #0d9488; }
    .arch-step.layer-3 { border-left: 4px solid #7c3aed; }

    .arch-pill {
      display: inline-block;
      font-size: 6.8pt;
      font-weight: 800;
      padding: 1.5px 6px;
      border-radius: 3px;
      text-transform: uppercase;
      margin-bottom: 1px;
    }

    .pill-blue { background: #e0f2fe; color: #0369a1; }
    .pill-teal { background: #ccfbf1; color: #0f766e; }
    .pill-purple { background: #f3e8ff; color: #6b21a8; }

    .connector-text {
      text-align: center;
      font-size: 7.5pt;
      font-weight: 800;
      color: #0d9488;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      margin: 1px 0;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8.4pt;
      margin-top: 1px;
    }

    th {
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 800;
      text-align: left;
      padding: 4px 6px;
      border: 1px solid #cbd5e1;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    td {
      padding: 3.5px 6px;
      border: 1px solid #e2e8f0;
      color: #334155;
      vertical-align: top;
      line-height: 1.32;
    }

    tr:nth-child(even) td {
      background: #f8fafc;
    }

    /* Flowchart styles on Page 2 */
    .flowchart-svg-wrap {
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-radius: 5px;
      padding: 4px;
      text-align: center;
    }

    /* Steps list */
    .step-card {
      display: flex;
      gap: 9px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 4px;
    }

    .step-card:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }

    .step-badge-num {
      background: #0f766e;
      color: #ffffff;
      font-size: 8.8pt;
      font-weight: 900;
      width: 23px;
      height: 23px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 1px;
      box-shadow: 0 1px 3px rgba(15, 118, 110, 0.3);
    }

    .step-text-wrap {
      flex: 1;
    }

    .step-top {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 1px;
    }

    .step-name {
      font-size: 9.5pt;
      font-weight: 800;
      color: #0f172a;
    }

    .step-tag {
      font-size: 7.2pt;
      background: #f0fdfa;
      border: 1px solid #99f6e4;
      color: #0f766e;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
    }

    .pearl-box {
      background: #f0fdf4;
      border-left: 3.5px solid #16a34a;
      padding: 3px 7px;
      margin-top: 2px;
      border-radius: 0 4px 4px 0;
      font-size: 8pt;
      color: #14532d;
      line-height: 1.32;
    }

    .warning-box {
      background: #fffbeb;
      border-left: 3.5px solid #d97706;
      padding: 3px 7px;
      margin-top: 2px;
      border-radius: 0 4px 4px 0;
      font-size: 8pt;
      color: #78350f;
      line-height: 1.32;
    }

    /* Triage styles on Page 3 */
    .triage-box {
      border-radius: 5px;
      padding: 6px 10px;
      border: 1.5px solid transparent;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .triage-red {
      background: #fef2f2;
      border-color: #fecaca;
      border-left: 5px solid #dc2626;
    }

    .triage-amber {
      background: #fffbeb;
      border-color: #fde68a;
      border-left: 5px solid #d97706;
    }

    .triage-green {
      background: #f0fdf4;
      border-color: #bbf7d0;
      border-left: 5px solid #16a34a;
    }

    .triage-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .triage-head strong {
      font-size: 9.8pt;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .triage-red strong { color: #991b1b; }
    .triage-amber strong { color: #92400e; }
    .triage-green strong { color: #14532d; }

    .triage-action-pill {
      font-size: 7.2pt;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 3px;
    }

    .triage-red .triage-action-pill { background: #fee2e2; color: #b91c1c; }
    .triage-amber .triage-action-pill { background: #fef3c7; color: #b45309; }
    .triage-green .triage-action-pill { background: #dcfce7; color: #15803d; }

    /* Finding card mockup */
    .mock-finding {
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-radius: 5px;
      padding: 6px 9px;
    }

    .mock-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #f1f5f9;
      padding-bottom: 3px;
      margin-bottom: 3px;
    }

    .mock-id {
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 7.6pt;
      background: #f1f5f9;
      color: #334155;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 700;
    }

    .mock-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 8px;
    }

    .mock-discuss {
      background: #f0fdfa;
      border: 1.2px dashed #0d9488;
      border-radius: 4px;
      padding: 3px 7px;
      margin-top: 3px;
    }

    .mock-discuss span {
      font-size: 7.2pt;
      font-weight: 800;
      color: #0f766e;
      text-transform: uppercase;
    }

    .mock-sidebar {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 4px 6px;
    }

    /* Badges & Pills */
    .pill-access { background: #dcfce7; color: #15803d; font-weight: 800; padding: 1.5px 6px; border-radius: 3px; display: inline-block; font-size: 7.4pt; }
    .pill-watch { background: #fef3c7; color: #b45309; font-weight: 800; padding: 1.5px 6px; border-radius: 3px; display: inline-block; font-size: 7.4pt; }
    .pill-reserve { background: #fee2e2; color: #b91c1c; font-weight: 800; padding: 1.5px 6px; border-radius: 3px; display: inline-block; font-size: 7.4pt; }

    .check-list {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .check-row {
      display: flex;
      align-items: flex-start;
      gap: 5px;
      font-size: 8.6pt;
      line-height: 1.32;
    }

    .check-icon {
      color: #0d9488;
      font-weight: 900;
      font-size: 9.5pt;
      margin-top: -1px;
    }

    /* Slip Mockup Box on Page 4 */
    .slip-box {
      border: 1.5px dashed #0d9488;
      background: #f0fdfa;
      border-radius: 5px;
      padding: 6px 9px;
    }
  </style>
</head>
<body>

  <!-- ==================== PAGE 1: OVERVIEW & SAFETY BOUNDARY ==================== -->
  <div class="page">
    <div class="page-header">
      <div class="header-logo-group">
        <svg class="logo-svg" viewBox="0 0 24 24">
          <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/>
        </svg>
        <div class="header-titles">
          <h1>AMR SENTINEL AI &bull; CLINICIAN OPERATIONAL MANUAL</h1>
          <p>CLINICAL DECISION SUPPORT &amp; ANTIMICROBIAL STEWARDSHIP AUDIT SYSTEM</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="header-badge">Clinical Edition 2.0</div>
        <div class="header-submeta">ICMR STG 2022 &bull; WHO AWaRe 2023 &bull; CDSCO</div>
      </div>
    </div>

    <div class="page-body">
      <!-- Hero Banner -->
      <div class="hero-box">
        <div class="hero-content">
          <h1>Prescriber Safety &amp; Stewardship Handbook</h1>
          <p>A bedside operational reference for practicing physicians, resident medical officers, and clinical pharmacists to enforce guideline-concordant antimicrobial therapy, eliminate toxic drug interactions, and combat superbug resistance.</p>
        </div>
        <div class="hero-badges">
          <span class="hero-tag">&#x2714; Zero LLM Hallucinations</span>
          <span class="hero-tag">&#x2714; 100% Deterministic Rules</span>
          <span class="hero-tag">&#x2714; Preserves Prescriber Autonomy</span>
        </div>
      </div>

      <!-- Core Operating Principles -->
      <h2>1. The Five Foundational Clinical Safeguards</h2>
      <div class="grid-2">
        <div class="card card-accent">
          <div class="card-title"><span>🛡️</span> 1. Absolute Preservation of Autonomy</div>
          <p>AMR Sentinel AI is strictly an <strong>assistive second-check</strong>. It <em>never</em> diagnoses illnesses, <em>never</em> calculates definitive doses, and <em>never</em> autonomously alters or cancels orders. All therapeutic authority rests solely with the treating clinician.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>⚙️</span> 2. Deterministic, Zero-Hallucination Core</div>
          <p>Clinical auditing executes on <strong>pure, frozen algorithmic rules</strong> with zero probabilistic guessing. Given identical confirmed patient physiological parameters, it executes identical safety checks every single time with 100% mathematical reproducibility.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>⚠️</span> 3. "No Rule Triggered" &ne; "Safe or Approved"</div>
          <p>A green triage status indicates that your prescription does not breach configured national safety gates. It does <em>not</em> constitute a medical endorsement of efficacy or safety. Clinical correlation and bedside judgment remain mandatory.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>🔍</span> 4. Zero False-Normal Assumptions</div>
          <p>When patient data is omitted (such as unrecorded eGFR or unconfirmed pregnancy), the platform <strong>never assumes normal values</strong>. It actively flags an explicit <em>Clinical Data Gap</em> to mandate baseline laboratory verification.</p>
        </div>
      </div>

      <!-- Two Layer Architecture -->
      <h2>2. Clinical Safety Architecture: Two-Layer Model</h2>
      <div class="arch-container">
        <div class="arch-step layer-1">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="arch-pill pill-blue">Layer 1: Assistive Intake (Untrusted)</span>
            <span style="font-size:7pt; color:#64748b; font-weight:700;">Optical OCR / Digital Form Ingestion</span>
          </div>
          <p style="font-size:8.4pt; margin-top:1px;">Extracts patient demographics, eGFR, pregnancy status, and antimicrobial orders from digital entries or scanned slips. Attaches confidence markers. <strong>Safety Lock:</strong> AI outputs remain completely inactive until verified by a physician.</p>
        </div>

        <div class="connector-text">
          <span>&#x25BC;</span> Mandatory Human Clinician Affirmation &amp; Signature <span>&#x25BC;</span>
        </div>

        <div class="arch-step layer-2">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="arch-pill pill-teal">Layer 2: Deterministic Clinical Audit Engine</span>
            <span style="font-size:7pt; color:#0f766e; font-weight:700;">Five-Tier Pure Guideline Core</span>
          </div>
          <p style="font-size:8.4pt; margin-top:1px;">Evaluates confirmed inputs across: <strong>Tier 1:</strong> Absolute Contraindications (Age, Pregnancy, Renal); <strong>Tier 2:</strong> CDSCO Banned Fixed-Dose Combinations; <strong>Tier 3:</strong> Indication Legitimacy (Viral Syndromes); <strong>Tier 4:</strong> WHO AWaRe Spectrum Optimization; <strong>Tier 5:</strong> Treatment Duration Limits.</p>
        </div>

        <div class="arch-step layer-3">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="arch-pill pill-purple">Layer 3: Clinical Decision Support Output</span>
            <span style="font-size:7pt; color:#6b21a8; font-weight:700;">Actionable Triage, Citations &amp; Audit Slip</span>
          </div>
          <p style="font-size:8.4pt; margin-top:1px;">Provides immediate traffic-light triage, evidence citations with ICMR chapter/table references, non-prescriptive discussion options, and an immutable audit trail for hospital pharmacy clearance.</p>
        </div>
      </div>

      <!-- Scope of Practice Table -->
      <h2>3. Covered Clinical Infection Syndromes &amp; Guidelines Matrix</h2>
      <table>
        <thead>
          <tr>
            <th style="width:23%;">Clinical Syndrome</th>
            <th style="width:27%;">ICMR STG 2022 Reference</th>
            <th style="width:24%;">Target Pathogens</th>
            <th style="width:26%;">Stewardship Focus</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Community Pneumonia (CAP)</strong></td>
            <td>Chapter 2: Adult Respiratory Infections</td>
            <td><em>S. pneumoniae, H. influenzae</em></td>
            <td>Access oral Amoxicillin first-line; restrict Watch macrolides.</td>
          </tr>
          <tr>
            <td><strong>Uncomplicated Lower UTI</strong></td>
            <td>Chapter 6: Genitourinary Infections</td>
            <td><em>E. coli, Klebsiella spp.</em></td>
            <td>Nitrofurantoin (eGFR &ge; 30) or Fosfomycin; avoid Ciprofloxacin.</td>
          </tr>
          <tr>
            <td><strong>Viral Bronchitis / Cold</strong></td>
            <td>Chapter 1: Upper Respiratory Tract</td>
            <td>Respiratory viruses (>95%)</td>
            <td>Withhold antibiotics; supportive hydration &amp; antipyretics.</td>
          </tr>
          <tr>
            <td><strong>Skin &amp; Soft Tissue (SSTI)</strong></td>
            <td>Chapter 8: Dermatology Infections</td>
            <td><em>S. aureus, S. pyogenes</em></td>
            <td>Narrow-spectrum Cefalexin; avoid broad carbapenems.</td>
          </tr>
          <tr>
            <td><strong>Acute Watery Diarrhea</strong></td>
            <td>Chapter 4: Gastrointestinal Illness</td>
            <td>Rotavirus, Norovirus, non-cholera</td>
            <td>Oral Rehydration (ORS) + Zinc; withhold Fluoroquinolones.</td>
          </tr>
        </tbody>
      </table>

      <!-- Bottom AMS Committee Box -->
      <div class="card card-accent" style="margin-top:1px;">
        <div class="card-title"><span>🏛️</span> Hospital Stewardship Committee Policy Alignment</div>
        <p style="font-size:8.2pt;">This platform complies with the <strong>National Action Plan on AMR (NAP-AMR)</strong>. Medical Superintendents and HODs receive de-identified ward-level analytics to maintain hospital accreditation standards and optimize local antibiotic procurement.</p>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Clinician Practice Manual</span>
      <span>National Health Safety Architecture &bull; Non-Prescriptive CDS</span>
      <span>Page 1 of 5</span>
    </div>
  </div>

  <!-- ==================== PAGE 2: WORKFLOW & ALGORITHM ==================== -->
  <div class="page">
    <div class="page-header">
      <div class="header-logo-group">
        <svg class="logo-svg" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
        <div class="header-titles">
          <h1>CLINICAL WORKFLOW &amp; ALGORITHM</h1>
          <p>STANDARDIZED STEP-BY-STEP PROCESS FOR OUTPATIENT AND INPATIENT PRESCRIBING</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="header-badge">Clinical Workflow</div>
        <div class="header-submeta">Rapid 4-Step Verification</div>
      </div>
    </div>

    <div class="page-body">
      <!-- Full Visual SVG Flowchart -->
      <h2>1. The End-to-End Clinical Decision Pathway</h2>
      <div class="flowchart-svg-wrap">
        <svg width="100%" height="92" viewBox="0 0 760 92" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Step 1 Box -->
          <rect x="5" y="5" width="130" height="80" rx="5" fill="#FFFFFF" stroke="#0D9488" stroke-width="1.8"/>
          <circle cx="70" cy="20" r="10" fill="#CCFBF1"/>
          <text x="70" y="24" font-size="10" font-weight="900" fill="#0F766E" text-anchor="middle">1</text>
          <text x="70" y="42" font-size="9" font-weight="800" fill="#0F172A" text-anchor="middle">Patient Profile</text>
          <text x="70" y="56" font-size="7.8" fill="#64748B" text-anchor="middle">Age, eGFR, Pregnancy</text>
          <text x="70" y="70" font-size="7.4" font-weight="700" fill="#0D9488" text-anchor="middle">Allergy Check</text>

          <!-- Arrow 1 -->
          <path d="M140 45 H160" stroke="#0D9488" stroke-width="2"/>

          <!-- Step 2 Box -->
          <rect x="165" y="5" width="130" height="80" rx="5" fill="#FFFFFF" stroke="#0D9488" stroke-width="1.8"/>
          <circle cx="230" cy="20" r="10" fill="#CCFBF1"/>
          <text x="230" y="24" font-size="10" font-weight="900" fill="#0F766E" text-anchor="middle">2</text>
          <text x="230" y="42" font-size="9" font-weight="800" fill="#0F172A" text-anchor="middle">Syndrome &amp; Setting</text>
          <text x="230" y="56" font-size="7.8" fill="#64748B" text-anchor="middle">Bacterial vs. Viral</text>
          <text x="230" y="70" font-size="7.4" font-weight="700" fill="#0D9488" text-anchor="middle">OPD vs. Inpatient Ward</text>

          <!-- Arrow 2 -->
          <path d="M300 45 H320" stroke="#0D9488" stroke-width="2"/>

          <!-- Step 3 Box -->
          <rect x="325" y="5" width="130" height="80" rx="5" fill="#FFFFFF" stroke="#0D9488" stroke-width="1.8"/>
          <circle cx="390" cy="20" r="10" fill="#CCFBF1"/>
          <text x="390" y="24" font-size="10" font-weight="900" fill="#0F766E" text-anchor="middle">3</text>
          <text x="390" y="42" font-size="9" font-weight="800" fill="#0F172A" text-anchor="middle">Regimen Entry</text>
          <text x="390" y="56" font-size="7.8" fill="#64748B" text-anchor="middle">Drug, Dose, Days</text>
          <text x="390" y="70" font-size="7.4" font-weight="700" fill="#0D9488" text-anchor="middle">Formulary / OCR Scan</text>

          <!-- Arrow 3 -->
          <path d="M460 45 H480" stroke="#0D9488" stroke-width="2"/>

          <!-- Step 4 Box -->
          <rect x="485" y="5" width="125" height="80" rx="5" fill="#F0FDFA" stroke="#0F766E" stroke-width="2"/>
          <circle cx="547" cy="20" r="10" fill="#0F766E"/>
          <text x="547" y="24" font-size="10" font-weight="900" fill="#FFFFFF" text-anchor="middle">4</text>
          <text x="547" y="42" font-size="9" font-weight="800" fill="#0F766E" text-anchor="middle">Doctor Sign-Off</text>
          <text x="547" y="56" font-size="7.8" fill="#334155" text-anchor="middle">Verify Draft Inputs</text>
          <text x="547" y="70" font-size="7.4" font-weight="700" fill="#0F766E" text-anchor="middle">Run 5-Tier Audit</text>

          <!-- Arrow 4 -->
          <path d="M615 45 H635" stroke="#0D9488" stroke-width="2"/>

          <!-- Result Box -->
          <rect x="640" y="5" width="115" height="80" rx="5" fill="#FFFFFF" stroke="#334155" stroke-width="1.8"/>
          <text x="697" y="22" font-size="8.8" font-weight="800" fill="#0F172A" text-anchor="middle">Audit Report</text>
          <rect x="648" y="28" width="98" height="15" rx="3" fill="#FEE2E2"/>
          <text x="697" y="39" font-size="7.4" font-weight="800" fill="#B91C1C" text-anchor="middle">&bull; Urgent Review</text>
          <rect x="648" y="45" width="98" height="15" rx="3" fill="#FEF3C7"/>
          <text x="697" y="56" font-size="7.4" font-weight="800" fill="#B45309" text-anchor="middle">&bull; Needs Review</text>
          <rect x="648" y="62" width="98" height="15" rx="3" fill="#DCFCE7"/>
          <text x="697" y="73" font-size="7.4" font-weight="800" fill="#15803D" text-anchor="middle">&bull; No Rule Triggered</text>
        </svg>
      </div>

      <!-- Detailed Prescriber Steps -->
      <h2>2. Detailed Step-by-Step Prescribing Guidance</h2>

      <div class="step-card">
        <div class="step-badge-num">1</div>
        <div class="step-text-wrap">
          <div class="step-top">
            <span class="step-name">Physiological Profiling &amp; Organ Clearance Assessment</span>
            <span class="step-tag">Step 1: Patient Context</span>
          </div>
          <p>Open <strong>New Audit</strong> (`/new-audit`). Enter patient biological age and gender. Toggle <em>"Pregnant / Gestational"</em> if applicable (triggers FDA &amp; ICMR teratogenicity warnings for Doxycycline, Fluoroquinolones, and Aminoglycosides). Enter calculated <strong>eGFR in mL/min/1.73m²</strong>.</p>
          <div class="pearl-box">
            <strong>Clinical Safety Pearl:</strong> Nitrofurantoin requires eGFR &ge; 30 mL/min for effective urinary concentration. Prescribing it below 30 mL/min leads to therapeutic failure and severe peripheral neurotoxicity.
          </div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-badge-num">2</div>
        <div class="step-text-wrap">
          <div class="step-top">
            <span class="step-name">Indication Categorization &amp; Clinical Setting</span>
            <span class="step-tag">Step 2: Diagnosis</span>
          </div>
          <p>Select working diagnosis from the clinical indication list. Differentiate between <strong>Bacterial Infections</strong> (e.g., Mild CAP, Acute Cystitis, Streptococcal Pharyngitis) and <strong>Self-Limiting / Viral Syndromes</strong> (e.g., Acute Bronchitis, Common Cold, Acute Watery Diarrhea). Choose setting: <em>Outpatient (OPD)</em> or <em>Inpatient (Ward)</em>.</p>
          <div class="warning-box">
            <strong>Stewardship Alert:</strong> Upper respiratory viral infections and watery diarrhea are flagged immediately for antibiotic de-escalation to prevent microbiome disruption and community resistance selection.
          </div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-badge-num">3</div>
        <div class="step-text-wrap">
          <div class="step-top">
            <span class="step-name">Antimicrobial Regimen Ingestion: Direct Entry or OCR Scan</span>
            <span class="step-tag">Step 3: Medication Lines</span>
          </div>
          <p><strong>Method A (Formulary Selector):</strong> Search generic drug names, enter unit dose (e.g. 500 mg), frequency (TDS/BD/OD), and intended duration in days.<br>
          <strong>Method B (Optical Scan Upload):</strong> Upload handwritten or typed prescription images. The assistive intake drafts medication names. <strong>Mandatory Check:</strong> Review highlighted low-confidence fields before proceeding.</p>
        </div>
      </div>

      <div class="step-card">
        <div class="step-badge-num">4</div>
        <div class="step-text-wrap">
          <div class="step-top">
            <span class="step-name">Mandatory Clinician Sign-Off &amp; Audit Execution</span>
            <span class="step-tag">Step 4: Audit Launch</span>
          </div>
          <p>Check the clinical confirmation box: <em>"I confirm that I have verified the entered patient context and medication regimen."</em> Click <strong>"Execute Deterministic Audit"</strong>. The closed-loop engine evaluates all 5 tiers of safety rules in under 3 seconds.</p>
        </div>
      </div>

      <!-- Inpatient Re-evaluation box -->
      <div class="card card-accent" style="margin-top:1px;">
        <div class="card-title"><span>⏰</span> The 48-to-72 Hour Antibiotic Time-Out Protocol</div>
        <p style="font-size:8.5pt; line-height:1.34;">For all inpatient ward admissions, clinical stewardship guidelines mandate a structured prescription review at <strong>48 to 72 hours</strong>. Prescribing clinicians must execute this 3-point checklist:</p>
        <div class="check-list" style="margin-top:2px;">
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Microbiology Review:</strong> Check preliminary blood/sputum/urine culture sensitivity reports.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Spectrum De-escalation:</strong> Switch broad-spectrum Watch/Reserve to narrow-spectrum Access agents once sensitivity is established.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>IV-to-Oral Conversion:</strong> Transition hemodynamically stable patients with functional GI tracts to oral formulations.</span>
          </div>
        </div>
      </div>

      <!-- Quick Outpatient vs Inpatient Grid -->
      <div class="grid-2" style="margin-top:1px;">
        <div class="card">
          <div class="card-title"><span style="color:#0f766e;">🩺</span> Outpatient (OPD) Target</div>
          <p style="font-size:8pt;">Prioritize narrow-spectrum oral <strong>Access</strong> antibiotics. Maintain therapy &le; 5 days for uncomplicated infections.</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#0284c7;">🏥</span> Inpatient (IPD) Target</div>
          <p style="font-size:8pt;">Collect cultures prior to starting first dose. Enforce 48h re-evaluation and rapid IV-to-oral step-down.</p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Clinician Practice Manual</span>
      <span>Grounded in ICMR STG 2022 &bull; WHO AWaRe 2023</span>
      <span>Page 2 of 5</span>
    </div>
  </div>

  <!-- ==================== PAGE 3: TRIAGE & FINDINGS ==================== -->
  <div class="page">
    <div class="page-header">
      <div class="header-logo-group">
        <svg class="logo-svg" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
        <div class="header-titles">
          <h1>CLINICAL AUDIT INTERPRETATION</h1>
          <p>TRIAGE STRATIFICATION, FINDING CARD ANATOMY, AND DATA GAP PROTOCOLS</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="header-badge">Audit Analysis</div>
        <div class="header-submeta">Evidence-Linked Triage</div>
      </div>
    </div>

    <div class="page-body">
      <!-- Traffic Light Triage -->
      <h2>1. The Three-Tier Clinical Triage Hierarchy</h2>
      
      <div class="triage-box triage-red">
        <div class="triage-head">
          <strong><span>&#9679;</span> NEEDS URGENT REVIEW (Red Severity Flag)</strong>
          <span class="triage-action-pill">Withhold / Immediate Bedside Review</span>
        </div>
        <p><strong>Clinical Significance:</strong> Direct breach of an absolute contraindication, black-box safety gate, or CDSCO-banned Fixed-Dose Combination. Examples include pediatric fluoroquinolone cartilage toxicity (age &lt; 18), pregnancy category-X teratogenic drugs, severe renal failure (eGFR &lt; 30 mL/min), or banned combinations (Cefixime + Azithromycin).</p>
      </div>

      <div class="triage-box triage-amber">
        <div class="triage-head">
          <strong><span>&#9679;</span> NEEDS REVIEW (Amber Stewardship Advisory)</strong>
          <span class="triage-action-pill">De-escalation &amp; Optimization Prompt</span>
        </div>
        <p><strong>Clinical Significance:</strong> Sub-optimal antimicrobial selection under WHO AWaRe or ICMR guidelines. Examples include: prescribing Watch/Reserve antibiotics (e.g. Azithromycin, Cefixime) for mild community infections where Access agents (Amoxicillin) are first-line; treating self-limiting viral bronchitis; or extending course beyond 5 days.</p>
      </div>

      <div class="triage-box triage-green">
        <div class="triage-head">
          <strong><span>&#9679;</span> NO RULE TRIGGERED (Green Concordant Status)</strong>
          <span class="triage-action-pill">Proceed with Standard Monitoring</span>
        </div>
        <p><strong>Clinical Significance:</strong> Regimen adheres to configured first-line guidelines and dosing limits. Clinicians should proceed with standard therapy and document bedside progress at the 48-hour antibiotic time-out.</p>
      </div>

      <!-- Anatomy of a Finding Card -->
      <h2>2. Anatomical Breakdown of a Clinical Finding Card</h2>
      <div class="mock-finding">
        <div class="mock-header">
          <div>
            <span class="mock-id">SAFETY.PEDIATRIC.CIPROFLOXACIN.AGE_LT_18</span>
            <strong style="font-size:9.2pt; color:#991b1b; margin-left:6px;">Pediatric Fluoroquinolone Contraindication</strong>
          </div>
          <span style="font-size:7.2pt; background:#fee2e2; color:#991b1b; font-weight:800; padding:2px 6px; border-radius:3px;">NEEDS URGENT REVIEW</span>
        </div>
        <div class="mock-grid">
          <div>
            <p style="font-size:8.4pt; color:#334155; line-height:1.32;"><strong>Clinical Rationale:</strong> Ciprofloxacin is contraindicated in pediatric patients under 18 years due to established risk of cartilage erosion, arthropathy in weight-bearing joints, and tendon rupture (ICMR Pediatric Guidelines &amp; FDA Boxed Warning).</p>
            <div class="mock-discuss">
              <span>Guideline Discussion Option:</span>
              <p style="font-size:7.8pt; color:#0f766e; margin-top:1px;">Consider oral Amoxicillin 40 mg/kg/day in divided doses or supportive oral rehydration (ORS + Zinc) under ICMR Pediatric Protocols.</p>
            </div>
          </div>
          <div class="mock-sidebar">
            <strong style="font-size:7.4pt; color:#475569; text-transform:uppercase;">Evaluated Facts:</strong>
            <ul style="font-size:7.2pt; color:#64748b; margin-left:14px; margin-top:2px; line-height:1.3;">
              <li>Patient Age: 8 Years</li>
              <li>Drug: Ciprofloxacin 250 mg</li>
              <li>Indication: Acute Diarrhea</li>
            </ul>
            <div style="margin-top:4px; border-top:1px solid #e2e8f0; padding-top:3px;">
              <span style="font-size:6.8pt; color:#0284c7; font-weight:800;">&bull; Citation: ICMR STG 2022, Ch. 4, Pg. 112</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Gap Protocol -->
      <h2>3. Handling Clinical Data Gaps (Unknown eGFR / Pregnancy)</h2>
      <div class="card card-accent">
        <div class="card-title"><span>⚠️</span> Protocol for Missing Clinical Parameters</div>
        <p style="font-size:8.6pt;">If an alert displays <em>"Data Gap: Renal Function (eGFR) Unspecified"</em> or <em>"Pregnancy Status Unconfirmed"</em>, the engine refuses to assume normal organ reserve. <strong>Mandatory Prescriber Actions:</strong></p>
        <div class="check-list" style="margin-top:3px;">
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Order Serum Creatinine:</strong> Calculate baseline eGFR (CKD-EPI formula) prior to dispensing aminoglycosides, glycopeptides, or nitrofurantoin.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Urine Pregnancy Test (UPT):</strong> Rule out pregnancy in females of reproductive age before prescribing tetracyclines, fluoroquinolones, or cotrimoxazole.</span>
          </div>
        </div>
      </div>

      <!-- Special Populations Matrix -->
      <h2>4. Vulnerable Patient Prescribing Safety Gates</h2>
      <table>
        <thead>
          <tr>
            <th style="width:23%;">Patient Population</th>
            <th style="width:35%;">High-Risk Antimicrobials</th>
            <th style="width:42%;">Clinical Precaution &amp; Action</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Geriatric (&ge; 65 Years)</strong></td>
            <td>Fluoroquinolones, Nitrofurantoin</td>
            <td>Assess Beers Criteria. High risk of delirium, tendon rupture, and neurotoxicity. Prefer oral Cefalexin or Amoxicillin.</td>
          </tr>
          <tr>
            <td><strong>Pediatric (&lt; 12 Years)</strong></td>
            <td>Tetracyclines, Fluoroquinolones</td>
            <td>Permanent dental enamel dysplasia and cartilage erosion. Use weight-based dosing (mg/kg/day) for beta-lactams.</td>
          </tr>
          <tr>
            <td><strong>Pregnancy &amp; Lactation</strong></td>
            <td>Doxycycline, Fluoroquinolones, Aminoglycosides</td>
            <td>FDA Category D/X teratogenicity (fetal bone deformity, ototoxicity). Prescribe safe penicillins, cefalexin, or erythromycin.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Clinician Practice Manual</span>
      <span>Grounded in ICMR STG 2022 &bull; WHO AWaRe 2023</span>
      <span>Page 3 of 5</span>
    </div>
  </div>

  <!-- ==================== PAGE 4: OVERRIDES & GOVERNANCE ==================== -->
  <div class="page">
    <div class="page-header">
      <div class="header-logo-group">
        <svg class="logo-svg" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
        <div class="header-titles">
          <h1>CLINICAL OVERRIDES &amp; GOVERNANCE</h1>
          <p>JUSTIFIED DEVIATIONS, HOSPITAL PHARMACY CLEARANCE, AND MEDICOLEGAL LOGS</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="header-badge">Clinical Governance</div>
        <div class="header-submeta">Immutable Audit Trail</div>
      </div>
    </div>

    <div class="page-body">
      <!-- Override Scenarios -->
      <h2>1. The Four Validated Clinical Override Scenarios</h2>
      <p>Clinical practice often necessitates deviation from generic population guidelines. AMR Sentinel provides a legally protected mechanism for prescribers to document clinical overrides across 4 structured categories:</p>

      <div class="grid-2">
        <div class="card">
          <div class="card-title"><span style="color:#0284c7;">🧪</span> 1. Culture &amp; Susceptibility Guided</div>
          <p>Microbiology laboratory sensitivity report proves pathogen resistance to standard first-line Access antimicrobials, justifying escalation to Watch or Reserve agents.</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#0f766e;">👨‍⚕️</span> 2. Specialist / ID Consultation</div>
          <p>Regimen was formulated in consultation with a designated Infectious Disease (ID) specialist, Pediatrician, or hospital Clinical Microbiologist.</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#d97706;">🚫</span> 3. Documented Severe Drug Allergy</div>
          <p>Patient has verified anaphylaxis, angioedema, or severe hypersensitivity to standard first-line agents (e.g. severe penicillin allergy requiring alternative coverage).</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#dc2626;">⚡</span> 4. Severe Sepsis / Septic Shock</div>
          <p>Patient exhibits hemodynamic instability, septic shock, or neutropenic fever requiring immediate empiric broad-spectrum coverage prior to lab return.</p>
        </div>
      </div>

      <!-- How to Record an Override -->
      <h2>2. Recording a Clinical Override in Three Steps</h2>
      
      <div class="step-card">
        <div class="step-badge-num">1</div>
        <div class="step-text-wrap">
          <span class="step-name">Click "Document Clinical Review &amp; Override"</span>
          <p>Located directly below any flagged finding card on the Results screen (`/results`).</p>
        </div>
      </div>

      <div class="step-card">
        <div class="step-badge-num">2</div>
        <div class="step-text-wrap">
          <span class="step-name">Select Clinical Justification &amp; Enter Registration Number</span>
          <p>Choose one of the 4 clinical categories, enter your State/National Medical Council Registration Number (e.g. MCI / NMC / GMC), and enter brief bedside clinical justification notes.</p>
        </div>
      </div>

      <div class="step-card">
        <div class="step-badge-num">3</div>
        <div class="step-text-wrap">
          <span class="step-name">Generate &amp; Print Stewardship Clearance Slip</span>
          <p>Click <em>"Print Clinical Audit Slip"</em> to output the official, timestamped physical clearance record for the patient's bedside case sheet and hospital pharmacy dispensing window.</p>
        </div>
      </div>

      <!-- Physical Slip Mockup -->
      <h2>3. Hospital Pharmacy Clearance &amp; Clinical Audit Slip</h2>
      <div class="slip-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #99f6e4; padding-bottom:3px; margin-bottom:3px;">
          <strong style="font-size:8.6pt; color:#0f766e;">HOSPITAL PHARMACY DISPENSING CLEARANCE SLIP</strong>
          <span style="font-size:7.2pt; color:#64748b; font-family:monospace;">AUD-2026-SYN-001 &bull; TIMESTAMP: 2026-11-06 09:40 UTC</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:7.8pt; color:#334155;">
          <div>
            <strong>Prescribing Clinician:</strong> Dr. Rajesh Sharma, MD (Reg: MCI-48921)<br>
            <strong>Indication:</strong> Community-Acquired Pneumonia (Mild Outpatient)<br>
            <strong>Regimen:</strong> Amoxicillin 500 mg TDS &times; 5 Days (Access Group)
          </div>
          <div>
            <strong>Stewardship Triage:</strong> <span class="pill-access">GUIDELINE CONCORDANT</span><br>
            <strong>Override Documented:</strong> None required (First-line ICMR STG 2022 compliant)<br>
            <strong>Pharmacist Clearance:</strong> Verified &amp; Dispensed [&check;]
          </div>
        </div>
      </div>

      <!-- Medicolegal Safeguards -->
      <h2>4. Medicolegal Safeguards &amp; Patient Data Privacy</h2>
      <div class="card card-accent">
        <div class="check-list">
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Tamper-Evident Audit Record:</strong> Every audit creates an immutable, timestamped record containing a unique Audit ID, evidence snapshot ID, and SHA-256 rule version hash.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Zero External PHI Leakage:</strong> Patient names, hospital numbers, and clinical details are processed locally within the institutional boundary and never transmitted to external cloud LLMs.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>Defensive Medicolegal Protection:</strong> Documenting evidence-linked overrides provides concrete evidence that the prescriber made an active, informed, and guidelines-aware clinical choice.</span>
          </div>
        </div>
      </div>

      <!-- Pharmacy Support Hotline -->
      <div class="card" style="margin-top:1px;">
        <div class="card-title"><span>📞</span> Hospital Pharmacy &amp; AMS Committee Escalation</div>
        <p style="font-size:8pt;">For urgent dispensing clearance during night shifts or critical care admissions where unlisted antimicrobials are required, contact the <strong>On-Call Clinical Pharmacist</strong> or the <strong>Infectious Disease Fellow</strong> via hospital extension <strong>#4402</strong>.</p>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Clinician Practice Manual</span>
      <span>Grounded in ICMR STG 2022 &bull; WHO AWaRe 2023</span>
      <span>Page 4 of 5</span>
    </div>
  </div>

  <!-- ==================== PAGE 5: CHEATSHEET & HIGH-ALERT TRAPS ==================== -->
  <div class="page">
    <div class="page-header">
      <div class="header-logo-group">
        <svg class="logo-svg" viewBox="0 0 24 24"><path d="M4.5 10.5C3.67 10.5 3 11.17 3 12s.67 1.5 1.5 1.5h15c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5h-15z"/></svg>
        <div class="header-titles">
          <h1>ANTIMICROBIAL STEWARDSHIP CHEATSHEET</h1>
          <p>WHO AWARE CLASSIFICATION, PRESCRIBING TRAPS &amp; FREQUENTLY ASKED QUESTIONS</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="header-badge">Clinical Reference</div>
        <div class="header-submeta">High-Alert Antimicrobial Traps</div>
      </div>
    </div>

    <div class="page-body">
      <!-- WHO AWaRe Table -->
      <h2>1. WHO AWaRe 2023 Prescribing Targets for Clinicians</h2>
      <table>
        <thead>
          <tr>
            <th style="width:16%;">AWaRe Class</th>
            <th style="width:26%;">Representative Antimicrobials</th>
            <th style="width:34%;">Clinical Stewardship Role</th>
            <th style="width:24%;">Prescribing Target</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="pill-access">ACCESS</span></td>
            <td>Amoxicillin, Amox-Clav, Cefalexin, Nitrofurantoin, Doxycycline</td>
            <td>First- and second-line therapy for common community infections. Narrower spectrum with lowest resistance potential.</td>
            <td><strong>&ge; 60%</strong> of total institutional antibiotic consumption.</td>
          </tr>
          <tr>
            <td><span class="pill-watch">WATCH</span></td>
            <td>Ciprofloxacin, Levofloxacin, Cefixime, Ceftriaxone, Azithromycin</td>
            <td>Broad-spectrum agents with high selective pressure for resistance. Restrict for confirmed severe indications.</td>
            <td>Strictly monitor; avoid for uncomplicated outpatient care.</td>
          </tr>
          <tr>
            <td><span class="pill-reserve">RESERVE</span></td>
            <td>Meropenem, Colistin, Linezolid, Polymyxin B</td>
            <td>"Last-resort" antimicrobials for confirmed multi-drug resistant (MDR) infections. Requires prior ID specialist sign-off.</td>
            <td>Protect strictly; never dispense without culture confirmation.</td>
          </tr>
        </tbody>
      </table>

      <!-- High-Alert Clinical Traps -->
      <h2>2. High-Alert Prescribing Traps Flagged by the Platform</h2>
      <table>
        <thead>
          <tr>
            <th style="width:24%;">High-Alert Drug / Class</th>
            <th style="width:36%;">Critical Contraindication / Clinical Trap</th>
            <th style="width:40%;">Recommended Guideline Remedy</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Fluoroquinolones</strong><br><span style="font-size:7pt; color:#64748b;">(Cipro, Levo, Norflox)</span></td>
            <td>Age &lt; 18 years (arthropathy/cartilage toxicity) or pregnancy; unindicated use in watery diarrhea.</td>
            <td>Use Oral Rehydration Salts (ORS) + Zinc for diarrhea; Cefalexin or Amoxicillin for confirmed bacterial infections.</td>
          </tr>
          <tr>
            <td><strong>Nitrofurantoin</strong></td>
            <td>eGFR &lt; 30 mL/min / severe renal impairment (ineffective concentration and neurotoxicity risk).</td>
            <td>Use single-dose oral Fosfomycin trometamol (3 g) or oral Cefalexin for lower urinary tract infections.</td>
          </tr>
          <tr>
            <td><strong>Banned Oral FDCs</strong><br><span style="font-size:7pt; color:#64748b;">(Cefixime + Azithromycin, Ofloxacin + Ornidazole)</span></td>
            <td>Banned by CDSCO Gazette. Lacks synergistic evidence; drives explosive resistance and severe gut dysbiosis.</td>
            <td>Prescribe targeted monotherapy directed strictly at the primary verified causative pathogen.</td>
          </tr>
          <tr>
            <td><strong>Macrolides</strong><br><span style="font-size:7pt; color:#64748b;">(Azithromycin in Bronchitis)</span></td>
            <td>Acute bronchitis / viral rhinopharyngitis (>95% viral etiology; zero antibiotic benefit).</td>
            <td>Reassure patient; prescribe supportive antipyretics (Paracetamol) and hydration. Withhold antibiotics.</td>
          </tr>
          <tr>
            <td><strong>Aminoglycosides</strong><br><span style="font-size:7pt; color:#64748b;">(Amikacin, Gentamicin)</span></td>
            <td>Unmonitored prolonged use in elderly or CKD; concurrent loop diuretics (ototoxicity/nephrotoxicity).</td>
            <td>Monitor peak and trough levels; limit duration &le; 5 days; switch to non-nephrotoxic beta-lactams.</td>
          </tr>
        </tbody>
      </table>

      <!-- Oral Switch Criteria Box -->
      <h2>3. IV-to-Oral Switch (IVOS) Clinical Discharge Criteria</h2>
      <div class="card card-accent">
        <p style="font-size:8.4pt;">Switch patients from IV Ceftriaxone / Piperacillin-Tazobactam to oral equivalents when all 4 conditions are met: <strong>1.</strong> Hemodynamically stable for &ge; 24h; <strong>2.</strong> Body temperature &lt; 37.8&deg;C for 24h; <strong>3.</strong> Tolerating oral liquids/diet; <strong>4.</strong> Normalizing white blood cell (WBC) count and CRP.</p>
      </div>

      <!-- Clinician FAQ -->
      <h2>4. Frequently Asked Questions (FAQ) for Doctors</h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-title"><span>❓</span> Can the platform alter my hospital EMR?</div>
          <p style="font-size:8.2pt;"><strong>No.</strong> AMR Sentinel AI is purely an assistive second-check. It does not possess write privileges to modify, suspend, or cancel hospital pharmacy orders.</p>
        </div>
        <div class="card">
          <div class="card-title"><span>❓</span> What if culture results are still pending?</div>
          <p style="font-size:8.2pt;">Initiate empiric narrow-spectrum <strong>Access</strong> therapy if bacterial infection is suspected, or document a temporary override under <em>Specialist Consultation</em>.</p>
        </div>
      </div>

      <!-- Stewardship Committee Hotline -->
      <div class="card" style="margin-top:1px;">
        <div class="card-title"><span>🏥</span> Institutional AMR Stewardship Support</div>
        <p style="font-size:8pt;">For queries regarding the hospital antibiogram, formulary restrictions, or outbreak management, reach out to the <strong>Hospital Infection Control Committee (HICC)</strong> or email <strong>stewardship@hospital.org</strong>.</p>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Clinician Practice Manual</span>
      <span>Grounded in ICMR STG 2022 &bull; WHO AWaRe 2023</span>
      <span>Page 5 of 5</span>
    </div>
  </div>

</body>
</html>
"""

def generate_pdf_and_render_images():
    html_path = r"c:\Seva Sankalp Hackathon\AMR Sentinel\docs\clinical_manual_template.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print("HTML template written successfully.")

    temp_dir = os.environ.get("TEMP", r"C:\Users\sanu6\AppData\Local\Temp")
    pdf_temp = os.path.join(temp_dir, "AMR_Sentinel_Clinician_User_Manual.pdf")
    user_data = os.path.join(temp_dir, "edge_pdf_profile")
    target_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\docs\AMR_Sentinel_Clinician_User_Manual.pdf"

    if os.path.exists(pdf_temp):
        os.remove(pdf_temp)

    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_bin,
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={user_data}",
        f"--print-to-pdf={pdf_temp}",
        "--no-pdf-header-footer",
        html_path
    ]
    subprocess.run(cmd, check=True)

    if os.path.exists(pdf_temp):
        shutil.copyfile(pdf_temp, target_pdf)
        print(f"Generated PDF at {target_pdf} ({os.path.getsize(target_pdf)} bytes)")

        # Convert to PNG using pymupdf
        doc = pymupdf.open(target_pdf)
        print(f"Total pages: {len(doc)}")
        for idx, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = rf"c:\Seva Sankalp Hackathon\AMR Sentinel\docs\page_{idx+1}.png"
            pix.save(img_path)
            print(f"Saved {img_path}")
    else:
        print("Error: PDF generation failed.")

if __name__ == "__main__":
    generate_pdf_and_render_images()
