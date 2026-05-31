---
name: resume-intelligence
description: Use when the user wants to build or tailor a resume, professional visual resume template, ATS/recruiter scorecard, cover letter, LinkedIn profile recommendations, interview preparation pack, project interview briefs, technical-stack interview guide, job match scoring report, or career evidence summary from LinkedIn profile content, local project documents, Confluence, Jira, public GitHub, GitHub Enterprise, open-source contributions, profile pictures, or job postings. Trigger for requests involving resume drafting, resume tailoring, ATS checks, keyword matching, designed resumes, professional templates, cover letters, LinkedIn optimization, project evidence extraction, recursive workspace document analysis, tool usage auditing, career impact analysis, job search matching, interview preparation, or multi-source professional profile synthesis.
---

# Resume Intelligence

Use this skill to convert approved career evidence into a professional resume and interview system: source inventory, tool usage log, evidence log, draft resume, ATS/recruiter scorecard, polished resume, optional designed resume, optional targeted resume, optional cover letter, job/market fit analysis, job match scoring report, project interview briefs, technical-stack interview guide, interview prep pack, and LinkedIn profile recommendations.

## Guardrails

- Do not scrape LinkedIn behind login or bypass platform controls.
- Use LinkedIn profile exports, pasted profile content, public profile content, or user notes.
- Do not store credentials in plugin files, generated outputs, templates, or evidence logs.
- Do not upload profile pictures, private documents, or resume content to Canva, Figma, or another third-party design service automatically.
- Treat GitHub Enterprise, private Confluence, private Jira, and private repositories as confidential by default.
- Preserve source provenance for every claim.
- Mark uncertain claims for user confirmation.
- Ask before including internal project names, customer names, repository names, Jira IDs, Confluence titles, private URLs, or exact internal metrics in final user-facing outputs.
- Do not copy wording from other professionals' public profiles.

## When To Load References

- Read `references/source-model.md` before collecting evidence from more than one source or any GitHub source.
- Read `references/privacy-sanitization.md` before writing final resume, cover letter, or LinkedIn text from enterprise or private sources.
- Read `references/resume-workflow.md` before producing the evidence log, resume files, cover letter, or LinkedIn recommendations.
- Read `references/interview-job-workflow.md` before producing project interview briefs, technical-stack interview guidance, interview preparation content, job search results, or job match scoring.

## Intake

Start by identifying the run goal:

- General resume.
- Role-specific resume.
- Company-specific resume.
- Job-posting-specific resume and cover letter.
- LinkedIn profile recommendations.
- Interview preparation from resume evidence.
- Job search and match scoring.
- Evidence extraction only.

Collect only the inputs needed for that goal:

- Years of experience and target seniority.
- Target roles, technologies, domains, and geography.
- LinkedIn profile export, pasted profile, public profile content, or notes.
- Local project-document folder path.
- Confluence CQL queries, spaces, titles, or page URLs approved by the user.
- Jira JQL queries, projects, issue keys, assignee identity, and date ranges approved by the user.
- Public GitHub account, repositories, PRs, issues, and date ranges.
- GitHub Enterprise host, username, organization, repositories, credential context, contribution type, date range, and disclosure level.
- Job posting text, URL content, or pasted listing.
- Optional local profile-picture path or attachment for designed resume templates.
- Confidentiality and redaction preferences.

## Source Collection

Create a source context for each approved source. Keep public GitHub and GitHub Enterprise separate even when the same person owns both identities.

Always create `source-inventory.md` and `tool-usage-log.md` before `evidence.md`. The inventory must prove what was in scope, what was scanned, what was skipped, and why. The tool log must record the concrete tools, connector calls, shell commands, browser actions, or manual inputs used for each source. Do not silently infer that a folder or connector was read.

For local document folders, recursively enumerate the approved root with `rg --files <folder>` whenever available. Use a `find` fallback only when `rg` is unavailable or unsuitable. Do not stop after the first subfolder. Include every nested file in the inventory, then classify files as scanned, skipped-unsupported-format, skipped-too-large, skipped-binary, skipped-permission, duplicate, or needs-user-input. Prefer text-oriented formats such as `.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`, `.html`, `.xml`, `.adoc`, `.rst`, `.log`, `.docx`, and `.pdf` when local extraction tools are available; record extraction limitations for formats that cannot be parsed.

If connector tools are available, use them after the user approves the query or repository scope:

- GitHub: repositories, authored pull requests, reviewed pull requests, issues, commits, comments, and diffs when relevant.
- Confluence: user-approved CQL searches and specific pages.
- Jira: user-approved JQL searches and selected fields.
- Local files: inspect text-oriented documents under the approved folder.
- Web research: use current public sources for job postings and public market research when the user asks for optimization or targeting.
- Profile picture: use only a user-provided local image path or attachment, and include it only in designed artifacts when requested.

If a connector is unavailable, credentials are missing, or a scoped source cannot be accessed, record the attempt in `tool-usage-log.md`, mark the source context as unavailable or needs-user-input, ask for pasted exports, local files, or manual summaries, and continue with other approved sources.

## Evidence Extraction

For each source, extract:

- Project or product name.
- Source context and evidence reference.
- User role and ownership.
- Business, customer, technical, operational, security, or platform problem.
- Actions performed by the user.
- Technologies and platforms.
- Scale, reliability, performance, cost, adoption, security, migration, or operational impact.
- Dates or time windows.
- Quantitative metrics.
- Collaborators and cross-functional scope.
- Confidence level: high, medium, or low.
- Disclosure level: public, internal-summary-only, confidential, excluded, or unknown.

Prefer direct evidence over inference. When evidence conflicts, ask the user which version is accurate.

## Output Location

Create outputs under:

```text
resume-runs/YYYY-MM-DD-<descriptive-slug>/
```

Use these filenames when the corresponding output is requested:

- `source-inventory.md`
- `tool-usage-log.md`
- `evidence.md`
- `draft-resume.md`
- `resume-scorecard.md`
- `professional-resume.md`
- `designed-resume.html`
- `targeted-resume.md`
- `cover-letter.md`
- `linkedin-recommendations.md`
- `gap-analysis.md`
- `job-match-report.md`
- `project-interview-briefs.md`
- `technical-stack-interview-guide.md`
- `interview-prep-pack.md`

Use the templates in `assets/templates/` as structure, not as rigid wording.

## Output Sequence

1. Build `source-inventory.md` and `tool-usage-log.md` first.
2. Build `evidence.md` from scanned or manually provided sources only.
3. Create `draft-resume.md` from high- and medium-confidence evidence.
4. Ask the user to confirm low-confidence claims and sensitive details before final wording.
5. Create `resume-scorecard.md` before final wording. Check page-length strategy, ATS parse safety, first-page recruiter strength, keyword coverage, unsupported claims, and job-posting gaps.
6. Create `professional-resume.md` using sanitized, evidence-backed bullets and the scorecard recommendations.
7. If a professional template, design export, or profile picture is requested, create `designed-resume.html` from the sanitized resume content.
8. If a job posting is provided, create `gap-analysis.md`, `targeted-resume.md`, and `cover-letter.md`.
9. If job search is requested, search current public job sources and create `job-match-report.md` with match scoring and citations.
10. If interview preparation is requested, create `project-interview-briefs.md`, `technical-stack-interview-guide.md`, and `interview-prep-pack.md`.
11. Create `linkedin-recommendations.md` with editable profile updates.

## Final Response

Summarize:

- Files created.
- Sources used and skipped.
- Inventory and tool-log coverage, including any approved folders or connector scopes that were unavailable.
- Sensitive items that require user review.
- Low-confidence claims that need confirmation.
- Scorecard findings for ATS safety, recruiter strength, page length, and keyword gaps.
- Strongest job matches and interview preparation gaps when those outputs were requested.
- Clear next actions for the user.
