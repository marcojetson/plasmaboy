import Phaser from 'phaser';
import type { Player } from '@/entities/Player';
import { burstParticles } from '@/utils/fx';
import { AudioManager } from '@/audio/AudioManager';

const HEALTH_HEAL_PERCENT = 0.2;

export class HealthPickup extends Phaser.Physics.Arcade.Sprite {
  private collected = false;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'heart-icon');
    scene.add.existing(this);
    scene.physics.add.existing(this);
    (this.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
    this.setDepth(15);
  }

  onCollect(player: Player): void {
    if (this.collected) return;
    this.collected = true;
    const healAmount = Math.floor(player.getMaxHealth() * HEALTH_HEAL_PERCENT);
    player.restoreHealth(healAmount);
    burstParticles(this.scene, this.x, this.y, 0x44ff44, 8);
    AudioManager.instance.play('pickup');
    this.scene.tweens.add({
      targets: this,
      scale: 1.6,
      alpha: 0,
      duration: 150,
      onComplete: () => this.destroy(),
    });
  }
}
