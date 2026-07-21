// Every sprite under src/sprites/*.svg, imported as its raw SVG source at build time, then
// turned into an in-page data: URI. Phaser's loader consumes these directly — no network
// fetch for sprites in dev OR prod. That's what lets the production build (with
// vite-plugin-singlefile) ship as ONE self-contained index.html that runs by double-clicking
// in any browser, offline, with no install. The texture key is the filename sans extension.
const modules = import.meta.glob('../sprites/*.svg', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>;

export const SPRITE_SOURCES: Record<string, string> = {};
for (const [path, svg] of Object.entries(modules)) {
  const key = path.split('/').pop()!.replace('.svg', '');
  SPRITE_SOURCES[key] = `data:image/svg+xml,${encodeURIComponent(svg)}`;
}
