# Gem Quest

A deliberately crude, black-and-white one-screen platformer built with Python
and Pygame Zero, using AI-generated images. Its Atari-inspired graphics use a black playfield, white 1-bit
shapes, oversized pixels, Pitfall-style block characters and a plain text HUD,
so the code stays the focus.

## Goal

Three gems float above the level. Collect all three, then reach the door on the
far right. The door stays locked until every gem is found.

- Touching a frog or the eagle costs one life.
- Falling into the water costs one life.
- You start with three lives. Lose all three and the game ends.

The frogs patrol their own stretches of ground, and the eagle circles above the
middle of the stage, so timing your jumps matters.

## How to Run

All package installation and game-run commands below use a project-local
virtual environment. Do not install Pygame Zero globally and do not use `sudo`.

1. Install Python 3.8 or newer.

2. Open a terminal in this folder and create the environment:

   ```bash
   python3 -m venv .venv
   ```

   On Windows, use:

   ```bash
   py -m venv .venv
   ```

3. Activate the environment.

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:

   ```bat
   .venv\Scripts\activate.bat
   ```

   Your prompt should now start with `(.venv)`. Every remaining command must be
   run in this activated environment.

4. Upgrade pip and install Pygame Zero inside the environment:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install pgzero
   ```

5. Run the game from this folder, still inside the environment:

   ```bash
   python -m pgzero game.py
   ```

   The equivalent command below also works while the environment is active, but
   `python -m pgzero` always uses the environment's Python:

   ```bash
   pgzero game.py
   ```

6. When finished, leave the environment:

   ```bash
   deactivate
   ```

Keep `game.py` beside the `images/`, `sounds/`, `music/` and `fonts/` folders.
Pygame Zero finds those folders automatically.

## Libraries

- **Pygame Zero 1.2+** — window, drawing, input, animation actors, text, images,
  sound effects and music.
- **Python standard library `math`** — only for the sine-wave bobbing of the
  eagle and gems, and for gem animation timing.

`game.py` does not import pygame directly. `Rect`, `Actor`, `screen`, `sounds`,
`music`, `keyboard`, `keys` and `exit` are supplied by Pygame Zero.

## Controls

| Input | Action |
| --- | --- |
| Left / Right arrows or `A` / `D` | Move |
| `Space`, Up arrow or `W` | Jump |
| `Enter` | Start game / play again |
| `Escape` | Return to the main menu |
| Mouse | Click the menu and end-screen buttons |

The three menu buttons are:

- **START GAME**
- **MUSIC & SOUNDS: ON/OFF** — turns the background music and all sound effects
  on or off together
- **EXIT**

## Files

| Path | Contents |
| --- | --- |
| `game.py` | The complete game |
| `images/` | 1-bit player, enemies, gems, door and terrain |
| `sounds/` | Jump, gem, hit, click, win and lose effects |
| `music/theme.ogg` | Generated looping square-wave chiptune |
| `fonts/pressstart2p.ttf` | Menu and HUD font |
| `fonts/OFL.txt` | SIL Open Font License for the font |
| `README.md` | This file |

## Assets and Credits

The game is intentionally rough-looking and inspired by early Atari-era
sprites. The characters are original 1-bit block figures: the player is a small
humanoid, the enemies are a low frog and a winged bird. They are drawn on 16x20,
20x14 and 24x20 pixel grids and scaled 3x with nearest-neighbor, so every pixel
is a chunky square. The Pitfall reference is stylistic only; no Atari or
Activision assets or code are used.

### Sunny Land art

by ansimuz (Luis Zuno), CC0 1.0 Universal.
<https://ansimuz.itch.io/sunny-land-pixel-game-art>

Source material for the gems and door. Those frames were cropped, exported,
then converted offline to coarse white-on-black pixel art. The gems were reduced
to about 15x13 blocks and the door to 11x16 before scaling back up. The player,
frog, eagle, black sky, blocky stars and clouds, horizon, water, ground and
platforms are simple 1-bit shapes drawn from scratch.

### Kenney sound effects

CC0 1.0 Universal:

- UI Audio — <https://kenney.nl/assets/ui-audio>
- Digital Audio — <https://kenney.nl/assets/digital-audio>
- Impact Sounds — <https://kenney.nl/assets/impact-sounds>
- Music Jingles — <https://kenney.nl/assets/music-jingles>

| File | Source |
| --- | --- |
| `jump.ogg` | Digital Audio / `phaseJump1.ogg` |
| `gem.ogg` | Digital Audio / `powerUp5.ogg` |
| `hit.ogg` | Impact Sounds / `impactGeneric_light_000.ogg` |
| `click.ogg` | UI Audio / `click1.ogg` |
| `win.ogg` | Music Jingles / `jingles_NES00.ogg` |
| `lose.ogg` | Digital Audio / `lowDown.ogg` |

### Background music

`music/theme.ogg` is an original 14.5-second square-wave loop generated for this
project. A one-off offline script combined a melody and bass line and rendered
them to OGG. Pygame Zero's music loader supports MP3, OGG and OGA, but not MIDI,
so OGG was chosen for compatibility. The script used NumPy and soundfile;
neither is needed to play the game.

### Font

"Press Start 2P" by CodeMan38 and The Press Start 2P Project Authors, SIL Open
Font License 1.1.
<https://fonts.google.com/specimen/Press+Start+2P>

The full license text is in `fonts/OFL.txt`.

The asset-preparation step also used Pillow, NumPy and soundfile. They are
development tools only; `game.py` itself needs nothing beyond Pygame Zero.

No network connection is needed to play.
