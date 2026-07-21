import Phaser from 'phaser';
import { burstParticles } from '@/utils/fx';
import { AudioManager } from '@/audio/AudioManager';

const COIN_SCORE = 25;

export class ScoreCoin extends Phaser.Physics.Arcade.Sprite {
  private collected = false;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'coin');
    scene.add.existing(this);
    scene.physics.add.existing(this);
    (this.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
    this.setDepth(15);
  }

  onCollect(): number {
    if (this.collected) return 0;
    this.collected = true;
    burstParticles(this.scene, this.x, this.y, 0xffd700, 8);
    AudioManager.instance.play('pickup');
    this.scene.tweens.add({
      targets: this,
      scale: 1.6,
      alpha: 0,
      duration: 150,
      onComplete: () => this.destroy(),
    });
    return COIN_SCORE;
  }
}
