# Resume Intelligence Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Codex plugin named `resume-intelligence` with one core skill that creates evidence-backed resumes, professional visual resume templates with optional profile-picture support, job-specific resumes, cover letters, and LinkedIn recommendations from LinkedIn, local documents, Confluence, Jira, public GitHub, and GitHub Enterprise sources.

**Architecture:** The plugin is documentation- and workflow-first in v1. It uses a validated plugin manifest, one focused skill, three reference files for detailed workflow guidance, Markdown templates for generated artifacts, one portable HTML/CSS designed resume template, and no custom network client or credential storage. Existing Codex tools/connectors remain the integration boundary for GitHub, Confluence, Jira, web research, and local file analysis.

**Tech Stack:** Codex plugin manifest JSON, Codex skill Markdown frontmatter, `agents/openai.yaml`, Markdown reference files, Markdown output templates, portable HTML/CSS template, official plugin and skill validator scripts.

---

## File Structure

- Create `plugins/resume-intelligence/.codex-plugin/plugin.json`: plugin manifest for local Codex discovery and validation.
- Create `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`: core skill trigger metadata and primary workflow.
- Create `plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml`: Codex UI metadata for the skill.
- Create `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md`: source-context schema, including public GitHub and GitHub Enterprise separation.
- Create `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md`: evidence-to-resume workflow, output sequence, and job-posting tailoring.
- Create `plugins/resume-intelligence/skills/resume-intelligence/references/privacy-sanitization.md`: confidentiality, redaction, and claim-confidence rules.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/evidence.md`: evidence log template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/draft-resume.md`: first-draft resume template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/professional-resume.md`: polished resume template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/designed-resume.html`: professional visual resume template with optional profile-picture slot and print styling.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/targeted-resume.md`: job-specific resume template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/cover-letter.md`: cover letter template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/linkedin-recommendations.md`: LinkedIn improvement template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/gap-analysis.md`: job/market fit analysis template.
- Create `plugins/resume-intelligence/validation/dry-run-scenarios.md`: validation scenarios that exercise the intended workflow without live credentials.

## Task 1: Scaffold Plugin Container

**Files:**
- Create: `plugins/resume-intelligence/.codex-plugin/plugin.json`
- Create: `plugins/resume-intelligence/skills/.gitkeep`

- [ ] **Step 1: Run the official plugin scaffold**

Run:

```bash
python3 /Users/rajain5/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py resume-intelligence --path plugins --with-skills
```

Expected: command exits 0 and prints:

```text
Created plugin scaffold: plugins/resume-intelligence
plugin manifest: plugins/resume-intelligence/.codex-plugin/plugin.json
```

- [ ] **Step 2: Create skills placeholder**

Run:

```bash
touch plugins/resume-intelligence/skills/.gitkeep
```

Expected: command exits 0.

- [ ] **Step 3: Verify scaffolded files**

Run:

```bash
find plugins/resume-intelligence -maxdepth 3 -type f -print
```

Expected output includes:

```text
plugins/resume-intelligence/.codex-plugin/plugin.json
plugins/resume-intelligence/skills/.gitkeep
```

- [ ] **Step 4: Replace the scaffolded manifest**

Edit `plugins/resume-intelligence/.codex-plugin/plugin.json` to exactly:

```json
{
  "name": "resume-intelligence",
  "version": "0.1.0",
  "description": "Build evidence-backed resumes, designed resume templates, cover letters, and LinkedIn recommendations from approved career sources.",
  "author": {
    "name": "Local developer"
  },
  "skills": "./skills/",
  "interface": {
    "displayName": "Resume Intelligence",
    "shortDescription": "Create polished resumes from verified evidence.",
    "longDescription": "Resume Intelligence guides Codex through approved LinkedIn, local document, Confluence, Jira, public GitHub, and GitHub Enterprise sources to produce evidence-backed resume drafts, professional resumes, professional visual resume templates with optional profile-picture support, job-specific resumes, cover letters, and LinkedIn profile recommendations with explicit provenance and confidentiality handling.",
    "developerName": "Local developer",
    "category": "Productivity",
    "capabilities": [
      "Read",
      "Write",
      "Interactive"
    ],
    "defaultPrompt": [
      "Use Resume Intelligence to build my resume from approved career evidence."
    ]
  }
}
```

- [ ] **Step 5: Validate manifest JSON syntax**

Run:

```bash
python3 -m json.tool plugins/resume-intelligence/.codex-plugin/plugin.json
```

Expected: command exits 0 and prints formatted JSON.

- [ ] **Step 6: Commit scaffold, manifest, and skills placeholder**

Run:

```bash
git add plugins/resume-intelligence/.codex-plugin/plugin.json plugins/resume-intelligence/skills/.gitkeep
git commit -m "Add resume intelligence plugin manifest"
```

Expected: commit succeeds with the created manifest file and skills placeholder.

## Task 2: Add Core Skill Metadata and Workflow

**Files:**
- Create: `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml`

- [ ] **Step 1: Create the skill directories**

Run:

```bash
mkdir -p plugins/resume-intelligence/skills/resume-intelligence/agents plugins/resume-intelligence/skills/resume-intelligence/references plugins/resume-intelligence/skills/resume-intelligence/assets/templates
```

Expected: command exits 0.

- [ ] **Step 2: Write the skill file**

Create `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md` with:

```markdown
---
name: resume-intelligence
description: Use when the user wants to build or tailor a resume, professional visual resume template, cover letter, LinkedIn profile recommendations, or career evidence summary from LinkedIn profile content, local project documents, Confluence, Jira, public GitHub, GitHub Enterprise, open-source contributions, profile pictures, or job postings. Trigger for requests involving resume drafting, resume tailoring, designed resumes, professional templates, cover letters, LinkedIn optimization, project evidence extraction, career impact analysis, or multi-source professional profile synthesis.
---

# Resume Intelligence

Use this skill to convert approved career evidence into a professional resume system: an evidence log, draft resume, polished resume, optional designed resume, optional targeted resume, optional cover letter, job/market fit analysis, and LinkedIn profile recommendations.

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
4. Create `professional-resume.md` using sanitized, evidence-backed bullets.
5. If a professional template, design export, or profile picture is requested, create `designed-resume.html` from the sanitized resume content.
6. If a job posting is provided, create `gap-analysis.md`, `targeted-resume.md`, and `cover-letter.md`.
7. Create `linkedin-recommendations.md` with editable profile updates.

## Final Response

Summarize:

- Files created.
- Sources used and skipped.
- Sensitive items that require user review.
- Low-confidence claims that need confirmation.
- Clear next actions for the user.
```

- [ ] **Step 3: Write the Codex UI metadata**

Create `plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml` with:

```yaml
interface:
  display_name: "Resume Intelligence"
  short_description: "Build polished resumes from verified evidence"
  brand_color: "#2563EB"
  default_prompt: "Use $resume-intelligence to build a professional resume template from my approved career evidence."

policy:
  allow_implicit_invocation: true
```

- [ ] **Step 4: Validate skill metadata**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/resume-intelligence/skills/resume-intelligence
```

Expected output:

```text
Skill is valid!
```

- [ ] **Step 5: Commit the core skill**

Run:

```bash
git add plugins/resume-intelligence/skills/resume-intelligence/SKILL.md plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml
git commit -m "Add resume intelligence core skill"
```

Expected: commit succeeds with the skill and UI metadata files.

## Task 3: Add Source, Workflow, and Privacy References

**Files:**
- Create: `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/references/privacy-sanitization.md`

- [ ] **Step 1: Write the source model reference**

Create `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md` with:

```markdown
# Source Model

Every evidence source is represented as a source context. Source contexts keep credentials, hosts, disclosure rules, and claim provenance separated.

## Source Context Fields

Use this structure in the evidence log:

- `id`: stable short identifier such as `github-public-rajain5` or `github-enterprise-webex`.
- `type`: `linkedin-profile`, `local-docs`, `confluence`, `jira`, `github-public`, `github-enterprise`, `job-posting`, `peer-market-research`, or `profile-picture`.
- `display_name`: user-facing source label.
- `host`: source host or workspace, such as `github.com`, a GitHub Enterprise hostname, Jira site, Confluence site, or local folder path.
- `identity`: username, email, display name, or user-provided identity used for attribution.
- `access_method`: connector, CLI, local file, pasted export, public web, or manual notes.
- `scope`: repositories, spaces, projects, folders, date ranges, keywords, issue keys, page titles, or PR numbers.
- `confidentiality`: public, internal, confidential, excluded, or unknown.
- `quoting_rule`: quote, summarize-only, anonymize, exclude, or ask-before-use.
- `status`: used, skipped, unavailable, narrowed, or needs-user-input.

## GitHub Public

Use `github-public` for open-source or public GitHub Cloud evidence. Public evidence can support visible open-source sections, repository links, project bullets, and community impact.

Record:

- GitHub username.
- Repository full names.
- Authored PRs.
- Reviewed PRs.
- Issues opened or resolved.
- Commits when available.
- Release, maintainer, or ownership signals.
- Public visibility confirmation.

## GitHub Enterprise

Use `github-enterprise` for employer-owned or private GitHub hosts. Keep each enterprise host as a separate source context.

Record:

- Enterprise hostname.
- Organization.
- Enterprise username or email.
- Repository names only when the user permits them.
- Authored PRs, reviewed PRs, issues, commits, and date ranges in scope.
- Disclosure rule for repository names, product names, customer names, and metrics.

Default GitHub Enterprise evidence to `summarize-only` unless the user explicitly permits names or exact metrics.

## Confluence

Use `confluence` for pages returned from user-approved CQL searches or specific page references.

Record:

- Site or workspace.
- CQL query or page identifiers.
- Page title handling rule.
- Space key.
- Date range.
- Confidentiality level.

## Jira

Use `jira` for issues returned from user-approved JQL searches.

Record:

- Site or workspace.
- JQL query.
- Project keys.
- Fields retrieved.
- Issue key handling rule.
- Date range.
- Confidentiality level.

## LinkedIn

Use `linkedin-profile` for user-provided profile content, exports, notes, or public profile text. Do not automate logged-in scraping.

Record:

- Source form: export, pasted text, public page, or notes.
- Profile URL when user provides it.
- Date collected.
- Sections included.

## Job Posting and Market Research

Use `job-posting` for a specific job listing. Use `peer-market-research` for public role and market calibration.

Research may inform keyword coverage, role framing, and gap analysis. It must not create unsupported experience claims.

## Profile Picture

Use `profile-picture` only for a user-provided local image path or attachment. Do not search for or scrape profile pictures.

Record:

- Local image path or attachment label.
- Whether the user requested use in the designed resume.
- Whether the image should be embedded, linked by local path, or omitted from shared artifacts.
- Any user-provided cropping or style preference.
```

- [ ] **Step 2: Write the resume workflow reference**

Create `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md` with:

```markdown
# Resume Workflow

## Evidence First

Start with `evidence.md`. Do not write polished resume bullets until the evidence log has source contexts, claims, confidence, and disclosure rules.

For each claim, capture:

- Claim text.
- Source context ID.
- Evidence reference.
- Confidence: high, medium, or low.
- Disclosure level.
- Resume use: include, include-sanitized, needs-confirmation, or exclude.

## Bullet Quality

Strong bullets connect action, technical depth, scope, and impact:

```text
Led <action> for <system/product/domain>, using <technology/method>, improving <metric/outcome> across <scale/audience>.
```

When metrics are unavailable, use truthful scope:

```text
Designed <system/change> for <team/platform>, reducing operational risk and enabling <business or engineering outcome>.
```

Do not invent metrics. Ask the user for numbers when a bullet needs quantitative support.

## Resume Order

For a general technical resume:

1. Name and contact placeholders if the user has not provided them.
2. Professional summary.
3. Core skills.
4. Professional experience.
5. Selected projects or open-source contributions.
6. Education and certifications.

For a job-specific resume:

1. Align summary to the role and seniority.
2. Reorder skills to match the posting.
3. Select bullets with the strongest evidence for the posting's requirements.
4. Preserve truthfulness and confidentiality rules.
5. Add a gap analysis instead of hiding missing requirements.

## Job Posting Match

For each important job requirement, classify:

- Strong match: direct evidence exists.
- Partial match: adjacent evidence exists.
- Gap: no evidence found.
- Needs user input: likely experience but not supported by collected sources.

Use this classification in `gap-analysis.md`, then produce `targeted-resume.md` and `cover-letter.md`.

## Designed Resume

Create `designed-resume.html` when the user requests a professional template, visual resume, Canva/Figma-ready layout, printable design, or profile-picture support.

Use the sanitized content from `professional-resume.md`. Keep the Markdown resume as the ATS-friendly source of truth.

The designed resume should:

- Use a restrained professional layout.
- Include a profile-picture slot only when the user provides or requests one.
- Use local image paths or clear replacement comments instead of fetching images.
- Include print CSS for browser-to-PDF export.
- Include a short comment explaining that the HTML can be copied into Canva, Figma, Google Docs, Word, or another design tool.
- Avoid decorative elements that make content hard to scan.

## LinkedIn Recommendations

Recommend editable changes for:

- Headline.
- About section.
- Experience sections.
- Featured projects or repositories.
- Skills ordering.
- Open-source positioning.
- Confidentiality-safe enterprise project wording.

Do not post changes automatically. Keep suggestions in `linkedin-recommendations.md`.
```

- [ ] **Step 3: Write the privacy and sanitization reference**

Create `plugins/resume-intelligence/skills/resume-intelligence/references/privacy-sanitization.md` with:

```markdown
# Privacy and Sanitization

## Defaults

- Public GitHub evidence may be named when the repository is public and the user approves.
- GitHub Enterprise evidence is summarized and anonymized by default.
- Jira and Confluence evidence is summarized and anonymized by default.
- LinkedIn content is used only when user-provided or publicly accessible without bypassing access controls.
- Credentials, tokens, cookies, private URLs, and secrets are never copied into outputs.
- Profile pictures are used only when user-provided and are never uploaded to external design services automatically.

## Sanitization Rules

Before final resume, cover letter, or LinkedIn wording:

- Replace internal repository names with generic system descriptions unless approved.
- Replace customer names with industry or segment descriptions unless approved.
- Replace Jira IDs with generic references unless approved.
- Replace Confluence page titles with project themes unless approved.
- Replace private URLs with source-context references in the evidence log only.
- Round or generalize sensitive metrics when the user asks for confidentiality.
- Use local image paths or user-approved embedded image references for designed resumes; omit images from shared artifacts when the user has not approved image sharing.

## Claim Confidence

Use high confidence when direct source evidence supports the claim and the user's role is clear.

Use medium confidence when the source supports the project but the user's exact role, metric, or scope needs interpretation.

Use low confidence when the claim comes from weak evidence, inferred role ownership, stale documents, or conflicting sources.

Low-confidence claims cannot be used in final outputs without user confirmation.

## User Review Gate

Pause for user review before final wording when outputs include:

- Internal project names.
- Exact confidential metrics.
- Customer or partner names.
- Private repository names.
- Jira issue keys.
- Confluence page titles.
- Security-sensitive architecture details.
- Profile pictures or image metadata in shared artifacts.
- Any low-confidence claim.
```

- [ ] **Step 4: Commit references**

Run:

```bash
git add plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md plugins/resume-intelligence/skills/resume-intelligence/references/privacy-sanitization.md
git commit -m "Add resume intelligence workflow references"
```

Expected: commit succeeds with three reference files.

## Task 4: Add Markdown Output Templates

**Files:**
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/evidence.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/draft-resume.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/professional-resume.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/designed-resume.html`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/targeted-resume.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/cover-letter.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/linkedin-recommendations.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/gap-analysis.md`

- [ ] **Step 1: Create `evidence.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/evidence.md` with:

```markdown
# Career Evidence

## Run Summary

- Goal:
- Target roles:
- Target seniority:
- Years of experience:
- Target technologies:
- Output files:

## Source Contexts

| ID | Type | Display Name | Host | Identity | Scope | Confidentiality | Quoting Rule | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## Claims

| Claim | Source Context | Evidence Reference | Confidence | Disclosure | Resume Use | User Review |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Projects

### Project Name

- Source contexts:
- User role:
- Problem:
- Actions:
- Technologies:
- Impact:
- Metrics:
- Dates:
- Disclosure notes:
- Resume bullet candidates:

## Sensitive Items For Review

- 

## Low-Confidence Claims

- 
```

- [ ] **Step 2: Create `draft-resume.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/draft-resume.md` with:

```markdown
# Draft Resume

## Contact

Name | Email | Phone | Location | LinkedIn | GitHub

## Professional Summary

Draft summary grounded in collected evidence.

## Core Skills

- Languages:
- Frameworks:
- Cloud and platforms:
- Data and storage:
- DevOps and delivery:
- Architecture and leadership:

## Professional Experience

### Company | Title | Dates

- Evidence-backed draft bullet.
- Evidence-backed draft bullet.
- Claim needing user confirmation.

## Selected Projects

### Project

- Evidence-backed project bullet.

## Open Source

- Public contribution bullet with repository or community context.

## Education and Certifications

- 

## Needs User Confirmation

- 
```

- [ ] **Step 3: Create `professional-resume.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/professional-resume.md` with:

```markdown
# Professional Resume

## Contact

Name | Email | Phone | Location | LinkedIn | GitHub

## Summary

Concise role-aligned summary.

## Technical Skills

Languages | Frameworks | Cloud | Data | DevOps | Architecture

## Experience

### Company | Title | Dates

- Polished sanitized impact bullet.
- Polished sanitized impact bullet.
- Polished sanitized impact bullet.

## Open Source and Community

- Public contribution bullet.

## Education

- 

## Certifications

- 
```

- [ ] **Step 4: Create `designed-resume.html` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/designed-resume.html` with:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Designed Resume</title>
  <style>
    :root {
      --ink: #172033;
      --muted: #5d667a;
      --line: #d9dee8;
      --accent: #2563eb;
      --paper: #ffffff;
      --soft: #f4f7fb;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: #e9edf4;
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.45;
    }

    .resume {
      width: min(100%, 8.5in);
      min-height: 11in;
      margin: 0 auto;
      background: var(--paper);
      display: grid;
      grid-template-columns: 2.25in 1fr;
    }

    .sidebar {
      background: var(--soft);
      padding: 0.42in 0.32in;
      border-right: 1px solid var(--line);
    }

    .main {
      padding: 0.42in 0.45in;
    }

    .photo {
      width: 1.35in;
      height: 1.35in;
      border-radius: 999px;
      border: 3px solid #ffffff;
      outline: 1px solid var(--line);
      object-fit: cover;
      display: block;
      margin-bottom: 0.22in;
      background: #dfe5ee;
    }

    .photo-placeholder {
      width: 1.35in;
      height: 1.35in;
      border-radius: 999px;
      border: 1px dashed var(--line);
      display: grid;
      place-items: center;
      color: var(--muted);
      font-size: 10px;
      margin-bottom: 0.22in;
      text-align: center;
      padding: 0.1in;
    }

    h1 {
      font-size: 30px;
      line-height: 1.05;
      margin: 0 0 0.08in;
      letter-spacing: 0;
    }

    h2 {
      color: var(--accent);
      font-size: 13px;
      margin: 0.24in 0 0.08in;
      text-transform: uppercase;
      letter-spacing: 0;
      border-bottom: 1px solid var(--line);
      padding-bottom: 0.04in;
    }

    h3 {
      font-size: 14px;
      margin: 0.16in 0 0.03in;
    }

    p {
      margin: 0 0 0.08in;
    }

    ul {
      margin: 0.05in 0 0.12in;
      padding-left: 0.18in;
    }

    li {
      margin-bottom: 0.05in;
    }

    .role-meta,
    .contact,
    .small {
      color: var(--muted);
      font-size: 11px;
    }

    .tag-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.05in;
      margin-top: 0.06in;
    }

    .tag {
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 0.03in 0.06in;
      background: #ffffff;
      font-size: 10.5px;
    }

    @media print {
      body {
        background: #ffffff;
      }

      .resume {
        width: 8.5in;
        margin: 0;
        box-shadow: none;
      }
    }
  </style>
</head>
<body>
  <!-- Copy this HTML into a browser for PDF export, or use the structure as a source for Canva, Figma, Google Docs, or Word. Replace PROFILE_PHOTO_PATH only when the user provides a profile picture and approves using it. -->
  <article class="resume">
    <aside class="sidebar">
      <div class="photo-placeholder">Optional profile photo</div>
      <!-- <img class="photo" src="PROFILE_PHOTO_PATH" alt="Profile photo"> -->
      <section>
        <h2>Contact</h2>
        <p class="contact">Name<br>Email<br>Phone<br>Location<br>LinkedIn<br>GitHub</p>
      </section>
      <section>
        <h2>Core Skills</h2>
        <div class="tag-list">
          <span class="tag">Skill</span>
          <span class="tag">Skill</span>
          <span class="tag">Skill</span>
        </div>
      </section>
      <section>
        <h2>Education</h2>
        <p class="small">Degree, School</p>
      </section>
    </aside>
    <main class="main">
      <header>
        <h1>Candidate Name</h1>
        <p class="role-meta">Target Role | Domain | Years of Experience</p>
      </header>
      <section>
        <h2>Summary</h2>
        <p>Evidence-backed professional summary.</p>
      </section>
      <section>
        <h2>Experience</h2>
        <h3>Company | Title</h3>
        <p class="role-meta">Dates</p>
        <ul>
          <li>Polished, sanitized impact bullet.</li>
          <li>Polished, sanitized impact bullet.</li>
          <li>Polished, sanitized impact bullet.</li>
        </ul>
      </section>
      <section>
        <h2>Selected Projects</h2>
        <h3>Project Name</h3>
        <ul>
          <li>Evidence-backed project bullet.</li>
        </ul>
      </section>
      <section>
        <h2>Open Source</h2>
        <ul>
          <li>Public contribution bullet.</li>
        </ul>
      </section>
    </main>
  </article>
</body>
</html>
```

- [ ] **Step 5: Create `targeted-resume.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/targeted-resume.md` with:

```markdown
# Targeted Resume

## Target Role

- Company:
- Job title:
- Posting source:
- Match strategy:

## Contact

Name | Email | Phone | Location | LinkedIn | GitHub

## Targeted Summary

Summary aligned to the posting and supported by evidence.

## Targeted Skills

- Direct matches:
- Adjacent strengths:
- Tools and platforms:

## Experience

### Company | Title | Dates

- Posting-aligned impact bullet.
- Posting-aligned impact bullet.
- Posting-aligned impact bullet.

## Selected Evidence For This Posting

- 
```

- [ ] **Step 6: Create `cover-letter.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/cover-letter.md` with:

```markdown
# Cover Letter

Dear Hiring Team,

Opening paragraph connecting the candidate's background to the role.

Middle paragraph with two or three evidence-backed examples.

Middle paragraph explaining fit for the company, team, domain, or technology.

Closing paragraph with interest and availability.

Sincerely,

Name

## Evidence Used

- 
```

- [ ] **Step 7: Create `linkedin-recommendations.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/linkedin-recommendations.md` with:

```markdown
# LinkedIn Recommendations

## Headline Options

1. 
2. 
3. 

## About Section Draft

Editable LinkedIn About section.

## Experience Updates

### Company | Title

- Recommended public-safe bullet.
- Recommended public-safe bullet.

## Featured Section

- Project, repository, article, talk, or portfolio item.

## Skills

- Add or prioritize:
- Remove or de-emphasize:

## Confidentiality Notes

- 
```

- [ ] **Step 8: Create `gap-analysis.md` template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/gap-analysis.md` with:

```markdown
# Gap Analysis

## Target Posting

- Company:
- Role:
- Seniority:
- Source:

## Requirement Match

| Requirement | Match Level | Evidence | Resume Action |
| --- | --- | --- | --- |
|  | Strong match |  |  |
|  | Partial match |  |  |
|  | Gap |  |  |
|  | Needs user input |  |  |

## Keyword Coverage

- Covered:
- Missing:
- Adjacent:

## Suggested Positioning

- 

## Honest Gap Mitigations

- 
```

- [ ] **Step 9: Commit templates**

Run:

```bash
git add plugins/resume-intelligence/skills/resume-intelligence/assets/templates/evidence.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/draft-resume.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/professional-resume.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/designed-resume.html plugins/resume-intelligence/skills/resume-intelligence/assets/templates/targeted-resume.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/cover-letter.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/linkedin-recommendations.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/gap-analysis.md
git commit -m "Add resume intelligence output templates"
```

Expected: commit succeeds with eight template files.

## Task 5: Add Dry-Run Validation Scenarios

**Files:**
- Create: `plugins/resume-intelligence/validation/dry-run-scenarios.md`

- [ ] **Step 1: Create validation directory**

Run:

```bash
mkdir -p plugins/resume-intelligence/validation
```

Expected: command exits 0.

- [ ] **Step 2: Write dry-run scenarios**

Create `plugins/resume-intelligence/validation/dry-run-scenarios.md` with:

```markdown
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
- Enterprise evidence: private PR summaries for CI/CD modernization, service reliability, and migration work.
- Public evidence: open-source Kubernetes operator contributions.

Expected outputs:

- `evidence.md` preserves separate source contexts.
- Enterprise repository names are summarized unless approved.
- Public open-source contributions are visible in a separate section.
- Final bullets combine career impact without losing provenance in the evidence log.

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
- Profile-picture evidence: user-provided local image path with permission to include it in visual resume output.

Expected outputs:

- `professional-resume.md` remains ATS-friendly and text-first.
- `designed-resume.html` includes sanitized resume content and a profile-picture slot.
- Profile picture is referenced only through the user-approved local path or left as a replacement placeholder.
- Output guidance explains browser-to-PDF export and copy/import into Canva, Figma, Google Docs, or Word.
```

- [ ] **Step 3: Commit validation scenarios**

Run:

```bash
git add plugins/resume-intelligence/validation/dry-run-scenarios.md
git commit -m "Add resume intelligence dry-run scenarios"
```

Expected: commit succeeds with the validation scenario file.

## Task 6: Validate Plugin, Skill, and Placeholder Hygiene

**Files:**
- Verify: `plugins/resume-intelligence/.codex-plugin/plugin.json`
- Verify: `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`
- Verify: `plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml`
- Verify: `plugins/resume-intelligence/skills/resume-intelligence/references/*.md`
- Verify: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/*.md`
- Verify: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/*.html`
- Verify: `plugins/resume-intelligence/validation/dry-run-scenarios.md`

- [ ] **Step 1: Run official plugin validation**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/resume-intelligence
```

Expected: command exits 0 and reports the plugin is valid.

- [ ] **Step 2: Run official skill validation**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/resume-intelligence/skills/resume-intelligence
```

Expected output:

```text
Skill is valid!
```

- [ ] **Step 3: Scan for placeholder markers**

Run:

```bash
rg -n "TO[D]O|TB[D]|FIX[M]E|\\[TO[D]O" plugins/resume-intelligence docs/superpowers
```

Expected: command exits 1 with no matches.

- [ ] **Step 4: Inspect final file list**

Run:

```bash
find plugins/resume-intelligence -maxdepth 6 -type f -print
```

Expected output includes:

```text
plugins/resume-intelligence/.codex-plugin/plugin.json
plugins/resume-intelligence/skills/resume-intelligence/SKILL.md
plugins/resume-intelligence/skills/resume-intelligence/agents/openai.yaml
plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md
plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md
plugins/resume-intelligence/skills/resume-intelligence/references/privacy-sanitization.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/evidence.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/draft-resume.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/professional-resume.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/designed-resume.html
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/targeted-resume.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/cover-letter.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/linkedin-recommendations.md
plugins/resume-intelligence/skills/resume-intelligence/assets/templates/gap-analysis.md
plugins/resume-intelligence/validation/dry-run-scenarios.md
```

- [ ] **Step 5: Commit validation cleanup if files changed**

Run:

```bash
git status --short
```

Expected: no output after prior commits, or only intended validation edits.

If validation edits were made, run:

```bash
git add plugins/resume-intelligence
git commit -m "Validate resume intelligence plugin"
```

Expected: commit succeeds only when validation edits exist.

## Self-Review

Spec coverage:

- Plugin source location under `plugins/resume-intelligence`: Task 1.
- Core skill: Task 2.
- Multi-source and multi-GitHub model: Task 2 and Task 3.
- Local docs, Confluence, Jira, GitHub, LinkedIn, job posting, and market research workflow: Task 2 and Task 3.
- Privacy, credential, and disclosure boundaries: Task 2 and Task 3.
- Markdown outputs and professional designed HTML template with optional profile-picture support: Task 4.
- Dry-run validation scenarios: Task 5.
- Official validation: Task 6.
- Marketplace install excluded from v1: covered by absence of marketplace task and plugin source staying in repo.

Placeholder scan:

- The plan avoids placeholder markers and uses empty Markdown template fields intentionally as user-fillable output structure.

Type and naming consistency:

- Plugin name, skill folder, skill frontmatter name, and metadata prompt all use `resume-intelligence`.
- Source context names match the design spec: `linkedin-profile`, `local-docs`, `confluence`, `jira`, `github-enterprise`, `github-public`, `job-posting`, `peer-market-research`, and `profile-picture`.
