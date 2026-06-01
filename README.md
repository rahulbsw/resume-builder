# Resume Intelligence

Resume Intelligence is a local Codex/Claude/Cursor-friendly plugin for building evidence-backed resumes, ATS-safe application files, recruiter-facing visual resumes, LinkedIn recommendations, job match reports, and interview prep from approved career evidence.

It is designed for profiles where evidence is spread across LinkedIn exports, local project documents, Confluence, Jira, public GitHub, GitHub Enterprise, open-source work, and job postings.

## What It Produces

- `source-inventory.md`: every approved source, folder, connector scope, skipped file, and scan status.
- `tool-usage-log.md`: tools, commands, connector calls, searches, and manual inputs used.
- `evidence.md`: source-backed claims with confidence and disclosure rules.
- `run-summary.md`: concise audit of sources scanned, tools used, outputs created, quality warnings, sensitive approvals, and missing user answers.
- `draft-resume.md` and `professional-resume.md`: evidence-backed resume drafts.
- `detailed-resume.md`: full interview/master resume with timeline, roles, responsibilities, projects, impact, metrics, and missing-info questions.
- `ats-resume.docx`: clean application resume for ATS/job portals.
- `designed-resume.html` and optional `designed-resume.pdf`: high-quality recruiter/referral visual resume.
- `designed-resume.docx`: optional editable Word companion, not the main visual surface.
- `resume-scorecard.md`: ATS, recruiter, page-count, keyword, and claim-risk review.
- `targeted-resume.md`, `cover-letter.md`, and `gap-analysis.md`: job-specific outputs.
- `job-match-report.md`: job search and match scoring.
- `project-interview-briefs.md`, `technical-stack-interview-guide.md`, and `interview-prep-pack.md`: interview prep.
- `linkedin-recommendations.md`: editable LinkedIn profile improvements.
- `visual-design-review.md` and `visual-tool-handoff.md`: Figma/Canva/HTML/PDF design handoff notes.

## Repository Layout

```text
.
|-- .agents/plugins/marketplace.json          # Codex local marketplace manifest
|-- .claude-plugin/marketplace.json           # Claude Code marketplace manifest
|-- plugins/resume-intelligence/
|   |-- .codex-plugin/plugin.json             # Codex plugin manifest
|   |-- .claude-plugin/plugin.json            # Claude Code plugin manifest
|   |-- .cursor-plugin/plugin.json            # Cursor plugin metadata
|   |-- skills/resume-intelligence/SKILL.md   # Main workflow
|   |-- skills/resume-intelligence/references/
|   |-- skills/resume-intelligence/assets/
|   |-- skills/resume-intelligence/scripts/
|   `-- validation/dry-run-scenarios.md
`-- docs/superpowers/
```

## Install For Codex

### From GitHub

After this repository is published:

```bash
codex plugin marketplace add rahulbsw/resume-builder
codex plugin add resume-intelligence@resume-builder-local
```

The Codex marketplace name is defined in `.agents/plugins/marketplace.json` as `resume-builder-local`.

### From A Local Clone

```bash
git clone https://github.com/rahulbsw/resume-builder.git
cd resume-builder
codex plugin marketplace add "$(pwd)"
codex plugin add resume-intelligence@resume-builder-local
```

### Update An Existing Local Codex Install

```bash
cd /path/to/resume-builder
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/resume-intelligence
codex plugin add resume-intelligence@resume-builder-local
```

Start a new Codex thread after reinstalling so new skill metadata and templates are loaded.

## Install For Claude Code

This repo includes Claude Code plugin manifests.

### Marketplace Install

```bash
claude plugin marketplace add rahulbsw/resume-builder
claude plugin install resume-intelligence@resume-builder
```

### Local Install For Development

```bash
git clone https://github.com/rahulbsw/resume-builder.git
cd resume-builder
claude plugin marketplace add "$(pwd)"
claude plugin install resume-intelligence@resume-builder
```

### One-Session Local Use

Use this when you want to test without installing a marketplace:

```bash
claude --plugin-dir plugins/resume-intelligence
```

## Install For Cursor

Cursor support depends on the Cursor version and plugin/MCP features available in your environment. This repo includes `.cursor-plugin/plugin.json` metadata and can be used in two practical ways.

### Project Context Use

```bash
git clone https://github.com/rahulbsw/resume-builder.git
cursor resume-builder
```

In Cursor, ask the agent to use:

```text
Use the Resume Intelligence skill in plugins/resume-intelligence to build my ATS resume, visual recruiter resume, job match report, and interview prep.
```

### MCP/Tool Setup

For best results in Cursor, add the same MCP tools you use in Codex or Claude: GitHub, Atlassian/Jira/Confluence, Figma, browser automation, and local filesystem access. Cursor supports adding MCP servers from the CLI:

```bash
cursor --add-mcp '{"name":"example-tool","command":"example-command","args":["--example"]}'
```

Use your real MCP server command and credentials. Do not commit tokens or secrets to this repository.

## Optional Tools For Best Experience

Resume Intelligence works with pasted text and local files, but it is strongest when the agent has tools for source collection, document rendering, and visual design.

Recommended optional tools:

- GitHub connector or `gh` CLI: public GitHub, GitHub Enterprise, PRs, issues, commits, and open-source evidence.
- Confluence connector: design docs, launch notes, architecture docs, and project summaries.
- Jira connector: epics, tickets, incidents, delivery evidence, and project timelines.
- Browser or Chrome tool: review local HTML resumes and export PDF when supported.
- Documents/DOCX tooling: create `ats-resume.docx` and render-check Word output.
- LibreOffice `soffice`: required for reliable DOCX render QA in many local environments.
- Figma plugin/MCP: create or refine a high-quality visual resume when you approve a target Figma file.
- Canva: useful for manual visual polish; use the generated HTML/PDF and `visual-tool-handoff.md` as the handoff package.
- Web search: current job postings, market language, and job match scoring.

Useful Codex installs when available:

```bash
codex plugin add github@openai-curated
codex plugin add browser@openai-bundled
codex plugin add chrome@openai-bundled
codex plugin add documents@openai-primary-runtime
codex plugin add figma@claude-plugins-official
```

Some plugin names and marketplaces vary by Codex installation. Run this to inspect what your environment exposes:

```bash
codex plugin list
```

## How To Use

Start with a new thread after installing or updating the plugin.

### General Resume

```text
Use $resume-intelligence to build my resume from:
- my LinkedIn export at <path or pasted text>
- local project docs under <folder>
- public GitHub user <username>
- GitHub Enterprise host <host> with internal-summary-only disclosure

Target role: Staff Platform Engineer
Years of experience: 12
Create ATS DOCX, professional HTML/PDF, LinkedIn recommendations, and interview prep.
```

### Job-Specific Resume And Cover Letter

```text
Use $resume-intelligence to tailor my resume and cover letter for this job posting: <paste posting or URL>.
Consider my years of experience, target seniority, required technologies, and evidence-backed achievements.
Create gap analysis and keyword coverage without inventing unsupported claims.
```

### Job Search And Match Scoring

```text
Use $resume-intelligence to search for matching senior/staff platform engineering jobs in the United States.
Score each job against my resume evidence, years of experience, target technologies, and location preference.
```

### Interview Prep

```text
Use $resume-intelligence to prepare interview material from my strongest projects.
Create project deep dives, technical-stack preparation, behavioral stories, system design prompts, and recruiter-screen talking points.
```

### Detailed Interview Resume / Master Timeline

```text
Use $resume-intelligence to create a detailed interview resume.
Include my full work timeline, every role, responsibilities, important projects, ownership, architecture decisions, impact, metrics, technologies, and questions for any missing information.
Do not invent dates, metrics, or ownership. Ask me for anything that is missing or low-confidence.
```

### Visual Resume

```text
Use $resume-intelligence to create my ATS DOCX plus a high-quality recruiter HTML/PDF resume.
Use visual-tool handoff if Canva or Figma would improve the design.
Do not upload private content to third-party tools without asking me first.
```

## Best Practices

- Keep ATS and visual outputs separate. Use `ats-resume.docx` for job portals and `designed-resume.html` or `designed-resume.pdf` for recruiter/referral sharing.
- Start with evidence. Require `source-inventory.md`, `tool-usage-log.md`, and `evidence.md` before polished resume wording.
- Keep current agent-guided behavior as the default. Helpers and quality gates improve visibility without blocking normal resume generation.
- Preserve public and enterprise GitHub as separate source contexts. They often have different identities, credentials, and disclosure rules.
- Treat enterprise Confluence, Jira, private repositories, customer names, internal URLs, and exact metrics as confidential until explicitly approved.
- Do not rely on LinkedIn scraping. Use pasted LinkedIn content, exports, public profile notes, or user-provided summaries.
- Prefer high-confidence claims. Mark weak or inferred claims for user confirmation instead of turning them into polished bullets.
- Use live search only for current job matching. Job postings change quickly.
- Use exact job keywords only when the evidence supports them. Avoid hidden keyword stuffing.
- Prefer HTML/PDF/Figma for visual quality. DOCX is important for editability and ATS submission, but it is not the best high-fidelity visual surface.
- Review every generated output before applying. The plugin helps draft and organize; you remain responsible for final truthfulness and disclosure.

## Optimization Tips

- Narrow connector queries by repo, project, space, date range, issue type, or keyword before pulling large histories.
- Use `python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py <approved-folder> --output resume-runs/<run>/source-inventory.md` for a deterministic first-pass inventory of a local evidence folder.
- Keep local evidence folders organized by project or employer. Recursive inventory works best when folders have meaningful names.
- Convert important PDFs, DOCX files, and exported tickets to text-friendly formats when possible.
- Keep one run per target role or job posting under `resume-runs/YYYY-MM-DD-<slug>/`.
- Reuse confirmed evidence across runs instead of re-collecting everything from scratch.
- Focus interview prep on the top 3-5 projects that show architecture, tradeoffs, ownership, impact, and lessons learned.
- Use `detailed-resume.md` as the master source for interview preparation, then trim into `professional-resume.md` and `targeted-resume.md` for applications.
- Use Figma or Canva only after content is sanitized and stable; otherwise visual polish will amplify content churn.

## Privacy And Credential Rules

- Never store credentials, tokens, cookies, or passwords in plugin files or generated outputs.
- Do not commit generated private resume runs unless you intentionally want them in Git.
- Do not upload private resume content, internal project details, or profile pictures to Canva, Figma, or another third-party service without explicit approval.
- Ask before including internal project names, customer names, repository names, Jira IDs, Confluence titles, private URLs, or exact internal metrics in final user-facing outputs.

## Validate The Plugin

Codex validation:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/resume-intelligence

python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/resume-intelligence/skills/resume-intelligence
```

If your Codex validator environment requires a custom `PYTHONPATH`, reuse the value from your local Codex setup.

Claude validation:

```bash
claude plugin validate .
claude plugin validate plugins/resume-intelligence
```

Generated DOCX structural check:

```bash
unzip -t plugins/resume-intelligence/skills/resume-intelligence/assets/docx-templates/ats-safe-resume-template.docx
unzip -t plugins/resume-intelligence/skills/resume-intelligence/assets/docx-templates/modern-technical-resume-template.docx
```

## Development Notes

After editing the Codex plugin, update the cachebuster and reinstall:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/resume-intelligence
codex plugin add resume-intelligence@resume-builder-local
```

Then start a new Codex thread before testing behavior.
