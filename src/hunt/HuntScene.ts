import Phaser from 'phaser';
import { AudioManager } from '@/audio/AudioManager';
import { HuntStick } from '@/hunt/HuntStick';
import { isTouchDevice } from '@/utils/platform';
import { WeaponPowerup, type PowerupWeaponType } from '@/collectibles/WeaponPowerup';
import { HealthPickup } from '@/collectibles/HealthPickup';
import { ScoreCoin } from '@/collectibles/ScoreCoin';
import { GemItem } from '@/collectibles/GemItem';
import { Player } from '@/entities/Player';
import { THEMES, generateSpawns } from '@/config/themes';
import { SUB_LEVELS, BIOMES, GEM_TINTS, GEM_I18N, subOf, themeOf } from '@/config/SubLevels';
import { t } from '@/i18n/i18n';
import { burstParticles, flashScreen, shakeCamera } from '@/utils/fx';
import { loadCharacter, type CharacterId } from '@/config/Characters';
import type { Spawn, EnemyKind } from '@/config/LevelData';

const POWERUP_SPAWN_INTERVAL_MS = 15000;
const POWERUP_WEAPON_TYPES: PowerupWeaponType[] = ['shoulder-cannon', 'katana'];

const ENEMY_BOLT_SPEED = 190;
const ENEMY_BOLT_DMG = 9;
const BOSS_HP = 500;
const BOSS_ACTIVATE_DIST = 340;
const BOSS_TOUCH_DMG = 18;
const BOSS_FIRE_MS = 1500;
const APPROACH_OFFSET_RANGE = 0.5;

interface EnemyKindConfig {
  hp: number;
  touchDmg: number;
  speed: number;
  points: number;
  immovable?: boolean;
  chargeSpeed?: number;
  wanderSpeed?: number;
  chargeToggleMs?: number;
  fire?: {
    range: number;
    boltSpeedMult: number;
    fireMs: number;
    projectileSkin: 'shooter' | 'aimer' | 'spore';
    animSkin?: 'aimer' | 'spore';
    openProp?: string;
    closeProp?: string;
    animDelayMs?: number;
  };
}

const ENEMY_KINDS: Record<EnemyKind, EnemyKindConfig> = {
  chaser: { hp: 30, touchDmg: 10, speed: 95, points: 10 },
  turret: { hp: 40, touchDmg: 10, speed: 0, points: 20, immovable: true, fire: { range: 320, boltSpeedMult: 1, fireMs: 1900, projectileSkin: 'shooter' } },
  aimer: { hp: 40, touchDmg: 10, speed: 0, points: 25, immovable: true, fire: { range: 320, boltSpeedMult: 1.1, fireMs: 1900, projectileSkin: 'aimer', animSkin: 'aimer', openProp: 'fire', closeProp: 'idle', animDelayMs: 150 } },
  spore: { hp: 30, touchDmg: 10, speed: 0, points: 20, immovable: true, fire: { range: 380, boltSpeedMult: 0.7, fireMs: 2500, projectileSkin: 'spore', animSkin: 'spore', openProp: 'open', closeProp: 'closed', animDelayMs: 200 } },
  flyer: { hp: 25, touchDmg: 8, speed: 120, points: 15 },
  worm: { hp: 35, touchDmg: 12, speed: 50, points: 30, chargeSpeed: 180, wanderSpeed: 50, chargeToggleMs: 3000 },
};

const ARENA_BASE = { w: 2000, h: 3000 };
const ARENA_SCALES = [1.0, 1.25, 1.5, 1.25];

interface HuntSceneData {
  theme?: keyof typeof THEMES;
  levelIndex?: number;
  score?: number;
  win?: boolean;
  kidsMode?: boolean;
  character?: CharacterId;
}

export class HuntScene extends Phaser.Scene {
  private theme!: keyof typeof THEMES;
  private levelIndex = 0;
  private player!: Player;
  private enemies!: Phaser.Physics.Arcade.Group;
  private playerBolts!: Phaser.Physics.Arcade.Group;
  private enemyBolts!: Phaser.Physics.Arcade.Group;
  private obstacles!: Phaser.Physics.Arcade.StaticGroup;
  private boss: Phaser.Physics.Arcade.Sprite | null = null;
  private bossActive = false;
  private bossFireTimer?: Phaser.Time.TimerEvent;

  private over = false;
  private restartAt = 0;

  private stick?: HuntStick;

  private energyBar!: Phaser.GameObjects.Graphics;
  private weapons!: Phaser.Physics.Arcade.Group;
  private healthPickups!: Phaser.Physics.Arcade.Group;
  private banner!: Phaser.GameObjects.Text;
  private bannerTimer?: Phaser.Time.TimerEvent;
  private placedObstacles: Array<{ x: number; y: number }> = [];
  private wormTimers = new Map<string, Phaser.Time.TimerEvent>();
  private ambientTimer?: Phaser.Time.TimerEvent;
  private powerupTimer?: Phaser.Time.TimerEvent;
  private healthTimer?: Phaser.Time.TimerEvent;
  private coins!: Phaser.Physics.Arcade.Group;
  private gemGroup!: Phaser.Physics.Arcade.Group;
  private gemItem: GemItem | null = null;
  private arenaW = ARENA_BASE.w;
  private arenaH = ARENA_BASE.h;
  private score = 0;
  private lastScore = -1;
  private scoreText!: Phaser.GameObjects.Text;
  // Reused pool of floating "+N" popups. Creating a fresh Text per kill uploads a new GPU
  // texture each time — a micro-stutter several times a second in combat. Reusing a handful
  // of Text objects (setText re-renders into the SAME texture) avoids that churn entirely.
  private scorePopups: Phaser.GameObjects.Text[] = [];
  private scorePopupIdx = 0;
  // Reused pool of hit-burst dots. burstParticles() created ~10 shapes + 10 tweens per kill (and
  // 8 per boss hit, several times a second) — steady GC churn that shows up as micro-stutters.
  // A ring of reused Arcs keeps the exact effect with zero per-kill allocation.
  private fxDots: Phaser.GameObjects.Arc[] = [];
  private fxDotIdx = 0;
  private levelStartTime = 0;
  private kidsMode = false;
  private characterId: CharacterId = 'plasmaboy';

  constructor() {
    super('Hunt');
  }

  create(data: HuntSceneData = {}): void {
    this.over = false;
    this.bossActive = false;
    this.score = data.score ?? 0;
    this.kidsMode = data.kidsMode ?? false;
    this.characterId = data.character ?? loadCharacter();
    this.levelStartTime = this.time.now;

    this.levelIndex = data.levelIndex ?? 0;
    const theme = data.theme ?? themeOf(this.levelIndex);
    const themeConfig = THEMES[theme];
    this.theme = theme;

    const subIdx = subOf(this.levelIndex);
    const scale = ARENA_SCALES[subIdx] ?? 1;
    this.arenaW = Math.round(ARENA_BASE.w * scale);
    this.arenaH = Math.round(ARENA_BASE.h * scale);

    this.physics.world.gravity.y = 0;
    this.physics.world.setBounds(0, 0, this.arenaW, this.arenaH);

    this.cameras.main.setBackgroundColor(themeConfig.skyColor);

    this.add
      .tileSprite(0, 0, this.arenaW, this.arenaH, themeConfig.ground.top ?? 'tile-ground')
      .setOrigin(0, 0)
      .setDepth(-10);

    if (themeConfig.ambientEffect === 'bubbles') {
      this.ambientTimer = this.time.addEvent({
        delay: 900,
        loop: true,
        callback: this.spawnBubble,
        callbackScope: this,
      });
    }

    this.obstacles = this.physics.add.staticGroup();
    this.placedObstacles = [];
    this.placeObstacles(theme);
    this.placeDeco(theme);

    this.enemies = this.physics.add.group();
    this.playerBolts = this.physics.add.group();
    this.enemyBolts = this.physics.add.group();
    this.weapons = this.physics.add.group();
    this.healthPickups = this.physics.add.group();
    this.coins = this.physics.add.group();
    this.gemGroup = this.physics.add.group();

    this.stick = isTouchDevice() ? new HuntStick() : undefined;

    this.player = new Player({
      scene: this,
      x: this.arenaW / 2,
      y: this.arenaH / 2,
      enemies: this.enemies,
      projectiles: this.playerBolts,
      obstacles: this.obstacles,
      stick: this.stick,
      healthMult: this.kidsMode ? 2 : 1,
      characterId: this.characterId,
    });

    const subLevel = subOf(this.levelIndex);
    const sub = SUB_LEVELS[subLevel]!;
    const spawns = generateSpawns(themeConfig, sub, this.arenaW, this.arenaH, this.arenaW / 2, this.arenaH / 2);
    const hpMult = this.kidsMode ? 2 : 1;
    for (const s of spawns) this.spawnEnemy(s, themeConfig.hpMult * sub.hpMult * hpMult);

    const isBossLevel = subLevel === 3;
    if (isBossLevel) {
      this.spawnBoss();
      if (this.boss) this.player.setBossRef(this.boss);
    } else {
      this.spawnGem();
    }

    this.physics.add.collider(this.player, this.obstacles);
    this.physics.add.collider(this.enemies, this.obstacles);
    this.physics.add.collider(this.enemies, this.enemies);
    this.physics.add.overlap(this.playerBolts, this.enemies, this.onBoltHitEnemy, undefined, this);
    if (isBossLevel && this.boss) {
      this.physics.add.overlap(this.playerBolts, this.boss, this.onBoltHitBoss, undefined, this);
      this.physics.add.overlap(this.player, this.boss, this.onBossTouch, undefined, this);
    }
    this.physics.add.overlap(this.player, this.enemies, this.onEnemyTouch, undefined, this);
    this.physics.add.overlap(this.player, this.enemyBolts, this.onEnemyBoltTouch, undefined, this);
    this.physics.add.overlap(this.player, this.weapons, this.onCollectWeapon, undefined, this);
    this.physics.add.overlap(this.player, this.healthPickups, this.onCollectHealth, undefined, this);
    this.physics.add.overlap(this.player, this.coins, this.onCollectCoin, undefined, this);
    this.physics.add.overlap(this.player, this.gemGroup, this.onCollectGem, undefined, this);

    for (const e of this.enemies.getChildren()) {
      const spr = e as Phaser.Physics.Arcade.Sprite;
      if (!spr.active) continue;
      for (const o of this.obstacles.getChildren()) {
        const obs = o as Phaser.Physics.Arcade.Sprite;
        if (!obs.active) continue;
        if (Phaser.Math.Distance.Between(spr.x, spr.y, obs.x, obs.y) < 40) {
          const away = Phaser.Math.Angle.Between(obs.x, obs.y, spr.x, spr.y);
          spr.x += Math.cos(away) * 50;
          spr.y += Math.sin(away) * 50;
          (spr.body as Phaser.Physics.Arcade.Body).reset(spr.x, spr.y);
        }
      }
    }

    this.cameras.main.setBounds(0, 0, this.arenaW, this.arenaH);
    this.cameras.main.startFollow(this.player, true, 0.15, 0.15);
    this.applyZoom();
    this.scale.on('resize', this.applyZoom, this);

    this.buildHud();
    this.powerupTimer = this.time.addEvent({
      delay: POWERUP_SPAWN_INTERVAL_MS,
      loop: true,
      callback: this.spawnRandomPowerup,
      callbackScope: this
    });
    this.healthTimer = this.time.addEvent({
      delay: 20000,
      loop: true,
      callback: this.spawnRandomHealth,
      callbackScope: this
    });
    this.time.delayedCall(3000, () => this.spawnRandomPowerup());
    this.time.delayedCall(5000, () => this.spawnRandomHealth());

    AudioManager.instance.setMood(themeConfig.mood);
    AudioManager.instance.startMusic();

    if (!isBossLevel && this.gemItem) {
      this.time.delayedCall(2500, () => {
        if (this.over || !this.gemItem?.active) return;
        this.showGemHint();
      });
    }

    if (data.win) this.time.delayedCall(500, () => this.win());

    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.scale.off('resize', this.applyZoom, this);
      this.stick?.destroy();

      this.ambientTimer?.remove();
      this.powerupTimer?.remove();
      this.healthTimer?.remove();
      this.bannerTimer?.remove();
      if (this.bossFireTimer) {
        this.bossFireTimer.remove();
        this.bossFireTimer = undefined;
      }
      for (const timer of this.wormTimers.values()) timer.remove();
      this.wormTimers.clear();

      AudioManager.instance.stopMusic();
    });
    const tryRestart = () => {
      if (!this.over || this.time.now < this.restartAt) return;
      if (this.player.isDead) {
        this.scene.start('Hunt', { levelIndex: this.levelIndex, theme: this.theme, score: this.score, kidsMode: this.kidsMode, character: this.characterId });
      } else {
        const nextLevel = this.levelIndex + 1;
        const totalLevels = BIOMES.length * 4;
        if (nextLevel >= totalLevels) {
          this.scene.start('MainMenu');
        } else {
          this.scene.start('Hunt', { levelIndex: nextLevel, score: this.score, kidsMode: this.kidsMode, character: this.characterId });
        }
      }
    };
    this.input.on('pointerdown', tryRestart);
  }

  private applyZoom(): void {
    const targetVisibleH = 640;
    const zoom = Phaser.Math.Clamp(this.scale.height / targetVisibleH, 1.0, 1.6);
    this.cameras.main.setZoom(zoom);

    const w = this.scale.width;
    const h = this.scale.height;
    if (this.banner?.active) {
      this.banner.setPosition(w / 2, h / 2);
      this.banner.setStyle({ wordWrap: { width: w - 150 } });
    }
  }

  private getEnemyTexture(kind: EnemyKind, skins: typeof THEMES[keyof typeof THEMES]['enemySkins']): string {
    switch (kind) {
      case 'chaser': return skins.walker.frame0;
      case 'turret': return skins.shooter.idle;
      case 'aimer': return skins.aimer.idle;
      case 'spore': return skins.spore.closed;
      case 'flyer': return skins.flyer?.frame0 ?? skins.walker.frame0;
      case 'worm': return skins.worm.mound;
      default: return skins.walker.frame0;
    }
  }

  private spawnEnemy(s: Spawn, hpMult = 1): void {
    const skins = THEMES[this.theme].enemySkins;
    const cfg = ENEMY_KINDS[s.kind];
    const tex = this.getEnemyTexture(s.kind, skins);

    const e = this.enemies.create(s.x, s.y, tex) as Phaser.Physics.Arcade.Sprite;
    e.setData('kind', s.kind)
      .setData('hp', Math.ceil(cfg.hp * hpMult))
      .setData('approachOffset', Phaser.Math.FloatBetween(-APPROACH_OFFSET_RANGE, APPROACH_OFFSET_RANGE));

    if (cfg.immovable) {
      (e.body as Phaser.Physics.Arcade.Body).setImmovable(true);
    }

    if (s.kind === 'chaser') {
      e.play(skins.walker.walkAnim);
    } else if (s.kind === 'flyer' && skins.flyer) {
      e.play(skins.flyer.flyAnim);
    } else if (s.kind === 'worm') {
      e.play(skins.worm.emerge);
      const timerKey = s.kind + '_' + s.x + '_' + s.y;
      const timer = this.time.addEvent({
        delay: cfg.chargeToggleMs! + Phaser.Math.Between(0, 1000),
        loop: true,
        callback: () => this.wormToggleCharge(e),
        callbackScope: this,
      });
      this.wormTimers.set(timerKey, timer);
      e.setData('wormTimerKey', timerKey);
      e.setData('charging', false);
    } else if (cfg.fire) {
      const fireTimer = this.time.addEvent({
        delay: cfg.fire.fireMs + Phaser.Math.Between(0, 600),
        loop: true,
        callback: () => this.enemyFire(e, s.kind),
        callbackScope: this,
      });
      e.setData('fireTimer', fireTimer);
    }
  }

  private spawnBoss(): void {
    const bossPositions = [
      { x: this.arenaW * 0.15, y: this.arenaH * 0.1 },
      { x: this.arenaW * 0.85, y: this.arenaH * 0.1 },
      { x: this.arenaW * 0.5, y: this.arenaH * 0.2 },
      { x: this.arenaW * 0.15, y: this.arenaH * 0.5 },
      { x: this.arenaW * 0.85, y: this.arenaH * 0.5 },
      { x: this.arenaW * 0.5, y: this.arenaH * 0.8 },
      { x: this.arenaW * 0.15, y: this.arenaH * 0.9 },
      { x: this.arenaW * 0.85, y: this.arenaH * 0.9 },
    ];
    const bossPos = Phaser.Math.RND.pick(bossPositions);
    const bossSkin = THEMES[this.theme].boss;

    this.boss = this.physics.add.sprite(
      bossPos.x,
      bossPos.y,
      bossSkin?.body ?? 'boss-body'
    )
      .setScale(1.1);

    this.boss.setDepth(1 + (this.boss.y + this.boss.displayHeight * 0.5) / this.arenaH);
    this.boss.setData('hp', bossSkin?.maxHealth ?? (THEMES[this.theme].boss?.maxHealth ?? BOSS_HP));
    (this.boss.body as Phaser.Physics.Arcade.Body).setImmovable(true);
    this.physics.add.collider(this.boss, this.obstacles);

    const angle = Phaser.Math.RadToDeg(
      Phaser.Math.Angle.Between(this.player.x, this.player.y, bossPos.x, bossPos.y)
    );

    let hintText: string;
    if (this.kidsMode) {
      if (angle >= -22.5 && angle < 22.5) {
        hintText = t('bossEast');
      } else if (angle >= 22.5 && angle < 67.5) {
        hintText = t('bossSouthEast');
      } else if (angle >= 67.5 && angle < 112.5) {
        hintText = t('bossSouth');
      } else if (angle >= 112.5 && angle < 157.5) {
        hintText = t('bossSouthWest');
      } else if (angle >= 157.5 || angle < -157.5) {
        hintText = t('bossWest');
      } else if (angle >= -157.5 && angle < -112.5) {
        hintText = t('bossNorthWest');
      } else if (angle >= -112.5 && angle < -67.5) {
        hintText = t('bossNorth');
      } else {
        hintText = t('bossNorthEast');
      }
    } else {
      hintText = t('defeatBoss');
    }

    this.time.delayedCall(2000, () => {
      this.showBanner(hintText, 2500);
    });
  }

  private spawnGem(): void {
    const sub = SUB_LEVELS[subOf(this.levelIndex)]!;
    const tint = GEM_TINTS[this.theme];
    const gemName = t((GEM_I18N[this.theme] ?? 'gemAmethyst') as Parameters<typeof t>[0]);
    let x: number;
    let y: number;
    let attempts = 0;
    do {
      x = Phaser.Math.Between(150, this.arenaW - 150);
      y = Phaser.Math.Between(150, this.arenaH - 150);
      attempts++;
    } while (
      attempts < 20 &&
      (this.isPositionInObstacle(x, y) ||
        Phaser.Math.Distance.Between(x, y, this.arenaW / 2, this.arenaH / 2) < sub.gemMinDist)
    );

    this.gemItem = new GemItem(this, x, y, tint, gemName, 0.55);
    this.gemGroup.add(this.gemItem);
    this.tweens.add({
      targets: this.gemItem,
      y: this.gemItem.y - 10,
      scale: { from: 0.5, to: 0.62 },
      duration: 900,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });
  }

  private showGemHint(): void {
    if (!this.gemItem?.active) return;
    const gemName = t((GEM_I18N[this.theme] ?? 'gemAmethyst') as Parameters<typeof t>[0]).toUpperCase();

    let hintText: string;
    if (this.kidsMode) {
      const angle = Phaser.Math.RadToDeg(
        Phaser.Math.Angle.Between(this.player.x, this.player.y, this.gemItem.x, this.gemItem.y)
      );

      if (angle >= -22.5 && angle < 22.5) {
        hintText = t('gemEast');
      } else if (angle >= 22.5 && angle < 67.5) {
        hintText = t('gemSouthEast');
      } else if (angle >= 67.5 && angle < 112.5) {
        hintText = t('gemSouth');
      } else if (angle >= 112.5 && angle < 157.5) {
        hintText = t('gemSouthWest');
      } else if (angle >= 157.5 || angle < -157.5) {
        hintText = t('gemWest');
      } else if (angle >= -157.5 && angle < -112.5) {
        hintText = t('gemNorthWest');
      } else if (angle >= -112.5 && angle < -67.5) {
        hintText = t('gemNorth');
      } else {
        hintText = t('gemNorthEast');
      }
      hintText = hintText.replace('{GEM}', gemName);
    } else {
      hintText = t('findGem').replace('{GEM}', gemName);
    }

    this.showBanner(hintText, 3000);
  }

  private spawnRandomPowerup(): void {
    if (this.over) return;

    let attempts = 0;
    let x: number;
    let y: number;
    const minDistFromPlayer = 150;

    do {
      x = Phaser.Math.Between(100, this.arenaW - 100);
      y = Phaser.Math.Between(300, this.arenaH - 300);
      attempts++;
    } while (
      (this.isPositionInObstacle(x, y) ||
        Phaser.Math.Distance.Between(x, y, this.player.x, this.player.y) < minDistFromPlayer) &&
      attempts < 20
    );

    if (attempts >= 50) return;

    const weaponType = Phaser.Math.RND.pick(POWERUP_WEAPON_TYPES);
    const powerup = new WeaponPowerup({ scene: this, x, y, weaponType });

    this.weapons.add(powerup);
    this.tweens.add({
      targets: powerup,
      y: powerup.y - 20,
      duration: 1000,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });
  }

  private spawnRandomHealth(): void {
    if (this.over) return;

    let attempts = 0;
    let x: number;
    let y: number;
    const minDistFromPlayer = 10;

    do {
      x = Phaser.Math.Between(100, this.arenaW - 100);
      y = Phaser.Math.Between(300, this.arenaH - 300);
      attempts++;
    } while (
      (this.isPositionInObstacle(x, y) ||
        Phaser.Math.Distance.Between(x, y, this.player.x, this.player.y) < minDistFromPlayer) &&
      attempts < 20
    );

    if (attempts >= 50) return;

    const pickup = new HealthPickup(this, x, y);
    this.healthPickups.add(pickup);
    this.tweens.add({
      targets: pickup,
      y: pickup.y - 15,
      duration: 1200,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });
  }

  private isPositionInObstacle(x: number, y: number): boolean {
    const r = 50;
    const r2 = r * r;
    for (const o of this.placedObstacles) {
      const dx = x - o.x;
      const dy = y - o.y;
      if (dx * dx + dy * dy < r2) return true;
    }
    return false;
  }

  private spawnBubble(): void {
    const x = Phaser.Math.Between(80, this.arenaW - 80);
    const y = this.arenaH + 20;
    const key = Math.random() < 0.25 ? 'bubble-cluster' : 'bubble';
    const s = key === 'bubble-cluster' ? Phaser.Math.FloatBetween(0.4, 0.8) : Phaser.Math.FloatBetween(0.5, 1.2);
    const bubble = this.add.sprite(x, y, key).setDepth(-4).setAlpha(0.45).setScale(s);
    this.tweens.add({
      targets: bubble,
      y: -30,
      x: x + Phaser.Math.Between(-20, 20),
      alpha: 0,
      duration: Phaser.Math.Between(10000, 16000),
      ease: 'Sine.easeInOut',
      onComplete: () => bubble.destroy(),
    });
  }

  private placeObstacles(theme: keyof typeof THEMES): void {
    const themeConfig = THEMES[theme];
    const obstacleSprites = themeConfig.obstacles;
    if (obstacleSprites.length === 0) return;

    const margin = 120;
    const placement = themeConfig.obstaclePlacement;
    const treeLike = obstacleSprites.filter(s => placement.treeLike.includes(s));
    const other = obstacleSprites.filter(s => !placement.treeLike.includes(s));

    const clusterCenters: Array<{ x: number; y: number }> = [];
    for (let i = 0; i < placement.clusterCount; i++) {
      clusterCenters.push({
        x: Phaser.Math.Between(margin, this.arenaW - margin),
        y: Phaser.Math.Between(margin, this.arenaH - margin),
      });
    }

    const treePositions: Array<{ x: number; y: number; tex: string; scale: number }> = [];
    for (const center of clusterCenters) {
      if (treeLike.length === 0) break;
      const count = Phaser.Math.Between(placement.treesPerCluster[0], placement.treesPerCluster[1]);
      for (let j = 0; j < count; j++) {
        const ox = center.x + Phaser.Math.Between(-placement.clusterSpread, placement.clusterSpread);
        const oy = center.y + Phaser.Math.Between(-placement.clusterSpread, placement.clusterSpread);
        const clampX = Phaser.Math.Clamp(ox, margin, this.arenaW - margin);
        const clampY = Phaser.Math.Clamp(oy, margin, this.arenaH - margin);
        const tex = Phaser.Math.RND.pick(treeLike);
        const s = (tex === 'bg-tree-0' || tex === 'bg-tree-1' || tex === 'cactus-bg')
          ? Phaser.Math.FloatBetween(placement.treeScaleRange[0], placement.treeScaleRange[1])
          : Phaser.Math.FloatBetween(0.85, 1.15);
        treePositions.push({ x: clampX, y: clampY, tex, scale: s });
      }
    }

    treePositions.sort((a, b) => a.y - b.y);
    for (const t of treePositions) {
      const sprite = this.physics.add.staticSprite(t.x, t.y, t.tex);
      sprite.setDepth(1 + (t.y + (102 * t.scale) * 0.5) / this.arenaH).setScale(t.scale);
      if (placement.treeLike.includes(t.tex)) {
        const body = sprite.body as Phaser.Physics.Arcade.StaticBody;
        body.setSize(16 * t.scale, 30 * t.scale);
        body.setOffset(28 * t.scale, 72 * t.scale);
      }
      this.obstacles.add(sprite);
      this.placedObstacles.push({ x: t.x, y: t.y });
    }

    if (other.length > 0) {
      for (let i = 0; i < placement.otherCount; i++) {
        const x = Phaser.Math.Between(margin, this.arenaW - margin);
        const y = Phaser.Math.Between(margin, this.arenaH - margin);
        const tex = other[Math.floor(Math.random() * other.length)]!;
        const sprite = this.physics.add.staticSprite(x, y, tex);
        sprite.setDepth(1 + y / this.arenaH);
        this.obstacles.add(sprite);
        this.placedObstacles.push({ x, y });
      }
    }

    if (themeConfig.extraObstacles === 'swampPonds') {
      this.placeSwampWater();
    } else if (themeConfig.extraObstacles === 'seaWater') {
      this.placeSeaWater();
    }
  }

  private placeSeaWater(): void {
    // A few BIG bodies of sea — proper bays, not ponds — so the beach reads as being at the
    // ocean's edge. Kept clear of the player's spawn (arena centre) so a giant pool can't trap them.
    const cxC = this.arenaW / 2;
    const cyC = this.arenaH / 2;
    const poolCount = Phaser.Math.Between(2, 3);
    let placed = 0;
    let tries = 0;
    while (placed < poolCount && tries < 40) {
      tries++;
      const w = Phaser.Math.Between(560, 980);
      const h = Phaser.Math.Between(360, 620);
      const cx = Phaser.Math.Between(Math.round(w / 2) + 60, this.arenaW - Math.round(w / 2) - 60);
      const cy = Phaser.Math.Between(Math.round(h / 2) + 60, this.arenaH - Math.round(h / 2) - 60);
      if (Phaser.Math.Distance.Between(cx, cy, cxC, cyC) < Math.max(w, h) * 0.5 + 220) continue;

      // Opaque fills (no stacked alphas → crisp, not muddy). A pale foam ring defines the
      // coastline, a deep body + lighter shallows give depth, and a few wave dashes add ripples.
      const g = this.add.graphics();
      g.fillStyle(0xdff2fb, 1);
      g.fillEllipse(cx, cy, w + 22, h + 22);                  // wet-sand / surf foam ring
      g.fillStyle(0x2f8fce, 1);
      g.fillEllipse(cx, cy, w, h);                            // deep water body
      g.fillStyle(0x57b0e6, 1);
      g.fillEllipse(cx, cy - h * 0.12, w * 0.74, h * 0.56);   // sunlit shallows
      g.fillStyle(0xbfe6ff, 1);
      g.fillEllipse(cx, cy - h * 0.26, w * 0.42, h * 0.2);    // bright shallow centre
      g.fillStyle(0xe8f6ff, 0.9);                             // wave-crest dashes
      for (let r = 0; r < 4; r++) {
        const ry = cy - h * 0.32 + r * h * 0.2;
        const rw = (w * 0.5) * (1 - Math.abs(r - 1.5) * 0.18);
        g.fillRect(cx - rw / 2, ry, rw, 3);
      }
      g.setDepth(0);

      const bw = w * 0.86;
      const bh = h * 0.86;
      const dummy = this.add.zone(cx, cy, bw, bh);
      this.physics.add.existing(dummy, true);
      (dummy.body as Phaser.Physics.Arcade.StaticBody).setSize(bw, bh);
      this.obstacles.add(dummy);
      this.placedObstacles.push({ x: cx, y: cy });
      placed++;
    }
  }

  private placeSwampWater(): void {
    const pondCount = Phaser.Math.Between(3, 5);
    for (let i = 0; i < pondCount; i++) {
      const cx = Phaser.Math.Between(200, this.arenaW - 200);
      const cy = Phaser.Math.Between(200, this.arenaH - 200);
      const w = Phaser.Math.Between(80, 160);
      const h = Phaser.Math.Between(40, 80);

      const g = this.add.graphics();
      g.fillStyle(0x2a4a3a, 0.7);
      g.fillEllipse(cx, cy, w, h);
      g.setDepth(0);

      const dummy = this.add.zone(cx, cy, w, h);
      this.physics.add.existing(dummy, true);
      (dummy.body as Phaser.Physics.Arcade.StaticBody).setSize(w, h);
      this.obstacles.add(dummy);
      this.placedObstacles.push({ x: cx, y: cy });
    }
  }

  private placeDeco(theme: keyof typeof THEMES): void {
    const themeConfig = THEMES[theme];
    const decoSprites = themeConfig.deco;
    if (decoSprites.length === 0) return;

    const margin = 80;
    for (let i = 0; i < 18; i++) {
      const x = Phaser.Math.Between(margin, this.arenaW - margin);
      const y = Phaser.Math.Between(margin, this.arenaH - margin);
      const tex = decoSprites[Math.floor(Math.random() * decoSprites.length)]!;
      const sprite = this.add.sprite(x, y, tex);
      sprite.setDepth(0).setAlpha(0.85);
    }
  }

  private onCollectWeapon(_playerObj: unknown, weaponObj: unknown): void {
    const weapon = weaponObj as WeaponPowerup;
    if (!weapon.active) return;
    weapon.onCollect(this.player);
  }

  private onCollectHealth(_playerObj: unknown, pickupObj: unknown): void {
    const pickup = pickupObj as HealthPickup;
    if (!pickup.active) return;
    pickup.onCollect(this.player);
  }

  private enemyFire(e: Phaser.Physics.Arcade.Sprite, kind: EnemyKind): void {
    if (this.over || !e.active) return;
    const cfg = ENEMY_KINDS[kind];
    if (!cfg.fire) return;
    if (Phaser.Math.Distance.Between(e.x, e.y, this.player.x, this.player.y) > cfg.fire.range) return;

    const angle = Phaser.Math.Angle.Between(e.x, e.y, this.player.x, this.player.y);
    const skins = THEMES[this.theme].enemySkins;
    const projectile = (skins[cfg.fire.projectileSkin] as Record<string, string>).projectile;

    if (cfg.fire.animSkin && cfg.fire.openProp && cfg.fire.closeProp && cfg.fire.animDelayMs) {
      const animSkin = skins[cfg.fire.animSkin] as Record<string, string>;
      const openTex = animSkin[cfg.fire.openProp]!;
      const closeTex = animSkin[cfg.fire.closeProp]!;
      const delay = cfg.fire.animDelayMs;
      e.setTexture(openTex);
      this.time.delayedCall(delay, () => {
        if (e.active) e.setTexture(closeTex);
      });
    }

    const b = this.enemyBolts.create(e.x, e.y, projectile) as Phaser.Physics.Arcade.Sprite;
    b.setDepth(16);
    this.physics.velocityFromRotation(angle, ENEMY_BOLT_SPEED * cfg.fire.boltSpeedMult, (b.body as Phaser.Physics.Arcade.Body).velocity);
    this.time.delayedCall(3500, () => b.active && b.destroy());
  }

  private wormToggleCharge(e: Phaser.Physics.Arcade.Sprite): void {
    if (this.over || !e.active) return;
    const charging = e.getData('charging');
    e.setData('charging', !charging);
    if (!charging) {
      e.setTexture(THEMES[this.theme].enemySkins.worm.charge);
    } else {
      e.setTexture(THEMES[this.theme].enemySkins.worm.mound);
    }
  }

  private bossFire(): void {
    if (this.over || !this.boss?.active) return;
    const bossSkin = THEMES[this.theme].boss;
    if (!bossSkin) return;

    const telegraphColor = bossSkin.telegraphColor ?? 0xffffff;
    this.boss.setTintFill(telegraphColor);
    this.time.delayedCall(300, () => {
      if (!this.boss?.active) return;
      this.boss.clearTint();

      if (bossSkin.special === 'slam') {
        this.bossSlam(bossSkin);
      } else {
        this.bossSpikeBurst(bossSkin);
      }
    });
  }

  private bossSlam(bossSkin: import('@/config/themes').BossVariant): void {
    const ringCount = 2;
    const boltsPerRing = 4;
    for (let ring = 0; ring < ringCount; ring++) {
      this.time.delayedCall(ring * 350, () => {
        if (this.over || !this.boss?.active) return;
        const speed = ENEMY_BOLT_SPEED * (0.7 + ring * 0.3);
        for (let i = 0; i < boltsPerRing; i++) {
          const angle = (i / boltsPerRing) * Math.PI * 2;
          const boss = this.boss!;
          const b = this.enemyBolts.create(boss.x, boss.y, bossSkin.orb);
          b.setDepth(16);
          this.physics.velocityFromRotation(angle, speed, (b.body as Phaser.Physics.Arcade.Body).velocity);
          this.time.delayedCall(3500, () => b.active && b.destroy());
        }
      });
    }
  }

  private bossSpikeBurst(bossSkin: import('@/config/themes').BossVariant): void {
    const n = 10;
    for (let i = 0; i < n; i++) {
      const angle = (i / n) * Math.PI * 2;
      const boss = this.boss!;
      const b = this.enemyBolts.create(boss.x, boss.y, bossSkin.spike);
      b.setDepth(16).setRotation(angle);
      this.physics.velocityFromRotation(angle, ENEMY_BOLT_SPEED * 1.1, (b.body as Phaser.Physics.Arcade.Body).velocity);
      this.time.delayedCall(4000, () => b.active && b.destroy());
    }
  }

  private onBoltHitEnemy(boltObj: unknown, enemyObj: unknown): void {
    const bolt = boltObj as Phaser.Physics.Arcade.Sprite;
    const e = enemyObj as Phaser.Physics.Arcade.Sprite;
    if (bolt.active) bolt.destroy();
    if (!e.active) return;
    const hp = (e.getData('hp') as number) - this.player.getCurrentBoltDamage();
    e.setData('hp', hp);
    e.setTintFill(0xffffff);
    this.time.delayedCall(60, () => e.active && e.clearTint());
    if (hp <= 0) {
      const kind = e.getData('kind') as EnemyKind;
      const pts = ENEMY_KINDS[kind].points;
      this.addScore(pts, e.x, e.y);
      this.burst(e.x, e.y, 0x5a9e4b, 10);
      AudioManager.instance.play(this.theme === 'water' ? 'bubble' : 'explosion');
      if (Math.random() < 0.35) this.spawnCoin(e.x, e.y);
      const fireTimer = e.getData('fireTimer') as Phaser.Time.TimerEvent | undefined;
      fireTimer?.remove();
      if (kind === 'worm') {
        const wormKey = e.getData('wormTimerKey') as string | undefined;
        if (wormKey) {
          this.wormTimers.get(wormKey)?.remove();
          this.wormTimers.delete(wormKey);
        }
      }
      e.destroy();
    }
  }

  private onBoltHitBoss(object1: unknown, object2: unknown): void {
    if (!this.boss) return;
    const obj1 = object1 as Phaser.Physics.Arcade.Sprite;
    const obj2 = object2 as Phaser.Physics.Arcade.Sprite;

    const bolt = obj1 === this.boss ? obj2 : obj1;
    if (!bolt.active || !this.boss.active || this.over) return;

    bolt.destroy();

    const currentHp = this.boss.getData('hp');
    if (typeof currentHp !== 'number') return;

    const hp = currentHp - this.player.getCurrentBoltDamage();
    this.boss.setData('hp', hp);

    const bossSkin = THEMES[this.theme].boss;
    this.boss.setTexture(bossSkin?.bodyFlash ?? 'boss-body-flash');

    const burstColor = bossSkin?.burstColor ?? 0xffffff;
    this.burst(this.boss.x, this.boss.y, burstColor, 8);

    const boss = this.boss;
    this.time.delayedCall(60, () => {
      if (boss.active) boss.setTexture(bossSkin?.body ?? 'boss-body');
    });

    if (hp <= 0) {
      this.addScore(200, this.boss.x, this.boss.y);
      this.win();
    }
  }

  private onEnemyTouch(_playerObj: unknown, enemyObj: unknown): void {
    const e = enemyObj as Phaser.Physics.Arcade.Sprite;
    const kind = e.getData('kind') as EnemyKind;
    this.hurtPlayer(ENEMY_KINDS[kind].touchDmg);
  }
  private onEnemyBoltTouch(_p: unknown, boltObj: unknown): void {
    (boltObj as Phaser.Physics.Arcade.Sprite).destroy();
    this.hurtPlayer(ENEMY_BOLT_DMG);
  }
  private onBossTouch(): void {
    this.hurtPlayer(BOSS_TOUCH_DMG);
  }

  private hurtPlayer(dmg: number): void {
    if (this.over) return;
    this.player.hurt(dmg);
    if (this.player.isDead) this.lose();
  }

  update(time: number, delta: number): void {
    if (this.over) return;

    this.player.update(time, delta);
    this.player.setDepth(1 + (this.player.y + this.player.displayHeight * 0.5) / this.arenaH);

    const speedMult = this.kidsMode ? 0.65 : 1;
    for (const obj of this.enemies.getChildren()) {
      const e = obj as Phaser.Physics.Arcade.Sprite;
      if (!e.active) continue;
      e.setDepth(1 + (e.y + e.displayHeight * 0.5) / this.arenaH);
      const kind = e.getData('kind') as EnemyKind;
      const cfg = ENEMY_KINDS[kind];
      if (cfg.speed > 0) {
        const offset = e.getData('approachOffset') as number;
        const a = Phaser.Math.Angle.Between(e.x, e.y, this.player.x, this.player.y) + offset;
        let speed = cfg.speed * speedMult;
        if (cfg.chargeSpeed !== undefined) {
          speed = (e.getData('charging') ? cfg.chargeSpeed : cfg.wanderSpeed!) * speedMult;
        }
        this.physics.velocityFromRotation(a, speed, (e.body as Phaser.Physics.Arcade.Body).velocity);
        e.setFlipX(this.player.x < e.x);
      }
    }

    if (this.boss?.active) {
      this.boss.setDepth(1 + (this.boss.y + this.boss.displayHeight * 0.5) / this.arenaH);
    }
    if (this.boss && !this.bossActive && this.boss.active && Phaser.Math.Distance.Between(this.player.x, this.player.y, this.boss.x, this.boss.y) < BOSS_ACTIVATE_DIST) {
      this.bossActive = true;
      (this.boss.body as Phaser.Physics.Arcade.Body).setImmovable(false);
      const aggression = (THEMES[this.theme].boss?.aggression ?? 1) * (this.kidsMode ? 2 : 1);
      this.bossFireTimer = this.time.addEvent({ delay: BOSS_FIRE_MS * aggression, loop: true, callback: this.bossFire, callbackScope: this });
    }
    if (this.bossActive && this.boss?.active) {
      const a = Phaser.Math.Angle.Between(this.boss.x, this.boss.y, this.player.x, this.player.y);
      const bossSpeed = (THEMES[this.theme].boss?.speed ?? 62) * (this.kidsMode ? 0.65 : 1);
      this.physics.velocityFromRotation(a, bossSpeed, (this.boss.body as Phaser.Physics.Arcade.Body).velocity);
    }

    this.drawHud();
  }

  private buildHud(): void {
    this.energyBar = this.add.graphics().setDepth(50);

    // Anchored bottom-right (origin 1,1) so it clears the iPhone status bar / notch at the top.
    this.scoreText = this.add.text(0, 0, '★ 0', {
      fontFamily: 'monospace', fontSize: '18px', fontStyle: 'bold', color: '#ffd700', stroke: '#000', strokeThickness: 3,
    }).setOrigin(1, 1).setScrollFactor(0).setDepth(101);

    this.banner = this.add.text(this.cameras.main.width / 2, this.cameras.main.height / 2, '', {
      fontFamily: 'monospace', fontSize: '20px', fontStyle: 'bold', color: '#ffffff', stroke: '#000', strokeThickness: 5, align: 'center',
      wordWrap: { width: this.cameras.main.width - 150 },
    }).setOrigin(0.5).setScrollFactor(0).setDepth(101);

    this.scorePopups = [];
    this.scorePopupIdx = 0;
    for (let i = 0; i < 10; i++) {
      const p = this.add.text(0, 0, '', {
        fontFamily: 'monospace', fontSize: '14px', fontStyle: 'bold', color: '#ffd700', stroke: '#000', strokeThickness: 2,
      }).setOrigin(0.5).setScrollFactor(0).setDepth(102).setVisible(false);
      this.scorePopups.push(p);
    }

    this.fxDots = [];
    this.fxDotIdx = 0;
    for (let i = 0; i < 48; i++) {
      this.fxDots.push(this.add.circle(0, 0, 3, 0xffffff).setDepth(20).setVisible(false).setActive(false));
    }
  }

  /** Pooled version of burstParticles for the hot paths (kills, boss hits): reuses Arc dots
   * from a ring buffer instead of allocating new shapes + tweens each time. */
  private burst(x: number, y: number, color: number, count: number): void {
    for (let i = 0; i < count; i++) {
      const dot = this.fxDots[this.fxDotIdx];
      this.fxDotIdx = (this.fxDotIdx + 1) % this.fxDots.length;
      if (!dot) continue;
      this.tweens.killTweensOf(dot);
      const angle = (Math.PI * 2 * i) / count + Phaser.Math.FloatBetween(-0.3, 0.3);
      const speed = Phaser.Math.Between(80, 160);
      dot.setFillStyle(color).setPosition(x, y).setScale(1).setAlpha(1).setVisible(true).setActive(true);
      this.tweens.add({
        targets: dot,
        x: x + Math.cos(angle) * speed * 0.3,
        y: y + Math.sin(angle) * speed * 0.3,
        alpha: 0,
        duration: 300,
        ease: 'Cubic.Out',
        onComplete: () => dot.setVisible(false).setActive(false),
      });
    }
  }

  private drawHud(): void {
    const cam = this.cameras.main;
    const sx = this.scale.width - 24;
    const sy = this.scale.height - 30; // bottom-right, clear of the top status bar / notch
    const wx = (sx - cam.width / 2) / cam.zoom + cam.width / 2;
    const wy = (sy - cam.height / 2) / cam.zoom + cam.height / 2;
    this.scoreText.setPosition(wx, wy);
    if (this.score !== this.lastScore) {
      this.scoreText.setText(`★ ${this.score}`);
      this.lastScore = this.score;
    }

    this.energyBar.clear();
    const healthPercent = this.player.getHealth() / this.player.getMaxHealth();

    const barWidth = 40;
    const barHeight = 4;
    const barX = this.player.x - barWidth / 2;
    const barY = this.player.y + this.player.displayHeight / 2 + 4;

    this.energyBar.fillStyle(0x000000, 0.6).fillRect(barX - 1, barY - 1, barWidth + 2, barHeight + 2);
    this.energyBar.fillStyle(0x550000).fillRect(barX, barY, barWidth, barHeight);
    const fillWidth = barWidth * Math.max(0, healthPercent);
    this.energyBar.fillStyle(healthPercent > 0.3 ? 0x44ff44 : 0xff4444).fillRect(barX, barY, fillWidth, barHeight);
  }

  private showBanner(text: string, ms: number): void {
    this.bannerTimer?.remove();
    this.banner.setText(text).setVisible(true);
    this.bannerTimer = this.time.delayedCall(ms, () => this.banner.setVisible(false));
  }

  private addScore(pts: number, x: number, y: number): void {
    this.score += pts;
    const cam = this.cameras.main;
    const sx = (x - cam.scrollX) / cam.zoom;
    const sy = (y - cam.scrollY) / cam.zoom;
    const label = this.scorePopups[this.scorePopupIdx];
    if (!label) return;
    this.scorePopupIdx = (this.scorePopupIdx + 1) % this.scorePopups.length;
    this.tweens.killTweensOf(label);
    label.setText(`+${pts}`).setPosition(sx, sy).setAlpha(1).setVisible(true);
    this.tweens.add({
      targets: label, y: sy - 30, alpha: 0, duration: 600, ease: 'Cubic.Out',
      onComplete: () => label.setVisible(false),
    });
  }

  private spawnCoin(x: number, y: number): void {
    const coin = new ScoreCoin(this, x, y);
    this.coins.add(coin);
    this.tweens.add({
      targets: coin, y: coin.y - 12, duration: 800, yoyo: true, repeat: -1, ease: 'Sine.easeInOut',
    });
  }

  private onCollectCoin(_playerObj: unknown, coinObj: unknown): void {
    const coin = coinObj as ScoreCoin;
    const pts = coin.onCollect();
    if (pts > 0) this.addScore(pts, coin.x, coin.y);
  }

  private onCollectGem(_playerObj: unknown, gemObj: unknown): void {
    const gem = gemObj as GemItem;
    const pts = gem.onCollect();
    if (pts > 0) this.addScore(pts, gem.x, gem.y);
    this.gemItem = null;
    this.gemLevelComplete();
  }

  private gemLevelComplete(): void {
    this.over = true;
    this.physics.pause();
    this.stick?.setEnabled(false);

    const levelBonus = 100;
    const elapsed = (this.time.now - this.levelStartTime) / 1000;
    const speedBonus = Math.max(0, Math.round(150 - elapsed * 2));
    this.addScore(levelBonus + speedBonus, this.player.x, this.player.y);

    AudioManager.instance.playEndJingle(true);
    this.celebratePlayer();
    this.updateTopScore();

    const nextLevel = this.levelIndex + 1;
    const totalLevels = BIOMES.length * 4;
    if (nextLevel >= totalLevels) {
      this.showBanner(`${t('allCleared')}\n\n${t('score')} ${this.score}\n\n${t('tapToReturn')}`, 999999);
    } else {
      this.showBanner(`${t('gemFound')}\n\n${t('score')} ${this.score}\n\n${t('tapToContinue')}`, 999999);
    }
    this.restartAt = this.time.now + 1000;
  }

  private win(): void {
    if (!this.boss) return;
    const bx = this.boss.x;
    const by = this.boss.y;
    this.boss.destroy();
    this.over = true;
    this.physics.pause();
    this.stick?.setEnabled(false);
    if (this.bossFireTimer) {
      this.bossFireTimer.remove();
      this.bossFireTimer = undefined;
    }

    const levelBonus = 100;
    const elapsed = (this.time.now - this.levelStartTime) / 1000;
    const speedBonus = Math.max(0, Math.round(150 - elapsed * 2));
    this.addScore(levelBonus + speedBonus, this.player.x, this.player.y);

    burstParticles(this, bx, by, 0x00ffff, 18);
    burstParticles(this, bx, by, 0xffffff, 12);
    flashScreen(this, 0xffffff, 300);
    shakeCamera(this, 400, 0.015);
    AudioManager.instance.play('explosion');
    AudioManager.instance.playEndJingle(true);

    this.celebratePlayer();
    this.spawnConfetti();

    this.updateTopScore();

    const nextLevel = this.levelIndex + 1;
    const totalLevels = BIOMES.length * 4;
    if (nextLevel >= totalLevels) {
      this.showBanner(`${t('allCleared')}\n\n${t('score')} ${this.score}\n\n${t('tapToReturn')}`, 999999);
    } else {
      this.showBanner(`${t('bossDefeated')}\n\n${t('score')} ${this.score}\n\n${t('tapToContinue')}`, 999999);
    }
    this.restartAt = this.time.now + 1000;
  }

  private celebratePlayer(): void {
    this.tweens.add({
      targets: this.player,
      scale: 1.3,
      duration: 200,
      yoyo: true,
      repeat: 3,
      ease: 'Sine.easeInOut',
    });
    const cam = this.cameras.main;
    const px = (this.player.x - cam.scrollX) / cam.zoom;
    const py = (this.player.y - cam.scrollY) / cam.zoom - 30;
    const star = this.add.text(px, py, '★', {
      fontFamily: 'monospace', fontSize: '28px', color: '#ffd700', stroke: '#000', strokeThickness: 3,
    }).setOrigin(0.5).setScrollFactor(0).setDepth(103);
    this.tweens.add({
      targets: star, y: py - 50, alpha: 0, scale: 2, duration: 1200, ease: 'Cubic.Out',
      onComplete: () => star.destroy(),
    });
  }

  private spawnConfetti(): void {
    const colors = [0xff5c7a, 0x5fb7e8, 0xffd700, 0x5a9e4b, 0xff8c42, 0xb06cff];
    const cam = this.cameras.main;
    for (let i = 0; i < 40; i++) {
      const x = Phaser.Math.Between(0, Math.round(cam.width));
      const startY = -Phaser.Math.Between(20, 100);
      const color = Phaser.Utils.Array.GetRandom(colors);
      const size = Phaser.Math.Between(2, 5);
      const dot = this.add.rectangle(x, startY, size, size, color).setScrollFactor(0).setDepth(104);
      this.tweens.add({
        targets: dot,
        y: cam.height + 20,
        x: x + Phaser.Math.Between(-60, 60),
        angle: Phaser.Math.Between(-180, 180),
        alpha: { from: 1, to: 0.3 },
        duration: Phaser.Math.Between(1500, 3000),
        ease: 'Sine.easeIn',
        onComplete: () => dot.destroy(),
      });
    }
  }

  private lose(): void {
    this.over = true;
    this.physics.pause();
    this.stick?.setEnabled(false);
    AudioManager.instance.playEndJingle(false);
    this.updateTopScore();
    const top = this.getTopScore();
    this.showBanner(`${t('gameOver')}\n\n${t('score')} ${this.score}\n${t('topScore')} ${top}\n\n${t('tapToRetry')}`, 999999);
    this.restartAt = this.time.now + 1000;
  }

  private updateTopScore(): void {
    const prev = this.getTopScore();
    if (this.score > prev) {
      try { localStorage.setItem('pb-top-score', String(this.score)); } catch { /* ignore */ }
    }
  }

  private getTopScore(): number {
    try { return Number(localStorage.getItem('pb-top-score')) || 0; } catch { return 0; }
  }
}
