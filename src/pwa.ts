import { APP_ICON_PNG } from '@/config/appIcon';

/** Make the game installable / "Add to Home Screen" as a fullscreen, landscape web app. Everything
 * is self-contained — the manifest is built at runtime as a blob and the icon is an embedded data
 * URI — so it needs no separate manifest.json/icon files and works whether the page is hosted or
 * opened directly. iOS reads the apple-* <meta> tags (in index.html) + apple-touch-icon for its
 * fullscreen home-screen mode; Android/Chrome reads the manifest. */
export function installPwa(): void {
  if (typeof document === 'undefined' || typeof URL.createObjectURL !== 'function') return;

  const manifest = {
    name: 'Plasma Boy vs Plantas Monstruo',
    short_name: 'Plasma Boy',
    description: 'A 2D action platformer — Plasma Boy vs the monster plants.',
    start_url: location.href,
    display: 'fullscreen',
    orientation: 'landscape',
    background_color: '#0a0a12',
    theme_color: '#0a0a12',
    icons: [{ src: APP_ICON_PNG, sizes: '512x512', type: 'image/png', purpose: 'any maskable' }],
  };

  const blob = new Blob([JSON.stringify(manifest)], { type: 'application/manifest+json' });
  const manifestLink = document.createElement('link');
  manifestLink.rel = 'manifest';
  manifestLink.href = URL.createObjectURL(blob);
  document.head.appendChild(manifestLink);

  // iOS uses a link tag (not the manifest) for the home-screen icon.
  const appleIcon = document.createElement('link');
  appleIcon.rel = 'apple-touch-icon';
  appleIcon.href = APP_ICON_PNG;
  document.head.appendChild(appleIcon);
}
