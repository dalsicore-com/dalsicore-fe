# Dalsicore Website

Modern, markdown-driven personal/company site for Dalsicore using Astro.

## Stack

- Astro
- Markdown Content Collections
- Modular component-based structure

## Run locally

```bash
npm install
npm run dev
```

## Content updates

Add new entries by creating markdown files in:

- `src/content/blog`
- `src/content/portfolio`
- `src/content/research`

Each entry uses frontmatter metadata defined in `src/content.config.ts`.

## Structure overview

- `src/pages` for routes
- `src/layouts` for reusable page shells
- `src/components` for UI and section components
- `src/styles` for design tokens and global styles
