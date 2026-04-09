import { defineCollection, z } from "astro:content";

const portfolio = defineCollection({
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    tagline: z.string(),
    status: z.enum(["in-development", "research-phase", "shipped"]),
    stack: z.array(z.string()),
    featured: z.boolean().default(false),
    order: z.number().default(999),
    links: z
      .object({
        github: z.string().url().optional(),
        demo: z.string().url().optional(),
        website: z.string().url().optional()
      })
      .optional(),
    screenshot: z.string().optional()
  })
});

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    publishedAt: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false)
  })
});

const research = defineCollection({
  schema: z.object({
    title: z.string(),
    shortTitle: z.string(),
    abstract: z.string(),
    field: z.string(),
    status: z.string(),
    platform: z.string(),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    publishedAt: z.coerce.date().optional(),
    links: z
      .object({
        paper: z.string().url().optional(),
        repository: z.string().url().optional(),
        demo: z.string().url().optional()
      })
      .optional()
  })
});

export const collections = { portfolio, blog, research };
