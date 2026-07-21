import type { EnemyKind, LevelTheme } from '@/config/LevelData';

export interface SubLevelConfig {
  spawnCount: number;
  hpMult: number;
  gemMinDist: number;
  allowedKinds: EnemyKind[];
}

export const BIOMES: LevelTheme[] = [
  'forest', 'desert', 'water', 'cave', 'swamp', 'museum',
  'space', 'beach', 'mountain', 'house',
];

export const GEM_TINTS: Record<LevelTheme, number> = {
  forest: 0xaa66dd,
  desert: 0xffdd00,
  water: 0x33aaff,
  cave: 0x888888,
  swamp: 0xbbaa44,
  museum: 0xffffff,
  space: 0x9ae86a,    // moldavite — the green glass gem forged by meteorite impact
  beach: 0x7fe0d8,    // aquamarine — pale sea green-blue
  mountain: 0xff4d5a, // ruby — bold red mined from the rock
  house: 0x3a7bff,    // sapphire — regal blue, the finale
};

export const GEM_I18N: Record<LevelTheme, string> = {
  forest: 'gemAmethyst',
  desert: 'gemCitrine',
  water: 'gemLapis',
  cave: 'gemObsidian',
  swamp: 'gemHematite',
  museum: 'gemDiamond',
  space: 'gemMoldavite',
  beach: 'gemAquamarine',
  mountain: 'gemRuby',
  house: 'gemSapphire',
};

export const SUB_LEVELS: SubLevelConfig[] = [
  { spawnCount: 12, hpMult: 0.7, gemMinDist: 800, allowedKinds: ['chaser'] },
  { spawnCount: 20, hpMult: 1.0, gemMinDist: 1200, allowedKinds: ['chaser', 'turret'] },
  { spawnCount: 28, hpMult: 1.3, gemMinDist: 1600, allowedKinds: ['chaser', 'turret', 'aimer', 'flyer'] },
  { spawnCount: 10, hpMult: 1.0, gemMinDist: 0, allowedKinds: ['chaser', 'turret', 'aimer', 'flyer', 'spore', 'worm'] },
];

export function biomeOf(levelIndex: number): number {
  return Math.floor(levelIndex / 4);
}

export function subOf(levelIndex: number): number {
  return levelIndex % 4;
}

export function themeOf(levelIndex: number): LevelTheme {
  return BIOMES[biomeOf(levelIndex)] ?? 'forest';
}

export function levelLabel(levelIndex: number): string {
  return `${biomeOf(levelIndex) + 1}-${subOf(levelIndex) + 1}`;
}
