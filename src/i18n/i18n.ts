// Tiny i18n layer. Language is auto-detected from the browser, overridable via ?lang= query
// string, and persisted in localStorage. Falls back to English for unknown locales.

export type Lang = 'es' | 'de' | 'en';

const STORAGE_KEY = 'pb-lang';
const LANGS: Lang[] = ['es', 'de', 'en'];
const VALID_LANGS: ReadonlySet<string> = new Set(LANGS);

function normalize(raw: string): Lang {
  const base = raw.toLowerCase().split('-')[0] ?? '';
  if (VALID_LANGS.has(base)) return base as Lang;
  return 'en';
}

function detectLang(): Lang {
  try {
    const qs = new URLSearchParams(window.location.search).get('lang');
    if (qs) return normalize(qs);
  } catch { /* ignore */ }

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && VALID_LANGS.has(saved)) return saved as Lang;
  } catch { /* ignore */ }

  const browserLang = navigator.language ?? (navigator as { userLanguage?: string }).userLanguage ?? '';
  return normalize(browserLang);
}

let current: Lang = detectLang();

export function getLang(): Lang {
  return current;
}

type StringKey =
  | 'subtitle'
  | 'vsPlantas'
  | 'tapStart'
  | 'huntTheBoss'
  | 'bossEast'
  | 'bossSouthEast'
  | 'bossSouth'
  | 'bossSouthWest'
  | 'bossWest'
  | 'bossNorthWest'
  | 'bossNorth'
  | 'bossNorthEast'
  | 'gemFound'
  | 'bossDefeated'
  | 'tapToContinue'
  | 'allCleared'
  | 'tapToReturn'
  | 'gameOver'
  | 'tapToRetry'
  | 'forestName'
  | 'desertName'
  | 'waterName'
  | 'caveName'
  | 'swampName'
  | 'museumName'
  | 'spaceName'
  | 'beachName'
  | 'mountainName'
  | 'houseName'
  | 'loading'
  | 'score'
  | 'topScore'
  | 'gemAmethyst'
  | 'gemCitrine'
  | 'gemLapis'
  | 'gemObsidian'
  | 'gemHematite'
  | 'gemDiamond'
  | 'gemMoldavite'
  | 'gemAquamarine'
  | 'gemRuby'
  | 'gemSapphire'
  | 'gemNorth'
  | 'gemNorthEast'
  | 'gemEast'
  | 'gemSouthEast'
  | 'gemSouth'
  | 'gemSouthWest'
  | 'gemWest'
  | 'gemNorthWest'
  | 'kidsMode'
  | 'expertMode'
  | 'defeatBoss'
  | 'findGem'
  | 'chooseHero'
  | 'charPlasmaboy'
  | 'charRanger'
  | 'charPlantgirl'
  | 'play';

const STRINGS: Record<StringKey, Record<Lang, string>> = {
  subtitle: {
    es: '¡Las plantas despertaron!',
    de: 'Die Pflanzen sind erwacht!',
    en: 'The plants have awakened...',
  },
  vsPlantas: {
    es: 'vs PLANTAS MONSTRUO',
    de: 'vs PFLANZEN-MONSTER',
    en: 'vs PLANT MONSTERS',
  },
  tapStart: {
    es: 'Toca para empezar',
    de: 'Tippe zum Starten',
    en: 'Tap to start',
  },
  huntTheBoss: {
    es: '¡CAZA AL JEFE!',
    de: 'JAGE DEN BOSS!',
    en: 'HUNT THE BOSS',
  },
  bossEast: {
    es: 'EL JEFE ESTÁ AL ESTE\n→',
    de: 'DER BOSS IST IM OSTEN\n→',
    en: 'BOSS IS EAST\n→',
  },
  bossSouthEast: {
    es: 'EL JEFE ESTÁ AL SUDESTE\n↙',
    de: 'DER BOSS IST IM SÜDOSTEN\n↙',
    en: 'BOSS IS SOUTH-EAST\n↙',
  },
  bossSouth: {
    es: 'EL JEFE ESTÁ AL SUR\n↓',
    de: 'DER BOSS IST IM SÜDEN\n↓',
    en: 'BOSS IS SOUTH\n↓',
  },
  bossSouthWest: {
    es: 'EL JEFE ESTÁ AL SUROESTE\n↙',
    de: 'DER BOSS IST IM SÜDWESTEN\n↙',
    en: 'BOSS IS SOUTH-WEST\n↙',
  },
  bossWest: {
    es: 'EL JEFE ESTÁ AL OESTE\n←',
    de: 'DER BOSS IST IM WESTEN\n←',
    en: 'BOSS IS WEST\n←',
  },
  bossNorthWest: {
    es: '↖\nEL JEFE ESTÁ AL NOROESTE',
    de: '↖\nDER BOSS IST IM NORWESTEN',
    en: '↖\nBOSS IS NORTH-WEST',
  },
  bossNorth: {
    es: '↑\nEL JEFE ESTÁ AL NORTE',
    de: '↑\nDER BOSS IST IM NORDEN',
    en: '↑\nBOSS IS NORTH',
  },
  bossNorthEast: {
    es: '↗\nEL JEFE ESTÁ AL NORESTE',
    de: '↗\nDER BOSS IST IM NORDOSTEN',
    en: '↗\nBOSS IS NORTH-EAST',
  },
  gemFound: {
    es: '¡GEMA ENCONTRADA!',
    de: 'EDELSTEIN GEFUNDEN!',
    en: 'GEM FOUND!',
  },
  bossDefeated: {
    es: '¡JEFE DERROTADO!',
    de: 'BOSS BESIEGT!',
    en: 'BOSS DEFEATED!',
  },
  kidsMode: {
    es: 'Modo Niños',
    de: 'Kindermodus',
    en: 'Kids Mode',
  },
  expertMode: {
    es: 'Modo Experto',
    de: 'Expertenmodus',
    en: 'Expert Mode',
  },
  defeatBoss: {
    es: '¡DERROTA AL JEFE!',
    de: 'BESIEGE DEN BOSS!',
    en: 'DEFEAT THE BOSS!',
  },
  findGem: {
    es: '¡ENCUENTRA {GEM}!',
    de: 'FINDE {GEM}!',
    en: 'FIND {GEM}!',
  },
  chooseHero: {
    es: 'ELIGE TU HÉROE',
    de: 'WÄHLE DEINEN HELDEN',
    en: 'CHOOSE YOUR HERO',
  },
  charPlasmaboy: {
    es: 'Plasma Boy',
    de: 'Plasma Boy',
    en: 'Plasma Boy',
  },
  charRanger: {
    es: 'Plasma Ranger',
    de: 'Plasma Ranger',
    en: 'Plasma Ranger',
  },
  charPlantgirl: {
    es: 'Chica Planta',
    de: 'Pflanzenmädchen',
    en: 'Plant Girl',
  },
  play: {
    es: 'JUGAR',
    de: 'SPIELEN',
    en: 'PLAY',
  },
  tapToContinue: {
    es: 'toca para continuar',
    de: 'tippe zum Weitermachen',
    en: 'tap to continue',
  },
  allCleared: {
    es: '¡TODOS LOS BIOMAS SUPERADOS!',
    de: 'ALLE BIOME GESCHAFFT!',
    en: 'ALL BIOMES CLEARED!',
  },
  tapToReturn: {
    es: 'toca para volver',
    de: 'tippe zum Zurückkehren',
    en: 'tap to return',
  },
  gameOver: {
    es: 'FIN DEL JUEGO',
    de: 'SPIEL VORBEI',
    en: 'GAME OVER',
  },
  tapToRetry: {
    es: 'toca para reintentar',
    de: 'tippe zum Wiederholen',
    en: 'tap to retry',
  },
  forestName: {
    es: 'El Bosque',
    de: 'Der Wald',
    en: 'The Forest',
  },
  desertName: {
    es: 'El Desierto',
    de: 'Die Wüste',
    en: 'The Desert',
  },
  waterName: {
    es: 'El Fondo del Mar',
    de: 'Die Tiefsee',
    en: 'The Deep Sea',
  },
  caveName: {
    es: 'La Cueva',
    de: 'Die Höhle',
    en: 'The Cave',
  },
  swampName: {
    es: 'El Pantano',
    de: 'Der Sumpf',
    en: 'The Swamp',
  },
  museumName: {
    es: 'El Jardín Botánico',
    de: 'Der Botanische Garten',
    en: 'The Botanical Garden',
  },
  spaceName: {
    es: 'El Jardín Estelar',
    de: 'Der Sternengarten',
    en: 'The Star Garden',
  },
  beachName: {
    es: 'La Playa',
    de: 'Der Strand',
    en: 'The Beach',
  },
  mountainName: {
    es: 'La Montaña',
    de: 'Der Berg',
    en: 'The Mountain',
  },
  houseName: {
    es: 'La Casa',
    de: 'Das Haus',
    en: 'The House',
  },
  loading: {
    es: 'Cargando...',
    de: 'Laden...',
    en: 'Loading...',
  },
  score: {
    es: 'Puntos:',
    de: 'Punkte:',
    en: 'Score:',
  },
  topScore: {
    es: 'Mejor:',
    de: 'Beste:',
    en: 'Best:',
  },
  gemAmethyst: {
    es: 'LA AMATISTA',
    de: 'DER AMETHYST',
    en: 'THE AMETHYST',
  },
  gemCitrine: {
    es: 'EL CITRINO',
    de: 'DER CITRIN',
    en: 'THE CITRINE',
  },
  gemLapis: {
    es: 'EL LAPIS LAZULI',
    de: 'DER LAZULIT',
    en: 'THE LAPIS LAZULI',
  },
  gemObsidian: {
    es: 'EL OBSIDIAN',
    de: 'DER OBSIDIAN',
    en: 'THE OBSIDIAN',
  },
  gemHematite: {
    es: 'LA HEMATITA',
    de: 'DER HEMATIT',
    en: 'THE HEMATITE',
  },
  gemDiamond: {
    es: 'EL DIAMANTE',
    de: 'DER DIAMANT',
    en: 'THE DIAMOND',
  },
  gemMoldavite: {
    es: 'LA MOLDAVITA',
    de: 'DER MOLDAVIT',
    en: 'THE MOLDAVITE',
  },
  gemAquamarine: {
    es: 'LA AGUAMARINA',
    de: 'DER AQUAMARIN',
    en: 'THE AQUAMARINE',
  },
  gemRuby: {
    es: 'EL RUBÍ',
    de: 'DER RUBIN',
    en: 'THE RUBY',
  },
  gemSapphire: {
    es: 'EL ZAFIRO',
    de: 'DER SAPHIR',
    en: 'THE SAPPHIRE',
  },
  gemNorth: {
    es: '↑\n{GEM} ESTÁ AL NORTE',
    de: '↑\n{GEM} IST IM NORDEN',
    en: '↑\n{GEM} IS NORTH',
  },
  gemNorthEast: {
    es: '↗\n{GEM} ESTÁ AL NORESTE',
    de: '↗\n{GEM} IST IM NORDOSTEN',
    en: '↗\n{GEM} IS NORTH-EAST',
  },
  gemEast: {
    es: '{GEM} ESTÁ AL ESTE\n→',
    de: '{GEM} IST IM OSTEN\n→',
    en: '{GEM} IS EAST\n→',
  },
  gemSouthEast: {
    es: '{GEM} ESTÁ AL SUDESTE\n↙',
    de: '{GEM} IST IM SÜDOSTEN\n↙',
    en: '{GEM} IS SOUTH-EAST\n↙',
  },
  gemSouth: {
    es: '↓\n{GEM} ESTÁ AL SUR',
    de: '↓\n{GEM} IST IM SÜDEN',
    en: '↓\n{GEM} IS SOUTH',
  },
  gemSouthWest: {
    es: '{GEM} ESTÁ AL SUROESTE\n↘',
    de: '{GEM} IST IM SÜDWESTEN\n↘',
    en: '{GEM} IS SOUTH-WEST\n↘',
  },
  gemWest: {
    es: '{GEM} ESTÁ AL OESTE\n←',
    de: '{GEM} IST IM WESTEN\n←',
    en: '{GEM} IS WEST\n←',
  },
  gemNorthWest: {
    es: '↖\n{GEM} ESTÁ AL NOROESTE',
    de: '↖\n{GEM} IST IM NORWESTEN',
    en: '↖\n{GEM} IS NORTH-WEST',
  },
};

export function t(key: StringKey): string {
  return STRINGS[key][current];
}
