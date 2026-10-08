# Lunar Lander Repair Lab

This project is a single-file Lunar Lander-lite clone using **Pygame**. It introduces students to vector physics, procedural terrain generation, and multi-condition landing validation using a small, readable object-oriented codebase.

---

## What's Provided

A working Lunar Lander-lite game with:

- A ship with rotation, thrust, gravity, and limited fuel, wrapping horizontally around the screen
- Procedurally generated terrain with two landing pads of different point multipliers
- Touchdown validation based on speed and angle, with a full HUD showing live telemetry
- Levels, lives, and scoring for successful landings

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Left/Right to rotate, Up to thrust, `R` to reset, Space to continue after landing or crashing.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the touchdown validation bug

> A safe landing is supposed to require the ship to be over a pad, descending slowly, roughly level, *and* not moving sideways too fast. In the current build, a ship can slam down sideways — well beyond `MAX_SPEED_X` — on a pad at a safe vertical speed and angle, and it still counts as a perfect landing. Check the condition in `touchdown()` against all three constants it defines near the top of the file (`MAX_SPEED_X`, `MAX_SPEED_Y`, `MAX_ANGLE`), and see which one it never actually checks.

### Task 2: Implement `ship_color(fuel_ratio)`

> Called once per frame in `draw`, as `color = ship_color(max(0.0, self.fuel) / FUEL_MAX) or (230, 230, 240)`. It receives the remaining fuel as a fraction from `0.0` (empty) to `1.0` (full) and should return an `(r, g, b)` hull color, or `None` to keep the default. Idea: shift the hull toward red as fuel runs low.

### Task 3: Implement `on_landing(score)`

> Called from `touchdown()` immediately after a successful landing's points are added to the score. It receives the number of points just earned from that landing. Its return value is ignored. Idea: a fireworks effect, or a distinct sound for a high-multiplier pad.

### Task 4: Implement `bonus_life_threshold()`

> Called every frame in `update()`. It takes no arguments and should return an integer score value, or `None` to disable bonus lives entirely. Whenever the score crosses a multiple of that value for the first time, one life is awarded automatically — the bookkeeping (`self.bonus_awarded`) is already implemented, so you only need to choose the threshold. Idea: return `1500`.

---

## Expected Behavior

- The ship wraps horizontally but never moves past the top of the screen; gravity and rotated thrust behave like real vectors
- Terrain always includes exactly two landing pads with different score multipliers
- A landing only counts as successful when the ship is over a pad, descending slowly, roughly level, and not drifting sideways too fast
- Fuel never goes negative, and thrust cuts out automatically once it runs out
- A crash costs a life; the game ends when lives reach zero

---

## Folder Structure

```
lunar_lander/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
