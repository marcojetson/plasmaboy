import Phaser from 'phaser';
import { gameConfig } from '@/config/GameConfig';
import { installPwa } from '@/pwa';

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}

installPwa();
const game = new Phaser.Game(gameConfig);

// Keep the canvas matched to the visual viewport. On mobile, visualViewport 'scroll' (and
// sometimes 'resize') fire in bursts — every address-bar nudge or touch-drag — but usually with
// the SAME dimensions. game.scale.resize() is heavyweight (recomputes the canvas + WebGL
// viewport), so calling it on every event caused the periodic freezing. We now (a) coalesce all
// events into at most one resize per animation frame, and (b) skip the resize entirely when the
// dimensions haven't actually changed. That turns a storm of hundreds of resizes into a handful.
let lastW = 0;
let lastH = 0;
let syncScheduled = false;
const syncSize = () => {
  syncScheduled = false;
  const vp = window.visualViewport;
  const w = Math.round(vp ? vp.width : window.innerWidth);
  const h = Math.round(vp ? vp.height : window.innerHeight);
  if (w === lastW && h === lastH) return;
  lastW = w;
  lastH = h;
  game.scale.resize(w, h);
};
const scheduleSync = () => {
  if (syncScheduled) return;
  syncScheduled = true;
  requestAnimationFrame(syncSize);
};
window.addEventListener('resize', scheduleSync);
window.visualViewport?.addEventListener('resize', scheduleSync);
window.visualViewport?.addEventListener('scroll', scheduleSync);

for (const ev of ['gesturestart', 'gesturechange', 'gestureend']) {
  document.addEventListener(ev, (e) => e.preventDefault(), { passive: false });
}
