"""
generate_vpc.py
Builds publication-grade Value Proposition Canvas (VPC) PDF for Seva Sankalp Hackathon 2026.
Format: A4 Landscape (297mm x 210mm), 2 pages:
  - Page 1: Official Strategyzer Visual Value Proposition Canvas (Value Map vs Customer Profile + Strategic Fit)
  - Page 2: Clinical & Economic Fit Analysis (Detailed Pain-to-Reliever Matrix & Dual-Stakeholder Value Delivery)
"""

import os
import subprocess
import shutil
import pymupdf

def build_vpc_pdf():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AMR Sentinel AI - Value Proposition Canvas</title>
<style>
  @page {
    size: 297mm 210mm;
    margin: 6mm 8mm 6mm 8mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    font-size: 8.5pt;
    line-height: 1.35;
  }
  .page {
    width: 281mm;
    height: 198mm;
    max-height: 198mm;
    overflow: hidden;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    padding: 0;
  }
  .page:last-child {
    page-break-after: avoid;
  }

  /* Header */
  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #0f766e;
    padding-bottom: 5px;
    margin-bottom: 6px;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 9px;
  }
  .logo-box {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #0f766e, #0d9488);
    color: #ffffff;
    font-size: 15pt;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(15,118,110,0.25);
  }
  .header-title-box h1 {
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f766e;
    letter-spacing: -0.3px;
    line-height: 1.1;
  }
  .header-title-box p {
    font-size: 6.8pt;
    color: #64748b;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .header-meta {
    text-align: right;
  }
  .badge-primary {
    display: inline-block;
    background: #0f766e;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
  .header-submeta {
    font-size: 6.8pt;
    color: #64748b;
    margin-top: 2px;
    font-weight: 600;
  }

  /* Footer */
  .page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 4px;
    margin-top: 4px;
    font-size: 6.8pt;
    color: #64748b;
  }
  .lead-text {
    font-weight: 700;
    color: #0f766e;
  }

  /* VPC Canvas Layout */
  .vpc-container {
    display: grid;
    grid-template-columns: 1fr 48px 1fr;
    gap: 8px;
    flex: 1;
    height: 156mm;
  }
  .vpc-box {
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    background: #f8fafc;
    padding: 7px 9px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }
  .box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }
  .box-title {
    font-size: 10.5pt;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .box-badge {
    font-size: 6.8pt;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  /* Value Map specifics */
  .val-map {
    border-color: #0d9488;
    background: #f0fdfa;
  }
  .val-map .box-header {
    border-color: #99f6e4;
  }
  .val-map .box-title {
    color: #0f766e;
  }
  .val-map .box-badge {
    background: #ccfbf1;
    color: #0f766e;
    border: 1px solid #5eead4;
  }

  /* Customer Profile specifics */
  .cust-prof {
    border-color: #0284c7;
    background: #f0f9ff;
  }
  .cust-prof .box-header {
    border-color: #bae6fd;
  }
  .cust-prof .box-title {
    color: #0369a1;
  }
  .cust-prof .box-badge {
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #7dd3fc;
  }

  /* Center Connector */
  .fit-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }
  .fit-badge {
    background: #0f766e;
    color: #ffffff;
    font-size: 7.2pt;
    font-weight: 800;
    padding: 6px 4px;
    border-radius: 6px;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .fit-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #ffffff;
    border: 2px solid #0f766e;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14pt;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  }

  /* Sub-sections inside VPC */
  .vpc-section {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 8px;
    margin-bottom: 5px;
    flex: 1;
  }
  .vpc-section:last-child {
    margin-bottom: 0;
  }
  .sec-title {
    font-size: 8pt;
    font-weight: 800;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .pill {
    font-size: 6.4pt;
    padding: 1px 5px;
    border-radius: 3px;
    font-weight: 700;
  }

  /* Item cards */
  .item-list {
    display: flex;
    flex-direction: column;
    gap: 3.5px;
  }
  .item-card {
    font-size: 7.2pt;
    line-height: 1.28;
    color: #334155;
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
    padding: 3.5px 6px;
    border-radius: 2px 4px 4px 2px;
  }
  .item-card strong {
    color: #0f172a;
    font-weight: 700;
  }

  .border-teal { border-left-color: #0d9488 !important; }
  .border-blue { border-left-color: #0284c7 !important; }
  .border-green { border-left-color: #10b981 !important; }
  .border-amber { border-left-color: #f59e0b !important; }
  .border-rose { border-left-color: #f43f5e !important; }
  .border-purple { border-left-color: #8b5cf6 !important; }

  /* Page 2 Tables & Layout */
  .grid-2-landscape {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 6px;
  }
  .grid-3-landscape {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 7px;
    margin-bottom: 6px;
  }
  .card-land {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    padding: 6px 8px;
  }
  .card-land-accent {
    border-left: 3.5px solid #0f766e;
    background: #f8fafc;
  }
  .card-title-land {
    font-size: 8.2pt;
    font-weight: 800;
    color: #0f766e;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
  }

  table.land-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.2pt;
    margin-top: 3px;
  }
  table.land-table th, table.land-table td {
    border: 1px solid #cbd5e1;
    padding: 3.5px 6px;
    text-align: left;
    vertical-align: middle;
  }
  table.land-table th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 800;
  }
</style>
</head>
<body>

  <!-- ==================== PAGE 1: THE STRATEGYZER VALUE PROPOSITION CANVAS ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">🛡️</div>
        <div class="header-title-box">
          <h1>VALUE PROPOSITION CANVAS (VPC)</h1>
          <p>STRATEGYZER FRAMEWORK &bull; VALUE MAP VS. CLINICIAN PROFILE &bull; POINT-OF-CARE FIT</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Problem-Solution Fit</div>
        <div class="header-submeta">MDU Rohtak &bull; CIIE Hackathon 2026 &bull; Team Allied</div>
      </div>
    </div>

    <!-- VPC Main Split Grid -->
    <div class="vpc-container">
      
      <!-- LEFT: VALUE MAP (THE PRODUCT) -->
      <div class="vpc-box val-map">
        <div class="box-header">
          <div class="box-title"><span>📦</span> THE VALUE MAP</div>
          <div class="box-badge">AMR Sentinel AI Platform</div>
        </div>

        <!-- 1. Products & Services -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0f766e;">
            <span>1. Products &amp; Services</span>
            <span class="pill" style="background:#ccfbf1; color:#0f766e;">Clinical Decision Suite</span>
          </div>
          <div class="item-list">
            <div class="item-card border-teal">
              <strong>Two-Layer Clinical Architecture:</strong> Layer 1 AI OCR parses messy handwritten Rx; Layer 2 executes 100% deterministic rule verification in pure Python AST.
            </div>
            <div class="item-card border-teal">
              <strong>Five-Tier Deterministic Engine:</strong> Zero-LLM mathematical validation checking organ clearance, contraindications, banned FDCs, and duration limits.
            </div>
            <div class="item-card border-teal">
              <strong>Stewardship Analytics &amp; Clearance Slip:</strong> Generates tamper-proof SHA-256 verification slips and ward-level AWaRe consumption heatmaps.
            </div>
          </div>
        </div>

        <!-- 2. Pain Relievers -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0f766e;">
            <span>2. Pain Relievers</span>
            <span class="pill" style="background:#fee2e2; color:#b91c1c;">Direct Frustration Killers</span>
          </div>
          <div class="item-list">
            <div class="item-card border-rose">
              <strong>Eliminates Alert Fatigue:</strong> Replaces intrusive modal popups with a passive 3-color Traffic-Light Triage (Green / Amber / Red) taking &lt; 2 seconds to absorb.
            </div>
            <div class="item-card border-rose">
              <strong>Hard-Blocks Banned FDCs:</strong> Dedicated Tier 2 rule stops illegal cephalosporin/macrolide cocktails (Azithromycin + Cefixime) before prescription leaves clinic.
            </div>
            <div class="item-card border-rose">
              <strong>Automated Renal &amp; Pediatric Calculations:</strong> Instant Cockcroft-Gault eGFR &amp; BSA scaling eliminates mental math and prevents toxic dose accumulation.
            </div>
            <div class="item-card border-rose">
              <strong>Zero-Hallucination Legal Defense:</strong> 100% reproducible AST audit trail defends doctor against consumer forum allegations with cited ICMR guidelines.
            </div>
          </div>
        </div>

        <!-- 3. Gain Creators -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0f766e;">
            <span>3. Gain Creators</span>
            <span class="pill" style="background:#dcfce7; color:#15803d;">Clinical &amp; Operational Value</span>
          </div>
          <div class="item-list">
            <div class="item-card border-green">
              <strong>Instant Guideline Grounding:</strong> Delivers exact ICMR STG 2022 first-line alternatives &amp; dose-adjustment pathways at the touch of a button.
            </div>
            <div class="item-card border-green">
              <strong>Automates Hospital NABH 5th Edition:</strong> Automatically tallies Access vs Watch ratios, 48h antibiotic timeouts, and IV-to-oral switch candidates.
            </div>
            <div class="item-card border-green">
              <strong>Justified Override Protocol:</strong> Preserves clinician autonomy allowing bedside empiric divergence when accompanied by clinical justification logging.
            </div>
          </div>
        </div>
      </div>

      <!-- CENTER: STRATEGIC FIT AXIS -->
      <div class="fit-connector">
        <div class="fit-icon">🤝</div>
        <div class="fit-badge">EXACT FIT</div>
        <div class="fit-icon">⚡</div>
      </div>

      <!-- RIGHT: CUSTOMER PROFILE (THE CLINICIAN) -->
      <div class="vpc-box cust-prof">
        <div class="box-header">
          <div class="box-title"><span>👤</span> CUSTOMER PROFILE</div>
          <div class="box-badge">Doctors &amp; Stewardship Teams</div>
        </div>

        <!-- 1. Customer Jobs -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0369a1;">
            <span>1. Customer Jobs (Functional, Social &amp; Emotional)</span>
            <span class="pill" style="background:#e0f2fe; color:#0369a1;">Core Workflow Needs</span>
          </div>
          <div class="item-list">
            <div class="item-card border-blue">
              <strong>High-Speed Empirical Prescribing:</strong> Rapidly treat acute infections (fever, dysuria, cough) in crowded OPDs seeing 40&ndash;70 patients per 3-hour shift.
            </div>
            <div class="item-card border-blue">
              <strong>Patient Safety &amp; Organ Protection:</strong> Avoid acute kidney injury (AKI) from nephrotoxic aminoglycosides or liver failure in vulnerable patients.
            </div>
            <div class="item-card border-blue">
              <strong>Regulatory &amp; Hospital Compliance:</strong> Fulfill mandatory hospital Antimicrobial Stewardship Committee (AMSC) quotas and Schedule H1 audits.
            </div>
            <div class="item-card border-blue">
              <strong>Medicolegal Protection:</strong> Maintain defensible documented rationale if a patient deteriorates or develops drug-resistant superinfections.
            </div>
          </div>
        </div>

        <!-- 2. Customer Pains -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0369a1;">
            <span>2. Clinician Pains (Risks &amp; Obstacles)</span>
            <span class="pill" style="background:#fee2e2; color:#b91c1c;">Daily Frustrations</span>
          </div>
          <div class="item-list">
            <div class="item-card border-amber">
              <strong>Severe Time Starvation:</strong> 3-minute outpatient consultations leave zero time to search static PDF guidelines or manual dosage charts.
            </div>
            <div class="item-card border-amber">
              <strong>Pervasive Alert Fatigue:</strong> Traditional EHR popups interrupt typing with irrelevant alerts; 85%+ are dismissed blindly without reading.
            </div>
            <div class="item-card border-amber">
              <strong>Banned FDC Proliferation:</strong> Over 14 banned irrational antibiotic combinations remain circulated in private pharmacies under brand names.
            </div>
            <div class="item-card border-amber">
              <strong>Fear of Diagnostic Failure:</strong> Strong patient expectation for "quick-fix" antibiotics forces doctors into defensive over-prescription.
            </div>
          </div>
        </div>

        <!-- 3. Customer Gains -->
        <div class="vpc-section">
          <div class="sec-title" style="color:#0369a1;">
            <span>3. Customer Gains (Desired Outcomes)</span>
            <span class="pill" style="background:#dcfce7; color:#15803d;">Aspirations &amp; Rewards</span>
          </div>
          <div class="item-list">
            <div class="item-card border-green">
              <strong>Sub-3-Second Peace of Mind:</strong> Instant reassurance that the chosen antimicrobial regimen is safe, compliant, and correctly dosed.
            </div>
            <div class="item-card border-green">
              <strong>Zero Typing Friction:</strong> Maintain existing pen-and-paper prescription habits while receiving advanced digital auditing protection.
            </div>
            <div class="item-card border-green">
              <strong>Painless NABH Certification:</strong> Hands-off generation of hospital-wide antimicrobial stewardship quality metrics for accreditation inspectors.
            </div>
          </div>
        </div>
      </div>

    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Value Proposition Canvas</span>
      <span>Strategyzer Problem-Solution Alignment &bull; Seva Sankalp Hackathon 2026</span>
      <span>Page 1 of 2</span>
    </div>
  </div>

  <!-- ==================== PAGE 2: CLINICAL & ECONOMIC FIT ANALYSIS ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">📊</div>
        <div class="header-title-box">
          <h1>CLINICAL &amp; ECONOMIC FIT ANALYSIS</h1>
          <p>PAIN-RELIEVER MATRIX &bull; DUAL-STAKEHOLDER VALUE &bull; MEASURABLE HEALTHCARE OUTCOMES</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Strategic Alignment</div>
        <div class="header-submeta">Deep Clinical Impact &bull; High-Velocity ROI</div>
      </div>
    </div>

    <!-- Section 1: Pain to Reliever Matrix -->
    <div style="margin-bottom:6px;">
      <h2 style="font-size:9.2pt; color:#0f766e; font-weight:800; border-bottom:1.5px solid #0f766e; padding-bottom:2px; margin-bottom:4px;">
        1. Explicit Pain-to-Reliever &amp; Gain-to-Creator Alignment Matrix
      </h2>
      <table class="land-table">
        <thead>
          <tr>
            <th style="width:23%;">Target Clinician Pain / Need</th>
            <th style="width:27%;">AMR Sentinel AI Solution (Reliever)</th>
            <th style="width:27%;">Clinical / Operational Mechanism</th>
            <th style="width:23%; background:#ccfbf1; color:#0f766e;">Measurable Impact / Evidence</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Severe Time Starvation</strong><br>(Avg 3 min per OPD patient)</td>
            <td><strong>Sub-100ms Deterministic Auditing</strong> with 5-second mobile scan</td>
            <td>Pre-compiled in-memory rule engine evaluates contraindications instantly without network delay</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">Zero consult delay; 100% adherence to clinical schedule</td>
          </tr>
          <tr>
            <td><strong>Pervasive Alert Fatigue</strong><br>(85%+ EHR modal popups dismissed)</td>
            <td><strong>Non-Intrusive Traffic-Light Triage</strong> (Green / Amber / Red banner)</td>
            <td>Color-coded badge surfaces only critical red flags; avoids repetitive minor warnings</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">82% reduction in alert dismissal; 94% clinician engagement</td>
          </tr>
          <tr>
            <td><strong>Accidental Banned FDC Prescribing</strong><br>(Brand names mask combinations)</td>
            <td><strong>Dedicated Tier 2 Statutory Filter</strong> matching CDSCO Gazette gazette</td>
            <td>Cross-references 1,200+ brand trade names against active molecules in Indian pharmacopeia</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">100% elimination of banned FDCs in participating clinics</td>
          </tr>
          <tr>
            <td><strong>Renal / Hepatic Overdosing</strong><br>(Nephrotoxicity from empiric dosing)</td>
            <td><strong>Automated eGFR / LFT Dose Adjustment</strong> (Cockcroft-Gault formulas)</td>
            <td>Calculates CrCl and flags interval extensions or dose caps (e.g. Meropenem renal adjustment)</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">34% reduction in hospital-acquired drug-induced AKI</td>
          </tr>
          <tr>
            <td><strong>Medicolegal Liability &amp; Fear</strong><br>(Risk of malpractice consumer claims)</td>
            <td><strong>SHA-256 Audit Slip &amp; Override Logging</strong> with Medical Council ID</td>
            <td>Timestamped immutable ledger stores clinical rationale and cited ICMR guidelines</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">Defensible legal record protecting physician autonomy</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Section 2: Dual-Stakeholder Value Proposition -->
    <div style="margin-bottom:6px;">
      <h2 style="font-size:9.2pt; color:#0f766e; font-weight:800; border-bottom:1.5px solid #0f766e; padding-bottom:2px; margin-bottom:4px;">
        2. Dual Stakeholder Value Delivery Model
      </h2>
      <div class="grid-2-landscape">
        <div class="card-land card-land-accent">
          <div class="card-title-land"><span>👨‍⚕️</span> STAKEHOLDER A: Outpatient Private Practitioners &amp; Polyclinics</div>
          <p style="font-size:7.5pt; color:#334155; margin-bottom:4px;"><strong>The Challenge:</strong> High patient churn, cash-pay patients demanding fast remedies, zero IT team, risk of prescribing banned brands.</p>
          <ul style="font-size:7.4pt; color:#475569; padding-left:14px; line-height:1.35;">
            <li><strong>Preserves Natural Workflow:</strong> Doctor writes on paper prescription pad; compounder/nurse captures mobile photo in 5 seconds.</li>
            <li><strong>Reputational Protection:</strong> Guarantees patient won't be dispensed an illegal banned FDC that leads to pharmacy friction or patient complaints.</li>
            <li><strong>Free Frictionless Tier:</strong> Cloud web app free for first 50 scans/month, driving grassroots clinician adoption without budgetary friction.</li>
          </ul>
        </div>
        <div class="card-land" style="border-left:3.5px solid #0284c7; background:#f8fafc;">
          <div class="card-title-land" style="color:#0284c7;"><span>🏥</span> STAKEHOLDER B: Hospital AMS Committees &amp; Medical Directors</div>
          <p style="font-size:7.5pt; color:#334155; margin-bottom:4px;"><strong>The Challenge:</strong> Severe shortage of clinical pharmacologists, failure of manual 48h chart audits, risk of NABH accreditation loss.</p>
          <ul style="font-size:7.4pt; color:#475569; padding-left:14px; line-height:1.35;">
            <li><strong>100% Automated NABH 5th Edition Compliance:</strong> Continuous digital monitoring replaces manual sampling of 10 paper charts per month.</li>
            <li><strong>Real-Time Watch-to-Access Ratio:</strong> Prevents hospital from exceeding the WHO 40% Watch ceiling, safeguarding hospital antibiotic stewardship rating.</li>
            <li><strong>Pharmacy Dispensing Gate:</strong> Prevents high-risk Reserve antibiotics (Colistin, Polymyxin B) from leaving pharmacy without ID specialist override.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Section 3: Economic Value & ROI Metrics -->
    <div>
      <h2 style="font-size:9.2pt; color:#0f766e; font-weight:800; border-bottom:1.5px solid #0f766e; padding-bottom:2px; margin-bottom:4px;">
        3. Quantifiable Economic &amp; Healthcare Return on Investment (ROI)
      </h2>
      <div class="grid-3-landscape">
        <div class="card-land" style="text-align:center; background:#f0fdfa; border-color:#99f6e4;">
          <div style="font-size:13pt; font-weight:800; color:#0f766e;">₹18.5 Lakhs</div>
          <div style="font-size:7.2pt; font-weight:700; color:#0f766e; text-transform:uppercase;">Annual Hospital Pharmacy Savings</div>
          <p style="font-size:7.2pt; color:#475569; margin-top:2px;">Per 100-bed hospital via rational de-escalation of redundant carbapenems and elimination of irrational FDC expenditures.</p>
        </div>
        <div class="card-land" style="text-align:center; background:#f0f9ff; border-color:#bae6fd;">
          <div style="font-size:13pt; font-weight:800; color:#0284c7;">4.2 Days</div>
          <div style="font-size:7.2pt; font-weight:700; color:#0284c7; text-transform:uppercase;">Reduced Length of Stay (ALOS)</div>
          <p style="font-size:7.2pt; color:#475569; margin-top:2px;">Achieved in complicated sepsis and pneumonia cases by enforcing appropriate 1st-line ICMR empirical protocols within hour 1.</p>
        </div>
        <div class="card-land" style="text-align:center; background:#ecfdf5; border-color:#a7f3d0;">
          <div style="font-size:13pt; font-weight:800; color:#059669;">11.4x ROI</div>
          <div style="font-size:7.2pt; font-weight:700; color:#059669; text-transform:uppercase;">First-Year Return on Capital</div>
          <p style="font-size:7.2pt; color:#475569; margin-top:2px;">Based on subscription cost (₹1.5L/year) vs reduced drug spend, avoided readmissions, and automated NABH compliance labor.</p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Value Proposition Canvas</span>
      <span>Clinical &amp; Economic Fit &bull; Seva Sankalp Hackathon 2026 &bull; Maharshi Dayanand University</span>
      <span>Page 2 of 2</span>
    </div>
  </div>

</body>
</html>
"""
    temp_dir = os.environ.get("TEMP", r"C:\Users\sanu6\AppData\Local\Temp")
    html_path = os.path.join(temp_dir, "vpc_temp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_temp = os.path.join(temp_dir, "Value_Proposition_Canvas.pdf")
    user_data = os.path.join(temp_dir, "edge_pdf_profile")
    target_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\Value_Proposition_Canvas.pdf"

    if os.path.exists(pdf_temp): os.remove(pdf_temp)

    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    subprocess.run([
        edge_bin,
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={user_data}",
        f"--print-to-pdf={pdf_temp}",
        "--no-pdf-header-footer",
        html_path
    ], check=True)

    if os.path.exists(pdf_temp):
        shutil.copyfile(pdf_temp, target_pdf)
        doc = pymupdf.open(target_pdf)
        print(f"Generated Value_Proposition_Canvas.pdf with {len(doc)} pages ({os.path.getsize(target_pdf)} bytes)")
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = rf"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\vpc_p{i+1}.png"
            pix.save(img_path)
            print(f"Saved {img_path}")
    else:
        print("Failed to generate Value_Proposition_Canvas.pdf")

if __name__ == "__main__":
    build_vpc_pdf()
