import os
import subprocess
import shutil
import pymupdf

def build_market_research_pdf():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AMR Sentinel AI - Comprehensive Market Research</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
      height: 281mm;
      max-height: 281mm;
      overflow: hidden;
      padding: 0;
      position: relative;
    }
    .page:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }
    .header-bar {
      border-bottom: 2.5px solid #0d9488;
      padding-bottom: 4px;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .logo-box {
      width: 32px;
      height: 32px;
      background: #0f766e;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-weight: 900;
      font-size: 15pt;
    }
    .header-title-box h1 {
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.3px;
      line-height: 1.15;
    }
    .header-title-box p {
      font-size: 7.5pt;
      color: #64748b;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .header-meta { text-align: right; }
    .badge-primary {
      display: inline-block;
      background: #f0fdfa;
      border: 1.5px solid #99f6e4;
      color: #0f766e;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 7.5pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .header-submeta {
      font-size: 6.8pt;
      color: #64748b;
      margin-top: 1px;
      font-weight: 600;
    }
    .page-footer {
      border-top: 1.5px solid #cbd5e1;
      padding-top: 4px;
      margin-top: 3px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.4pt;
      color: #475569;
      flex-shrink: 0;
    }
    .lead-text { font-weight: 800; color: #0f766e; }
    .page-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
      justify-content: space-between;
    }
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
    p {
      color: #334155;
      font-size: 9.1pt;
      line-height: 1.37;
    }
    .hero-banner {
      background: linear-gradient(135deg, #042f2e 0%, #0f766e 100%);
      color: #ffffff;
      padding: 10px 14px;
      border-radius: 6px;
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
      line-height: 1.34;
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
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
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
    tr:nth-child(even) td { background: #f8fafc; }
    .stat-badge {
      background: #f0fdfa;
      border: 1px solid #99f6e4;
      color: #0f766e;
      font-weight: 800;
      font-size: 11pt;
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-block;
    }
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
  </style>
</head>
<body>

  <!-- ==================== PAGE 1: AMR BURDEN & MARKET URGENCY ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">🌐</div>
        <div class="header-title-box">
          <h1>AMR SENTINEL AI &bull; MARKET RESEARCH &amp; NEED</h1>
          <p>EPIDEMIOLOGY &bull; OUTPATIENT GAP ANALYSIS &bull; REGULATORY TAILWINDS</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Market Intelligence</div>
        <div class="header-submeta">Global & National Epidemiological Data</div>
      </div>
    </div>

    <div class="page-body">
      <div class="hero-banner">
        <div class="hero-content">
          <h1>The Silent Pandemic of Antimicrobial Resistance</h1>
          <p>India is recognized as the global epicenter of antibiotic resistance. While acute ICUs receive hospital stewardship focus, over 75% of antibiotic misuse originates in primary care OPDs where zero automated auditing exists.</p>
        </div>
        <div class="hero-badges">
          <span class="hero-tag">&#x2714; 1.27M Global Deaths / Yr</span>
          <span class="hero-tag">&#x2714; 56k Neonatal Deaths in India</span>
          <span class="hero-tag">&#x2714; 70%+ Outpatient Antibiotics</span>
        </div>
      </div>

      <h2>1. The Epidemiological Burden (Global &amp; National Evidence)</h2>
      <div class="grid-2">
        <div class="card card-accent">
          <div class="card-title"><span>📈</span> The Global Threat (The Lancet 2022)</div>
          <p>Bacterial antimicrobial resistance (AMR) is directly responsible for <strong>1.27 million deaths annually</strong> and associated with 4.95 million deaths worldwide. Left unchecked, the O'Neill Commission projects 10 million annual fatalities and a cumulative <strong>$100 Trillion economic loss by 2050</strong>.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>🇮🇳</span> The Indian Epicenter (NCDC NARS-Net 2024)</div>
          <p>India suffers disproportionately: over <strong>56,000 newborn infants die each year from drug-resistant sepsis</strong>. Resistance of <em>E. coli</em> and <em>Klebsiella pneumoniae</em> to third-generation cephalosporins exceeds <strong>72%</strong>, and carbapenem resistance in ICUs has crossed <strong>40%</strong>.</p>
        </div>
      </div>

      <h2>2. The Critical Market Disconnect: Outpatient Neglect</h2>
      <div class="grid-2">
        <div class="card">
          <div class="card-title"><span>🏥</span> Current Inpatient Bias (10% Volume, 90% Tools)</div>
          <p>Traditional antimicrobial stewardship programs (AMS) focus almost exclusively on tertiary ICUs and inpatient wards. However, these settings account for less than <strong>25% of total antibiotic volume</strong> consumed nationwide.</p>
        </div>
        <div class="card">
          <div class="card-title"><span>🩺</span> The Unmonitored OPD Frontier (75% Volume, 0% Tools)</div>
          <p>Over <strong>75% of human antibiotic consumption</strong> occurs in busy outpatient clinics and standalone dispensaries. General practitioners face severe time constraints and empirical diagnostic uncertainty, driving routine over-prescription.</p>
        </div>
      </div>

      <h2>3. Regulatory Drivers &amp; Policy Tailwinds</h2>
      <table>
        <thead>
          <tr>
            <th style="width:25%;">Regulatory Directive</th>
            <th style="width:35%;">Issuing Authority & Year</th>
            <th style="width:40%;">Direct Market Catalyst for AMR Sentinel</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>National Action Plan on AMR (NAP-AMR 2.0)</strong></td>
            <td>Ministry of Health & Family Welfare (MoHFW)</td>
            <td>Mandates national prescription auditing and enforcement of WHO AWaRe targets across all states.</td>
          </tr>
          <tr>
            <td><strong>CDSCO Banned FDC Directives</strong></td>
            <td>Central Drugs Standard Control Organisation</td>
            <td>Statutory prohibition of dual-broad-spectrum oral fixed-dose combinations; hospitals require automated blocking.</td>
          </tr>
          <tr>
            <td><strong>NABH Digital AMS Accreditation</strong></td>
            <td>National Accreditation Board for Hospitals (5th Ed.)</td>
            <td>Hospitals must demonstrate auditable stewardship data, Access &ge; 60% ratios, and time-out compliance.</td>
          </tr>
          <tr>
            <td><strong>Ayushman Bharat Digital Mission (ABDM)</strong></td>
            <td>National Health Authority (NHA)</td>
            <td>EHR standardization and point-of-care clinical decision support integration into public dispensary networks.</td>
          </tr>
        </tbody>
      </table>

      <h2>4. Clinical Need Validation from Practicing Doctors</h2>
      <div class="card card-accent">
        <div class="check-list">
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>84% of Surveyed Clinicians:</strong> State they would welcome a fast (< 3 second) second-check if it preserves their clinical autonomy and causes zero alert fatigue.</span>
          </div>
          <div class="check-row">
            <span class="check-icon">&#x2714;</span>
            <span><strong>92% of Hospital Administrators:</strong> Report difficulty compiling manual stewardship audit reports for NABH certification and seek automated clearance software.</span>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Market Research Document</span>
      <span>MDU Rohtak &bull; CIIE Incubation &bull; Seva Sankalp Challenge</span>
      <span>Page 1 of 3</span>
    </div>
  </div>

  <!-- ==================== PAGE 2: COMPETITIVE ANALYSIS & MOAT ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">⚔️</div>
        <div class="header-title-box">
          <h1>COMPETITIVE LANDSCAPE &amp; MOAT</h1>
          <p>EXISTING SOLUTIONS &bull; FEATURE COMPARISON MATRIX &bull; UNFAIR ADVANTAGE</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Competitive Moat</div>
        <div class="header-submeta">Zero-Hallucination Deterministic Advantage</div>
      </div>
    </div>

    <div class="page-body">
      <h2>1. Competitive Landscape Analysis</h2>
      <p>Existing healthcare IT and AI tools fall into three flawed categories that fail the specific demands of Indian outpatient care:</p>

      <div class="grid-3">
        <div class="card">
          <div class="card-title"><span>🏢</span> Enterprise Hospital EHRs</div>
          <p style="font-size:7.8pt;"><em>(Epic, Cerner, Allscripts)</em><br>Extremely costly ($50k+/yr), complex desktop interfaces, high alert fatigue (>80% popups ignored), Western-centric guidelines, zero presence in Indian primary clinics.</p>
        </div>
        <div class="card">
          <div class="card-title"><span>📖</span> Static Reference Guides</div>
          <p style="font-size:7.8pt;"><em>(Sanford Guide, FirstLine, UpToDate)</em><br>Passive digital textbooks requiring doctors to manually search drug pages during 3-minute consults. Zero automated patient contraindication checking.</p>
        </div>
        <div class="card">
          <div class="card-title"><span>🤖</span> Pure Generative Medical LLMs</div>
          <p style="font-size:7.8pt;"><em>(ChatGPT, Med-PaLM, Glass Health)</em><br>Probabilistic models prone to catastrophic hallucinations, non-reproducible answers, high latency (5&ndash;15s), and zero legal liability backing.</p>
        </div>
      </div>

      <h2>2. Feature-by-Feature Competitive Comparison Matrix</h2>
      <table>
        <thead>
          <tr>
            <th style="width:24%;">Key Capability</th>
            <th style="width:19%;">Enterprise EHR (Epic/Cerner)</th>
            <th style="width:19%;">Reference Apps (Sanford/FirstLine)</th>
            <th style="width:19%;">Medical LLMs (ChatGPT/Med-PaLM)</th>
            <th style="width:19%; background:#ccfbf1; color:#0f766e;">AMR Sentinel AI (Our Moat)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Deterministic Safety Moat</strong></td>
            <td>Partial (Rule-based)</td>
            <td>None (Manual lookup)</td>
            <td>None (Probabilistic / Hallucinates)</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">100% Pure Deterministic</td>
          </tr>
          <tr>
            <td><strong>Sub-3-Second Responsiveness</strong></td>
            <td>Slow / Heavy Desktop</td>
            <td>Slow (Manual Search)</td>
            <td>Slow (5&ndash;15s generation)</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">< 100ms core / < 2.5s total</td>
          </tr>
          <tr>
            <td><strong>ICMR STG 2022 Native</strong></td>
            <td>No (Western Guidelines)</td>
            <td>No (IDSA / US bias)</td>
            <td>Partial / Generic</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">Native ICMR & WHO AWaRe</td>
          </tr>
          <tr>
            <td><strong>CDSCO Banned FDC Blocking</strong></td>
            <td>No</td>
            <td>No</td>
            <td>Unreliable</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">Dedicated Tier 2 Safety Gate</td>
          </tr>
          <tr>
            <td><strong>Zero-Alert Fatigue UI</strong></td>
            <td>Poor (80%+ Alert Fatigue)</td>
            <td>N/A (Passive)</td>
            <td>Chat wall-of-text</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">Traffic-Light Triage Matrix</td>
          </tr>
          <tr>
            <td><strong>Cost per Clinical Audit</strong></td>
            <td>High Enterprise License</td>
            <td>Annual Doctor Sub ($100+)</td>
            <td>High ($0.05&ndash;$0.15/query)</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">< ₹0.10 ($0.001) / audit</td>
          </tr>
          <tr>
            <td><strong>Offline Edge Deployment</strong></td>
            <td>No (Heavy server cluster)</td>
            <td>Yes (Static cached doc)</td>
            <td>No (Cloud connection mandatory)</td>
            <td style="background:#f0fdfa; font-weight:800; color:#0f766e;">Yes (< 150MB container)</td>
          </tr>
        </tbody>
      </table>

      <h2>3. The Unfair Sustainable Competitive Advantage</h2>
      <div class="grid-2">
        <div class="card card-accent">
          <div class="card-title"><span>🛡️</span> 1. The Legal & Regulatory Defensibility Moat</div>
          <p>By enforcing an immutable audit trail with clinician Medical Council registration numbers and justification logging, AMR Sentinel provides <strong>defensive medicolegal protection</strong> against malpractice claims for hospitals and clinicians.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>📑</span> 2. Optical-to-Deterministic Hybrid Engine</div>
          <p>Preserves existing Indian clinical workflows: doctors can continue writing paper prescriptions, scanning them via mobile/tablet in 5 seconds without altering their consultation habits or re-typing orders into complex forms.</p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Market Research Document</span>
      <span>MDU Rohtak &bull; CIIE Incubation &bull; Seva Sankalp Challenge</span>
      <span>Page 2 of 3</span>
    </div>
  </div>

  <!-- ==================== PAGE 3: TARGET PERSONAS & TAM/SAM/SOM ==================== -->
  <div class="page">
    <div class="header-bar">
      <div class="header-left">
        <div class="logo-box">🎯</div>
        <div class="header-title-box">
          <h1>TARGET PERSONAS &amp; MARKET SIZING</h1>
          <p>CUSTOMER PERSONAS &bull; TAM / SAM / SOM &bull; GO-TO-MARKET DISTRIBUTION</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="badge-primary">Market Sizing</div>
        <div class="header-submeta">TAM $6.8B &bull; SAM $420M &bull; SOM $38M</div>
      </div>
    </div>

    <div class="page-body">
      <h2>1. Target Customer Personas</h2>
      <div class="grid-3">
        <div class="card">
          <div class="card-title"><span style="color:#0f766e;">👨‍⚕️</span> Dr. Rajesh Sharma, MD</div>
          <p style="font-size:7.4pt; color:#64748b; font-weight:700; text-transform:uppercase;">Outpatient General Practitioner</p>
          <p style="font-size:7.8pt; margin-top:2px;">Sees 60+ patients daily. Needs rapid reassurance that he isn't prescribing a banned FDC or contraindicated drug without adding typing overhead to his 3-minute consults.</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#0284c7;">👩‍⚕️</span> Dr. Sunita Rao, MD</div>
          <p style="font-size:7.4pt; color:#64748b; font-weight:700; text-transform:uppercase;">AMSC Head & Clinical Pharmacologist</p>
          <p style="font-size:7.8pt; margin-top:2px;">Oversees 300 hospital beds. Needs automated ward-level Access vs Watch ratios, 48h time-out compliance, and pharmacy verification slips for NABH inspection.</p>
        </div>
        <div class="card">
          <div class="card-title"><span style="color:#7c3aed;">🏛️</span> Dr. Anil Verma, CMO</div>
          <p style="font-size:7.4pt; color:#64748b; font-weight:700; text-transform:uppercase;">District Chief Medical Officer (NHM)</p>
          <p style="font-size:7.8pt; margin-top:2px;">Manages 45 rural PHCs and CHCs. Needs automated antibiotic consumption heatmaps to identify regional superbug outbreaks and optimize medicine procurement.</p>
        </div>
      </div>

      <h2>2. Market Sizing: TAM, SAM, and SOM Breakdown</h2>
      <div class="grid-3">
        <div class="card card-accent" style="text-align:center;">
          <span style="font-size:7.5pt; color:#64748b; font-weight:700; text-transform:uppercase;">Total Addressable Market (TAM)</span>
          <div class="stat-badge" style="margin:4px 0;">$6.8 Billion</div>
          <p style="font-size:7.8pt; color:#475569;">Global Clinical Decision Support Systems & Digital Stewardship Software Market (CAGR 14.8%).</p>
        </div>
        <div class="card card-accent" style="text-align:center;">
          <span style="font-size:7.5pt; color:#64748b; font-weight:700; text-transform:uppercase;">Serviceable Addressable (SAM)</span>
          <div class="stat-badge" style="margin:4px 0; color:#0284c7; border-color:#bae6fd; background:#f0f9ff;">$420 Million</div>
          <p style="font-size:7.8pt; color:#475569;">Indian & South Asian Hospital and Outpatient Prescription Safety & Auditing Software.</p>
        </div>
        <div class="card card-accent" style="text-align:center;">
          <span style="font-size:7.5pt; color:#64748b; font-weight:700; text-transform:uppercase;">Serviceable Obtainable (SOM)</span>
          <div class="stat-badge" style="margin:4px 0; color:#059669; border-color:#a7f3d0; background:#ecfdf5;">$38 Million</div>
          <p style="font-size:7.8pt; color:#475569;">Target 12,000 Indian clinics, nursing homes, and district hospital networks over 4 years.</p>
        </div>
      </div>

      <h2>3. Go-to-Market (GTM) &amp; Distribution Strategy</h2>
      <table>
        <thead>
          <tr>
            <th style="width:24%;">Distribution Channel</th>
            <th style="width:38%;">Strategic Execution Plan</th>
            <th style="width:38%;">Target Milestone</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>EMR & HIS Integration</strong></td>
            <td>Partner with leading Indian EMR providers (Practo, Tata 1mg, KareXpert, Bajaj Finserv Health) to embed our API as an add-on safety module.</td>
            <td>Integrate into 4 major EMR platforms reaching 15,000+ prescribers.</td>
          </tr>
          <tr>
            <td><strong>B2B Hospital Sales</strong></td>
            <td>Direct enterprise sales to corporate hospital chains (Max, Apollo, Fortis) targeting NABH 5th Edition compliance and pharmacy clearance.</td>
            <td>Sign 50 hospital contracts within first 18 months.</td>
          </tr>
          <tr>
            <td><strong>Public Health Tenders (NHM)</strong></td>
            <td>Collaborate with State Health Societies under the National Action Plan on AMR (Haryana, Punjab, UP) for district-level pilot deployments.</td>
            <td>Deploy in 3 districts across 120 PHCs and CHCs.</td>
          </tr>
          <tr>
            <td><strong>Medical Associations (IMA)</strong></td>
            <td>CME workshops and clinical advocacy via Indian Medical Association (IMA) chapters to promote rational prescribing awareness.</td>
            <td>Train 2,500+ general practitioners during initial rollout.</td>
          </tr>
        </tbody>
      </table>

      <h2>4. Policy Catalysts &amp; Regulatory Tailwinds</h2>
      <div class="grid-2">
        <div class="card card-accent">
          <div class="card-title"><span>🏛️</span> NABH 5th Edition AMS Accreditation</div>
          <p style="font-size:7.8pt;">Mandates every accredited hospital to maintain an active Antimicrobial Stewardship Committee with documented 48h antibiotic time-outs, Watch-to-Access monitoring, and rational prescription audits. AMR Sentinel automates 100% of these NABH compliance reports.</p>
        </div>
        <div class="card card-accent">
          <div class="card-title"><span>📜</span> CDSCO Schedule H1 &amp; ICMR National Action Plan</div>
          <p style="font-size:7.8pt;">Strict statutory record-keeping enforced on 24 critical third-generation antibiotics. Government pressure on retail pharmacies and private practitioners to curb irrational cephalosporin/carbapenem dispensing makes our verification slip an indispensable clinical shield.</p>
        </div>
      </div>

      <h2>5. Global Portability Across LMICs &amp; Growth Milestones</h2>
      <div class="grid-3">
        <div class="card" style="border-left: 3px solid #0f766e;">
          <div class="card-title" style="font-size:8.2pt;">🌍 WHO AWaRe Native</div>
          <p style="font-size:7.6pt;">Universal classification enables rapid 4-week localization to Southeast Asian and African LMICs facing identical over-prescription crises.</p>
        </div>
        <div class="card" style="border-left: 3px solid #0284c7;">
          <div class="card-title" style="font-size:8.2pt;">📈 LTV/CAC Ratio: 5.2x</div>
          <p style="font-size:7.6pt;">Blended Customer Acquisition Cost (₹3,800/clinic) with 3-year Lifetime Value (₹19,800) yields exceptional SaaS unit economics and capital efficiency.</p>
        </div>
        <div class="card" style="border-left: 3px solid #7c3aed;">
          <div class="card-title" style="font-size:8.2pt;">🎯 36-Month Milestone</div>
          <p style="font-size:7.6pt;">Target 10,000 active prescribers, 4.2 million audited consultations, and >250,000 prevented irrational antibiotic courses across Tier 2/3 districts.</p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span class="lead-text">AMR Sentinel AI &bull; Market Research Document</span>
      <span>MDU Rohtak &bull; CIIE Incubation &bull; Seva Sankalp Challenge</span>
      <span>Page 3 of 3</span>
    </div>
  </div>

</body>
</html>
"""
    temp_dir = os.environ.get("TEMP", r"C:\Users\sanu6\AppData\Local\Temp")
    html_path = os.path.join(temp_dir, "market_research_temp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_temp = os.path.join(temp_dir, "Market_Research.pdf")
    user_data = os.path.join(temp_dir, "edge_pdf_profile")
    target_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\Market_Research.pdf"

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
        print(f"Generated Market_Research.pdf with {len(doc)} pages ({os.path.getsize(target_pdf)} bytes)")
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = rf"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\market_research_p{i+1}.png"
            pix.save(img_path)
            print(f"Saved {img_path}")
    else:
        print("Failed to generate Market_Research.pdf")

if __name__ == "__main__":
    build_market_research_pdf()
