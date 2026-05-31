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
