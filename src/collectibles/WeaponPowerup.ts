import Phaser from 'phaser';
import type { Player } from '@/entities/Player';
import { burstParticles } from '@/utils/fx';
import { AudioManager } from '@/audio/AudioManager';

export type PowerupWeaponType = 'shoulder-cannon' | 'katana';

const TEXTURES: Record<PowerupWeaponType, string> = {
  'shoulder-cannon': 'capsule-shoulder',
  katana: 'capsule-katana',
};

export interface WeaponPowerupConfig {
  scene: Phaser.Scene;
  x: number;
  y: number;
  weaponType: PowerupWeaponType;
}

export class WeaponPowerup extends Phaser.Physics.Arcade.Sprite {
  readonly weaponType: PowerupWeaponType;
  private collected = false;

  constructor(config: WeaponPowerupConfig) {
    super(config.scene, config.x, config.y, TEXTURES[config.weaponType]);
    this.weaponType = config.weaponType;
    config.scene.add.existing(this);
    config.scene.physics.add.existing(this);
    (this.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
  }

  onCollect(player: Player): void {
    if (this.collected) return;
    this.collected = true;
    player.activatePowerup(this.weaponType);
    burstParticles(this.scene, this.x, this.y, 0xffe066, 8);
    AudioManager.instance.play('pickup');
    this.scene.tweens.add({
      targets: this,
      scale: 1.6,
      alpha: 0,
      duration: 150,
      onComplete: () => this.destroy(),
    });
  }

  settleBody(): void {
    (this.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
  }
}
