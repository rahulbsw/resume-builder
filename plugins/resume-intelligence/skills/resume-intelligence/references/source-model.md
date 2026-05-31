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
