# Resume Workflow

## Evidence First

Start with `evidence.md`. Do not write polished resume bullets until the evidence log has source contexts, claims, confidence, and disclosure and quoting rules.

For each claim, capture:

- Claim text.
- Source context ID.
- Evidence reference.
- Confidence: high, medium, or low.
- Disclosure level: public, internal-summary-only, confidential, excluded, or unknown.
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
4. Preserve truthfulness and disclosure and quoting rules.
5. Add a gap analysis instead of hiding missing requirements.

## Job Posting Match

For each important job requirement, classify:

- Strong match: direct evidence exists.
- Partial match: adjacent evidence exists.
- Gap: no evidence found.
- Needs user input: likely experience but not supported by collected sources.

Use this classification in `gap-analysis.md`, then produce `targeted-resume.md` and `cover-letter.md`.

## Resume Scorecard

Create `resume-scorecard.md` before final resume wording. Use it as a gate before producing `professional-resume.md`, `targeted-resume.md`, and `designed-resume.html`.

### Page-Length Strategy

- Recommend one page for early-career profiles, highly focused applications, or when the strongest evidence fits cleanly without shrinking text.
- Recommend two pages by default for senior, staff, principal, management, enterprise, or open-source-heavy profiles with more than about 8 years of experience.
- Recommend more than two pages only for academic CVs, federal/government resumes, patent/publication-heavy profiles, executive packets, or when the user explicitly asks.
- Never reduce readability to force one page. Prefer a clean two-page resume over tiny text, cramped margins, or deleted impact.

### ATS Safety

For the ATS-safe resume, check:

- No profile photo, icons, text boxes, complex tables, headers/footers carrying important content, or multi-column content that must parse correctly.
- Standard section headings: Summary, Technical Skills, Professional Experience, Selected Projects, Open Source, Education, Certifications.
- Text-based Markdown/DOCX/PDF source, not an image-only or scanned PDF.
- Plain job titles, company names, dates, skills, and bullets that an applicant tracking system can extract.
- No hidden keyword stuffing or unsupported claims.

The designed HTML resume can be more polished, but it is not the primary ATS submission format.

### Recruiter First-Page Strength

The first page should show the role match within a short skim:

- Header or summary includes the target role family and seniority.
- Summary states domain, scope, leadership level, and strongest technical themes.
- Skills are grouped by category and prioritize the target role's required technologies.
- The first experience section contains the strongest 3-5 quantified or scope-backed bullets.
- Enterprise work is sanitized without becoming vague.
- Public open-source contributions appear when they strengthen the target role match.

### Keyword Coverage

When a job posting is provided, extract keywords into:

- Role and seniority keywords.
- Required technologies.
- Preferred technologies.
- Domain and platform terms.
- Leadership and collaboration terms.
- Outcome terms such as reliability, cost, latency, scale, security, adoption, productivity, or incident reduction.

For each keyword, classify:

- Covered: direct evidence supports using the keyword.
- Partial: adjacent evidence supports a related keyword.
- Gap: no evidence supports it.
- Needs user input: likely experience but not supported by collected sources.
- Exclude: keyword would be misleading or unsupported.

Use exact posting terms naturally when evidence supports them. Do not add keywords only to game ATS ranking.

### Scorecard Outcome

End the scorecard with:

- Recommended page count.
- ATS risk level: low, medium, or high.
- Recruiter skim strength: strong, adequate, or weak.
- Keyword coverage percentage or qualitative summary.
- Top five fixes before applying.
- Claims that need user confirmation.

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
- Disclosure-safe enterprise project wording.

Do not post changes automatically. Keep suggestions in `linkedin-recommendations.md`.
