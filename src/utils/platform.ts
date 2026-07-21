/** Touch-play detection. True on phones/tablets (coarse pointer + touch points), false on a
 * desktop with a mouse — even a touchscreen laptop, which we treat as desktop. Force it either
 * way for testing with ?touch=1 / ?touch=0 on the URL. */
export function isTouchDevice(): boolean {
  if (typeof window !== 'undefined') {
    const forced = new URLSearchParams(window.location.search).get('touch');
    if (forced !== null) return forced !== '0';
  }
  if (typeof navigator === 'undefined' || typeof window === 'undefined') return false;
  const coarse = window.matchMedia?.('(pointer: coarse)').matches ?? false;
  return coarse && navigator.maxTouchPoints > 0;
}

/** The Phaser canvas resolution. Uses the visual viewport dimensions so the game fills 100% of
 * the viewport on every device — no black bars, no letterboxing. visualViewport correctly
 * accounts for safe-area insets (PWA standalone, notched phones) that window.innerHeight misses. */
export function getGameSize(): { width: number; height: number } {
  const vp = window.visualViewport;
  if (vp) {
    return {
      width: Math.round(vp.width),
      height: Math.round(vp.height),
    };
  }
  return { width: window.innerWidth, height: window.innerHeight };
}
