// Static reachability / sanity check for the hand-authored level data. Not a runtime test — it
// re-implements the jump reach from the physics constants and walks the platform graph, then flags
// unreachable platforms, un-crossable pits, floating enemies/collectibles, and boss placement.
//   node scripts/validate_levels.mjs
import fs from 'fs';
import path from 'path';

const DEFAULT = { g: 1400, jv: 620, run: 280 };
const AERIAL = new Set(['spinner', 'flyer', 'faller']); // don't need a floor under them

function apex(p) { return (p.jv * p.jv) / (2 * p.g); }
// Max horizontal distance a jump can cover to land on a surface `rise` px higher than the start.
function maxHoriz(p, rise) {
  if (rise <= 0) return p.run * (2 * p.jv) / p.g + p.run * Math.sqrt((2 * -rise) / p.g) + 40; // dropping: generous
  const disc = p.jv * p.jv - 2 * p.g * rise;
  if (disc < 0) return -1; // can't rise that high at all
  return p.run * (p.jv + Math.sqrt(disc)) / p.g;
}

function loadLevel(file) {
  const text = fs.readFileSync(file, 'utf8');
  const start = text.indexOf('{', text.indexOf('= '));
  let depth = 0, end = -1;
  for (let i = start; i < text.length; i++) {
    if (text[i] === '{') depth++;
    else if (text[i] === '}') { depth--; if (depth === 0) { end = i; break; } }
  }
  const obj = text.slice(start, end + 1);
  return new Function('return (' + obj + ')')();
}

function seg(pl) { return { x1: pl.x, x2: pl.x + pl.width, y: pl.y, ground: pl.height >= 64 }; }
function horizGap(a, b) {
  if (a.x2 >= b.x1 && b.x2 >= a.x1) return 0; // overlap
  return a.x2 < b.x1 ? b.x1 - a.x2 : a.x1 - b.x2;
}

function validate(level) {
  const p = level.physics ? { g: level.physics.gravityY, jv: level.physics.jumpVelocity, run: DEFAULT.run } : DEFAULT;
  const A = apex(p);
  const segs = level.platforms.map(seg);
  const issues = [];

  // reachability BFS from the spawn platform
  const spawnSeg = segs.find((s) => s.ground && s.x1 <= level.playerSpawn.x && level.playerSpawn.x <= s.x2);
  if (!spawnSeg) issues.push(`spawn x=${level.playerSpawn.x} is not over any ground platform`);
  const reach = new Set();
  const queue = [];
  if (spawnSeg) { reach.add(spawnSeg); queue.push(spawnSeg); }
  while (queue.length) {
    const a = queue.shift();
    for (const b of segs) {
      if (reach.has(b)) continue;
      const rise = a.y - b.y; // b higher if positive
      if (rise > A + 1) continue; // can't rise that high
      const gap = horizGap(a, b);
      if (gap <= maxHoriz(p, rise) + 1) { reach.add(b); queue.push(b); }
    }
  }
  for (const s of segs) {
    if (!reach.has(s)) issues.push(`UNREACHABLE platform [${s.x1}-${s.x2}] @${s.y}`);
  }

  // boss on a reachable ground platform inside its arena
  const bs = level.miniBossSpawn;
  if (bs) {
    const bseg = segs.find((s) => s.ground && s.x1 <= bs.x && bs.x <= s.x2);
    if (!bseg) issues.push(`boss x=${bs.x} not on a ground platform`);
    else if (!reach.has(bseg)) issues.push(`boss platform not reachable`);
    if (bs.x < bs.arenaLeft || bs.x > bs.arenaRight) issues.push(`boss x outside arena`);
  }

  // floating enemies (non-aerial must stand on a platform)
  for (const e of level.enemySpawns) {
    if (AERIAL.has(e.type)) continue;
    const on = segs.find((s) => s.x1 - 8 <= e.x && e.x <= s.x2 + 8 && s.y >= e.y - 4 && s.y <= e.y + 90);
    if (!on) issues.push(`FLOATING ${e.type} @(${e.x},${e.y}) — no platform beneath`);
  }

  // collectibles grabbable (on/above a surface within jump reach)
  for (const c of level.collectibleSpawns) {
    const ok = segs.some((s) => c.x >= s.x1 - 70 && c.x <= s.x2 + 70 && s.y - c.y >= -12 && s.y - c.y <= A + 60);
    if (!ok) issues.push(`UNREACHABLE ${c.type} @(${c.x},${c.y})`);
  }
  return { apex: Math.round(A), maxFlat: Math.round(maxHoriz(p, 0)), issues };
}

const files = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6'];
let total = 0;
for (const f of files) {
  const level = loadLevel(path.join('src/config', f + '.ts'));
  const r = validate(level);
  total += r.issues.length;
  console.log(`\n=== ${f} (${level.theme})  apex=${r.apex}px  flatReach=${r.maxFlat}px ===`);
  if (r.issues.length === 0) console.log('  OK — all platforms reachable, no floating entities, boss placed.');
  else r.issues.forEach((i) => console.log('  ⚠ ' + i));
}
console.log(`\n${total === 0 ? '✅ ALL LEVELS PASS' : '❌ ' + total + ' issue(s)'}`);
