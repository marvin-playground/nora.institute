# Nora Institute Blog Publishing Workflow

## Overview

Two-step publishing: Write Markdown, publish to GitHub Pages with one command.

## Usage

### 1. Create Markdown Article

Write a `.md` file in `blog/` with:
- Title: `# Your Article Title`
- Metadata: `**Date:** YYYY-MM-DD` (extracted automatically)
- Content: Standard Markdown

Example: `blog/your-article.md`

```markdown
# The Attention Allocation Problem

**Date:** 2026-02-18 | **Status:** Draft

Your article content here...

## Section Heading

More content.
```

### 2. Publish

```bash
cd projects/nora-labs-institute/site
python3 publish.py your-article
```

This:
- Converts `blog/your-article.md` → `blog/your-article.html`
- Extracts metadata (title, date, read time)
- Generates responsive HTML with Nora design
- Commits and pushes to GitHub Pages
- Outputs: `✅ Published: [Title]`

## Supported Markdown

- **Headings:** `## Section` → `<h2>`, `### Subsection` → `<h3>`
- **Bold:** `**text**` → `<strong>`
- **Italic:** `*text*` → `<em>`
- **Links:** `[text](url)` → `<a href>`
- **Lists:** `- item` → `<ul><li>`
- **Blockquotes:** `> quote` → `<blockquote>`
- **Tables:** Standard markdown tables `| col | col |`
- **Horizontal rules:** `---` or `***`

## Automation

To automate publishing on commit:

```bash
# Create a GitHub Actions workflow (future enhancement)
mkdir -p .github/workflows
```

For now, one-command publishing via `python3 publish.py [article]` is the workflow.

## SEO

HTML output includes:
- `<title>` and `<meta description>`
- Open Graph tags (og:title, og:description, og:type)
- Proper heading hierarchy
- Responsive viewport

## Files Structure

```
site/
├── blog/
│   ├── article-name.md      ← Write here
│   ├── article-name.html    ← Generated automatically
│   └── index.html           ← Blog listing
├── publish.py               ← Run this
└── PUBLISHING.md            ← This file
```

## Example Workflow

```bash
# 1. Write article
nano blog/my-research.md

# 2. Publish
python3 publish.py my-research

# 3. Check GitHub Pages
# https://nora.institute/blog/my-research.html
```

---

**Note:** The Python publisher is designed to work offline and handle network errors gracefully. If git push fails, the HTML is still generated locally.
