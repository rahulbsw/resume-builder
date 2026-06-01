# Resume Intelligence Dry-Run Scenarios

Use these scenarios to validate the skill workflow without live credentials.

## Scenario 1: Public GitHub Only

Input:

- Goal: general resume.
- Years of experience: 8.
- Target role: senior backend engineer.
- Source context: `github-public`.
- Public GitHub evidence: authored PRs to an open-source API gateway, issue triage, release notes, and repository maintainer notes.

Expected outputs:

- `source-inventory.md` lists all approved source contexts before evidence extraction.
- `tool-usage-log.md` records the public GitHub tool or manual export used.
- `evidence.md` includes public source context and public quoting rule.
- `draft-resume.md` includes open-source contribution section.
- `detailed-resume.md` is created when interview prep or full timeline detail is requested.
- `resume-scorecard.md` recommends one or two pages based on evidence density and flags ATS risks before final wording.
- `professional-resume.md` uses public repository context only when evidence confirms visibility.

## Scenario 2: GitHub Enterprise Plus Public GitHub

Input:

- Goal: role-specific resume.
- Years of experience: 12.
- Target role: staff platform engineer.
- Source contexts: `github-enterprise` and `github-public`.
- Public GitHub source context: `github-public-rajain5`, type `github-public`, host `github.com`, identity `rajain5`, credential boundary `public-web-or-public-github-connector`, disclosure `public`, quoting rule `ask-before-use`.
- Enterprise GitHub source context: `github-enterprise-work`, type `github-enterprise`, host `ghe.example.internal`, identity `work-user@example.com`, credential boundary `enterprise-connector-work`, disclosure `internal-summary-only`, quoting rule `summarize-only`.
- Enterprise evidence: private PR summaries for CI/CD modernization, service reliability, and migration work.
- Public evidence: open-source Kubernetes operator contributions.

Expected outputs:

- `source-inventory.md` lists public and enterprise GitHub contexts separately.
- `tool-usage-log.md` records separate tool attempts for public GitHub and Enterprise GitHub.
- `evidence.md` preserves separate source contexts.
- `evidence.md` contains separate source-context rows with distinct host, identity, credential boundary, disclosure level, and quoting rule.
- Enterprise repository names are summarized unless approved.
- Public open-source contributions are visible in a separate section.
- Final bullets combine career impact without losing provenance in the evidence log.
- No credentials, tokens, cookies, private URLs, Enterprise hostnames, private repository names, PR URLs, or raw internal identifiers appear in final user-facing outputs unless explicitly approved.
- Claims from public GitHub and Enterprise GitHub reference their own source-context IDs and are not merged into a single provenance entry.

## Scenario 3: Jira, Confluence, and Local Documents

Input:

- Goal: general resume and LinkedIn recommendations.
- Years of experience: 10.
- Target role: engineering manager or principal engineer.
- Source contexts: `jira`, `confluence`, and `local-docs`.
- Jira evidence: completed epics, incidents, and platform tickets.
- Confluence evidence: design documents and launch reviews.
- Local documents: project summaries and architecture notes.

Expected outputs:

- `source-inventory.md` includes every nested file under the approved local document folder, not only the first subfolder.
- `source-inventory.md` records scanned, skipped unsupported, permission, binary, duplicate, and needs-user-input statuses when applicable.
- `tool-usage-log.md` records the recursive local inventory command, plus Jira and Confluence tool attempts or manual exports.
- `evidence.md` includes issue and page source contexts with internal-summary-only disclosure.
- `professional-resume.md` uses sanitized project descriptions.
- `linkedin-recommendations.md` avoids Jira IDs and Confluence page titles.

## Scenario 4: Job-Posting-Specific Resume and Cover Letter

Input:

- Goal: job-posting-specific resume and cover letter.
- Years of experience: 9.
- Target posting: senior cloud platform engineer requiring Kubernetes, Terraform, observability, incident management, and cross-functional leadership.
- Evidence: mixed public GitHub, enterprise GitHub summaries, and local design documents.

Expected outputs:

- `source-inventory.md` and `tool-usage-log.md` include the job posting source or job-posting URL retrieval attempt.
- `gap-analysis.md` classifies requirements as strong match, partial match, gap, or needs user input.
- `resume-scorecard.md` maps required and preferred posting keywords to evidence, gaps, or needed user input.
- `targeted-resume.md` reorders skills and bullets to match the posting.
- `cover-letter.md` uses only supported achievements.
- Missing requirements are addressed honestly.

## Scenario 5: Designed Resume With Optional Profile Picture

Input:

- Goal: professional designed resume.
- Years of experience: 11.
- Target role: senior engineering leader.
- Source contexts: `linkedin-profile`, `local-docs`, and `profile-picture`.
- LinkedIn evidence: exported profile content, pasted profile content, user notes, or user-approved manually provided public profile text; no automated LinkedIn scraping.
- Profile-picture evidence: user-provided local image path with permission to include it in visual resume output.

Expected outputs:

- `source-inventory.md` records LinkedIn content as user-provided and the profile picture as a local user-approved source.
- `evidence.md` records the `linkedin-profile` source form and confirms no automated scraping.
- `evidence.md` records the `profile-picture` source context with local path or attachment label, user approval, and embed/link/omit preference.
- `professional-resume.md` remains ATS-friendly and text-first.
- `designed-resume.html` includes sanitized resume content and a profile-picture slot.
- `designed-resume.html` does not fetch, search for, scrape, or upload profile pictures.
- Profile picture is referenced only through the user-approved local path or left as a replacement placeholder.
- Output guidance explains browser-to-PDF export and copy/import into Canva, Figma, Google Docs, or Word.
- Guidance states third-party design import is manual only and profile pictures/private resume content are not uploaded automatically.
- If DOCX is requested, `ats-resume.docx` is created as the application version and `designed-resume.docx` is created only as a recruiter/referral companion.
- `docx-render-review.md` records the selected DOCX template profile and render QA result or renderer limitation.

## Scenario 6: Recursive Workspace Documents

Input:

- Goal: evidence extraction and resume update.
- Years of experience: 11.
- Target role: staff platform engineer.
- Local root contains nested folders: `platform/architecture/`, `platform/incidents/`, `platform/launches/`, `opensource/`, and `management/`.
- Relevant documents are spread across multiple subfolders and include Markdown, text, JSON, DOCX, PDF, and unsupported binary files.

Expected outputs:

- `source-inventory.md` proves the full approved root was recursively enumerated with `rg --files` or documented fallback.
- Files from every nested folder appear in the inventory.
- Unsupported, binary, inaccessible, duplicate, or too-large files are listed with reasons instead of omitted.
- `tool-usage-log.md` includes the actual local inventory command and extraction methods used.
- `evidence.md` uses only scanned or manually summarized files for claims.

## Scenario 7: Interview Preparation From Key Projects

Input:

- Goal: interview preparation.
- Years of experience: 12.
- Target role: staff or principal engineer.
- Evidence: three high-confidence platform projects, one open-source contribution, and one low-confidence leadership claim needing confirmation.
- Target stack: Kubernetes, Terraform, Java, microservices, observability, incident response, and cloud architecture.

Expected outputs:

- `project-interview-briefs.md` includes selected projects with 30-second pitch, 90-second pitch, STAR story, architecture, tradeoffs, impact, and likely follow-up questions.
- `detailed-resume.md` includes full chronology, role responsibilities, project workstreams, impact, metrics, and questions for missing dates or outcomes.
- `technical-stack-interview-guide.md` maps each target technology to evidence level, architecture role, tradeoffs, alternatives, failure modes, and interview questions.
- `interview-prep-pack.md` includes recruiter screen, resume walk-through, behavioral story bank, technical deep dives, system design prompts, questions to ask, and study plan.
- Confidential enterprise names and raw internal identifiers remain sanitized.
- Low-confidence claims are marked for confirmation instead of used as polished answers.

## Scenario 8: Job Search And Match Scoring

Input:

- Goal: search jobs matched to resume profile.
- Years of experience: 10.
- Target role: senior or staff cloud platform engineer.
- Target technologies: Kubernetes, Terraform, observability, Java, distributed systems, CI/CD, incident management.
- Work model: remote or hybrid in the United States.

Expected outputs:

- Live job search or user-provided job listings are recorded in `source-inventory.md` with search date, query, source URL, company, role, location, and posting date when available.
- `tool-usage-log.md` records the web search or job-board tool attempts.
- `job-match-report.md` scores each accessible listing using role/seniority, required technical skills, domain/platform fit, impact/leadership fit, location/work model, and gap risk.
- Listings that are expired, inaccessible, or missing full text are marked and not treated as validated opportunities.
- `gap-analysis.md`, `targeted-resume.md`, `cover-letter.md`, and `interview-prep-pack.md` use evidence-backed keywords only.

## Scenario 9: Professional DOCX Template Quality

Input:

- Goal: professional DOCX resume template.
- Years of experience: 12.
- Target role: staff platform engineer.
- User feedback: previous DOCX was too plain and not impressive.
- Evidence: sanitized professional resume content with strong technical projects and skill categories.

Expected outputs:

- `ats-resume.docx` uses the `ats-safe` profile, standard section headings, no profile photo, no sidebar, and no important content hidden in headers or footers.
- `designed-resume.docx` uses `modern-technical` or `executive-compact` with stronger typography, restrained accent color, compact skill treatment, and clear first-page role fit.
- `designed-resume.html` remains available for Canva/Figma/manual design import when requested.
- `docx-render-review.md` documents visual QA or states that LibreOffice/rendering was unavailable.
- The final response tells the user which file to submit to ATS and which file to use for recruiter/referral sharing.

## Scenario 10: Visual Tool Resume Handoff

Input:

- Goal: improve visual quality beyond DOCX.
- User feedback: HTML resume looked good, but DOCX did not have the same visual quality.
- Requested tools: Canva, Figma, or available Codex/Claude visual tooling.
- Evidence: sanitized professional resume content and optional user-approved profile photo.

Expected outputs:

- `ats-resume.docx` remains the ATS/application file.
- `designed-resume.html` is treated as the high-fidelity visual source of truth.
- `designed-resume.pdf` is produced when browser/PDF export tooling is available or requested.
- `visual-design-review.md` records browser/PDF/Figma/Canva QA status and any limitations.
- `visual-tool-handoff.md` provides Canva copy blocks, Figma handoff notes, and privacy/upload status.
- Figma tools are used only when a target Figma file is provided or approved.
- Canva upload is not automatic; the workflow provides a manual/import handoff unless the user explicitly approves third-party upload.

## Scenario 11: Detailed Interview Resume

Input:

- Goal: detailed interview resume and master career timeline.
- Years of experience: 14.
- Evidence: LinkedIn export, current resume, local project documents, GitHub Enterprise summaries, public GitHub contributions, and Jira/Confluence exports.
- Known gaps: missing exact dates for two roles, missing incident-reduction metric, unclear ownership boundary on one migration, and unapproved internal project names.

Expected outputs:

- `detailed-resume.md` includes a full work timeline with dates, companies, titles, team/product scope, technologies, source evidence, and confidence.
- Each role includes responsibilities, systems owned, leadership/collaboration scope, key projects, decisions, tradeoffs, impact, and metrics.
- Metrics are captured in a metrics bank with confidence and disclosure status.
- Missing information is captured as direct user questions, not invented.
- Sensitive enterprise names, customer names, private repository names, internal URLs, Jira IDs, and Confluence titles are sanitized or marked for approval.
- `interview-prep-pack.md` references `detailed-resume.md` for the resume walkthrough and story selection.
- `resume-scorecard.md` lists detailed-resume gaps that need user confirmation before final interview prep.

## Scenario 12: Compatibility And Warning-Only Quality Gates

Input:

- Goal: general resume and interview prep.
- Years of experience: 12.
- Sources: pasted LinkedIn profile, local documents, and public GitHub summary.
- Limitation: local inventory helper is unavailable.
- Evidence gaps: missing exact metric and one unclear ownership boundary.

Expected outputs:

- Existing outputs such as `source-inventory.md`, `tool-usage-log.md`, `evidence.md`, `draft-resume.md`, `professional-resume.md`, and interview-prep files still use the existing workflow.
- `tool-usage-log.md` records that the optional inventory helper was unavailable.
- `run-summary.md` lists the limitation and missing user questions.
- `resume-scorecard.md` treats missing metrics and weak ownership as warnings.
- Resume generation continues unless credentials, secrets, private URLs, or unapproved confidential details would be exposed.

## Scenario 13: Deterministic Local Source Inventory

Input:

- Goal: evidence extraction and detailed interview resume.
- Local root contains nested folders with Markdown, JSON, DOCX, PDF, PNG, and unsupported custom files.
- User approves the local root for inventory.

Expected outputs:

- `source-inventory.md` is produced or seeded from `scripts/inventory_sources.py`.
- Every nested file appears in the inventory.
- Text-oriented files are marked scanned for first-pass review.
- DOCX and PDF files are marked needs-user-input or later updated when document tooling extracts text.
- Binary and unsupported files are listed with reasons.
- `tool-usage-log.md` records the inventory helper command or documented fallback.
- `run-summary.md` reports total scanned, skipped, and needs-user-input files.

## Scenario 14: Evidence Schema And Run Summary

Input:

- Goal: job-specific resume and interview prep.
- Evidence contains five claims across local docs, public GitHub, and GitHub Enterprise summaries.
- Two claims are medium confidence because metrics are missing.
- One claim requires sanitized enterprise wording.

Expected outputs:

- `evidence.md` follows the evidence schema fields in human-readable Markdown.
- If `evidence.json` is created, it follows `references/evidence-schema.md`.
- `run-summary.md` lists source contexts, outputs created, warning-only quality gates, missing metrics, and sensitive approval needs.
- Final polished outputs use high-confidence and approved medium-confidence claims only.
- Low-confidence or sensitive claims remain questions or sanitized summaries.

## Scenario 15: Career And Interview Coach

Input:

- Goal: career and interview coaching.
- Years of experience: 14.
- Target role: staff platform engineer or principal platform engineer.
- Evidence: detailed resume, scorecard, public GitHub contributions, enterprise summaries, and local architecture notes.
- Gaps: missing exact ownership for one project, missing scale for one migration, and unconfirmed seniority positioning.

Expected outputs:

- `career-master-run.md` connects evidence coverage, resume strategy, interview strategy, LinkedIn positioning, and job-search direction.
- `missing-information-loop.md` asks concise high-priority questions for dates, ownership, metrics, scale, and disclosure.
- `career-positioning-coach.md` recommends best-fit roles, seniority evidence, differentiators, risks, and next moves without inventing claims.
- `interview-readiness-scorecard.md` scores recruiter screen, resume walk-through, key project deep dives, technical stack explanations, system design, behavioral stories, job-specific mapping, and redaction safety.
- `project-interview-briefs.md`, `technical-stack-interview-guide.md`, and `interview-prep-pack.md` reuse evidence-backed project and technology claims.

## Scenario 16: Visual Template Profile Selection

Input:

- Goal: impressive visual resume with optional profile picture.
- Years of experience: 12.
- Target role: staff platform engineer with AI automation and open-source experience.
- Evidence: sanitized professional resume, public GitHub links, enterprise summaries, and user-provided profile picture path.

Expected outputs:

- `visual-template-selector.md` selects one profile from modern-technical, executive-compact, open-source-builder, enterprise-platform, or ai-automation.
- `visual-template-selector.md` records profile-picture approval status and third-party upload status.
- `designed-resume.html` uses sanitized content and keeps `ats-resume.docx` as the job-portal artifact.
- `visual-design-review.md` checks first-page role fit, readability, print/PDF page breaks, and profile-picture handling.
- `visual-tool-handoff.md` states Canva/Figma upload is manual or requires explicit user approval.

## Scenario 17: Safe Local-Only Open-Source Run

Input:

- Goal: create resume and interview prep without external connectors.
- User approves only local files, pasted LinkedIn export, and local job posting text.
- GitHub, Jira, Confluence, browser, Figma, Canva, and job-board access are disabled or not approved.

Expected outputs:

- `safe-local-mode-checklist.md` records allowed local sources, disabled external tools, and fallbacks.
- `setup_doctor.py` can be used to report required files and optional command availability without blocking basic resume generation.
- `source-inventory.md` and `tool-usage-log.md` record local recursive inventory and disabled connector attempts.
- `evidence.md`, `professional-resume.md`, `resume-scorecard.md`, and `run-summary.md` are still produced from approved local evidence.
- Missing connector data is recorded as a limitation, not silently ignored.

## Scenario 18: Enterprise Disclosure And Redaction Audit

Input:

- Goal: targeted resume, cover letter, LinkedIn recommendations, and visual resume using private enterprise evidence.
- Sources: GitHub Enterprise PR summaries, Jira issues, Confluence pages, and local private design docs.
- Sensitive items: internal project names, private repository names, Jira keys, Confluence page titles, customer names, exact metrics, and one low-confidence claim.

Expected outputs:

- `disclosure-approval-queue.md` lists every sensitive item, source context, proposed treatment, pending user decision, and output impact.
- `final-redaction-review.md` checks final outputs for credentials, secrets, private URLs, unapproved names, unapproved metrics, issue keys, page titles, low-confidence claims, and profile-image approval.
- `professional-resume.md`, `targeted-resume.md`, `cover-letter.md`, `linkedin-recommendations.md`, and `designed-resume.html` use sanitized wording unless the user approved exact details.
- `run-summary.md` records sensitive approvals still needed and any outputs that are not share-ready.
