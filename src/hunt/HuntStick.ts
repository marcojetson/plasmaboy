// A whole-screen floating analog stick for the hunt mode: touch ANYWHERE and drag to steer in
// any direction (Vampire-Survivors style, one thumb). Exposes a normalised vector (x, y each in
// -1..1, magnitude clamped to 1) that the scene reads each frame. DOM-based so it floats above the
// canvas and gets its own pointer stream. Desktop can ignore it and use the keyboard instead.
const RADIUS = 70; // px of drag for full tilt
const DEAD = 8; // px before movement registers

export class HuntStick {
  x = 0;
  y = 0;

  private readonly root: HTMLDivElement;
  private readonly base: HTMLDivElement;
  private readonly knob: HTMLDivElement;
  private pointerId: number | null = null;
  private ox = 0;
  private oy = 0;
  private readonly cleanups: Array<() => void> = [];

  constructor() {
    this.root = document.createElement('div');
    Object.assign(this.root.style, {
      position: 'fixed',
      inset: '0',
      zIndex: '50',
      touchAction: 'none',
    } as CSSStyleDeclaration);

    this.base = ring(RADIUS * 2, '3px solid rgba(232,240,245,0.45)', 'rgba(20,24,32,0.22)');
    this.knob = ring(54, 'none', 'rgba(232,240,245,0.6)');
    this.base.style.display = 'none';
    this.knob.style.display = 'none';
    this.root.append(this.base, this.knob);

    const down = (e: PointerEvent) => {
      if (this.pointerId !== null) return;
      e.preventDefault();
      this.pointerId = e.pointerId;
      this.ox = e.clientX;
      this.oy = e.clientY;
      this.draw(e.clientX, e.clientY);
    };
    const move = (e: PointerEvent) => {
      if (e.pointerId !== this.pointerId) return;
      e.preventDefault();
      let dx = e.clientX - this.ox;
      let dy = e.clientY - this.oy;
      const dist = Math.hypot(dx, dy);
      if (dist < DEAD) {
        this.x = this.y = 0;
      } else {
        const clamped = Math.min(dist, RADIUS);
        this.x = (dx / dist) * (clamped / RADIUS);
        this.y = (dy / dist) * (clamped / RADIUS);
      }
      // Clamp the knob to the ring for display.
      if (dist > RADIUS) { dx = (dx / dist) * RADIUS; dy = (dy / dist) * RADIUS; }
      this.drawAt(this.ox, this.oy, this.ox + dx, this.oy + dy);
    };
    const up = (e: PointerEvent) => {
      if (e.pointerId !== this.pointerId) return;
      this.pointerId = null;
      this.x = this.y = 0;
      this.base.style.display = 'none';
      this.knob.style.display = 'none';
    };

    this.root.addEventListener('pointerdown', down);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
    window.addEventListener('pointercancel', up);
    this.cleanups.push(() => {
      this.root.removeEventListener('pointerdown', down);
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
      window.removeEventListener('pointercancel', up);
    });

    document.body.appendChild(this.root);
  }

  private draw(cx: number, cy: number): void {
    this.drawAt(cx, cy, cx, cy);
  }
  private drawAt(bx: number, by: number, kx: number, ky: number): void {
    this.base.style.left = `${bx - RADIUS}px`;
    this.base.style.top = `${by - RADIUS}px`;
    this.base.style.display = 'block';
    this.knob.style.left = `${kx - 27}px`;
    this.knob.style.top = `${ky - 27}px`;
    this.knob.style.display = 'block';
  }

  destroy(): void {
    for (const c of this.cleanups) c();
    this.cleanups.length = 0;
    this.x = this.y = 0;
    this.root.remove();
  }

  setEnabled(enabled: boolean): void {
    this.root.style.pointerEvents = enabled ? 'auto' : 'none';
  }
}

function ring(size: number, border: string, bg: string): HTMLDivElement {
  const d = document.createElement('div');
  Object.assign(d.style, {
    position: 'absolute',
    width: `${size}px`,
    height: `${size}px`,
    borderRadius: '50%',
    border,
    background: bg,
    boxSizing: 'border-box',
    pointerEvents: 'none',
  } as CSSStyleDeclaration);
  return d;
}
