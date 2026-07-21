import Phaser from 'phaser';
import type { LevelTheme, Spawn, EnemyKind } from '@/config/LevelData';
import type { MusicMood } from '@/audio/AudioManager';
import type { SubLevelConfig } from '@/config/SubLevels';

/** Texture keys for one enemy behavior archetype. Same shape across themes; only the art
 * differs. The factory hands the right skin to each enemy so a desert level fields
 * desert-plant enemies without duplicating any behavior code. */
export interface EnemySkins {
  /** WalkingMushroom archetype — two walk frames + the animation key that cycles them. */
  walker: { frame0: string; frame1: string; walkAnim: string };
  /** ThornBush archetype — stationary straight-shooter. */
  shooter: { idle: string; fire: string; projectile: string };
  /** AngrySunflower archetype — aimed shooter that rotates to track the player. */
  aimer: { idle: string; fire: string; projectile: string };
  /** VineWorm archetype — burrow / emerge / charge. */
  worm: { mound: string; emerge: string; charge: string };
  /** PoisonFlower archetype — closed / open spore-cone. */
  spore: { closed: string; open: string; projectile: string };
  /** Spinner — floating spinning hazard. Only on themes whose levels field it (2+). */
  spinner?: { texture: string };
  /** Flyer — fast wave-swimming aerial enemy. Only on themes whose levels field it (3+). */
  flyer?: { frame0: string; frame1: string; flyAnim: string };
  /** Faller — rock that drops from the ceiling. Only on themes that field it (4+). */
  faller?: { texture: string };
}

/** Textures + accent colors + tuning for the end boss so the same MiniBoss behavior can appear
 * as the forest Venus flytrap or the (tougher) desert cactus. */
export interface BossVariant {
  body: string;
  bodyFlash: string;
  seed: string;
  orb: string;
  maxHealth: number;
  /** Movement speed in px/s. */
  speed: number;
  /** Cooldown/telegraph multiplier: <1 attacks faster (harder), 1 is the baseline. */
  aggression: number;
  /** 'slam' = expanding ground shockwave rings, 'spikeBurst' = radial spike volley. */
  special: 'slam' | 'spikeBurst';
  spike: string;
  telegraphColor: number;
  burstColor: number;
  debrisColors: [number, number];
}

export interface ObstaclePlacement {
  clusterCount: number;
  treesPerCluster: [number, number];
  clusterSpread: number;
  otherCount: number;
  treeScaleRange: [number, number];
  treeLike: string[];
}

export interface ThemeConfig {
  skyColor: number;
  ground: { top: string; sub: string };
  platform: string;
  enemySkins: EnemySkins;
  mood: MusicMood;
  /** Collidable sprites — trees, bushes, rocks. Player and enemies cannot pass through. */
  obstacles: string[];
  /** Visual-only sprites — flowers, grass, moss. Walkable, pure decoration. */
  deco: string[];
  obstaclePlacement: ObstaclePlacement;
  /** Theme-specific enemy spawn layout. */
  spawns: Spawn[];
  /** HP multiplier for all enemies in this biome. */
  hpMult: number;
  /** Ambient visual effect spawned periodically. */
  ambientEffect?: 'bubbles';
  /** Extra obstacle type for this theme (e.g. swamp ponds, beach sea pools). */
  extraObstacles?: 'swampPonds' | 'seaWater';
  boss?: BossVariant;
}

export const THEMES: Record<LevelTheme, ThemeConfig> = {
  forest: {
    skyColor: 0x5fb7e8,
    mood: 'default',
    ground: { top: 'tile-ground', sub: 'tile-dirt' },
    platform: 'tile-platform',
    obstacles: ['bush', 'bg-tree-0', 'bg-tree-1'],
    deco: ['grass-tuft', 'daisy', 'hidden-flower'],
    // Forest was a big outlier — up to ~130 trees vs 8–56 in every other biome. All of them are
    // y-depth-sorted every frame and can't batch, so scrolling into a dense cluster spiked the
    // draw calls and stuttered (worst on mobile). Trimmed to ~24–42 trees: still a forest, far cheaper.
    obstaclePlacement: { clusterCount: 7, treesPerCluster: [3, 6], clusterSpread: 90, otherCount: 6, treeScaleRange: [0.8, 1.4], treeLike: ['bg-tree-0', 'bg-tree-1'] },
    hpMult: 1.0,
    spawns: [
      { x: 375, y: 250, kind: 'chaser' }, { x: 625, y: 438, kind: 'chaser' },
      { x: 1375, y: 313, kind: 'turret' }, { x: 1000, y: 375, kind: 'chaser' },
      { x: 250, y: 688, kind: 'chaser' }, { x: 1250, y: 625, kind: 'chaser' },
      { x: 750, y: 625, kind: 'turret' }, { x: 1625, y: 750, kind: 'chaser' },
      { x: 500, y: 938, kind: 'chaser' }, { x: 1125, y: 875, kind: 'chaser' },
      { x: 188, y: 1063, kind: 'turret' }, { x: 1500, y: 1125, kind: 'chaser' },
      { x: 688, y: 1250, kind: 'chaser' }, { x: 1313, y: 1313, kind: 'chaser' },
      { x: 375, y: 1375, kind: 'turret' }, { x: 938, y: 1438, kind: 'chaser' },
      { x: 1688, y: 1438, kind: 'chaser' }, { x: 250, y: 1688, kind: 'chaser' },
      { x: 813, y: 1625, kind: 'turret' }, { x: 1375, y: 1563, kind: 'chaser' },
      { x: 500, y: 1875, kind: 'chaser' }, { x: 1125, y: 1813, kind: 'chaser' },
      { x: 1563, y: 1875, kind: 'turret' }, { x: 188, y: 2125, kind: 'chaser' },
      { x: 688, y: 2063, kind: 'chaser' }, { x: 1250, y: 2125, kind: 'chaser' },
      { x: 375, y: 2375, kind: 'turret' }, { x: 938, y: 2438, kind: 'chaser' },
      { x: 1500, y: 2438, kind: 'chaser' }, { x: 625, y: 2688, kind: 'chaser' },
      { x: 1250, y: 2750, kind: 'turret' }, { x: 250, y: 2813, kind: 'chaser' },
    ],
    enemySkins: {
      walker: { frame0: 'mushroom-0', frame1: 'mushroom-1', walkAnim: 'mushroom-walk' },
      shooter: { idle: 'thorn-bush-idle', fire: 'thorn-bush-fire', projectile: 'enemy-spike' },
      aimer: { idle: 'sunflower-idle', fire: 'sunflower-fire', projectile: 'enemy-seed' },
      worm: { mound: 'vine-worm-mound', emerge: 'vine-worm-emerge', charge: 'vine-worm-charge' },
      spore: { closed: 'poison-flower-closed', open: 'poison-flower-open', projectile: 'enemy-spore' },
    },
    boss: {
      body: 'boss-body',
      bodyFlash: 'boss-body-flash',
      seed: 'boss-seed',
      orb: 'boss-orb',
      maxHealth: 300,
      speed: 68,
      aggression: 1.25,
      special: 'slam',
      spike: 'enemy-spike',
      telegraphColor: 0xff6fb5,
      burstColor: 0x8fe06f,
      debrisColors: [0x3a8f4f, 0x1f5c30],
    },
  },
  desert: {
    skyColor: 0xf3b76b,
    mood: 'desert',
    ground: { top: 'tile-sand', sub: 'tile-sand-sub' },
    platform: 'tile-sandstone',
    obstacles: ['rock', 'cactus-bg'],
    deco: ['dry-shrub', 'cactus-small'],
    obstaclePlacement: { clusterCount: 5, treesPerCluster: [2, 4], clusterSpread: 60, otherCount: 10, treeScaleRange: [0.8, 1.4], treeLike: ['cactus-bg'] },
    hpMult: 1.1,
    spawns: [
      { x: 375, y: 250, kind: 'chaser' }, { x: 1000, y: 200, kind: 'flyer' },
      { x: 1625, y: 313, kind: 'turret' }, { x: 600, y: 500, kind: 'worm' },
      { x: 1375, y: 438, kind: 'chaser' }, { x: 250, y: 750, kind: 'flyer' },
      { x: 800, y: 688, kind: 'turret' }, { x: 1500, y: 625, kind: 'chaser' },
      { x: 500, y: 1000, kind: 'chaser' }, { x: 1125, y: 938, kind: 'flyer' },
      { x: 1750, y: 875, kind: 'worm' }, { x: 188, y: 1250, kind: 'turret' },
      { x: 700, y: 1313, kind: 'chaser' }, { x: 1375, y: 1188, kind: 'flyer' },
      { x: 375, y: 1500, kind: 'worm' }, { x: 1000, y: 1438, kind: 'turret' },
      { x: 1688, y: 1500, kind: 'chaser' }, { x: 250, y: 1750, kind: 'flyer' },
      { x: 813, y: 1813, kind: 'chaser' }, { x: 1500, y: 1750, kind: 'turret' },
      { x: 500, y: 2063, kind: 'worm' }, { x: 1125, y: 2000, kind: 'flyer' },
      { x: 1750, y: 2125, kind: 'chaser' }, { x: 188, y: 2375, kind: 'turret' },
      { x: 688, y: 2313, kind: 'chaser' }, { x: 1375, y: 2438, kind: 'worm' },
      { x: 250, y: 2625, kind: 'flyer' }, { x: 1000, y: 2563, kind: 'chaser' },
      { x: 1625, y: 2688, kind: 'turret' }, { x: 500, y: 2813, kind: 'chaser' },
    ],
    enemySkins: {
      walker: { frame0: 'barrel-0', frame1: 'barrel-1', walkAnim: 'barrel-walk' },
      shooter: { idle: 'needle-cactus-idle', fire: 'needle-cactus-fire', projectile: 'cactus-needle' },
      aimer: { idle: 'agave-idle', fire: 'agave-fire', projectile: 'agave-seed' },
      worm: { mound: 'sandworm-mound', emerge: 'sandworm-emerge', charge: 'sandworm-charge' },
      spore: { closed: 'puffball-closed', open: 'puffball-open', projectile: 'puff-spore' },
      spinner: { texture: 'spin-burr' }, // spinning tumble-burr — new in level 2
    },
    boss: {
      body: 'boss-cactus',
      bodyFlash: 'boss-cactus-flash',
      seed: 'cactus-seed',
      orb: 'cactus-orb',
      // Tougher than the flytrap: more health, faster attacks, and a signature radial
      // needle burst instead of the ground slam.
      maxHealth: 380,
      speed: 55,
      aggression: 0.78,
      special: 'spikeBurst',
      spike: 'boss-spike',
      telegraphColor: 0xffe066,
      burstColor: 0xffd24a,
      debrisColors: [0x3f8f3a, 0x2f6a2a],
    },
  },
  water: {
    skyColor: 0x1f6f8f,
    mood: 'water',
    ground: { top: 'tile-seabed', sub: 'tile-seabed-sub' },
    platform: 'tile-coral-rock',
    obstacles: ['sea-rock', 'coral'],
    deco: ['sea-shell', 'seaweed-tuft'],
    obstaclePlacement: { clusterCount: 5, treesPerCluster: [2, 4], clusterSpread: 60, otherCount: 8, treeScaleRange: [0.85, 1.15], treeLike: [] },
    ambientEffect: 'bubbles',
    hpMult: 1.15,
    spawns: [
      { x: 375, y: 250, kind: 'chaser' }, { x: 1000, y: 313, kind: 'aimer' },
      { x: 1625, y: 250, kind: 'flyer' }, { x: 625, y: 563, kind: 'spore' },
      { x: 1375, y: 500, kind: 'chaser' }, { x: 250, y: 813, kind: 'flyer' },
      { x: 875, y: 750, kind: 'turret' }, { x: 1500, y: 688, kind: 'aimer' },
      { x: 500, y: 1063, kind: 'chaser' }, { x: 1125, y: 1000, kind: 'spore' },
      { x: 1750, y: 938, kind: 'flyer' }, { x: 188, y: 1250, kind: 'aimer' },
      { x: 688, y: 1375, kind: 'chaser' }, { x: 1313, y: 1313, kind: 'turret' },
      { x: 375, y: 1563, kind: 'spore' }, { x: 1000, y: 1500, kind: 'flyer' },
      { x: 1688, y: 1563, kind: 'aimer' }, { x: 250, y: 1813, kind: 'chaser' },
      { x: 813, y: 1750, kind: 'flyer' }, { x: 1500, y: 1813, kind: 'spore' },
      { x: 500, y: 2063, kind: 'turret' }, { x: 1125, y: 2000, kind: 'aimer' },
      { x: 1750, y: 2125, kind: 'chaser' }, { x: 188, y: 2375, kind: 'flyer' },
      { x: 688, y: 2438, kind: 'spore' }, { x: 1375, y: 2375, kind: 'turret' },
      { x: 250, y: 2688, kind: 'aimer' }, { x: 1000, y: 2625, kind: 'chaser' },
      { x: 1625, y: 2750, kind: 'flyer' }, { x: 500, y: 2875, kind: 'spore' },
    ],
    enemySkins: {
      walker: { frame0: 'algae-crawl-0', frame1: 'algae-crawl-1', walkAnim: 'algae-walk' },
      shooter: { idle: 'urchin-idle', fire: 'urchin-fire', projectile: 'algae-spine' },
      aimer: { idle: 'anemone-idle', fire: 'anemone-fire', projectile: 'algae-seed' },
      worm: { mound: 'eel-mound', emerge: 'eel-emerge', charge: 'eel-charge' },
      spore: { closed: 'bloom-closed', open: 'bloom-open', projectile: 'spore-bubble' },
      spinner: { texture: 'spin-urchin' }, // spinning urchin — carried over from level 2
      flyer: { frame0: 'fish-0', frame1: 'fish-1', flyAnim: 'fish-swim' }, // darting fish — new in level 3
    },
    // Yellow tube sponge (Aplysina fistularis): expels a radial burst of spores from its
    // tubes, and a heavy bubble-orb once wounded.
    boss: {
      body: 'boss-sponge',
      bodyFlash: 'boss-sponge-flash',
      seed: 'sponge-spore',
      orb: 'sponge-orb',
      maxHealth: 340,
      speed: 62,
      aggression: 0.85,
      special: 'spikeBurst',
      spike: 'sponge-jet',
      telegraphColor: 0x5fd0ff,
      burstColor: 0xffe066,
      debrisColors: [0xffcf3a, 0xe0932a],
    },
  },
  cave: {
    skyColor: 0x0d0d18,
    mood: 'cave',
    ground: { top: 'tile-cave', sub: 'tile-cave-sub' },
    platform: 'tile-cave-rock',
    obstacles: ['boulder-small'],
    deco: ['cave-mushroom', 'crystal', 'moss-patch'],
    obstaclePlacement: { clusterCount: 4, treesPerCluster: [2, 4], clusterSpread: 50, otherCount: 8, treeScaleRange: [0.85, 1.15], treeLike: [] },
    hpMult: 1.2,
    spawns: [
      { x: 375, y: 250, kind: 'chaser' }, { x: 1000, y: 313, kind: 'turret' },
      { x: 1625, y: 250, kind: 'worm' }, { x: 625, y: 563, kind: 'spore' },
      { x: 1375, y: 500, kind: 'chaser' }, { x: 250, y: 813, kind: 'turret' },
      { x: 875, y: 750, kind: 'worm' }, { x: 1500, y: 688, kind: 'chaser' },
      { x: 500, y: 1063, kind: 'spore' }, { x: 1125, y: 1000, kind: 'turret' },
      { x: 1750, y: 938, kind: 'chaser' }, { x: 188, y: 1250, kind: 'worm' },
      { x: 688, y: 1375, kind: 'spore' }, { x: 1313, y: 1313, kind: 'turret' },
      { x: 375, y: 1563, kind: 'chaser' }, { x: 1000, y: 1500, kind: 'worm' },
      { x: 1688, y: 1563, kind: 'spore' }, { x: 250, y: 1813, kind: 'turret' },
      { x: 813, y: 1750, kind: 'chaser' }, { x: 1500, y: 1813, kind: 'worm' },
      { x: 500, y: 2063, kind: 'turret' }, { x: 1125, y: 2000, kind: 'spore' },
      { x: 1750, y: 2125, kind: 'chaser' }, { x: 188, y: 2375, kind: 'worm' },
      { x: 688, y: 2438, kind: 'turret' }, { x: 1375, y: 2375, kind: 'spore' },
      { x: 250, y: 2688, kind: 'chaser' }, { x: 1000, y: 2625, kind: 'worm' },
      { x: 1625, y: 2750, kind: 'turret' }, { x: 500, y: 2875, kind: 'spore' },
    ],
    enemySkins: {
      walker: { frame0: 'moss-crawl-0', frame1: 'moss-crawl-1', walkAnim: 'moss-walk' },
      shooter: { idle: 'moss-shooter-idle', fire: 'moss-shooter-fire', projectile: 'moss-spine' },
      aimer: { idle: 'cave-bloom-idle', fire: 'cave-bloom-fire', projectile: 'moss-seed' },
      worm: { mound: 'rockworm-mound', emerge: 'rockworm-emerge', charge: 'rockworm-charge' },
      spore: { closed: 'fungus-closed', open: 'fungus-open', projectile: 'moss-spore' },
      faller: { texture: 'falling-rock' }, // NEW: drops from the ceiling
    },
    // Dry resurrection plant (Selaginella lepidophylla): a curled, spiky brown ball that
    // pulses a dust shockwave (slam) and flings a heavy dust-orb once wounded.
    boss: {
      body: 'boss-resurrection',
      bodyFlash: 'boss-resurrection-flash',
      seed: 'spore-dust',
      orb: 'dust-orb',
      maxHealth: 360,
      speed: 60,
      aggression: 1.15,
      special: 'slam',
      spike: 'enemy-spike', // unused by slam bosses
      telegraphColor: 0xd8b070,
      burstColor: 0xb89a5a,
      debrisColors: [0x8a6a3a, 0x5a4426],
    },
  },
  swamp: {
    skyColor: 0x41503a,
    mood: 'swamp',
    ground: { top: 'tile-mud', sub: 'tile-mud-sub' },
    platform: 'tile-bog',
    obstacles: ['bog-rock', 'swamp-mushroom'],
    deco: ['lily-pad', 'reed'],
    obstaclePlacement: { clusterCount: 4, treesPerCluster: [2, 4], clusterSpread: 50, otherCount: 8, treeScaleRange: [0.85, 1.15], treeLike: [] },
    extraObstacles: 'swampPonds',
    hpMult: 1.25,
    spawns: [
      { x: 375, y: 250, kind: 'chaser' }, { x: 1000, y: 200, kind: 'worm' },
      { x: 1625, y: 313, kind: 'aimer' }, { x: 625, y: 500, kind: 'flyer' },
      { x: 1375, y: 438, kind: 'chaser' }, { x: 250, y: 750, kind: 'spore' },
      { x: 875, y: 688, kind: 'worm' }, { x: 1500, y: 625, kind: 'turret' },
      { x: 500, y: 1000, kind: 'flyer' }, { x: 1125, y: 938, kind: 'chaser' },
      { x: 1750, y: 875, kind: 'aimer' }, { x: 188, y: 1250, kind: 'worm' },
      { x: 688, y: 1313, kind: 'turret' }, { x: 1313, y: 1188, kind: 'spore' },
      { x: 375, y: 1500, kind: 'flyer' }, { x: 1000, y: 1438, kind: 'chaser' },
      { x: 1688, y: 1500, kind: 'worm' }, { x: 250, y: 1750, kind: 'aimer' },
      { x: 813, y: 1813, kind: 'spore' }, { x: 1500, y: 1750, kind: 'flyer' },
      { x: 500, y: 2063, kind: 'turret' }, { x: 1125, y: 2000, kind: 'chaser' },
      { x: 1750, y: 2125, kind: 'worm' }, { x: 188, y: 2375, kind: 'flyer' },
      { x: 688, y: 2313, kind: 'aimer' }, { x: 1375, y: 2438, kind: 'spore' },
      { x: 250, y: 2625, kind: 'chaser' }, { x: 1000, y: 2563, kind: 'worm' },
      { x: 1625, y: 2688, kind: 'turret' }, { x: 500, y: 2813, kind: 'flyer' },
    ],
    enemySkins: {
      walker: { frame0: 'bog-crawl-0', frame1: 'bog-crawl-1', walkAnim: 'bog-walk' },
      shooter: { idle: 'reed-idle', fire: 'reed-fire', projectile: 'reed-dart' },
      aimer: { idle: 'bogflower-idle', fire: 'bogflower-fire', projectile: 'bog-seed' },
      worm: { mound: 'leech-mound', emerge: 'leech-emerge', charge: 'leech-charge' },
      spore: { closed: 'swampshroom-closed', open: 'swampshroom-open', projectile: 'swamp-spore' },
      flyer: { frame0: 'dragon-0', frame1: 'dragon-1', flyAnim: 'dragon-fly' }, // dragonflies
    },
    // Lesser bulrush / cattail (Typha): a tall reed with a brown seed-head that bursts into a
    // radial cloud of fluffy seeds; toughest boss (final level).
    boss: {
      body: 'boss-bulrush',
      bodyFlash: 'boss-bulrush-flash',
      seed: 'bulrush-seed',
      orb: 'bulrush-orb',
      maxHealth: 400,
      speed: 50,
      aggression: 0.8,
      special: 'spikeBurst',
      spike: 'bulrush-fluff',
      telegraphColor: 0xe8dcc0,
      burstColor: 0xe8dcc0,
      debrisColors: [0x6b8f3f, 0x8a6a3a],
    },
  },
  museum: {
    skyColor: 0xc4e4d0,
    mood: 'museum',
    ground: { top: 'tile-greenhouse', sub: 'tile-greenhouse-sub' },
    platform: 'tile-planter',
    obstacles: ['garden-bench', 'potted-plant', 'potted-plant'],
    deco: ['fern', 'flower-bed'],
    obstaclePlacement: { clusterCount: 4, treesPerCluster: [2, 4], clusterSpread: 50, otherCount: 8, treeScaleRange: [0.85, 1.15], treeLike: [] },
    hpMult: 1.3,
    spawns: [
      { x: 375, y: 250, kind: 'aimer' }, { x: 1000, y: 200, kind: 'flyer' },
      { x: 1625, y: 313, kind: 'worm' }, { x: 625, y: 500, kind: 'spore' },
      { x: 1375, y: 438, kind: 'chaser' }, { x: 250, y: 750, kind: 'turret' },
      { x: 875, y: 688, kind: 'aimer' }, { x: 1500, y: 625, kind: 'flyer' },
      { x: 500, y: 1000, kind: 'worm' }, { x: 1125, y: 938, kind: 'spore' },
      { x: 1750, y: 875, kind: 'chaser' }, { x: 188, y: 1250, kind: 'turret' },
      { x: 688, y: 1313, kind: 'aimer' }, { x: 1313, y: 1188, kind: 'flyer' },
      { x: 375, y: 1500, kind: 'spore' }, { x: 1000, y: 1438, kind: 'worm' },
      { x: 1688, y: 1500, kind: 'chaser' }, { x: 250, y: 1750, kind: 'turret' },
      { x: 813, y: 1813, kind: 'flyer' }, { x: 1500, y: 1750, kind: 'aimer' },
      { x: 500, y: 2063, kind: 'spore' }, { x: 1125, y: 2000, kind: 'worm' },
      { x: 1750, y: 2125, kind: 'chaser' }, { x: 188, y: 2375, kind: 'turret' },
      { x: 688, y: 2438, kind: 'aimer' }, { x: 1375, y: 2375, kind: 'flyer' },
      { x: 250, y: 2688, kind: 'spore' }, { x: 1000, y: 2625, kind: 'worm' },
      { x: 1625, y: 2750, kind: 'chaser' }, { x: 500, y: 2875, kind: 'turret' },
    ],
    enemySkins: {
      walker: { frame0: 'mushroom-0', frame1: 'mushroom-1', walkAnim: 'mushroom-walk' },
      shooter: { idle: 'needle-cactus-idle', fire: 'needle-cactus-fire', projectile: 'cactus-needle' },
      aimer: { idle: 'anemone-idle', fire: 'anemone-fire', projectile: 'algae-seed' },
      worm: { mound: 'leech-mound', emerge: 'leech-emerge', charge: 'leech-charge' },
      spore: { closed: 'fungus-closed', open: 'fungus-open', projectile: 'moss-spore' },
      spinner: { texture: 'spin-burr' },
      flyer: { frame0: 'dragon-0', frame1: 'dragon-1', flyAnim: 'dragon-fly' },
      faller: { texture: 'falling-rock' },
    },
    // Final boss: the rare corpse flower (Rafflesia) — a huge fleshy speckled bloom that belches
    // a radial cloud of spores.
    boss: {
      body: 'boss-corpse',
      bodyFlash: 'boss-corpse-flash',
      seed: 'corpse-spore',
      orb: 'corpse-orb',
      maxHealth: 420,
      speed: 58,
      aggression: 0.76,
      special: 'spikeBurst',
      spike: 'corpse-spike',
      telegraphColor: 0xc0506a,
      burstColor: 0xd08a5a,
      debrisColors: [0x8a3a4a, 0x5a2a2a],
    },
  },
  // ---- Level 7: SPACE — a botanical void where plants live sealed in glass domes (the
  // Little-Prince rose). New environment + a NEW walker (glass-bubble orbling) and spore
  // (glass pod); the rest reuse cave/water skins. Boss: the Cosmic Rose under a cracked dome.
  space: {
    skyColor: 0x05060f,
    mood: 'space',
    ground: { top: 'tile-space', sub: 'tile-space' },
    platform: 'tile-space',
    obstacles: ['asteroid', 'meteor-rock'],
    deco: ['star-twinkle', 'star-far', 'star-far'],
    obstaclePlacement: { clusterCount: 3, treesPerCluster: [2, 4], clusterSpread: 50, otherCount: 9, treeScaleRange: [0.85, 1.15], treeLike: [] },
    hpMult: 1.35,
    spawns: [],
    enemySkins: {
      walker: { frame0: 'orbling-0', frame1: 'orbling-1', walkAnim: 'orbling-float' },
      shooter: { idle: 'moss-shooter-idle', fire: 'moss-shooter-fire', projectile: 'moss-spine' },
      aimer: { idle: 'anemone-idle', fire: 'anemone-fire', projectile: 'algae-seed' },
      worm: { mound: 'rockworm-mound', emerge: 'rockworm-emerge', charge: 'rockworm-charge' },
      spore: { closed: 'podbloom-closed', open: 'podbloom-open', projectile: 'pod-spore' },
      flyer: { frame0: 'fish-0', frame1: 'fish-1', flyAnim: 'fish-swim' },
    },
    boss: {
      body: 'boss-rose',
      bodyFlash: 'boss-rose-flash',
      seed: 'rose-seed',
      orb: 'rose-orb',
      maxHealth: 430,
      speed: 60,
      aggression: 0.8,
      special: 'spikeBurst',
      spike: 'rose-shard',
      telegraphColor: 0x5fe0ff,
      burstColor: 0xff9db0,
      debrisColors: [0x6a1b6f, 0x2a0a2e],
    },
  },
  // ---- Level 8: BEACH — sunny sand with big impassable pools of sea (extraObstacles:'seaWater'),
  // clustered coconut palms, and a rolling-coconut walker. Foes reuse the underwater biome.
  // Boss: a giant carnivorous pineapple.
  beach: {
    skyColor: 0x7ec8f0,
    mood: 'beach',
    ground: { top: 'tile-beach', sub: 'tile-beach' },
    platform: 'tile-beach',
    obstacles: ['palm-tree', 'sea-rock'],
    deco: ['sea-shell', 'starfish', 'beach-grass'],
    obstaclePlacement: { clusterCount: 6, treesPerCluster: [2, 4], clusterSpread: 70, otherCount: 8, treeScaleRange: [0.85, 1.15], treeLike: ['palm-tree'] },
    extraObstacles: 'seaWater',
    hpMult: 1.4,
    spawns: [],
    enemySkins: {
      walker: { frame0: 'coco-0', frame1: 'coco-1', walkAnim: 'coco-roll' },
      shooter: { idle: 'urchin-idle', fire: 'urchin-fire', projectile: 'algae-spine' },
      aimer: { idle: 'anemone-idle', fire: 'anemone-fire', projectile: 'algae-seed' },
      worm: { mound: 'eel-mound', emerge: 'eel-emerge', charge: 'eel-charge' },
      spore: { closed: 'bloom-closed', open: 'bloom-open', projectile: 'spore-bubble' },
      flyer: { frame0: 'fish-0', frame1: 'fish-1', flyAnim: 'fish-swim' },
    },
    boss: {
      body: 'boss-pineapple',
      bodyFlash: 'boss-pineapple-flash',
      seed: 'pineapple-seed',
      orb: 'pineapple-orb',
      maxHealth: 450,
      speed: 58,
      aggression: 0.78,
      special: 'spikeBurst',
      spike: 'pineapple-spike',
      telegraphColor: 0xfff3b0,
      burstColor: 0x7ed957,
      debrisColors: [0xc99a26, 0x2c6e35],
    },
  },
  // ---- Level 9: MOUNTAIN — cold alpine stone dusted with snow, clustered firs, a rolling
  // pinecone walker. Foes reuse forest/cave/swamp skins. Boss: a giant ancient pinecone.
  mountain: {
    skyColor: 0x9fb8d8,
    mood: 'mountain',
    ground: { top: 'tile-mountain', sub: 'tile-mountain' },
    platform: 'tile-mountain',
    obstacles: ['pine-tree', 'boulder-small'],
    deco: ['edelweiss', 'snow-patch'],
    obstaclePlacement: { clusterCount: 6, treesPerCluster: [2, 5], clusterSpread: 80, otherCount: 6, treeScaleRange: [0.85, 1.15], treeLike: ['pine-tree'] },
    hpMult: 1.45,
    spawns: [],
    enemySkins: {
      walker: { frame0: 'pinecone-0', frame1: 'pinecone-1', walkAnim: 'pinecone-roll' },
      shooter: { idle: 'thorn-bush-idle', fire: 'thorn-bush-fire', projectile: 'enemy-spike' },
      aimer: { idle: 'sunflower-idle', fire: 'sunflower-fire', projectile: 'enemy-seed' },
      worm: { mound: 'rockworm-mound', emerge: 'rockworm-emerge', charge: 'rockworm-charge' },
      spore: { closed: 'fungus-closed', open: 'fungus-open', projectile: 'moss-spore' },
      flyer: { frame0: 'dragon-0', frame1: 'dragon-1', flyAnim: 'dragon-fly' },
    },
    boss: {
      body: 'boss-pinecone',
      bodyFlash: 'boss-pinecone-flash',
      seed: 'pinecone-boss-seed',
      orb: 'pinecone-orb',
      maxHealth: 470,
      speed: 56,
      aggression: 0.76,
      special: 'spikeBurst',
      spike: 'pinecone-needle',
      telegraphColor: 0xeef4fb,
      burstColor: 0x63bf5f,
      debrisColors: [0x6b4522, 0x3f8f52],
    },
  },
  // ---- Level 10 (FINAL): HOUSE — a cozy room overrun by houseplants. Wood floor, furniture +
  // potted-plant obstacles, a toddling potted-plant walker and a NEW potted-cactus shooter.
  // Boss: the Monstera Monstruo (Swiss-cheese plant) with a whipping-vine shockwave slam.
  house: {
    skyColor: 0x8a6f52,
    mood: 'house',
    ground: { top: 'tile-house', sub: 'tile-house' },
    platform: 'tile-house',
    obstacles: ['potted-fig', 'sofa', 'potted-plant'],
    deco: ['small-succulent', 'floor-rug'],
    obstaclePlacement: { clusterCount: 4, treesPerCluster: [2, 4], clusterSpread: 50, otherCount: 12, treeScaleRange: [0.85, 1.15], treeLike: [] },
    hpMult: 1.5,
    spawns: [],
    enemySkins: {
      walker: { frame0: 'pot-crawler-0', frame1: 'pot-crawler-1', walkAnim: 'pot-walk' },
      shooter: { idle: 'potted-cactus-idle', fire: 'potted-cactus-fire', projectile: 'cactus-needle' },
      aimer: { idle: 'sunflower-idle', fire: 'sunflower-fire', projectile: 'enemy-seed' },
      worm: { mound: 'leech-mound', emerge: 'leech-emerge', charge: 'leech-charge' },
      spore: { closed: 'fungus-closed', open: 'fungus-open', projectile: 'moss-spore' },
      flyer: { frame0: 'dragon-0', frame1: 'dragon-1', flyAnim: 'dragon-fly' },
    },
    boss: {
      body: 'boss-monstera',
      bodyFlash: 'boss-monstera-flash',
      seed: 'monstera-seed',
      orb: 'monstera-orb',
      maxHealth: 500,
      speed: 54,
      aggression: 0.72,
      special: 'slam',
      spike: 'monstera-spike',
      telegraphColor: 0x8fe07a,
      burstColor: 0x54b45a,
      debrisColors: [0x1f6b2c, 0x2a1a0a],
    },
  },
};

const SKIN_KIND_MAP: Partial<Record<EnemyKind, keyof ThemeConfig['enemySkins']>> = {
  chaser: 'walker',
  turret: 'shooter',
  aimer: 'aimer',
  worm: 'worm',
  spore: 'spore',
  flyer: 'flyer',
};

export function generateSpawns(
  themeConfig: ThemeConfig,
  sub: SubLevelConfig,
  arenaW: number,
  arenaH: number,
  playerStartX: number,
  playerStartY: number,
): Spawn[] {
  const kinds = sub.allowedKinds.filter((k) => {
    const skinKey = SKIN_KIND_MAP[k];
    return skinKey ? skinKey in themeConfig.enemySkins : true;
  });
  if (kinds.length === 0) kinds.push('chaser');

  const margin = 120;
  const spawns: Spawn[] = [];
  const usedX: number[] = [];
  const usedY: number[] = [];

  for (let i = 0; i < sub.spawnCount; i++) {
    let x = Phaser.Math.Between(margin, arenaW - margin);
    let y = Phaser.Math.Between(margin, arenaH - margin);
    if (Phaser.Math.Distance.Between(x, y, playerStartX, playerStartY) < 200) {
      const angle = Phaser.Math.Angle.Between(playerStartX, playerStartY, x, y);
      x = playerStartX + Math.cos(angle) * 250;
      y = playerStartY + Math.sin(angle) * 250;
    }
    usedX.push(x);
    usedY.push(y);
    spawns.push({ x, y, kind: Phaser.Utils.Array.GetRandom(kinds) });
  }
  return spawns;
}
