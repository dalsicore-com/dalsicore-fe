const MARKDOWN_IMAGE_REGEX = /!\[[^\]]*\]\(([^)\s]+(?:\s+"[^"]*")?)\)/;

export const getFirstImageFromMarkdown = (markdownBody: string): string | undefined => {
  const match = markdownBody.match(MARKDOWN_IMAGE_REGEX);
  if (!match?.[1]) return undefined;

  const raw = match[1].trim();
  const url = raw.split(" ")[0]?.trim();
  if (!url) return undefined;

  if (url.startsWith("<") && url.endsWith(">")) {
    return url.slice(1, -1);
  }

  return url;
};
