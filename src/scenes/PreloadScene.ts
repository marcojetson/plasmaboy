import Phaser from 'phaser';
import { SPRITE_SOURCES } from '@/config/SpriteAssets';
import { registerPlayerAnimations, registerEnemyAnimations } from '@/config/AnimationDefs';
import { t } from '@/i18n/i18n';

export class PreloadScene extends Phaser.Scene {
  private finished = false;

  constructor() {
    super('Preload');
  }

  create(): void {
    this.finished = false;
    this.add
      .text(this.scale.width / 2, this.scale.height / 2, t('loading'), {
        fontFamily: 'monospace',
        fontSize: '24px',
        color: '#ffffff',
      })
      .setOrigin(0.5);

    const entries = Object.entries(SPRITE_SOURCES);
    const pending = new Set(entries.filter(([key]) => !this.textures.exists(key)).map(([key]) => key));

    if (pending.size === 0) {
      this.finish();
      return;
    }

    const onResolved = (key: string): void => {
      if (!pending.has(key)) return;
      pending.delete(key);
      this.checkDone();
    };
    const onAdd = (key: string): void => onResolved(key);
    const onError = (key: string): void => {
      console.warn('[Preload] texture failed:', key);
      onResolved(key);
    };

    this.textures.on(Phaser.Textures.Events.ADD, onAdd);
    this.textures.on(Phaser.Textures.Events.ERROR, onError);

    for (const [key, uri] of entries) {
      if (!pending.has(key)) continue;
      try {
        this.textures.addBase64(key, uri);
      } catch (err) {
        console.warn('[Preload] addBase64 threw for', key, err);
        onResolved(key);
      }
    }

    this.time.delayedCall(8000, () => this.finish());
    this.time.addEvent({
      delay: 250,
      loop: true,
      callback: () => this.checkDone(),
    });
  }

  private checkDone(): void {
    if (this.finished || !this.scene.isActive()) return;
    const keys = Object.keys(SPRITE_SOURCES);
    const loaded = keys.filter((k) => this.textures.exists(k));
    if (loaded.length === keys.length) {
      this.finish();
    }
  }

  private finish(): void {
    if (this.finished) return;
    this.finished = true;
    registerPlayerAnimations(this);
    registerEnemyAnimations(this);
    this.prewarmTextures();
    this.time.delayedCall(80, () => this.scene.start('MainMenu'));
  }

  private prewarmTextures(): void {
    const warm: Phaser.GameObjects.Image[] = [];
    for (const key of this.textures.getTextureKeys()) {
      try {
        warm.push(this.add.image(0, 0, key).setScale(0.01));
      } catch {
        // skip textures that can't be rendered yet
      }
    }
    this.time.delayedCall(60, () => warm.forEach((img) => img.destroy()));
  }
}
