---
name: resume-intelligence
description: Use when the user wants to build or tailor a resume, professional visual resume template, ATS/recruiter scorecard, cover letter, LinkedIn profile recommendations, or career evidence summary from LinkedIn profile content, local project documents, Confluence, Jira, public GitHub, GitHub Enterprise, open-source contributions, profile pictures, or job postings. Trigger for requests involving resume drafting, resume tailoring, ATS checks, keyword matching, designed resumes, professional templates, cover letters, LinkedIn optimization, project evidence extraction, career impact analysis, or multi-source professional profile synthesis.
---

# Resume Intelligence

Use this skill to convert approved career evidence into a professional resume system: an evidence log, draft resume, ATS/recruiter scorecard, polished resume, optional designed resume, optional targeted resume, optional cover letter, job/market fit analysis, and LinkedIn profile recommendations.

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

## Intake

Start by identifying the run goal:

- General resume.
- Role-specific resume.
- Company-specific resume.
- Job-posting-specific resume and cover letter.
- LinkedIn profile recommendations.
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

If connector tools are available, use them after the user approves the query or repository scope:

- GitHub: repositories, authored pull requests, reviewed pull requests, issues, commits, comments, and diffs when relevant.
- Confluence: user-approved CQL searches and specific pages.
- Jira: user-approved JQL searches and selected fields.
- Local files: inspect text-oriented documents under the approved folder.
- Web research: use current public sources for job postings and public market research when the user asks for optimization or targeting.
- Profile picture: use only a user-provided local image path or attachment, and include it only in designed artifacts when requested.

If a connector is unavailable or credentials are missing, ask for pasted exports, local files, or manual summaries and continue with other approved sources.

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

- `evidence.md`
- `draft-resume.md`
- `resume-scorecard.md`
- `professional-resume.md`
- `designed-resume.html`
- `targeted-resume.md`
- `cover-letter.md`
- `linkedin-recommendations.md`
- `gap-analysis.md`

Use the templates in `assets/templates/` as structure, not as rigid wording.

## Output Sequence

1. Build `evidence.md` first.
2. Create `draft-resume.md` from high- and medium-confidence evidence.
3. Ask the user to confirm low-confidence claims and sensitive details before final wording.
4. Create `resume-scorecard.md` before final wording. Check page-length strategy, ATS parse safety, first-page recruiter strength, keyword coverage, unsupported claims, and job-posting gaps.
5. Create `professional-resume.md` using sanitized, evidence-backed bullets and the scorecard recommendations.
6. If a professional template, design export, or profile picture is requested, create `designed-resume.html` from the sanitized resume content.
7. If a job posting is provided, create `gap-analysis.md`, `targeted-resume.md`, and `cover-letter.md`.
8. Create `linkedin-recommendations.md` with editable profile updates.

## Final Response

Summarize:

- Files created.
- Sources used and skipped.
- Sensitive items that require user review.
- Low-confidence claims that need confirmation.
- Scorecard findings for ATS safety, recruiter strength, page length, and keyword gaps.
- Clear next actions for the user.
