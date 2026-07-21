import Phaser from 'phaser';
import { HuntStick } from '@/hunt/HuntStick';
import { PLAYER, DEPTH } from '@/config/Constants';
import { EventBus, GameEvents } from '@/events/EventBus';
import type { PowerupWeaponType } from '@/collectibles/WeaponPowerup';
import { CHARACTERS, type CharacterId } from '@/config/Characters';

const PLAYER_SPEED = 190;
const FIRE_MS = 420;
const BOLT_SPEED = 460;
const BOLT_DMG = 12;
const BOLT_RANGE = 340;

const MAX_ENERGY = 100;
const ENERGY_COST_PER_SHOT = 15;
const ENERGY_REGEN_PER_SECOND = 25;

const WEAPON_SPRITES: Record<PowerupWeaponType, string> = {
  'shoulder-cannon': 'player-shoulder-cannon',
  katana: 'player-katana',
};

const WEAPON_PROJECTILES: Record<PowerupWeaponType, string> = {
  'shoulder-cannon': 'shoulder-shell',
  katana: 'katana-slash',
};

export interface PlayerConfig {
  scene: Phaser.Scene;
  x: number;
  y: number;
  enemies: Phaser.Physics.Arcade.Group;
  projectiles: Phaser.Physics.Arcade.Group;
  obstacles: Phaser.Physics.Arcade.StaticGroup;
  stick?: HuntStick;
  healthMult?: number;
  characterId?: CharacterId;
}

export class Player extends Phaser.Physics.Arcade.Sprite {
  private enemies: Phaser.Physics.Arcade.Group;
  private projectiles: Phaser.Physics.Arcade.Group;
  private stick?: HuntStick;
  private boss?: Phaser.Physics.Arcade.Sprite;
  private keys!: {
    UP: Phaser.Input.Keyboard.Key; DOWN: Phaser.Input.Keyboard.Key; LEFT: Phaser.Input.Keyboard.Key; RIGHT: Phaser.Input.Keyboard.Key;
  };

  private _health: number;
  private readonly maxHp: number;
  private invulnerableUntil = 0;
  public isDead = false;

  private energy = MAX_ENERGY;
  private energyRegenCooldown = 0;

  private currentFireInterval = FIRE_MS;
  private currentBoltDamage = BOLT_DMG;
  private currentBoltSpeed = BOLT_SPEED;
  private currentDamageReduction = 0;
  private lastFireTime = 0;
  private currentProjectileTexture = 'plasma-bolt';
  private activePowerup: { type: PowerupWeaponType; expires: number } | null = null;
  private weaponOverlay: Phaser.GameObjects.Sprite | null = null;
  private readonly idleAnim: string;
  private readonly walkAnim: string;

  constructor(config: PlayerConfig) {
    const char = CHARACTERS[config.characterId ?? 'plasmaboy'];
    super(config.scene, config.x, config.y, char.idleFrame);
    this.idleAnim = char.idleAnim;
    this.walkAnim = char.walkAnim;

    this.enemies = config.enemies;
    this.projectiles = config.projectiles;
    this.stick = config.stick;
    this.maxHp = PLAYER.maxHealth * (config.healthMult ?? 1);
    this._health = this.maxHp;

    this.keys = config.scene.input.keyboard!.addKeys('UP,DOWN,LEFT,RIGHT') as typeof this.keys;

    this.setDepth(DEPTH.player);

    config.scene.add.existing(this);
    config.scene.physics.add.existing(this);

    this.setCollideWorldBounds(true);
    (this.body as Phaser.Physics.Arcade.Body).setSize(24, 34).setOffset(8, 10);

    this.play(this.idleAnim);
  }

  update(time: number, delta: number): void {
    if (this.isDead) return;
    this.updateMovement();
    this.updateEnergy(delta);
    this.updateAutoFire(time);
    this.updatePowerup(time);
    if (this.weaponOverlay?.active) {
      const type = this.activePowerup?.type;
      const isKatana = type === 'katana';
      let offsetX = 0;
      let offsetY = 0;
      if (type === 'shoulder-cannon') {
        offsetX = this.flipX ? -20 : 20;
        offsetY = -12;
      } else if (isKatana) {
        offsetX = this.flipX ? 5 : -14;
        offsetY = -11;
      }
      this.weaponOverlay.setPosition(this.x + offsetX, this.y + offsetY);
      this.weaponOverlay.setDepth(this.depth + (isKatana ? 1 : -1));
      if (!isKatana) this.weaponOverlay.setFlipX(this.flipX);
    }
  }

  // ---- Movement ----

  private updateMovement(): void {
    let vx = this.stick?.x ?? 0;
    let vy = this.stick?.y ?? 0;

    if (this.keys.LEFT.isDown) vx = -1;
    if (this.keys.RIGHT.isDown) vx = 1;
    if (this.keys.UP.isDown) vy = -1;
    if (this.keys.DOWN.isDown) vy = 1;

    const mag = Math.hypot(vx, vy);
    const body = this.body as Phaser.Physics.Arcade.Body;

    if (mag > 0.01) {
      body.setVelocity((vx / mag) * PLAYER_SPEED * Math.min(mag, 1), (vy / mag) * PLAYER_SPEED * Math.min(mag, 1));
      if (Math.abs(vx) > 0.05) this.setFlipX(vx < 0);
      if (this.anims.currentAnim?.key !== this.walkAnim) this.play(this.walkAnim);
    } else {
      body.setVelocity(0, 0);
      if (this.anims.currentAnim?.key !== this.idleAnim) this.play(this.idleAnim);
    }
  }

  // ---- Energy ----

  private updateEnergy(delta: number): void {
    if (this.scene.time.now > this.energyRegenCooldown) {
      const deltaSeconds = Math.min(delta / 1000, 0.016);
      this.energy = Math.min(MAX_ENERGY, this.energy + ENERGY_REGEN_PER_SECOND * deltaSeconds);
    }
  }

  // ---- Auto-fire ----

  private updateAutoFire(time: number): void {
    if (time - this.lastFireTime >= this.currentFireInterval) {
      this.autoFire();
      this.lastFireTime = time;
    }
  }

  private autoFire(): void {
    if (this.energy < ENERGY_COST_PER_SHOT) return;

    const target = this.nearestTarget();
    if (!target) return;

    const angle = Phaser.Math.Angle.Between(this.x, this.y, target.x, target.y);
    const spawnDist = 14;
    const sx = this.x + Math.cos(angle) * spawnDist;
    const sy = this.y + Math.sin(angle) * spawnDist;

    const bolt = this.projectiles.create(sx, sy, this.currentProjectileTexture) as Phaser.Physics.Arcade.Sprite;
    bolt.setDepth(19).setRotation(angle);
    this.scene.physics.velocityFromRotation(angle, this.currentBoltSpeed, (bolt.body as Phaser.Physics.Arcade.Body).velocity);
    this.scene.time.delayedCall(1400, () => bolt.active && bolt.destroy());

    this.energy = Math.max(0, this.energy - ENERGY_COST_PER_SHOT);
    this.energyRegenCooldown = this.scene.time.now + 500;
  }

  private nearestTarget(): Phaser.Physics.Arcade.Sprite | null {
    let best: Phaser.Physics.Arcade.Sprite | null = null;
    let bestD = BOLT_RANGE;

    for (const obj of this.enemies.getChildren()) {
      const e = obj as Phaser.Physics.Arcade.Sprite;
      if (!e.active) continue;
      const d = Phaser.Math.Distance.Between(this.x, this.y, e.x, e.y);
      if (d < bestD) { bestD = d; best = e; }
    }

    if (this.boss?.active) {
      const d = Phaser.Math.Distance.Between(this.x, this.y, this.boss.x, this.boss.y);
      if (d < bestD) best = this.boss;
    }

    return best;
  }

  // ---- Health / Damage ----

  public hurt(damage: number): void {
    if (this.isInvulnerable()) return;

    const reducedDmg = damage * (1 - this.currentDamageReduction);
    this._health = Math.max(0, this._health - reducedDmg);
    this.invulnerableUntil = this.scene.time.now + PLAYER.invulnMs;

    this.setTintFill(0xff5555);
    this.scene.cameras.main.shake(140, 0.008);
    this.scene.time.delayedCall(120, () => this.active && this.clearTint());

    EventBus.emit(GameEvents.PlayerHealthChanged, { health: this._health, maxHealth: this.maxHp });

    if (this._health <= 0) {
      this.isDead = true;
      this.setActive(false);
      this.setVisible(false);
      EventBus.emit(GameEvents.PlayerDied, undefined);
    }
  }

  public restoreHealth(amount: number): void {
    if (this.isDead) return;
    this._health = Math.min(this.maxHp, this._health + amount);
    EventBus.emit(GameEvents.PlayerHealthChanged, { health: this._health, maxHealth: this.maxHp });
  }

  public isInvulnerable(): boolean {
    return this.scene.time.now < this.invulnerableUntil;
  }

  // ---- Powerups ----

  public activatePowerup(type: PowerupWeaponType): void {
    this.clearPowerup();
    this.activePowerup = {
      type,
      expires: this.scene.time.now + 10000,
    };
    this.weaponOverlay = this.scene.add.sprite(this.x, this.y, WEAPON_SPRITES[type]).setDepth(type === 'katana' ? this.depth + 1 : this.depth - 1).setScale(type === 'katana' ? 1.2 : 0.7).setFlipY(type === 'katana');
    this.currentProjectileTexture = WEAPON_PROJECTILES[type];
    this.applyPowerupEffects(type);
  }

  private applyPowerupEffects(type: string): void {
    this.currentFireInterval = FIRE_MS;
    this.currentBoltDamage = BOLT_DMG;
    this.currentBoltSpeed = BOLT_SPEED;
    this.currentDamageReduction = 0;

    switch (type) {
      case 'shoulder-cannon':
        this.currentFireInterval = FIRE_MS * 0.6;
        this.currentBoltDamage = BOLT_DMG * 3;
        this.currentBoltSpeed = BOLT_SPEED * 1.3;
        break;
      case 'katana':
        this.currentFireInterval = FIRE_MS * 1.3;
        this.currentBoltDamage = BOLT_DMG * 4;
        this.currentBoltSpeed = BOLT_SPEED * 0.9;
        this.currentDamageReduction = 0.4;
        break;
    }
  }

  private updatePowerup(time: number): void {
    if (this.activePowerup && time >= this.activePowerup.expires) {
      this.clearPowerup();
    }
  }

  private clearPowerup(): void {
    this.activePowerup = null;
    this.currentFireInterval = FIRE_MS;
    this.currentBoltDamage = BOLT_DMG;
    this.currentBoltSpeed = BOLT_SPEED;
    this.currentDamageReduction = 0;
    this.currentProjectileTexture = 'plasma-bolt';
    if (this.weaponOverlay?.active) {
      this.weaponOverlay.destroy();
      this.weaponOverlay = null;
    }
  }

  // ---- Getters for HUD ----

  public getHealth(): number { return this._health; }
  public getMaxHealth(): number { return this.maxHp; }
  public getEnergy(): number { return this.energy; }
  public getMaxEnergy(): number { return MAX_ENERGY; }
  public getCurrentBoltDamage(): number { return this.currentBoltDamage; }
  public getActivePowerup(): { type: PowerupWeaponType; expires: number } | null { return this.activePowerup; }

  setBossRef(boss: Phaser.Physics.Arcade.Sprite): void {
    this.boss = boss;
  }
}
