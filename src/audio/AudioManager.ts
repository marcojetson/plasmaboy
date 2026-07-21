// Fully procedural audio via the Web Audio API — no audio files. Produces a looping
// John-Carpenter-style synth-horror ostinato (that "70s Halloween movie" vibe: minor-key
// detuned-saw arpeggio over a low pulsing drone) plus short synthesized sound effects.
//
// Browsers start an AudioContext suspended until a user gesture; we attach one-time
// window listeners that resume it on the first key/pointer interaction.

type SfxName =
  | 'shootPlasma'
  | 'shootShoulder'
  | 'katana'
  | 'explosion'
  | 'hit'
  | 'pickup'
  | 'bossPhase'
  | 'bubble'
  | 'gem';

/** Per-biome music flavor. Each has its own track (tempo, timbre, patterns). */
export type MusicMood =
  | 'default' | 'desert' | 'water' | 'cave' | 'swamp' | 'museum'
  | 'space' | 'beach' | 'mountain' | 'house';

const A = 440;
/** Equal-temperament note frequency by name, e.g. note('E', 2). */
function note(name: string, octave: number): number {
  const semis: Record<string, number> = {
    C: -9, 'C#': -8, D: -7, 'D#': -6, E: -5, F: -4,
    'F#': -3, G: -2, 'G#': -1, A: 0, 'A#': 1, B: 2,
  };
  const n = (semis[name] ?? 0) + (octave - 4) * 12;
  return A * Math.pow(2, n / 12);
}

// ---- Tracks -------------------------------------------------------------------------------
// Each biome gets its own looping track (tempo, timbre, patterns) rather than one theme with
// tweaks. A track is a set of voices; each voice is a per-step note pattern + a synth timbre.
// durMul/releaseMul are multiples of one step's duration.
interface VoiceOpts {
  type: OscillatorType;
  detune?: number;
  filterHz?: number;
  q?: number;
  attack?: number;
  peak?: number;
  durMul?: number;
  releaseMul?: number;
  vibrato?: number;
}
interface Voice {
  pattern: (number | null)[]; // freq per step; null = rest
  opts: VoiceOpts;
}
interface Track {
  bpm: number;
  steps: number;
  voices: Voice[];
  echoWet: number; // delay/echo send level
  bubbles?: boolean; // underwater bubble layer
}

const _ = null; // rest, for readable patterns

// Forest: the original tense E-minor detuned-saw ostinato.
const T_DEFAULT: Track = {
  bpm: 104,
  steps: 16,
  echoWet: 0,
  voices: [
    {
      pattern: [
        note('E', 3), note('B', 3), note('E', 4), note('B', 3),
        note('E', 3), note('C', 4), note('E', 4), note('C', 4),
        note('E', 3), note('B', 3), note('E', 4), note('G', 4),
        note('E', 3), note('C', 4), note('E', 4), note('D', 4),
      ],
      opts: { type: 'sawtooth', detune: 8, filterHz: 1400, q: 6, attack: 0.004, peak: 0.5, durMul: 0.9, releaseMul: 0.7 },
    },
    {
      pattern: [note('E', 2), _, _, _, note('E', 2), _, _, _, note('C', 2), _, _, _, note('C', 2), _, _, _],
      opts: { type: 'sawtooth', detune: 4, filterHz: 320, q: 2, attack: 0.02, peak: 0.9, durMul: 3.6, releaseMul: 2 },
    },
    {
      pattern: [_, _, note('B', 4), _, _, _, _, _, _, _, _, _, _, _, _, _],
      opts: { type: 'triangle', filterHz: 3000, q: 1, attack: 0.05, peak: 0.35, durMul: 5, releaseMul: 3, vibrato: 5 },
    },
  ],
};

// Desert: hotter and exotic — an E Phrygian-dominant arp (the b2/major-3 give that Spanish/
// Middle-Eastern "sun-scorched" flavor), driving a touch faster over an E→bVI pedal.
const T_DESERT: Track = {
  bpm: 116,
  steps: 16,
  echoWet: 0,
  voices: [
    {
      pattern: [
        note('E', 4), note('F', 4), note('G#', 4), note('F', 4),
        note('E', 4), note('B', 4), note('A', 4), note('G#', 4),
        note('E', 4), note('F', 4), note('G#', 4), note('A', 4),
        note('B', 4), note('A', 4), note('G#', 4), note('F', 4),
      ],
      opts: { type: 'sawtooth', detune: 9, filterHz: 1650, q: 5, attack: 0.004, peak: 0.46, durMul: 0.88, releaseMul: 0.55 },
    },
    {
      pattern: [note('E', 2), _, _, _, note('E', 2), _, _, _, note('C', 2), _, _, _, note('C', 2), _, _, _],
      opts: { type: 'sawtooth', detune: 4, filterHz: 340, q: 2, attack: 0.02, peak: 0.85, durMul: 3.6, releaseMul: 2 },
    },
    {
      pattern: [_, _, _, _, _, _, note('G#', 5), _, _, _, _, _, _, _, note('B', 5), _],
      opts: { type: 'triangle', filterHz: 2800, q: 1, attack: 0.05, peak: 0.3, durMul: 4, releaseMul: 3, vibrato: 7 },
    },
  ],
};

// Water: calm, bright A-major-pentatonic arpeggio in soft triangles, a low sine pad, a high
// shimmer, gentle echo — plus the bubble layer. Reads clearly "underwater / peaceful".
const T_WATER: Track = {
  bpm: 92,
  steps: 16,
  echoWet: 0.22,
  bubbles: true,
  voices: [
    {
      pattern: [
        note('A', 4), note('C#', 5), note('E', 5), note('F#', 5),
        note('E', 5), note('C#', 5), note('B', 4), note('D', 5),
        note('A', 4), note('C#', 5), note('E', 5), note('F#', 5),
        note('E', 5), note('D', 5), note('C#', 5), note('B', 4),
      ],
      opts: { type: 'triangle', detune: 3, filterHz: 2600, q: 1, attack: 0.02, peak: 0.3, durMul: 1.1, releaseMul: 1.1 },
    },
    {
      pattern: [note('A', 2), _, _, _, _, _, _, _, note('E', 2), _, _, _, _, _, _, _],
      opts: { type: 'sine', filterHz: 400, q: 0.7, attack: 0.06, peak: 0.5, durMul: 7.5, releaseMul: 4 },
    },
    {
      pattern: [_, _, _, _, _, _, note('A', 5), _, _, _, _, _, _, _, note('E', 5), _],
      opts: { type: 'triangle', filterHz: 4200, q: 1, attack: 0.04, peak: 0.18, durMul: 3, releaseMul: 3, vibrato: 6 },
    },
  ],
};

// Cave: slow, sparse and dark — a low sustained drone with a soft mid pad and rare eerie pings
// that ring out through a heavy echo. Genuinely different from the ostinato (not a slowdown).
const T_CAVE: Track = {
  bpm: 66,
  steps: 16,
  echoWet: 0.5,
  voices: [
    {
      pattern: [note('E', 2), _, _, _, _, _, _, _, note('C', 2), _, _, _, _, _, _, _],
      opts: { type: 'sawtooth', detune: 5, filterHz: 220, q: 1.5, attack: 0.12, peak: 0.7, durMul: 7.6, releaseMul: 5 },
    },
    {
      pattern: [_, _, _, _, note('G', 3), _, _, _, _, _, _, _, note('B', 3), _, _, _],
      opts: { type: 'triangle', filterHz: 900, q: 1, attack: 0.2, peak: 0.22, durMul: 5, releaseMul: 4 },
    },
    {
      pattern: [_, _, note('B', 4), _, _, _, _, _, _, _, _, note('E', 5), _, _, _, _],
      opts: { type: 'triangle', filterHz: 2600, q: 1, attack: 0.03, peak: 0.26, durMul: 4, releaseMul: 4, vibrato: 4 },
    },
  ],
};

// Swamp: murky, mid-tempo E-minor blues (with the flat-5 for unease), squelchy square lead over
// a plodding bass.
const T_SWAMP: Track = {
  bpm: 84,
  steps: 16,
  echoWet: 0.16,
  voices: [
    {
      pattern: [
        note('E', 3), note('G', 3), note('A', 3), note('A#', 3),
        note('B', 3), note('A', 3), note('G', 3), note('E', 3),
        note('E', 3), note('G', 3), note('A#', 3), note('B', 3),
        note('D', 4), note('B', 3), note('A', 3), note('G', 3),
      ],
      opts: { type: 'square', detune: 5, filterHz: 820, q: 5, attack: 0.006, peak: 0.32, durMul: 0.85, releaseMul: 0.6 },
    },
    {
      pattern: [note('E', 2), _, _, _, note('A', 2), _, _, _, note('E', 2), _, _, _, note('B', 2), _, _, _],
      opts: { type: 'sawtooth', detune: 4, filterHz: 260, q: 2, attack: 0.02, peak: 0.85, durMul: 3.4, releaseMul: 2 },
    },
    {
      pattern: [_, _, _, _, _, _, note('D', 4), _, _, _, _, _, _, _, _, _],
      opts: { type: 'triangle', filterHz: 2000, q: 1, attack: 0.04, peak: 0.22, durMul: 4, releaseMul: 3, vibrato: 5 },
    },
  ],
};

// Museum: hushed and minimalist — you have to be quiet in a museum. A slow, elegant music-box
// melody (Am arpeggio, Satie-ish) over a barely-there breathing pad and one careful high chime,
// all soaked in the echo of a big stone gallery. Lots of silence between the notes.
const T_MUSEUM: Track = {
  bpm: 60,
  steps: 16,
  echoWet: 0.2,
  voices: [
    {
      pattern: [note('A', 4), _, _, _, _, note('C', 5), _, _, note('E', 5), _, _, _, note('D', 5), _, _, _],
      opts: { type: 'triangle', filterHz: 2600, q: 1, attack: 0.04, peak: 0.32, durMul: 3, releaseMul: 3, vibrato: 3 },
    },
    {
      pattern: [note('A', 2), _, _, _, _, _, _, _, note('F', 2), _, _, _, _, _, _, _],
      opts: { type: 'sine', filterHz: 480, q: 1, attack: 0.3, peak: 0.42, durMul: 7, releaseMul: 4 },
    },
    {
      pattern: [_, _, _, _, _, _, _, _, _, _, _, _, _, _, note('E', 6), _],
      opts: { type: 'triangle', filterHz: 3200, q: 1, attack: 0.02, peak: 0.2, durMul: 4, releaseMul: 5, vibrato: 4 },
    },
  ],
};

// Space: weightless and wondrous — a slow A-major-pentatonic bell arpeggio drifting over a deep
// sine drone and a distant high shimmer, drenched in echo. Reads clearly "floating in a starry void".
const T_SPACE: Track = {
  bpm: 72,
  steps: 16,
  echoWet: 0.42,
  voices: [
    {
      pattern: [note('A', 4), _, _, _, note('E', 5), _, _, note('C#', 5), _, _, _, note('F#', 5), _, _, note('B', 4), _],
      opts: { type: 'triangle', detune: 3, filterHz: 2800, q: 1, attack: 0.05, peak: 0.28, durMul: 2.6, releaseMul: 3, vibrato: 4 },
    },
    {
      pattern: [note('A', 2), _, _, _, _, _, _, _, note('E', 2), _, _, _, _, _, _, _],
      opts: { type: 'sine', filterHz: 380, q: 0.7, attack: 0.3, peak: 0.5, durMul: 7.6, releaseMul: 4 },
    },
    {
      pattern: [_, _, _, _, _, _, note('E', 6), _, _, _, _, _, _, _, note('A', 6), _],
      opts: { type: 'triangle', filterHz: 4200, q: 1, attack: 0.05, peak: 0.16, durMul: 3, releaseMul: 4, vibrato: 6 },
    },
  ],
};

// Beach: bright and sunny — a bouncy C-major-pentatonic triangle melody over a happy I–V–vi–IV
// bass, with a high plucked sparkle. Warm and carefree.
const T_BEACH: Track = {
  bpm: 100,
  steps: 16,
  echoWet: 0.14,
  voices: [
    {
      pattern: [
        note('C', 5), note('E', 5), note('G', 5), note('E', 5),
        note('A', 5), note('G', 5), note('E', 5), note('D', 5),
        note('C', 5), note('E', 5), note('G', 5), note('A', 5),
        note('G', 5), note('E', 5), note('D', 5), note('C', 5),
      ],
      opts: { type: 'triangle', detune: 3, filterHz: 2800, q: 1, attack: 0.02, peak: 0.3, durMul: 1.0, releaseMul: 1.0 },
    },
    {
      pattern: [note('C', 3), _, _, _, note('G', 2), _, _, _, note('A', 2), _, _, _, note('F', 2), _, _, _],
      opts: { type: 'sine', filterHz: 440, q: 0.8, attack: 0.05, peak: 0.5, durMul: 3.6, releaseMul: 3 },
    },
    {
      pattern: [_, _, note('G', 5), _, _, _, _, _, _, _, note('C', 6), _, _, _, _, _],
      opts: { type: 'triangle', filterHz: 3600, q: 1, attack: 0.02, peak: 0.2, durMul: 2.5, releaseMul: 3, vibrato: 4 },
    },
  ],
};

// Mountain: noble and airy — a slow horn-like triangle melody over an open-fifth drone with a
// high wind shimmer and a long alpine echo. Wide and majestic.
const T_MOUNTAIN: Track = {
  bpm: 76,
  steps: 16,
  echoWet: 0.32,
  voices: [
    {
      pattern: [note('D', 4), _, _, note('A', 4), _, _, note('D', 5), _, _, note('C', 5), _, note('A', 4), _, _, note('G', 4), _],
      opts: { type: 'triangle', detune: 4, filterHz: 1800, q: 1, attack: 0.06, peak: 0.34, durMul: 1.8, releaseMul: 2, vibrato: 3 },
    },
    {
      pattern: [note('D', 2), _, _, _, _, _, _, _, note('A', 2), _, _, _, _, _, _, _],
      opts: { type: 'sawtooth', detune: 5, filterHz: 280, q: 1.5, attack: 0.12, peak: 0.6, durMul: 7.6, releaseMul: 5 },
    },
    {
      pattern: [_, _, _, _, note('A', 5), _, _, _, _, _, _, _, note('D', 6), _, _, _],
      opts: { type: 'triangle', filterHz: 3800, q: 1, attack: 0.06, peak: 0.18, durMul: 3, releaseMul: 4, vibrato: 5 },
    },
  ],
};

// House: cozy and playful — a gentle C-major music-box melody over a warm I–vi–IV–V bass and a
// soft low pad. Homey, like a lullaby in a lamp-lit room.
const T_HOUSE: Track = {
  bpm: 88,
  steps: 16,
  echoWet: 0.12,
  voices: [
    {
      pattern: [note('E', 5), _, note('G', 5), _, note('C', 6), _, note('G', 5), _, note('A', 5), _, note('G', 5), _, note('E', 5), _, note('D', 5), _],
      opts: { type: 'triangle', filterHz: 3000, q: 1, attack: 0.02, peak: 0.3, durMul: 1.4, releaseMul: 2.5, vibrato: 3 },
    },
    {
      pattern: [note('C', 3), _, _, _, note('A', 2), _, _, _, note('F', 2), _, _, _, note('G', 2), _, _, _],
      opts: { type: 'sine', filterHz: 460, q: 0.8, attack: 0.05, peak: 0.46, durMul: 3.6, releaseMul: 3 },
    },
    {
      pattern: [note('C', 4), _, _, _, _, _, _, _, note('E', 4), _, _, _, _, _, _, _],
      opts: { type: 'triangle', filterHz: 1200, q: 1, attack: 0.2, peak: 0.2, durMul: 5, releaseMul: 4 },
    },
  ],
};

const TRACKS: Record<MusicMood, Track> = {
  default: T_DEFAULT,
  desert: T_DESERT,
  water: T_WATER,
  cave: T_CAVE,
  swamp: T_SWAMP,
  museum: T_MUSEUM,
  space: T_SPACE,
  beach: T_BEACH,
  mountain: T_MOUNTAIN,
  house: T_HOUSE,
};

export class AudioManager {
  private static _instance: AudioManager | null = null;
  static get instance(): AudioManager {
    if (!this._instance) this._instance = new AudioManager();
    return this._instance;
  }

  private ctx: AudioContext | null = null;
  private musicGain: GainNode | null = null;
  private sfxGain: GainNode | null = null;
  private echoSend: GainNode | null = null; // dry-path send into the delay/echo bus
  private noiseBuffer: AudioBuffer | null = null;

  private nextNoteTime = 0;
  private step = 0;
  private musicPlaying = false;
  private muted = false;

  private bpm = 104;
  private mood: MusicMood = 'default';
  private track: Track = T_DEFAULT;
  private readonly stepsPerBeat = 2; // eighth notes
  private schedulerInterval: ReturnType<typeof setInterval> | null = null;

  private constructor() {
    const resume = () => this.unlock();
    if (typeof window !== 'undefined') {
      window.addEventListener('pointerdown', resume);
      window.addEventListener('keydown', resume);
      window.addEventListener('touchstart', resume);
    }
    // Never let audio keep playing in a backgrounded/hidden tab — suspend when the page is
    // hidden, resume when it's visible again. This is what stops "the music won't stop"
    // when someone tabs away instead of closing the game.
    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', () => {
        if (!this.ctx) return;
        if (document.hidden) void this.ctx.suspend();
        else if (!this.muted) void this.ctx.resume();
      });
    }
  }

  /** Lazily create + resume the context. Safe to call repeatedly / from any gesture. */
  unlock(): void {
    if (!this.ctx) {
      const Ctor = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!Ctor) return;
      this.ctx = new Ctor();

      this.musicGain = this.ctx.createGain();
      this.musicGain.gain.value = 0.16;
      this.musicGain.connect(this.ctx.destination);

      this.sfxGain = this.ctx.createGain();
      this.sfxGain.gain.value = 0.5;
      this.sfxGain.connect(this.ctx.destination);

      // Echo/delay bus for moody biomes. Music always plays dry (musicGain -> destination);
      // when echoSend is opened, a delayed, darkened, self-feeding copy is mixed in on top.
      const delay = this.ctx.createDelay(1.0);
      delay.delayTime.value = 0.3;
      const feedback = this.ctx.createGain();
      feedback.gain.value = 0.34;
      const echoLP = this.ctx.createBiquadFilter();
      echoLP.type = 'lowpass';
      echoLP.frequency.value = 1600;
      this.echoSend = this.ctx.createGain();
      this.echoSend.gain.value = this.track.echoWet;
      this.musicGain.connect(this.echoSend);
      this.echoSend.connect(delay);
      delay.connect(echoLP);
      echoLP.connect(feedback);
      feedback.connect(delay); // feedback loop → repeating echoes
      echoLP.connect(this.ctx.destination); // wet output

      this.noiseBuffer = this.makeNoiseBuffer();
    }
    if (this.ctx.state === 'suspended') void this.ctx.resume();
  }

  /** Switch to the biome's track (called on each level load). Restarts the pattern cleanly so
   * the new tempo/timbre begins on a boundary rather than warping mid-loop. */
  setMood(mood: MusicMood): void {
    if (mood === this.mood) return; // e.g. forest→desert both use 'default' — keep it seamless
    this.mood = mood;
    this.track = TRACKS[mood];
    this.bpm = this.track.bpm;
    if (this.echoSend && this.ctx) {
      this.echoSend.gain.setTargetAtTime(this.track.echoWet, this.ctx.currentTime, 0.2);
    }
    if (this.musicPlaying && this.ctx) {
      this.step = 0;
      this.nextNoteTime = this.ctx.currentTime + 0.1;
    }
  }

  toggleMute(): boolean {
    this.muted = !this.muted;
    this.applyMusicGain();
    if (this.sfxGain) this.sfxGain.gain.value = this.muted ? 0 : 0.5;
    return this.muted;
  }

  private applyMusicGain(): void {
    if (!this.musicGain) return;
    const target = this.muted ? 0 : 0.16;
    if (this.ctx) this.musicGain.gain.setTargetAtTime(target, this.ctx.currentTime, 0.04);
    else this.musicGain.gain.value = target;
  }

  // ---- Music ----

  startMusic(): void {
    this.unlock();
    if (!this.ctx || this.musicPlaying) return;
    this.musicPlaying = true;
    this.step = 0;
    this.nextNoteTime = this.ctx.currentTime + 0.1;
    this.schedulerInterval = window.setInterval(() => this.scheduleAhead(), 25);
  }

  stopMusic(): void {
    if (this.schedulerInterval !== null) {
      clearInterval(this.schedulerInterval);
      this.schedulerInterval = null;
    }
    this.musicPlaying = false;
  }

  private scheduleAhead(): void {
    if (!this.ctx) return;
    const secondsPerStep = 60 / this.bpm / this.stepsPerBeat;
    // If the tab was throttled/backgrounded, the audio clock kept advancing while this
    // timer was paused. Resync rather than dumping a burst of overdue notes all at once.
    if (this.nextNoteTime < this.ctx.currentTime) {
      this.nextNoteTime = this.ctx.currentTime + 0.05;
    }
    while (this.nextNoteTime < this.ctx.currentTime + 0.12) {
      this.scheduleStep(this.step, this.nextNoteTime, secondsPerStep);
      this.nextNoteTime += secondsPerStep;
      this.step = (this.step + 1) % this.track.steps;
    }
  }

  /** Play every voice of the current track that has a note on this step. */
  private scheduleStep(step: number, time: number, stepDur: number): void {
    for (const voice of this.track.voices) {
      const freq = voice.pattern[step % voice.pattern.length];
      if (freq == null) continue;
      const o = voice.opts;
      this.playSynth(freq, time, stepDur * (o.durMul ?? 0.9), {
        type: o.type,
        detune: o.detune,
        filterHz: o.filterHz,
        q: o.q,
        attack: o.attack,
        peak: o.peak,
        release: stepDur * (o.releaseMul ?? 0.7),
        vibrato: o.vibrato,
      });
    }

    // Underwater: scatter little rising "bloop" bubbles over the bed.
    if (this.track.bubbles) this.maybeBubble(step, time);
  }

  /** A short rising sine pop — a water bubble. Played into the music bus so it respects mute. */
  private maybeBubble(step: number, time: number): void {
    const pitches: Record<number, number> = {
      1: note('E', 5),
      4: note('G', 5),
      7: note('B', 5),
      10: note('A', 5),
      13: note('D', 5),
    };
    const target = pitches[step];
    if (!target || !this.ctx || !this.musicGain) return;
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(target * 0.55, time);
    osc.frequency.exponentialRampToValueAtTime(target, time + 0.09);
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(0.0001, time);
    gain.gain.exponentialRampToValueAtTime(0.12, time + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, time + 0.16);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.2);
  }

  private playSynth(
    freq: number,
    time: number,
    dur: number,
    opts: {
      type: OscillatorType;
      detune?: number;
      filterHz?: number;
      q?: number;
      attack?: number;
      peak?: number;
      release?: number;
      vibrato?: number;
    },
  ): void {
    if (!this.ctx || !this.musicGain) return;
    const ctx = this.ctx;

    const osc = ctx.createOscillator();
    osc.type = opts.type;
    osc.frequency.setValueAtTime(freq, time);
    if (opts.detune) osc.detune.setValueAtTime(opts.detune, time);

    // Second slightly-detuned osc for a fatter analog-synth unison.
    const osc2 = ctx.createOscillator();
    osc2.type = opts.type;
    osc2.frequency.setValueAtTime(freq, time);
    osc2.detune.setValueAtTime(-(opts.detune ?? 6), time);

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(opts.filterHz ?? 1500, time);
    filter.Q.setValueAtTime(opts.q ?? 1, time);

    const gain = ctx.createGain();
    const attack = opts.attack ?? 0.01;
    const peak = opts.peak ?? 0.5;
    const release = opts.release ?? dur;
    gain.gain.setValueAtTime(0.0001, time);
    gain.gain.exponentialRampToValueAtTime(peak, time + attack);
    gain.gain.exponentialRampToValueAtTime(0.0001, time + attack + release);

    osc.connect(filter);
    osc2.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);

    if (opts.vibrato) {
      const lfo = ctx.createOscillator();
      lfo.frequency.setValueAtTime(opts.vibrato, time);
      const lfoGain = ctx.createGain();
      lfoGain.gain.setValueAtTime(6, time);
      lfo.connect(lfoGain);
      lfoGain.connect(osc.frequency);
      lfoGain.connect(osc2.frequency);
      lfo.start(time);
      lfo.stop(time + dur + 0.1);
    }

    osc.start(time);
    osc2.start(time);
    osc.stop(time + dur + 0.1);
    osc2.stop(time + dur + 0.1);
  }

  // ---- Sound effects ----

  play(name: SfxName): void {
    if (!this.ctx || !this.sfxGain) return;
    const t = this.ctx.currentTime;
    switch (name) {
      case 'shootPlasma':
        this.blip(900, 260, 0.1, 'square', 0.3);
        break;
      case 'shootShoulder':
        this.blip(180, 50, 0.28, 'sawtooth', 0.5);
        this.noise(0.18, 500, 0.35);
        break;
      case 'katana':
        this.noise(0.22, 3200, 0.4, 'bandpass', 900);
        this.blip(1400, 500, 0.18, 'triangle', 0.25);
        break;
      case 'explosion':
        this.noise(0.4, 1800, 0.7, 'lowpass');
        this.blip(120, 40, 0.35, 'sawtooth', 0.5);
        break;
      case 'hit':
        this.blip(420, 200, 0.06, 'square', 0.25);
        break;
      case 'pickup':
        this.arpUp([note('E', 4), note('G', 4), note('B', 4)], t, 0.28);
        break;
      case 'bossPhase':
        this.blip(90, 60, 0.5, 'sawtooth', 0.6);
        this.noise(0.5, 900, 0.5, 'lowpass');
        break;
      case 'bubble':
        this.blip(300, 800, 0.12, 'sine', 0.25);
        this.blip(400, 1200, 0.08, 'sine', 0.15);
        break;
      case 'gem':
        this.arpUp([note('C', 5), note('E', 5), note('G', 5), note('C', 6)], t, 0.45);
        break;
    }
  }

  private blip(fromHz: number, toHz: number, dur: number, type: OscillatorType, vol: number): void {
    if (!this.ctx || !this.sfxGain) return;
    const ctx = this.ctx;
    const t = ctx.currentTime;
    const osc = ctx.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(fromHz, t);
    osc.frequency.exponentialRampToValueAtTime(Math.max(1, toHz), t + dur);
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(t);
    osc.stop(t + dur + 0.05);
  }

  private noise(
    dur: number,
    filterHz: number,
    vol: number,
    filterType: BiquadFilterType = 'lowpass',
    q = 1,
  ): void {
    if (!this.ctx || !this.sfxGain || !this.noiseBuffer) return;
    const ctx = this.ctx;
    const t = ctx.currentTime;
    const src = ctx.createBufferSource();
    src.buffer = this.noiseBuffer;
    const filter = ctx.createBiquadFilter();
    filter.type = filterType;
    filter.frequency.setValueAtTime(filterHz, t);
    filter.frequency.exponentialRampToValueAtTime(Math.max(80, filterHz * 0.3), t + dur);
    filter.Q.setValueAtTime(q, t);
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(filter);
    filter.connect(gain);
    gain.connect(this.sfxGain);
    src.start(t);
    src.stop(t + dur + 0.05);
  }

  private arpUp(freqs: number[], startTime: number, total: number): void {
    if (!this.ctx || !this.sfxGain) return;
    const ctx = this.ctx;
    const step = total / freqs.length;
    freqs.forEach((f, i) => {
      const t = startTime + i * step;
      const osc = ctx.createOscillator();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(f, t);
      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.3, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + step * 1.6);
      osc.connect(gain);
      gain.connect(this.sfxGain!);
      osc.start(t);
      osc.stop(t + step * 1.6 + 0.05);
    });
  }

  // ---- End-screen jingles ----
  // One-shot melodies for the game-over screen. Routed through the SFX bus so they play over the
  // stopped biome music and honour mute. Victory = a bright rising fanfare; defeat = a short,
  // sinking "aww" motif (the classic lost-a-life sting).

  playEndJingle(victory: boolean): void {
    if (!this.ctx || !this.sfxGain) return;
    const t0 = this.ctx.currentTime + 0.06;
    if (victory) {
      // A full triumphant fanfare: a rising call, a little turnaround, then a resolving cadence
      // onto a big held bright chord with sparkles on top.
      const lead: [number, number, number][] = [
        [note('G', 4), 0.0, 0.12],
        [note('C', 5), 0.12, 0.12],
        [note('E', 5), 0.24, 0.12],
        [note('G', 5), 0.36, 0.12],
        [note('E', 5), 0.48, 0.12],
        [note('G', 5), 0.6, 0.34],
        [note('A', 5), 0.98, 0.12],
        [note('G', 5), 1.1, 0.12],
        [note('E', 5), 1.22, 0.12],
        [note('C', 5), 1.34, 0.12],
        [note('D', 5), 1.46, 0.12],
        [note('G', 5), 1.58, 0.12],
        [note('C', 6), 1.72, 0.8],
      ];
      for (const [f, off, dur] of lead) this.tone(f, t0 + off, dur, 'square', 0.3);
      // Harmony + body under the two held notes.
      this.tone(note('B', 4), t0 + 0.6, 0.34, 'triangle', 0.16);
      this.tone(note('E', 6), t0 + 1.72, 0.8, 'triangle', 0.2); // held third
      this.tone(note('G', 6), t0 + 1.86, 0.66, 'triangle', 0.16); // sparkle
      this.tone(note('C', 4), t0 + 1.72, 0.85, 'sawtooth', 0.14); // low root
      this.tone(note('C', 7), t0 + 2.24, 0.4, 'triangle', 0.12); // final high ping
    } else {
      // A longer sinking motif (chromatic descent) resolving low, then the "sad trombone" slide.
      const fall: [number, number, number][] = [
        [note('B', 4), 0.0, 0.16],
        [note('A', 4), 0.16, 0.16],
        [note('G', 4), 0.32, 0.16],
        [note('F#', 4), 0.48, 0.16],
        [note('E', 4), 0.64, 0.16],
        [note('C', 4), 0.8, 0.3],
      ];
      for (const [f, off, dur] of fall) this.tone(f, t0 + off, dur, 'triangle', 0.28);
      this.slideTone(note('E', 3), note('A', 2), t0 + 1.12, 0.62, 'sawtooth', 0.32);
    }
  }

  /** A single enveloped tone scheduled at an absolute time, on the SFX bus. */
  private tone(freq: number, time: number, dur: number, type: OscillatorType, vol: number): void {
    if (!this.ctx || !this.sfxGain) return;
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, time);
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(0.0001, time);
    gain.gain.exponentialRampToValueAtTime(vol, time + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, time + dur);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(time);
    osc.stop(time + dur + 0.05);
  }

  /** A tone that glides from one pitch to another — the descending "wah" tail of the defeat sting. */
  private slideTone(fromHz: number, toHz: number, time: number, dur: number, type: OscillatorType, vol: number): void {
    if (!this.ctx || !this.sfxGain) return;
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(fromHz, time);
    osc.frequency.exponentialRampToValueAtTime(Math.max(1, toHz), time + dur);
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(vol, time);
    gain.gain.exponentialRampToValueAtTime(0.0001, time + dur);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(time);
    osc.stop(time + dur + 0.05);
  }

  private makeNoiseBuffer(): AudioBuffer {
    const ctx = this.ctx!;
    const len = ctx.sampleRate * 1;
    const buffer = ctx.createBuffer(1, len, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    // Deterministic pseudo-random so we don't depend on Math.random (fine either way for noise).
    let seed = 1337;
    for (let i = 0; i < len; i++) {
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      data[i] = (seed / 0x3fffffff) - 1;
    }
    return buffer;
  }
}
