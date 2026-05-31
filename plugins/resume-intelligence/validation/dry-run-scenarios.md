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

- `evidence.md` includes public source context and public quoting rule.
- `draft-resume.md` includes open-source contribution section.
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

- `gap-analysis.md` classifies requirements as strong match, partial match, gap, or needs user input.
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

- `evidence.md` records the `linkedin-profile` source form and confirms no automated scraping.
- `evidence.md` records the `profile-picture` source context with local path or attachment label, user approval, and embed/link/omit preference.
- `professional-resume.md` remains ATS-friendly and text-first.
- `designed-resume.html` includes sanitized resume content and a profile-picture slot.
- `designed-resume.html` does not fetch, search for, scrape, or upload profile pictures.
- Profile picture is referenced only through the user-approved local path or left as a replacement placeholder.
- Output guidance explains browser-to-PDF export and copy/import into Canva, Figma, Google Docs, or Word.
- Guidance states third-party design import is manual only and profile pictures/private resume content are not uploaded automatically.
