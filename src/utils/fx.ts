import Phaser from 'phaser';
import { DEPTH } from '@/config/Constants';

/** Small burst of fading, outward-flying dots — the only "hit feedback" placeholder art can give. */
export function burstParticles(scene: Phaser.Scene, x: number, y: number, color: number, count = 6): void {
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count + Phaser.Math.FloatBetween(-0.3, 0.3);
    const speed = Phaser.Math.Between(80, 160);
    const dot = scene.add.circle(x, y, 3, color).setDepth(DEPTH.fx);
    scene.tweens.add({
      targets: dot,
      x: x + Math.cos(angle) * speed * 0.3,
      y: y + Math.sin(angle) * speed * 0.3,
      alpha: 0,
      duration: 300,
      ease: 'Cubic.Out',
      onComplete: () => dot.destroy(),
    });
  }
}

export function shakeCamera(scene: Phaser.Scene, durationMs = 120, intensity = 0.006): void {
  scene.cameras.main.shake(durationMs, intensity);
}

/** Full-screen flash overlay, used sparingly for high-stakes moments (boss phase transitions). */
export function flashScreen(scene: Phaser.Scene, color = 0xffffff, durationMs = 180): void {
  const cam = scene.cameras.main;
  const overlay = scene.add
    .rectangle(cam.width / 2, cam.height / 2, cam.width, cam.height, color, 0.8)
    .setScrollFactor(0)
    .setDepth(DEPTH.fx + 1);
  scene.tweens.add({
    targets: overlay,
    alpha: 0,
    duration: durationMs,
    onComplete: () => overlay.destroy(),
  });
}
