# Resume Intelligence Roadmap Design

Date: 2026-06-01

## Goal

Evolve Resume Intelligence from a workflow-first plugin into a more reliable career assistant while preserving the current working behavior.

The roadmap should support three important use cases without splitting the project into separate products:

- Personal local assistant for the user's resume, interview prep, LinkedIn updates, and job search.
- Reusable open-source plugin that other Codex, Claude, and Cursor users can install and understand.
- Enterprise-safe assistant for private Jira, Confluence, GitHub Enterprise, local documents, and confidential project evidence.
- Visual resume designer that can produce impressive recruiter-facing templates while preserving ATS-safe application files.
- Career and interview coach that helps the user improve positioning, rehearse stories, close gaps, and prepare for interviews.

## Compatibility Rule

Current behavior remains the default.

New features must be additive unless the change prevents a privacy, credential, or disclosure risk. Existing output names, skill triggers, and the normal `$resume-intelligence` flow should keep working. New stricter checks should report warnings first instead of blocking resume generation, except when the output would expose credentials, secrets, private URLs, or unapproved confidential details.

## Non-Goals

- Do not replace the current agent-guided workflow with a rigid automation-only CLI.
- Do not build custom OAuth, credential storage, or background syncing.
- Do not scrape LinkedIn behind login or bypass platform controls.
- Do not upload private content, profile photos, internal documents, or resume drafts to third-party design tools automatically.
- Do not require Jira, Confluence, GitHub Enterprise, Figma, Canva, or browser tools for basic local use.
- Do not make generated claims more confident than the source evidence supports.

## Recommended Architecture

Use a layered roadmap with a shared foundation.

```text
Resume Intelligence
|-- Foundation reliability layer
|-- Personal workflow layer
|-- Visual template layer
|-- Career and interview coach layer
|-- Open-source usability layer
|-- Enterprise safety layer
`-- Advanced automation layer
```

The foundation layer should improve every workflow. Personal, visual, coaching, open-source, and enterprise features should then reuse the same source inventory, evidence model, redaction checks, and quality gates.

## Foundation Reliability Layer

The foundation layer protects current behavior while making runs more repeatable.

### Source Inventory Helper

Add a deterministic local helper that recursively inventories approved folders and writes structured rows for `source-inventory.md`.

Responsibilities:

- Enumerate all nested files under approved roots.
- Classify each file as scanned, skipped unsupported format, skipped binary, skipped too large, skipped permission, duplicate, or needs user input.
- Record relative path, extension, size, modified date when available, and extraction method.
- Keep the current agent workflow as the default caller. The helper should assist the agent, not replace agent judgment.

### Evidence Normalization

Define a structured evidence schema that can be reused by templates and scoring.

Core fields:

- Source context ID.
- Employer or organization.
- Role title and date range.
- Project or workstream.
- User ownership and responsibilities.
- Technologies and platforms.
- Scale, impact, and metrics.
- Confidence level.
- Disclosure level.
- Resume use decision.
- Missing user question when evidence is incomplete.

This can start as a documented JSON shape and later become a script-generated `evidence.json` companion to `evidence.md`.

### Run Summary

Create a concise `run-summary.md` output for every substantial run.

It should show:

- Requested goal.
- Sources approved.
- Sources scanned.
- Tools or commands used.
- Files skipped and why.
- Outputs created.
- Sensitive details awaiting approval.
- Missing dates, metrics, ownership, or project outcomes.
- Recommended next user answers.

### Quality Gates

Add reusable checks before final delivery:

- ATS parse risk.
- Recruiter first-page strength.
- Unsupported or weak claims.
- Keyword coverage for job-specific runs.
- Page-length strategy.
- Missing metrics and vague impact.
- Confidentiality and redaction risk.
- Tool coverage, especially whether approved folders were recursively inventoried.

Quality gates should be visible in `resume-scorecard.md` and the final response. They should not block normal generation unless there is a credential or privacy risk.

## Personal Workflow Layer

Personal workflows should make the plugin more useful for the user's own career system.

### Career Master Run

Add guidance for a complete career reconstruction run that produces:

- `detailed-resume.md`
- `professional-resume.md`
- `resume-scorecard.md`
- `project-interview-briefs.md`
- `technical-stack-interview-guide.md`
- `interview-prep-pack.md`
- `linkedin-recommendations.md`
- `run-summary.md`

This mode should focus on timeline accuracy, role responsibilities, key projects, measurable impact, technical depth, and interview story readiness.

### Missing-Information Loop

After initial evidence extraction, the plugin should ask targeted questions instead of guessing.

High-priority question categories:

- Exact role dates.
- Title changes and promotion timing.
- Personal ownership boundaries.
- Team size, system scale, and user/customer scope.
- Before-and-after metrics.
- Sensitive names that must be anonymized.
- Strongest stories for leadership, conflict, failure, ambiguity, and technical depth.

### Job Search and Scoring

Improve job-search support by separating:

- Strong matches: high evidence fit and low gap risk.
- Good matches: strong fit with manageable gaps.
- Stretch matches: possible but require positioning or learning.
- Weak matches: meaningful must-have gaps.

Scoring should remain transparent and cite job source URLs or user-provided posting text when available.

## Visual Template Layer

The visual template layer should make recruiter-facing output more impressive without weakening ATS safety.

### Two-Surface Resume Strategy

Keep two resume surfaces:

- `ats-resume.docx`: clean, single-column, text-first, and suitable for job portals.
- `designed-resume.html`, `designed-resume.pdf`, `designed-resume.docx`, or Figma/Canva handoff: visually stronger output for recruiters, referrals, networking, and portfolio-style sharing.

The visual layer must not become the only application resume. The ATS-safe version remains the default submission file.

### Visual Template Profiles

Add named visual profiles so the user can choose a direction without redesigning from scratch.

Recommended profiles:

- Modern technical: strong for senior, staff, principal, cloud, platform, AI, and backend engineering profiles.
- Executive compact: strong for engineering manager, director, principal, and cross-functional leadership profiles.
- Open-source builder: highlights public projects, GitHub work, community contribution, and product/platform impact.
- Enterprise transformation: emphasizes modernization, reliability, scale, governance, migration, and operational impact.
- Minimal ATS-plus: a conservative but more polished version for users who want one file close to ATS-safe.

Each profile should define typography, spacing, section priority, accent color, project treatment, skill grouping, and optional profile-picture behavior.

### Visual Quality Gates

Before delivering an impressive template, check:

- First-page role fit is obvious within a recruiter skim.
- Header, summary, skills, and top experience sections are visually distinct.
- Important text is not placed only in images, headers, footers, or complex shapes.
- Profile picture is optional and user-approved.
- Exported PDF or rendered pages do not clip, overlap, or shrink text too far.
- Visual design does not hide unsupported claims or keyword stuffing.
- Canva/Figma upload remains manual or explicitly approved.

### Visual Tool Handoff

The plugin should prefer local HTML/PDF for high-fidelity visual output. Figma and Canva should be treated as optional handoff or refinement tools unless the user explicitly approves using them.

The handoff should include:

- Sanitized copy blocks.
- Section hierarchy.
- Color and typography guidance.
- Profile-picture placement guidance.
- Export instructions.
- Privacy and upload warnings.

## Career and Interview Coach Layer

The coach layer should help the user improve career positioning and interview readiness, not only generate documents.

### Career Positioning Coach

Add a coaching workflow that reviews the evidence-backed profile and recommends:

- Target role families and seniority level.
- Strongest positioning themes.
- Weak or missing proof points.
- Skills to emphasize, learn, or de-emphasize.
- LinkedIn headline and About-section direction.
- Portfolio, open-source, certification, or project gaps.
- Resume and interview stories that best support the target role.

Recommendations should distinguish evidence-backed strengths from user-input-needed assumptions.

### Interview Coaching Loop

Add an iterative preparation loop:

1. Generate project, behavioral, technical, system-design, and recruiter-screen questions.
2. Ask the user to answer selected questions.
3. Review answers for clarity, depth, structure, metrics, and risk.
4. Rewrite or outline stronger answers without inventing facts.
5. Track follow-up study items and missing evidence.

The coach should use the detailed resume, evidence log, interview prep pack, and job posting when available.

### Interview Readiness Scorecard

Create an optional scorecard that rates readiness by category:

- Resume walk-through.
- Technical depth.
- System design.
- Behavioral stories.
- Leadership and influence.
- Metrics and impact.
- Role-specific job requirements.
- Communication clarity.
- Confidentiality-safe storytelling.

The scorecard should produce practical next steps, not just a score.

### Coaching Artifacts

Potential outputs:

- `career-positioning.md`
- `interview-coach-plan.md`
- `mock-interview-questions.md`
- `answer-review.md`
- `interview-readiness-scorecard.md`
- `study-plan.md`

## Open-Source Usability Layer

The plugin should be easier for other users to install, test, and trust.

### Setup Doctor

Add a setup checklist or script that reports environment readiness.

Checks:

- Codex plugin manifest validation.
- Claude plugin manifest validation.
- Skill validation.
- Optional tools available: GitHub, browser, documents, Figma, Confluence, Jira, web search, LibreOffice.
- Local marketplace path configured.
- Plugin cachebuster version visible.

The setup doctor should never require private credentials. It should report missing optional tools as recommendations, not failures.

### Sample Runs

Add fake-data examples under a safe examples folder.

Suggested examples:

- Public GitHub only.
- Local documents only.
- Job posting tailoring.
- Detailed interview resume.
- Enterprise sanitized summary using mock internal names.

Examples should not contain real private career data.

### User-Facing Prompt Library

Add prompt examples for common workflows:

- Build my first resume.
- Create detailed interview resume.
- Tailor to this job.
- Search and score jobs.
- Improve my LinkedIn profile.
- Prepare for staff/principal engineer interviews.
- Run in safe local-only mode.

## Enterprise Safety Layer

Enterprise features should make private-source usage safer and more auditable.

### Source Identity Separation

Keep separate source contexts for:

- Public GitHub Cloud.
- GitHub Enterprise hosts.
- Jira sites.
- Confluence sites.
- Local document roots.
- LinkedIn export or pasted profile content.
- Job postings and job search results.

Each context should retain host, identity, credential boundary label, scope, disclosure level, quoting rule, and status.

### Disclosure Approval Queue

Add a review artifact that lists details requiring explicit user approval before they appear in final public-facing outputs.

Approval categories:

- Internal project names.
- Customer names.
- Private repository names.
- Jira IDs.
- Confluence page titles.
- Internal URLs.
- Exact internal metrics.
- Enterprise hostnames.
- Confidential architecture details.

Default final output should use sanitized summaries until approval is granted.

### Audit-Friendly Logs

Strengthen `tool-usage-log.md` and `source-inventory.md` so a user can answer:

- What did the tool actually read?
- What did it skip?
- Which connector or command was used?
- Which source produced each claim?
- Which details were sanitized?
- Which claims still need confirmation?

## Advanced Automation Layer

Automation should come after the foundation stabilizes.

Possible additions:

- `resume-runner` helper that creates a run folder, copies templates, inventories sources, and prepares empty output files.
- `evidence-normalizer` helper that turns structured evidence JSON into Markdown tables.
- `scorecard-checker` helper that validates quality-gate completeness.
- `docx-render-check` wrapper for local DOCX structural and visual QA when render tools are available.
- Job-search pipeline that records source URLs, search date, job text availability, and match score.

These helpers should be optional. The skill should still work with pasted content and manual files.

## Phased Roadmap

### Phase 1: Protect Current Behavior

- Document the compatibility rule.
- Add roadmap and validation scenarios.
- Add warning-only quality-gate language.
- Ensure existing prompt examples still work.

### Phase 2: Deterministic Source and Evidence Helpers

- Add local source inventory helper.
- Add evidence schema reference.
- Add `run-summary.md` template.
- Add dry-run scenarios for recursive inventory and missing-info loops.

### Phase 3: Guided Personal Workflow

- Add career master run guidance.
- Strengthen `detailed-resume.md` and interview-prep linkages.
- Add missing-information loop template.
- Improve job-search match categories.

### Phase 4: Visual Templates and Coaching

- Add named visual template profile guidance.
- Add visual quality gates.
- Add career positioning coach workflow.
- Add interview coaching loop and readiness scorecard templates.
- Add dry-run scenarios for impressive visual resumes and coaching artifacts.

### Phase 5: Open-Source Experience

- Add setup doctor checklist or script.
- Add fake sample runs.
- Add prompt library.
- Improve README onboarding around safe local-only mode and optional tools.

### Phase 6: Enterprise Redaction and Audit Hardening

- Add disclosure approval queue template.
- Strengthen source identity separation checks.
- Add enterprise dry-run scenarios with mock private details.
- Add final-output redaction review guidance.

### Phase 7: Advanced Automation

- Add optional runner helpers.
- Add structured evidence JSON support.
- Add scorecard completeness checks.
- Add job-search pipeline improvements.
- Add richer generated QA reports.

## Testing and Validation

Each phase should include validation that proves current behavior still works.

Required checks:

- Codex plugin validation.
- Skill validation.
- Claude marketplace validation.
- Claude plugin validation.
- Placeholder scan for incomplete roadmap markers.
- `git diff --check`.
- Dry-run scenario updates.

Behavioral checks:

- Existing general resume prompt still works.
- Existing visual resume prompt still works.
- Existing detailed interview resume prompt still works.
- Visual template selection keeps a separate ATS-safe application file.
- Career and interview coaching artifacts use evidence-backed claims and ask for missing facts.
- Existing job-specific resume and cover-letter flow still works.
- Local-only mode works without optional enterprise tools.
- Enterprise mock scenario preserves redaction and provenance.

## Implementation Boundaries

Implementation should be split into small plans. The first implementation plan should focus on Phase 1 and Phase 2 only, because those phases create the foundation for the remaining roadmap without disrupting current behavior.

Do not begin implementation until this spec is reviewed and approved.
