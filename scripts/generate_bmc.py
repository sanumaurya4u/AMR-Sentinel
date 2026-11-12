"""
generate_bmc.py
Builds publication-grade Business Model Canvas (BMC) PDF for Seva Sankalp Hackathon 2026.
Format: A4 Landscape (297mm x 210mm), 2 pages:
  - Page 1: Canonical 9-Box Osterwalder Business Model Canvas Grid
  - Page 2: Revenue Economics, Pricing Strategy, Risk Matrix & CIIE Milestones
"""

import os
import subprocess
import shutil
import pymupdf

def build_bmc_pdf():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AMR Sentinel AI - Business Model Canvas</title>
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
    font-size: 8.2pt;
    line-height: 1.32;
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
    margin-bottom: 5px;
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

  /* Canonical Osterwalder 9-Box Grid */
  .bmc-grid {
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex: 1;
    height: 157mm;
  }
  .bmc-top-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1.15fr 1fr 1fr;
    gap: 5px;
    flex: 3;
    height: 108mm;
  }
  .bmc-split-col {
    display: flex;
    flex-direction: column;
    gap: 5px;
    height: 100%;
  }
  .bmc-bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    flex: 1.1;
    height: 44mm;
  }

  /* Box Styles */
  .bmc-box {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    padding: 5px 7px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .bmc-box-accent {
    border-top: 3px solid #0f766e;
    background: #fafdfc;
  }
  .bmc-box-vp {
    border-top: 3.5px solid #0d9488;
    background: #f0fdfa;
    border-color: #99f6e4;
  }
  .bmc-box-finance {
    border-top: 3px solid #0284c7;
    background: #f8fafc;
  }

  .box-title {
    font-size: 7.6pt;
    font-weight: 800;
    color: #0f766e;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 3px;
    margin-bottom: 4px;
  }
  .box-title span.icon {
    font-size: 9pt;
    margin-right: 4px;
  }
  .box-badge {
    font-size: 6.2pt;
    font-weight: 700;
    padding: 1px 4px;
    border-radius: 3px;
    background: #f1f5f9;
    color: #475569;
  }

  .bmc-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
    flex: 1;
  }
  .bmc-item {
    font-size: 6.8pt;
    line-height: 1.25;
    color: #334155;
    background: #ffffff;
    border-left: 2.5px solid #cbd5e1;
    padding: 2.5px 5px;
    border-radius: 2px;
  }
  .bmc-item strong {
    color: #0f172a;
    font-weight: 700;
  }

  .b-teal { border-left-color: #0d9488 !important; }
  .b-blue { border-left-color: #0284c7 !important; }
  .b-purple { border-left-color: #7c3aed !important; }
  .b-amber { border-left-color: #f59e0b !important; }
  .b-emerald { border-left-color: #10b981 !important; }
  .b-rose { border-left-color: #f43f5e !important; }

  /* Page 2 Styles */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin-bottom: 5px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 6px;
    margin-bottom: 5px;
  }
  .grid-4 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 6px;
    margin-bottom: 5px;
  }
  .sec-h2 {
    font-size: 8.8pt;
    font-weight: 800;
    color: #0f766e;
    border-bottom: 1.5px solid #0f766e;
    padding-bottom: 2px;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  table.bmc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7pt;
  }
  table.bmc-table th, table.bmc-table td {
    border: 1px solid #cbd5e1;
    padding: 3.5px 6px;
    text-align: left;
    vertical-align: middle;
  }
  table.bmc-table th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 800;
  }
  .card-p2 {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    padding: 6px 8px;
  }
</style>
</head>
<body>

  <!-- ==================== PAGE 1: CANONICAL 9-BOX BUSINESS MODEL CANVAS ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">🏛️</div>
        <div class="header-title-box">
          <h1>BUSINESS MODEL CANVAS (BMC)</h1>
          <p>OSTERWALDER FRAMEWORK &bull; COMMERCIALIZATION &bull; HEALTHCARE SUSTAINABILITY</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Strategic Architecture</div>
        <div class="header-submeta">MDU Rohtak &bull; CIIE Incubation &bull; Team Allied</div>
      </div>
    </div>

    <!-- Osterwalder 9-Box Grid -->
    <div class="bmc-grid">
      
      <!-- Top Row: 5 Columns (KP, KA/KR, VP, CR/CH, CS) -->
      <div class="bmc-top-row">
        
        <!-- 1. Key Partners -->
        <div class="bmc-box bmc-box-accent">
          <div class="box-title">
            <div><span class="icon">🤝</span> Key Partners</div>
            <span class="box-badge">Ecosystem</span>
          </div>
          <div class="bmc-list">
            <div class="bmc-item b-teal">
              <strong>EMR / HIS Vendors:</strong> Practo, Tata 1mg, KareXpert, Bajaj Finserv Health to embed API.
            </div>
            <div class="bmc-item b-teal">
              <strong>Medical Associations:</strong> IMA, FOGSI, API, IAP for CME training and physician advocacy.
            </div>
            <div class="bmc-item b-teal">
              <strong>Academic &amp; Research:</strong> ICMR AMR Network, MDU Rohtak CIIE, Clinical Pharmacology labs.
            </div>
            <div class="bmc-item b-teal">
              <strong>Accreditation Bodies:</strong> NABH (National Accreditation Board for Hospitals) &amp; NHM.
            </div>
            <div class="bmc-item b-teal">
              <strong>State Health Societies:</strong> Haryana &amp; NCR National Action Plan on AMR committees.
            </div>
          </div>
        </div>

        <!-- 2. Split Col: Key Activities & Key Resources -->
        <div class="bmc-split-col">
          <!-- Key Activities -->
          <div class="bmc-box bmc-box-accent" style="flex:1;">
            <div class="box-title">
              <div><span class="icon">⚙️</span> Key Activities</div>
              <span class="box-badge">Execution</span>
            </div>
            <div class="bmc-list">
              <div class="bmc-item b-blue">
                <strong>Guideline Curation:</strong> Compiling ICMR STG, CDSCO bans &amp; WHO AWaRe updates into AST rules.
              </div>
              <div class="bmc-item b-blue">
                <strong>Engine Optimization:</strong> Sub-100ms deterministic validation &amp; handwriting OCR fine-tuning.
              </div>
              <div class="bmc-item b-blue">
                <strong>EMR Integration:</strong> RESTful JSON &amp; HL7/FHIR microservice connectors.
              </div>
              <div class="bmc-item b-blue">
                <strong>Clinical Stewardship:</strong> CME workshops &amp; hospital AMS committee onboarding.
              </div>
            </div>
          </div>
          <!-- Key Resources -->
          <div class="bmc-box bmc-box-accent" style="flex:1;">
            <div class="box-title">
              <div><span class="icon">🔬</span> Key Resources</div>
              <span class="box-badge">Assets</span>
            </div>
            <div class="bmc-list">
              <div class="bmc-item b-purple">
                <strong>Proprietary AST Rulebase:</strong> 5-Tier deterministic rule database.
              </div>
              <div class="bmc-item b-purple">
                <strong>Prescription Vision Engine:</strong> Fine-tuned Indian doctor OCR model.
              </div>
              <div class="bmc-item b-purple">
                <strong>Multidisciplinary Team:</strong> Clinical pharmacologists &amp; software architects.
              </div>
              <div class="bmc-item b-purple">
                <strong>CIIE MDU Rohtak Lab:</strong> Incubation compute and testing infrastructure.
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Value Propositions (Center Hero) -->
        <div class="bmc-box bmc-box-vp">
          <div class="box-title" style="color:#0f766e;">
            <div><span class="icon">💡</span> Value Propositions</div>
            <span class="box-badge" style="background:#ccfbf1; color:#0f766e;">Core Moat</span>
          </div>
          <div class="bmc-list">
            <div class="bmc-item b-emerald">
              <strong>Zero-Hallucination Safety:</strong> 100% deterministic closed-loop mathematical audit engine; zero LLM guesswork.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Sub-3-Second Workflow:</strong> Instant 5-sec prescription scan to audit verification; zero typing friction for busy OPD doctors.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Banned FDC Elimination:</strong> Hard-blocks illegal fixed-dose combinations (CDSCO gazette) before pharmacy dispensing.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Automated NABH Compliance:</strong> Hands-off generation of 48h timeout slips and ward-level AWaRe metric reports.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Medicolegal Protection:</strong> Cryptographic SHA-256 audit slip with clinician ID protects against consumer litigation.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Edge Offline Capability:</strong> Runs fully offline on low-spec hardware (&lt; 150MB) for remote PHCs and disaster relief.
            </div>
          </div>
        </div>

        <!-- 4. Split Col: Customer Relationships & Channels -->
        <div class="bmc-split-col">
          <!-- Customer Relationships -->
          <div class="bmc-box bmc-box-accent" style="flex:1;">
            <div class="box-title">
              <div><span class="icon">🤝</span> Relationships</div>
              <span class="box-badge">Retention</span>
            </div>
            <div class="bmc-list">
              <div class="bmc-item b-amber">
                <strong>High-Touch Institutional:</strong> Dedicated onboarding for hospital AMS committees &amp; medical directors.
              </div>
              <div class="bmc-item b-amber">
                <strong>Self-Service Digital:</strong> Freemium cloud app with zero-friction signup for individual doctors.
              </div>
              <div class="bmc-item b-amber">
                <strong>CME Stewardship Badging:</strong> Annual certificates of rational prescribing recognized by medical boards.
              </div>
            </div>
          </div>
          <!-- Channels -->
          <div class="bmc-box bmc-box-accent" style="flex:1;">
            <div class="box-title">
              <div><span class="icon">📢</span> Channels</div>
              <span class="box-badge">Distribution</span>
            </div>
            <div class="bmc-list">
              <div class="bmc-item b-blue">
                <strong>EMR Marketplace Stores:</strong> Native plug-in for Practo, Tata 1mg, KareXpert.
              </div>
              <div class="bmc-item b-blue">
                <strong>Direct B2B Enterprise:</strong> Sales to corporate hospital chains (Max, Apollo, Fortis).
              </div>
              <div class="bmc-item b-blue">
                <strong>Public Health Tenders:</strong> National Health Mission (NHM) state pilots.
              </div>
              <div class="bmc-item b-blue">
                <strong>Medical Conferences:</strong> IMA, APICON, and regional CME symposiums.
              </div>
            </div>
          </div>
        </div>

        <!-- 5. Customer Segments -->
        <div class="bmc-box bmc-box-accent">
          <div class="box-title">
            <div><span class="icon">👥</span> Customer Segments</div>
            <span class="box-badge">Users</span>
          </div>
          <div class="bmc-list">
            <div class="bmc-item b-purple">
              <strong>Private Outpatient Doctors:</strong> 400,000+ Indian GPs &amp; specialists managing high-velocity OPD consults.
            </div>
            <div class="bmc-item b-purple">
              <strong>Secondary &amp; Tertiary Hospitals:</strong> 45,000+ private nursing homes &amp; hospitals requiring NABH 5th Edition.
            </div>
            <div class="bmc-item b-purple">
              <strong>Public Health Systems:</strong> 25,000+ rural PHCs, CHCs, and District Hospitals under State NHM.
            </div>
            <div class="bmc-item b-purple">
              <strong>Retail &amp; Hospital Pharmacies:</strong> Gatekeeper pharmacists verifying Schedule H1 antibiotic clearance.
            </div>
            <div class="bmc-item b-purple">
              <strong>Health Insurance Payers:</strong> Insurers seeking to eliminate fraudulent or irrational antibiotic claims.
            </div>
          </div>
        </div>

      </div>

      <!-- Bottom Row: Cost Structure & Revenue Streams -->
      <div class="bmc-bottom-row">
        
        <!-- Cost Structure -->
        <div class="bmc-box bmc-box-finance">
          <div class="box-title" style="color:#0284c7;">
            <div><span class="icon">📉</span> Cost Structure</div>
            <span class="box-badge" style="background:#e0f2fe; color:#0369a1;">₹3.60 Lakhs / month fixed</span>
          </div>
          <div class="bmc-list" style="display:grid; grid-template-columns:1fr 1fr; gap:3px;">
            <div class="bmc-item b-rose">
              <strong>Cloud &amp; OCR Inference:</strong> ₹45,000/mo (Vercel, Railway, Edge workers, GPU inference).
            </div>
            <div class="bmc-item b-rose">
              <strong>Clinical Panel Honorariums:</strong> ₹60,000/mo (Pharmacologists &amp; infectious disease MDs).
            </div>
            <div class="bmc-item b-rose">
              <strong>Core Engineering &amp; QA:</strong> ₹1,80,000/mo (Full-stack, AST engine, security devs).
            </div>
            <div class="bmc-item b-rose">
              <strong>Compliance &amp; Marketing:</strong> ₹75,000/mo (ISO 27001, legal audits, CME doctor workshops).
            </div>
          </div>
        </div>

        <!-- Revenue Streams -->
        <div class="bmc-box bmc-box-finance">
          <div class="box-title" style="color:#059669;">
            <div><span class="icon">💰</span> Revenue Streams</div>
            <span class="box-badge" style="background:#ecfdf5; color:#059669;">Multi-Tier Monetization</span>
          </div>
          <div class="bmc-list" style="display:grid; grid-template-columns:1fr 1fr; gap:3px;">
            <div class="bmc-item b-emerald">
              <strong>B2B Hospital SaaS:</strong> ₹12,500/mo per 100 beds (₹1.5L/year) for automated NABH AMSC auditing.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Outpatient Clinic Pro:</strong> ₹999/mo per prescriber (unlimited scans, clinic letterhead, audit export).
            </div>
            <div class="bmc-item b-emerald">
              <strong>EMR Marketplace Royalties:</strong> ₹0.50 per transaction via Practo/Tata 1mg API integration.
            </div>
            <div class="bmc-item b-emerald">
              <strong>Govt District Licenses:</strong> ₹15&ndash;25 Lakhs per district annual surveillance tender (NHM).
            </div>
          </div>
        </div>

      </div>

    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Business Model Canvas</span>
      <span>Alexander Osterwalder 9-Box Architecture &bull; Seva Sankalp Hackathon 2026</span>
      <span>Page 1 of 2</span>
    </div>
  </div>

  <!-- ==================== PAGE 2: FINANCIAL SUSTAINABILITY & EXECUTION ROADMAP ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">📈</div>
        <div class="header-title-box">
          <h1>BUSINESS ECONOMICS &amp; EXECUTION ROADMAP</h1>
          <p>3-YEAR REVENUE TRAJECTORY &bull; PRICING TIERS &bull; RISK MATRIX &bull; CIIE INCUBATION ASK</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Financial Feasibility</div>
        <div class="header-submeta">Break-Even Month 14 &bull; High Margin SaaS</div>
      </div>
    </div>

    <!-- Section 1: 3-Year Financial Model Table -->
    <div style="margin-bottom:5px;">
      <div class="sec-h2">
        <span>1. Three-Year Financial Forecast &amp; Unit Economics Trajectory</span>
        <span style="font-size:7.2pt; font-weight:700; color:#64748b;">(Values in ₹ INR Lakhs)</span>
      </div>
      <table class="bmc-table">
        <thead>
          <tr>
            <th style="width:22%;">Key Financial Metric</th>
            <th style="width:19%;">Year 1 (Pilot &amp; MDU Incubation)</th>
            <th style="width:19%;">Year 2 (Regional Hospital Expansion)</th>
            <th style="width:19%;">Year 3 (National Scaling &amp; Public Health)</th>
            <th style="width:21%; background:#ccfbf1; color:#0f766e;">CAGR / Growth Driver</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Active Prescribing Doctors</strong></td>
            <td>450 Clinicians</td>
            <td>2,800 Clinicians</td>
            <td>10,500 Clinicians</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">383% YoY via EMR partnerships</td>
          </tr>
          <tr>
            <td><strong>Partner Hospitals &amp; Clinics</strong></td>
            <td>25 Hospitals (2,500 Beds)</td>
            <td>160 Hospitals (16,000 Beds)</td>
            <td>650 Hospitals (65,000 Beds)</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">NABH 5th Edition compliance mandates</td>
          </tr>
          <tr>
            <td><strong>Gross Annual Revenue</strong></td>
            <td>₹48.2 Lakhs ($58K)</td>
            <td>₹284.6 Lakhs ($342K)</td>
            <td>₹1,180.0 Lakhs ($1.42M)</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">395% CAGR across B2B + API</td>
          </tr>
          <tr>
            <td><strong>Operating Expenses (OPEX)</strong></td>
            <td>₹43.2 Lakhs ($52K)</td>
            <td>₹128.5 Lakhs ($155K)</td>
            <td>₹345.0 Lakhs ($415K)</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">High operating leverage (Software margin)</td>
          </tr>
          <tr>
            <td><strong>EBITDA / Net Profit Margin</strong></td>
            <td>₹5.0 Lakhs (10.4%)</td>
            <td>₹156.1 Lakhs (54.8%)</td>
            <td>₹835.0 Lakhs (70.8%)</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">Break-even achieved in Month 14</td>
          </tr>
          <tr>
            <td><strong>Annual Prevented Irrational Courses</strong></td>
            <td>~18,000 courses</td>
            <td>~115,000 courses</td>
            <td>~520,000 courses</td>
            <td style="background:#f0fdfa; font-weight:700; color:#0f766e;">Direct reduction in community AMR pressure</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Section 2: Pricing Tiers & Monetization Structure -->
    <div style="margin-bottom:5px;">
      <div class="sec-h2">
        <span>2. Multi-Tier Commercialization &amp; Pricing Architecture</span>
        <span style="font-size:7.2pt; font-weight:700; color:#64748b;">Transparent Tiered SaaS</span>
      </div>
      <div class="grid-4">
        <div class="card-p2" style="border-top:3px solid #64748b;">
          <div style="font-size:8pt; font-weight:800; color:#1e293b;">COMMUNITY FREE</div>
          <div style="font-size:11pt; font-weight:800; color:#0f766e; margin:2px 0;">₹0 <span style="font-size:7pt; color:#64748b;">/ forever</span></div>
          <p style="font-size:6.8pt; color:#475569;">Up to 50 prescription scans/mo. Full 5-tier deterministic audit, traffic-light triage, standard ICMR guidance. For solo rural practitioners.</p>
        </div>
        <div class="card-p2" style="border-top:3px solid #0f766e; background:#f0fdfa;">
          <div style="font-size:8pt; font-weight:800; color:#0f766e;">CLINIC PRO</div>
          <div style="font-size:11pt; font-weight:800; color:#0f766e; margin:2px 0;">₹999 <span style="font-size:7pt; color:#64748b;">/ doctor / mo</span></div>
          <p style="font-size:6.8pt; color:#475569;">Unlimited scans, branded clinic letterhead, PDF audit clearance slip export, WhatsApp patient regimen instructions, medicolegal vault.</p>
        </div>
        <div class="card-p2" style="border-top:3px solid #0284c7; background:#f0f9ff;">
          <div style="font-size:8pt; font-weight:800; color:#0284c7;">HOSPITAL AMSC</div>
          <div style="font-size:11pt; font-weight:800; color:#0284c7; margin:2px 0;">₹12,500 <span style="font-size:7pt; color:#64748b;">/ 100 beds / mo</span></div>
          <p style="font-size:6.8pt; color:#475569;">Ward-level AWaRe dashboard, automated 48h timeout alerts, pharmacy dispensing integration, NABH 5th Edition compliance export.</p>
        </div>
        <div class="card-p2" style="border-top:3px solid #7c3aed; background:#faf5ff;">
          <div style="font-size:8pt; font-weight:800; color:#7c3aed;">PUBLIC HEALTH</div>
          <div style="font-size:11pt; font-weight:800; color:#7c3aed; margin:2px 0;">₹18 Lakhs <span style="font-size:7pt; color:#64748b;">/ district / yr</span></div>
          <p style="font-size:6.8pt; color:#475569;">District-wide deployment across all PHCs/CHCs, anonymized consumption heatmaps, outbreak surveillance feed for State Health Mission.</p>
        </div>
      </div>
    </div>

    <!-- Section 3: Risk Mitigation Matrix & Incubation Ask -->
    <div class="grid-2">
      <!-- Risk Matrix -->
      <div class="card-p2" style="border-left:3.5px solid #0f766e;">
        <div style="font-size:8pt; font-weight:800; color:#0f766e; margin-bottom:3px; display:flex; justify-content:space-between;">
          <span>🛡️ Strategic Risk Matrix &amp; Defensibility</span>
          <span style="font-size:6.8pt; color:#64748b;">Mitigation Strategy</span>
        </div>
        <p style="font-size:7pt; line-height:1.3; color:#334155; margin-bottom:2px;">
          <strong>Risk 1: Doctor Inertia &amp; Time Pressure:</strong> Mitigated by 5-second camera capture with zero keyboard entry.
        </p>
        <p style="font-size:7pt; line-height:1.3; color:#334155; margin-bottom:2px;">
          <strong>Risk 2: Medicolegal Liability of AI:</strong> Mitigated by 100% deterministic rule isolation; AI never makes medical decisions.
        </p>
        <p style="font-size:7pt; line-height:1.3; color:#334155;">
          <strong>Risk 3: Unreliable Rural Connectivity:</strong> Mitigated by standalone offline edge runtime (&lt; 150MB local container).
        </p>
      </div>

      <!-- CIIE Ask & Roadmap -->
      <div class="card-p2" style="border-left:3.5px solid #0284c7;">
        <div style="font-size:8pt; font-weight:800; color:#0284c7; margin-bottom:3px; display:flex; justify-content:space-between;">
          <span>🎯 CIIE MDU Rohtak Incubation Ask &amp; Milestones</span>
          <span style="font-size:6.8pt; color:#64748b;">₹15 Lakhs Seed Ask</span>
        </div>
        <p style="font-size:7pt; line-height:1.3; color:#334155; margin-bottom:2px;">
          <strong>Month 1&ndash;3 (Clinical Validation):</strong> Deploy in 100-bed hospital in Rohtak/NCR; validate 5,000 OPD prescriptions.
        </p>
        <p style="font-size:7pt; line-height:1.3; color:#334155; margin-bottom:2px;">
          <strong>Month 4&ndash;6 (EMR Partner Integration):</strong> Launch native connector for top Indian EMR; onboard 500 active GPs.
        </p>
        <p style="font-size:7pt; line-height:1.3; color:#334155;">
          <strong>Month 7&ndash;12 (NABH Commercial Launch):</strong> Sign 25 corporate hospital contracts and submit NHM district pilot proposal.
        </p>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Business Model Canvas</span>
      <span>Financial Sustainability &bull; Seva Sankalp Hackathon 2026 &bull; Maharshi Dayanand University</span>
      <span>Page 2 of 2</span>
    </div>
  </div>

</body>
</html>
"""
    temp_dir = os.environ.get("TEMP", r"C:\Users\sanu6\AppData\Local\Temp")
    html_path = os.path.join(temp_dir, "bmc_temp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_temp = os.path.join(temp_dir, "Business_Model_Canvas.pdf")
    user_data = os.path.join(temp_dir, "edge_pdf_profile")
    target_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\Business_Model_Canvas.pdf"

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
        print(f"Generated Business_Model_Canvas.pdf with {len(doc)} pages ({os.path.getsize(target_pdf)} bytes)")
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = rf"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\bmc_p{i+1}.png"
            pix.save(img_path)
            print(f"Saved {img_path}")
    else:
        print("Failed to generate Business_Model_Canvas.pdf")

if __name__ == "__main__":
    build_bmc_pdf()
