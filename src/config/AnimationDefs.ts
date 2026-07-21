import Phaser from 'phaser';

export function registerPlayerAnimations(scene: Phaser.Scene): void {
  const anims = scene.anims;
  if (anims.exists('player-idle')) return;

  anims.create({
    key: 'player-idle',
    frames: [{ key: 'player-idle-0' }, { key: 'player-idle-1' }],
    frameRate: 3,
    repeat: -1,
  });

  anims.create({
    key: 'player-walk',
    frames: [{ key: 'player-walk-0' }, { key: 'player-walk-1' }],
    frameRate: 8,
    repeat: -1,
  });

  // Extra playable characters — same idle/walk cadence, different skins.
  for (const id of ['ranger', 'plantgirl']) {
    anims.create({
      key: `${id}-idle`,
      frames: [{ key: `${id}-idle-0` }, { key: `${id}-idle-1` }],
      frameRate: 3,
      repeat: -1,
    });
    anims.create({
      key: `${id}-walk`,
      frames: [{ key: `${id}-walk-0` }, { key: `${id}-walk-1` }],
      frameRate: 8,
      repeat: -1,
    });
  }
}

export function registerEnemyAnimations(scene: Phaser.Scene): void {
  const anims = scene.anims;
  if (anims.exists('mushroom-walk')) return;

  anims.create({
    key: 'mushroom-walk',
    frames: [{ key: 'mushroom-0' }, { key: 'mushroom-1' }],
    frameRate: 4,
    repeat: -1,
  });

  // Desert walker (barrel-cactus roller) — same cadence, desert skin.
  anims.create({
    key: 'barrel-walk',
    frames: [{ key: 'barrel-0' }, { key: 'barrel-1' }],
    frameRate: 4,
    repeat: -1,
  });

  // Underwater walker (drifting algae clump) — same cadence, algae skin.
  anims.create({
    key: 'algae-walk',
    frames: [{ key: 'algae-crawl-0' }, { key: 'algae-crawl-1' }],
    frameRate: 4,
    repeat: -1,
  });

  // Flyer (darting fish) tail-flap.
  anims.create({
    key: 'fish-swim',
    frames: [{ key: 'fish-0' }, { key: 'fish-1' }],
    frameRate: 6,
    repeat: -1,
  });

  // Cave walker (crawling moss clump).
  anims.create({
    key: 'moss-walk',
    frames: [{ key: 'moss-crawl-0' }, { key: 'moss-crawl-1' }],
    frameRate: 4,
    repeat: -1,
  });

  // Swamp walker (bog crawler).
  anims.create({
    key: 'bog-walk',
    frames: [{ key: 'bog-crawl-0' }, { key: 'bog-crawl-1' }],
    frameRate: 4,
    repeat: -1,
  });

  // Swamp flyer (dragonfly) wing-beat.
  anims.create({
    key: 'dragon-fly',
    frames: [{ key: 'dragon-0' }, { key: 'dragon-1' }],
    frameRate: 10,
    repeat: -1,
  });

  // Space walker (sprout drifting in a glass bubble).
  anims.create({
    key: 'orbling-float',
    frames: [{ key: 'orbling-0' }, { key: 'orbling-1' }],
    frameRate: 3,
    repeat: -1,
  });

  // Beach walker (rolling coconut).
  anims.create({
    key: 'coco-roll',
    frames: [{ key: 'coco-0' }, { key: 'coco-1' }],
    frameRate: 5,
    repeat: -1,
  });

  // Mountain walker (rolling pinecone).
  anims.create({
    key: 'pinecone-roll',
    frames: [{ key: 'pinecone-0' }, { key: 'pinecone-1' }],
    frameRate: 5,
    repeat: -1,
  });

  // House walker (toddling potted plant).
  anims.create({
    key: 'pot-walk',
    frames: [{ key: 'pot-crawler-0' }, { key: 'pot-crawler-1' }],
    frameRate: 4,
    repeat: -1,
  });
}
