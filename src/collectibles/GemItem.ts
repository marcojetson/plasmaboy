import Phaser from 'phaser';
import { burstParticles } from '@/utils/fx';
import { AudioManager } from '@/audio/AudioManager';

const GEM_SCORE = 100;

export class GemItem extends Phaser.Physics.Arcade.Sprite {
  private collected = false;

  constructor(scene: Phaser.Scene, x: number, y: number, tint: number, _name: string, scale = 0.7) {
    super(scene, x, y, 'gem');
    scene.add.existing(this);
    scene.physics.add.existing(this);
    (this.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
    this.setDepth(15);
    this.setTint(tint);
    this.setScale(scale);
  }

  onCollect(): number {
    if (this.collected) return 0;
    this.collected = true;
    burstParticles(this.scene, this.x, this.y, this.tint, 12);
    AudioManager.instance.play('gem');
    this.scene.tweens.add({
      targets: this,
      scale: 1.5,
      alpha: 0,
      duration: 300,
      onComplete: () => this.destroy(),
    });
    return GEM_SCORE;
  }
}
