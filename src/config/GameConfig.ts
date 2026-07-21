import Phaser from 'phaser';
import { getGameSize } from '@/utils/platform';
import { BootScene } from '@/scenes/BootScene';
import { PreloadScene } from '@/scenes/PreloadScene';
import { MainMenuScene } from '@/scenes/MainMenuScene';
import { HuntScene } from '@/hunt/HuntScene';

const { width, height } = getGameSize();

export const gameConfig: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: 'app',
  width,
  height,
  pixelArt: true,
  backgroundColor: '#5fb7e8',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 },
      debug: false,
    },
  },
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.NO_CENTER,
  },
  scene: [BootScene, PreloadScene, MainMenuScene, HuntScene],
};
