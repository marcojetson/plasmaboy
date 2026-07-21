import Phaser from 'phaser';
import { AudioManager } from '@/audio/AudioManager';
import { t } from '@/i18n/i18n';
import { themeOf } from '@/config/SubLevels';
import {
  CHARACTERS, CHARACTER_ORDER, type CharacterId, loadCharacter, saveCharacter,
} from '@/config/Characters';

const EXPERT_KEY = 'plasma-boy-expert-mode';
const SELECTED_SCALE = 2.9;
const UNSELECTED_SCALE = 2.4;

interface Card {
  id: CharacterId;
  ring: Phaser.GameObjects.Rectangle;
  sprite: Phaser.GameObjects.Image;
  name: Phaser.GameObjects.Text;
  zone: Phaser.GameObjects.Rectangle;
}

export class MainMenuScene extends Phaser.Scene {
  private defaultLevel = 0;
  private winMode = false;
  private kidsMode = true;
  private selected: CharacterId = 'plasmaboy';

  private title!: Phaser.GameObjects.Text;
  private subtitle!: Phaser.GameObjects.Text;
  private heroPrompt!: Phaser.GameObjects.Text;
  private cards: Card[] = [];
  private expertBox!: Phaser.GameObjects.Rectangle;
  private expertCheck!: Phaser.GameObjects.Text;
  private expertLabel!: Phaser.GameObjects.Text;
  private expertZone!: Phaser.GameObjects.Rectangle;
  private playBg!: Phaser.GameObjects.Rectangle;
  private playLabel!: Phaser.GameObjects.Text;

  constructor() {
    super('MainMenu');
  }

  create(): void {
    AudioManager.instance.unlock();
    this.cameras.main.setBackgroundColor('#2d6a4f');

    const params = new URLSearchParams(window.location.search);
    const urlLevel = Number.parseInt(params.get('level') ?? '', 10);
    if (Number.isFinite(urlLevel) && urlLevel >= 1) {
      this.defaultLevel = urlLevel - 1;
    }
    this.winMode = params.has('win');
    this.kidsMode = localStorage.getItem(EXPERT_KEY) !== 'true';
    this.selected = loadCharacter();

    this.title = this.add.text(0, 0, 'PLASMA BOY', {
      fontFamily: 'monospace', fontSize: '46px', color: '#ffd54f', stroke: '#000000', strokeThickness: 7,
    }).setOrigin(0.5);

    this.subtitle = this.add.text(0, 0, t('vsPlantas'), {
      fontFamily: 'monospace', fontSize: '20px', color: '#7ed957', stroke: '#000000', strokeThickness: 5,
    }).setOrigin(0.5);

    this.heroPrompt = this.add.text(0, 0, t('chooseHero'), {
      fontFamily: 'monospace', fontSize: '18px', fontStyle: 'bold', color: '#ffffff', stroke: '#000000', strokeThickness: 4,
    }).setOrigin(0.5);

    // Character cards — tapping a card only SELECTS it; the PLAY button starts the game.
    this.cards = CHARACTER_ORDER.map((id) => {
      const def = CHARACTERS[id];
      const ring = this.add.rectangle(0, 0, 92, 128, 0xffd54f, 0.14)
        .setStrokeStyle(4, 0xffd54f)
        .setVisible(id === this.selected);
      const sprite = this.add.image(0, 0, def.idleFrame).setScale(id === this.selected ? SELECTED_SCALE : UNSELECTED_SCALE);
      const name = this.add.text(0, 0, t(def.nameKey), {
        fontFamily: 'monospace', fontSize: '13px', color: '#e0f5e9', stroke: '#000', strokeThickness: 3,
      }).setOrigin(0.5);
      const zone = this.add.rectangle(0, 0, 104, 168, 0xffffff, 0.001).setInteractive({ useHandCursor: true });
      zone.on('pointerover', () => sprite.setScale(this.baseScale(id) + 0.25));
      zone.on('pointerout', () => sprite.setScale(this.baseScale(id)));
      zone.on('pointerup', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
        ev.stopPropagation();
        this.select(id);
      });
      this.tweens.add({ targets: sprite, y: '-=4', duration: 1100, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      return { id, ring, sprite, name, zone };
    });

    // Expert-mode toggle. The box + label are visuals; one wide invisible zone over the whole
    // row is the tap target, so the checkbox is easy to hit on mobile (not just the tiny box).
    this.expertBox = this.add.rectangle(0, 0, 22, 22, 0x000000, 0).setStrokeStyle(2, 0xffffff);
    this.expertCheck = this.add.text(0, 0, this.kidsMode ? '' : '✓', {
      fontFamily: 'monospace', fontSize: '18px', color: '#ff6666',
    }).setOrigin(0.5);
    this.expertLabel = this.add.text(0, 0, t('expertMode'), {
      fontFamily: 'monospace', fontSize: '16px', color: '#ffffff',
    }).setOrigin(0, 0.5);
    this.expertZone = this.add.rectangle(0, 0, 220, 46, 0xffffff, 0.001).setInteractive({ useHandCursor: true });
    this.expertZone.on('pointerup', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      this.kidsMode = !this.kidsMode;
      localStorage.setItem(EXPERT_KEY, String(!this.kidsMode));
      this.expertCheck.setText(this.kidsMode ? '' : '✓');
    });

    // PLAY button — the single, explicit "start" action.
    this.playBg = this.add.rectangle(0, 0, 200, 60, 0xffd54f)
      .setStrokeStyle(4, 0x1b3a2a)
      .setInteractive({ useHandCursor: true });
    this.playLabel = this.add.text(0, 0, t('play'), {
      fontFamily: 'monospace', fontSize: '28px', fontStyle: 'bold', color: '#1b3a2a',
    }).setOrigin(0.5);
    this.playBg.on('pointerup', (_p: Phaser.Input.Pointer, _x: number, _y: number, ev: Phaser.Types.Input.EventData) => {
      ev.stopPropagation();
      this.startGame(this.defaultLevel, this.selected);
    });
    this.tweens.add({ targets: [this.playBg, this.playLabel], scale: 1.06, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });

    this.layout();
    this.scale.on('resize', this.layout, this);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => this.scale.off('resize', this.layout, this));
  }

  private baseScale(id: CharacterId): number {
    return id === this.selected ? SELECTED_SCALE : UNSELECTED_SCALE;
  }

  private layout(): void {
    const cx = this.scale.width / 2;
    const h = this.scale.height;

    this.title.setPosition(cx, h * 0.11);
    this.subtitle.setPosition(cx, h * 0.17);
    this.heroPrompt.setPosition(cx, h * 0.26);

    const gap = Math.min(this.scale.width * 0.29, 132);
    const cardY = h * 0.42;
    this.cards.forEach((card, i) => {
      const x = cx + (i - 1) * gap;
      card.ring.setPosition(x, cardY);
      card.sprite.setPosition(x, cardY);
      card.name.setPosition(x, cardY + 78);
      card.zone.setPosition(x, cardY + 8);
    });

    const expertY = h * 0.65;
    this.expertBox.setPosition(cx - 62, expertY);
    this.expertCheck.setPosition(cx - 62, expertY);
    this.expertLabel.setPosition(cx - 44, expertY);
    this.expertZone.setPosition(cx, expertY); // wide tap target over the whole box+label row

    this.playBg.setPosition(cx, h * 0.82);
    this.playLabel.setPosition(cx, h * 0.82);
  }

  private select(id: CharacterId): void {
    if (this.selected === id) return;
    this.selected = id;
    saveCharacter(id);
    AudioManager.instance.play('pickup');
    this.cards.forEach((c) => {
      c.ring.setVisible(c.id === id);
      c.sprite.setScale(this.baseScale(c.id));
    });
  }

  private startGame(levelIndex = 0, character: CharacterId = this.selected): void {
    AudioManager.instance.startMusic();
    this.scene.start('Hunt', {
      levelIndex,
      theme: themeOf(levelIndex),
      win: this.winMode,
      kidsMode: this.kidsMode,
      character,
    });
  }
}
