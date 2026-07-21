/** Visual theme of a level. Drives tile art, background decoration, sky color, the enemy
 * "skin" each behavior archetype wears, and which boss variant appears. Behavior is identical
 * across themes — only the art changes. */
export type LevelTheme =
  | 'forest' | 'desert' | 'water' | 'cave' | 'swamp' | 'museum'
  | 'space' | 'beach' | 'mountain' | 'house';

export type EnemyKind = 'chaser' | 'turret' | 'aimer' | 'spore' | 'flyer' | 'worm';

export interface Spawn {
  x: number;
  y: number;
  kind: EnemyKind;
}

export interface PlatformSpec {
  x: number;
  y: number;
  width: number;
  height: number;
}

/** Minimal level data used by the decoration system. */
export interface LevelData {
  theme: LevelTheme;
  widthPx: number;
  heightPx: number;
  platforms: PlatformSpec[];
}
