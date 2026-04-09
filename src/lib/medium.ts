import {XMLParser} from "fast-xml-parser";
import sanitizeHtml from "sanitize-html";

const MEDIUM_FEED_URL = "https://medium.com/feed/@anafthdev_";
const MEDIUM_PROXY_LINK_REGEX = /https:\/\/medium\.com\/media\/[a-zA-Z0-9]+\/href/g;

export interface MediumPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  contentHtml: string;
  thumbnail?: string;
  sourceUrl: string;
  publishedAt: Date;
  author: string;
  tags: string[];
}

const toArray = <T>(value: T | T[] | undefined): T[] => {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
};

const stripText = (html: string) =>
  sanitizeHtml(html, { allowedTags: [], allowedAttributes: {} })
    .replace(/\s+/g, " ")
    .trim();

const toExcerpt = (html: string) => {
  const text = stripText(html);
  if (text.length <= 185) return text;
  return `${text.slice(0, 182).trimEnd()}...`;
};

const toSlug = (url: string) => {
  const pathname = new URL(url).pathname;
  const value = pathname.split("/").filter(Boolean).pop() ?? "";
  return value.toLowerCase();
};

const extractFirstImage = (html: string) => {
  const matches = Array.from(html.matchAll(/<img[^>]+src=["']([^"']+)["'][^>]*>/gi));
  const candidate = matches
    .map((item) => item[1])
    .find((src) => src.includes("cdn-images") || src.includes("miro.medium"));
  return candidate ?? matches[0]?.[1];
};

const normalizeProxyAnchors = (html: string) =>
  html.replace(
    /<a([^>]*?)href=["'](https:\/\/medium\.com\/media\/[a-zA-Z0-9]+\/href)["']([^>]*)>(.*?)<\/a>/gis,
    (_full, before, href, after, inner) => {
      const textOnly = stripText(inner);
      const plainUrlMatch = textOnly.match(/https?:\/\/[^\s)]+/i);
      const finalHref = plainUrlMatch?.[0] ?? href;
      return `<a${before}href="${finalHref}"${after}>${inner}</a>`;
    }
  );

const resolveMediumProxyLinks = async (html: string) => {
  const matches = html.match(MEDIUM_PROXY_LINK_REGEX);
  if (!matches || matches.length === 0) return html;

  const uniqueMatches = Array.from(new Set(matches));
  const replacements = new Map<string, string>();

  await Promise.all(
    uniqueMatches.map(async (url) => {
      try {
        const response = await fetch(url, { redirect: "follow" });
        replacements.set(url, response.url || url);
      } catch {
        replacements.set(url, url);
      }
    })
  );

  let updatedHtml = html;
  for (const [from, to] of replacements.entries()) {
    updatedHtml = updatedHtml.split(from).join(to);
  }

  return updatedHtml;
};

const sanitizeMediumContent = (html: string) =>
  sanitizeHtml(html, {
    disallowedTagsMode: "discard",
    allowedTags: [
      "p",
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
      "blockquote",
      "pre",
      "code",
      "strong",
      "em",
      "ul",
      "ol",
      "li",
      "a",
      "img",
      "figure",
      "figcaption",
      "hr",
      "br"
    ],
    allowedAttributes: {
      a: ["href", "name", "target", "rel"],
      img: ["src", "alt", "width", "height"],
      figure: ["class"],
      code: ["class"]
    },
    transformTags: {
      a: (_tagName, attribs) => ({
        tagName: "a",
        attribs: {
          ...attribs,
          target: "_blank",
          rel: "noopener noreferrer"
        }
      })
    }
  });

const parseMediumItem = async (item: Record<string, unknown>): Promise<MediumPost> => {
  const sourceUrl = String(item.link ?? "").split("?")[0];
  const contentRaw = String(item["content:encoded"] ?? "");
  const resolvedContent = await resolveMediumProxyLinks(contentRaw);
  const normalizedContent = normalizeProxyAnchors(resolvedContent);
  const contentHtml = sanitizeMediumContent(normalizedContent);
  const title = String(item.title ?? "Untitled");
  const tags = toArray(item.category).map((tag) => String(tag).toLowerCase());
  const publishedAt = new Date(String(item.pubDate ?? Date.now()));
  const author = String(item["dc:creator"] ?? "Anaf Naufalian");
  const slug = toSlug(sourceUrl);
  const thumbnail = extractFirstImage(contentHtml);

  return {
    id: String(item.guid ?? slug),
    slug,
    title,
    excerpt: toExcerpt(contentHtml),
    contentHtml,
    thumbnail,
    sourceUrl,
    publishedAt,
    author,
    tags
  };
};

export const getMediumPosts = async (): Promise<MediumPost[]> => {
  const response = await fetch(MEDIUM_FEED_URL, {
    headers: {
      Accept: "application/rss+xml, application/xml, text/xml"
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch Medium feed: ${response.status}`);
  }

  const xml = await response.text();
  const parser = new XMLParser({
    ignoreAttributes: false,
    parseTagValue: true,
    trimValues: true
  });

  const parsed = parser.parse(xml);
  const items = toArray(parsed?.rss?.channel?.item);
  const posts = await Promise.all(items.map((item: Record<string, unknown>) => parseMediumItem(item)));

  return posts
    .filter((post) => post.slug && post.sourceUrl)
    .sort((a, b) => b.publishedAt.getTime() - a.publishedAt.getTime());
};
