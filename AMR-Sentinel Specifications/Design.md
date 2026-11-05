# AMR Sentinel AI — Design System

## 1. Product character

Calm, credible, and fast: a modern clinical SaaS workspace that helps a professional review information under time pressure. It should feel precise rather than alarmist, and visually separate urgent safety findings from ordinary information.

## 2. Visual tokens

| Token | Value | Use |
|---|---|---|
| `ink` | `#102A43` | primary text / navigation |
| `slate` | `#627D98` | secondary text |
| `canvas` | `#F7FAFC` | page background |
| `surface` | `#FFFFFF` | cards / panels |
| `primary` | `#0F766E` | actions / trusted clinical accent |
| `info` | `#2563EB` | links / neutral guidance |
| `review` | `#B45309` | needs-review / amber |
| `urgent` | `#B42318` | urgent-review / red |
| `success` | `#15803D` | no-rule-triggered / green, never “safe” |
| `border` | `#D9E2EC` | dividers / controls |

Use status labels and icons alongside color. Contrast must meet WCAG AA (4.5:1 for normal text).

## 3. Typography and layout

- Font: **Inter** (or system fallback); use tabular numerals for values and scores.
- Base: 16 px; body line-height 1.5; labels 12–14 px medium; H1 30–36 px semibold; H2 20–24 px semibold.
- 8 px spacing scale; max content width 1440 px; 24 px desktop / 16 px mobile gutters.
- Cards: 10–12 px radius, subtle border, minimal shadow. Avoid “glass” effects and dense gradients.

## 4. Primary screens

### Dashboard

Header with organization/demo badge, notification-free utility area, and primary “New audit” action. Main area: welcome/title, sample cases, recent synthetic audits, and de-identified trends. Never display PHI in dashboard previews.

### New audit

Stepper: **Patient context → Prescription → Confirm facts → Review**. Group inputs by clinical meaning; show mandatory/unknown states plainly. The upload card says “Extract to a draft; verify before audit.” Keep a fixed right-side (or mobile bottom) summary of missing data.

### Results

Top summary includes status, “not a prescription” disclaimer, input-confirmation state, and audit time/version. Findings appear in priority order with: severity, concise title, reason, data used, what needs confirmation, evidence link, and clinician acknowledgement. Do not use a single numeric risk score as the primary decision surface.

### Evidence drawer

Shows source organization, title, jurisdiction, publication/review date, rule-set version, cited excerpt/reference locator, and a clear “verify current local guidance” note.

## 5. Components and states

- `StatusBadge`: urgent review / needs review / no rule triggered / incomplete / unavailable.
- `FindingCard`: clear visual priority, never hides lower-priority issues.
- `DataGapCallout`: neutral blue/gray, actionable request for confirmation.
- `EvidenceLink`: external-link icon and source metadata.
- `ConfidenceChip`: extraction confidence only, never clinical confidence.
- Every form control has visible label, help text, error message, focus ring, and keyboard path.
- Respect `prefers-reduced-motion`; use skeletons only for short waits; provide empty/error/retry states.

## 6. Content voice

Use direct, non-judgmental language: “This combination needs review because…” and “Confirm renal function before this check can be completed.” Avoid “approved”, “safe”, “wrong prescription”, or blame. Show uncertainty explicitly.

## 7. Responsive behavior

Desktop uses sidebar navigation and two-column review layout. Tablet collapses the sidebar. Mobile uses a single column, sticky primary action, no horizontal tables, and expandable evidence panels. Minimum tap target: 44 × 44 px.
