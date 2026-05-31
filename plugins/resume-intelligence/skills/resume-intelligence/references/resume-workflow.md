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
