import Phaser from 'phaser';

export const EventBus = new Phaser.Events.EventEmitter();

export const GameEvents = {
  PlayerHealthChanged: 'player-health-changed',
  PlayerDied: 'player-died',
} as const;

export interface PlayerHealthChangedPayload {
  health: number;
  maxHealth: number;
}
