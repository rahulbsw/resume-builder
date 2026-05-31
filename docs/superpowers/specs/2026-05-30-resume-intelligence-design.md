# Resume Intelligence Plugin Design

Date: 2026-05-30

## Goal

Build a Codex/Claude plugin named `resume-intelligence` with one core skill that helps a user turn verified career evidence into a professional resume, ATS/recruiter scorecard, optional professional visual resume template, optional job-specific resume and cover letter, and LinkedIn profile improvement recommendations.

The plugin should support users whose work evidence is spread across LinkedIn, local documents, Confluence, Jira, GitHub Enterprise, and public GitHub. It must handle enterprise and open-source contributions as separate source contexts because they may use different hosts, credentials, access rules, and disclosure constraints.

## Non-Goals

- Do not scrape LinkedIn behind login or bypass platform controls.
- Do not store credentials in plugin files, generated resumes, or local artifacts.
- Do not publish confidential company, customer, repository, Jira, or Confluence details without an explicit user-approved sanitization step.
- Do not build a custom OAuth or account-management service in the first version.
- Do not guarantee truth of extracted achievements; the workflow must mark uncertain claims for user review.
- Do not upload profile pictures, private documents, or resume content to Canva, Figma, or another third-party design service automatically.

## Recommended Shape

Use a plugin rather than a standalone skill.

The plugin gives us a durable container for:

- A core `resume-intelligence` skill.
- Resume and cover-letter templates.
- Reference guidance for source handling, evidence scoring, and sanitization.
- Future deterministic scripts for parsing local documents and normalizing evidence.

The first version should rely on existing Codex tools/connectors where available instead of implementing new network clients.

## Source Model

The workflow treats every evidence source as a named source context:

- `linkedin-profile`: user-provided LinkedIn export, pasted profile content, public profile content, or notes.
- `local-docs`: files under a user-selected folder, such as design docs, status reports, exported tickets, project summaries, PDFs, Markdown, Word documents, or text files.
- `confluence`: Confluence pages returned by user-approved CQL searches.
- `jira`: Jira tickets returned by user-approved JQL searches.
- `github-enterprise`: one or more GitHub Enterprise hosts, each with its own organization, account identity, credential context, repository scope, and disclosure rules.
- `github-public`: public GitHub or GitHub Cloud activity, including repositories, PRs, issues, and open-source contributions.
- `job-posting`: optional pasted job listing, URL content, or downloaded posting text.
- `peer-market-research`: public role/profile/job evidence used to calibrate keywords, seniority, and expectations.
- `profile-picture`: optional user-provided local image path or attachment used only when the user requests a visual resume template.

Each source context should record:

- Source type and display name.
- Host or workspace identifier, when relevant.
- User identity used for attribution, such as GitHub username or enterprise email.
- Access method, such as existing connector, CLI, pasted export, local file, or browser-provided content.
- Allowed scope, such as specific repositories, Confluence spaces, Jira projects, date ranges, or folders.
- Confidentiality level: public, internal, confidential, or unknown.
- Whether raw details may be quoted, summarized only, or excluded from final documents.

## Multi-GitHub Requirement

The plugin must assume the user may have multiple GitHub identities:

- Public GitHub Cloud account for open-source work.
- GitHub Enterprise account for employer-owned work.
- Separate credentials or connector sessions for each host.
- Different repository visibility and disclosure policies.

The skill should ask the user to identify GitHub sources separately. It should never merge enterprise and public evidence without preserving provenance. Final resume bullets may combine the impact story, but the evidence log must retain which claims came from which host.

Recommended GitHub intake prompts:

- Which GitHub hosts should be considered?
- For each host, what username, organization, repositories, and date ranges are in scope?
- Is the evidence public, internal-summary-only, or excluded from final wording?
- Should contribution data be limited to authored PRs, reviewed PRs, commits, issues, or all available activity?

## Workflow

### 1. Intake

Collect the user's profile inputs and permissions:

- Target resume type: general, role-specific, company-specific, or job-posting-specific.
- Years of experience and target seniority.
- Target roles, technologies, domains, and geography.
- LinkedIn profile content or export.
- Local folder path for project documents.
- Optional Confluence CQL queries.
- Optional Jira JQL queries.
- GitHub source contexts, including enterprise and public hosts.
- Optional job posting.
- Optional profile picture for designed resume templates.
- Confidentiality and redaction preferences.

### 2. Evidence Collection

For each approved source, gather evidence into a structured career evidence set:

- Projects and products.
- Role and ownership.
- Technologies, frameworks, platforms, and tools.
- Business or customer problem.
- Implementation details.
- Scale, reliability, performance, security, cost, adoption, or operational impact.
- Dates and duration.
- Collaborators and cross-functional scope.
- Quantitative results.
- Evidence references and confidence.

The workflow should prefer direct evidence from user-owned documents and approved connectors over inferred claims.

### 3. Local Document Analysis

Analyze files under the selected folder to find project information. The first version should support text-oriented formats directly and note unsupported formats for later scripts.

Extract:

- Project names and aliases.
- Architecture, design, migration, incident, launch, or operational themes.
- Technologies and platform names.
- Metrics and outcomes.
- User's role and actions.
- Dates or release windows.
- Resume-ready achievement candidates.

### 4. Draft Resume

Create an initial resume draft from the evidence set:

- Professional summary.
- Core skills and technical strengths.
- Experience by role/company.
- Project-impact bullets.
- Open-source section when public contributions are meaningful.
- Education, certifications, patents, publications, talks, or awards when provided.

All bullets should be traceable back to source evidence. Unverified or weakly supported claims should be marked for user confirmation.

### 4a. Resume Scorecard

Before final resume wording, create a scorecard that checks:

- Recommended page count.
- ATS parse safety.
- Recruiter first-page strength.
- Job-posting keyword coverage.
- Unsupported or risky claims.
- Top fixes before applying.

### 5. Market and Peer Research

Use current public research only when the user asks for resume optimization or job targeting.

Research should consider:

- Similar LinkedIn-visible profiles or public professional profiles when accessible.
- Job postings for similar roles, technologies, seniority, and years of experience.
- Common keywords, responsibilities, seniority signals, and must-have skills.
- Gaps between the user's draft and market expectations.

The skill should distinguish public evidence from inference and should avoid copying wording from other users' profiles.

### 6. Professional Resume

Produce a polished resume that is:

- Truthful and evidence-backed.
- Optimized for applicant tracking systems.
- Tailored to target role, seniority, and technology stack.
- Explicit about public open-source contributions when useful.
- Sanitized for confidential enterprise work.
- Available as Markdown plus a professional, print-friendly designed template.

### 6a. Professional Template and Profile Picture

When the user requests a professional template or provides a profile picture, create a designed resume artifact that can be exported or copied into tools such as Canva, Figma, Google Docs, Word, or another design editor.

The designed template should:

- Keep the resume content ATS-friendly in the Markdown version.
- Provide a visually polished HTML/CSS layout for human review and PDF printing.
- Include an optional profile-picture slot only when the user provides an image or asks for one.
- Avoid embedding private image metadata into shared artifacts when possible.
- Include concise export guidance instead of uploading content to external design services automatically.

### 7. Job-Specific Resume and Cover Letter

When the user provides a job listing, generate:

- A targeted resume version aligned to the posting.
- A cover letter grounded in the user's actual experience.
- A match analysis showing key requirements, evidence, gaps, and suggested mitigations.

The skill should not invent missing requirements. It may recommend how the user can address gaps honestly.

### 8. LinkedIn Profile Recommendations

Provide recommended LinkedIn updates:

- Headline.
- About section.
- Featured projects or repositories.
- Experience section improvements.
- Skills ordering.
- Open-source contribution positioning.
- Confidentiality-safe project descriptions.
- Keyword gaps from market/job research.

Recommendations should be written as editable suggestions, not posted automatically.

## Outputs

The plugin should produce a structured output folder for each run:

- `evidence.md`: source summary, claims, confidence, and redaction notes.
- `draft-resume.md`: initial resume based on collected evidence.
- `resume-scorecard.md`: ATS, recruiter, page-count, keyword, and claim-risk checklist.
- `professional-resume.md`: polished general resume.
- `designed-resume.html`: optional professional visual resume template with optional profile-picture support.
- `targeted-resume.md`: job-specific resume when a posting is provided.
- `cover-letter.md`: job-specific cover letter when a posting is provided.
- `linkedin-recommendations.md`: suggested LinkedIn edits.
- `gap-analysis.md`: optional market/job fit analysis.

## Privacy and Disclosure Rules

- Always preserve source provenance internally.
- Require user confirmation before including internal project names, customer names, metrics, repository names, Jira IDs, or Confluence titles in final outputs.
- Default enterprise evidence to sanitized summaries.
- Default public GitHub evidence to quotable only when it is truly public.
- Redact secrets, credentials, access tokens, private URLs, and internal identifiers.
- Make uncertainty visible instead of turning weak evidence into confident claims.

## Error Handling

- If a connector is unavailable, ask for pasted exports, local files, or manual summaries.
- If credentials are missing for one GitHub host, continue with other approved sources and mark the skipped source.
- If a source returns too much data, narrow by date range, repo/project/space, or keyword.
- If source evidence conflicts, prefer user confirmation over inference.
- If a document format cannot be parsed, record it as skipped and suggest conversion or future parser support.

## Plugin Contents

Initial plugin structure:

- `.codex-plugin/plugin.json`
- `skills/resume-intelligence/SKILL.md`
- `skills/resume-intelligence/agents/openai.yaml`
- `skills/resume-intelligence/references/source-model.md`
- `skills/resume-intelligence/references/resume-workflow.md`
- `skills/resume-intelligence/references/privacy-sanitization.md`
- `skills/resume-intelligence/assets/templates/`
- `skills/resume-intelligence/assets/templates/designed-resume.html`

Scripts can be added later for deterministic document parsing, evidence normalization, and output rendering.

## Validation

The first implementation should be validated by:

- Running plugin manifest validation.
- Running skill validation.
- Reading the generated skill metadata to ensure the trigger description is specific.
- Testing a dry-run workflow with mocked inputs for:
  - public GitHub only,
  - GitHub Enterprise plus public GitHub,
  - Jira and Confluence with local documents,
  - professional designed resume with optional profile picture,
  - job-posting-specific resume and cover letter.

## Implementation Defaults

- Place the plugin source in this repository under `plugins/resume-intelligence` so it can be versioned with the project and edited without writing outside the workspace.
- Generate Markdown outputs and one professional HTML/CSS designed resume template in v1. DOCX and native PDF generation can be added after the skill workflow is stable.
- In v1, the skill should instruct Codex to analyze text-oriented local documents using available local tools. Deterministic parsing scripts for PDF, DOCX, and evidence normalization can be added after the core skill is usable.
- Do not create or update a personal marketplace entry unless the user explicitly asks to install the plugin into the Codex app.
- Do not depend on Canva, Figma, or any external design service for v1. Provide portable HTML/CSS and copy/export guidance instead.
