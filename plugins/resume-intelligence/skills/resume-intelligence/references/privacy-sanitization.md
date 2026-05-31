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
