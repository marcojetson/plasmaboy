// Playable characters. Behaviour is identical; only the sprite set (and its animations) differ.
// All three share the same 16x22 art grid, arm-cannon position and physics footprint, so the
// weapon overlays and collision body line up for every character.

export type CharacterId = 'plasmaboy' | 'ranger' | 'plantgirl';

export interface CharacterDef {
  id: CharacterId;
  /** i18n StringKey for the display name. */
  nameKey: 'charPlasmaboy' | 'charRanger' | 'charPlantgirl';
  /** Idle animation key (registered in AnimationDefs). */
  idleAnim: string;
  /** Walk animation key. */
  walkAnim: string;
  /** Texture key used for the initial frame + menu portrait. */
  idleFrame: string;
}

export const CHARACTERS: Record<CharacterId, CharacterDef> = {
  plasmaboy: { id: 'plasmaboy', nameKey: 'charPlasmaboy', idleAnim: 'player-idle', walkAnim: 'player-walk', idleFrame: 'player-idle-0' },
  ranger: { id: 'ranger', nameKey: 'charRanger', idleAnim: 'ranger-idle', walkAnim: 'ranger-walk', idleFrame: 'ranger-idle-0' },
  plantgirl: { id: 'plantgirl', nameKey: 'charPlantgirl', idleAnim: 'plantgirl-idle', walkAnim: 'plantgirl-walk', idleFrame: 'plantgirl-idle-0' },
};

/** Display order on the character-select screen. */
export const CHARACTER_ORDER: CharacterId[] = ['plasmaboy', 'ranger', 'plantgirl'];

const STORAGE_KEY = 'pb-character';

export function isCharacterId(v: unknown): v is CharacterId {
  return typeof v === 'string' && v in CHARACTERS;
}

export function loadCharacter(): CharacterId {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (isCharacterId(saved)) return saved;
  } catch { /* ignore */ }
  return 'plasmaboy';
}

export function saveCharacter(id: CharacterId): void {
  try { localStorage.setItem(STORAGE_KEY, id); } catch { /* ignore */ }
}
