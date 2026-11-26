import math

WIDTH, HEIGHT, GROUND = 768, 480, 384
SPEED, JUMP, GRAVITY = 210, -650, 1800
FONT = "pressstart2p"
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
SURFACES = ((GROUND, 0, 352), (GROUND, 416, WIDTH),
            (304, 96, 224), (280, 544, 672))
GEMS = ((160, 268), (608, 244), (384, 300))
DOOR = Rect(698, 318, 44, 66)
MENU = [Rect(234, y, 300, 40) for y in (214, 270, 326)]
END = [Rect(234, y, 300, 42) for y in (240, 296)]


class Animation:

    def __init__(self, base, frames, fps):
        self.base, self.frames, self.fps = base, frames, fps
        self.index = self.timer = 0

    def update(self, dt):
        self.timer = (self.timer + dt) % (self.frames / self.fps)
        self.index = int(self.timer * self.fps)

    def image(self, facing):
        return f"{self.base}_{facing}{self.index}"


class Character:

    hit_w = hit_h = 40

    def __init__(self, x, y, animations):
        self.x, self.y, self.facing = x, y, "r"
        self.animations, self.anim = animations, animations["idle"]
        self.actor = Actor(self.anim.image("r"), pos=(x, y),
                           anchor=("center", "bottom"))

    def play(self, name):
        if self.anim is not self.animations[name]:
            self.anim = self.animations[name]
            self.anim.index = self.anim.timer = 0

    def animate(self, dt):
        self.anim.update(dt)
        self.actor.image = self.anim.image(self.facing)
        self.actor.pos = (self.x, self.y)

    def hitbox(self):
        return Rect(self.x - self.hit_w / 2, self.y - self.hit_h,
                    self.hit_w, self.hit_h)


class Player(Character):
    hit_w, hit_h = 36, 56

    def __init__(self):
        super().__init__(70, GROUND, {
            "idle": Animation("player_idle", 4, 7),
            "run": Animation("player_run", 6, 13),
            "jump": Animation("player_jump", 2, 8),
            "hurt": Animation("player_hurt", 2, 8),
        })
        self.vx = self.vy = self.stun = 0
        self.grounded = True

    def respawn(self):
        self.x, self.y, self.vx, self.vy = 70, GROUND, 0, 0
        self.stun, self.grounded = 1.2, True

    def update(self, dt):
        self.stun = max(0, self.stun - dt)
        left = keyboard.left or keyboard.a
        right = keyboard.right or keyboard.d
        self.vx = SPEED * (right - left) if self.stun < 0.9 else 0
        if self.vx:
            self.facing = "r" if self.vx > 0 else "l"
        jump = keyboard.space or keyboard.up or keyboard.w
        if jump and self.grounded and self.stun < 0.9:
            self.vy, self.grounded = JUMP, False
            play_sound("jump")

        self.x = min(WIDTH - 24, max(24, self.x + self.vx * dt))
        old_y = self.y
        self.vy = min(900, self.vy + GRAVITY * dt)
        self.y += self.vy * dt
        self.grounded = False
        if self.vy >= 0:
            for top, left, right in SURFACES:
                if (left - 10 <= self.x <= right + 10
                        and old_y <= top <= self.y):
                    self.y, self.vy, self.grounded = top, 0, True
                    break

        if self.stun > 0.7:
            self.play("hurt")
        elif not self.grounded:
            self.play("jump")
        elif self.vx:
            self.play("run")
        else:
            self.play("idle")
        self.animate(dt)


class Enemy(Character):

    def __init__(self, x, left, right, animations, flying=False):
        super().__init__(x, 215 if flying else GROUND, animations)
        self.left, self.right, self.start = left, right, x
        self.flying = flying
        self.hit_w, self.hit_h = (54, 44) if flying else (52, 32)
        self.direction, self.pause, self.time = -1, 0, 0

    def reset(self):
        self.x, self.y = self.start, 215 if self.flying else GROUND
        self.direction, self.pause, self.time = -1, 0, 0
        self.play("idle")

    def update(self, dt):
        self.time += dt
        self.pause = max(0, self.pause - dt)
        if self.pause:
            self.play("idle")
        else:
            self.x += self.direction * (75 if self.flying else 55) * dt
            self.facing = "r" if self.direction > 0 else "l"
            self.play("move")
            if not self.left <= self.x <= self.right:
                self.x = max(self.left, min(self.right, self.x))
                self.direction *= -1
                self.pause = 1.5 if self.flying else 1.2
        if self.flying:
            rate, height = (3, 18) if self.pause else (2.2, 30)
            self.y = 215 + math.sin(self.time * rate) * height
        self.animate(dt)


def patrol(idle, idle_frames, move, move_frames):
    return {"idle": Animation(idle, idle_frames, 6),
            "move": Animation(move, move_frames, 9)}


state, audio_on, lives, gems_left = "menu", True, 3, 3
hint, hint_timer, gem_time = "", 0, 0
player = Player()
frogs = (Enemy(210, 150, 300, patrol("frog_idle", 4, "frog_move", 2)),
         Enemy(560, 450, 690, patrol("frog_idle", 4, "frog_move", 2)))
eagle = Enemy(384, 280, 500, patrol("eagle_idle", 2, "eagle_fly", 4), True)
enemies = (*frogs, eagle)
gems = [Actor("gem_0", pos=spot) for spot in GEMS]
taken = [False] * 3

background = Actor("back", topleft=(0, 0))
ground = (Actor("ground_left", topleft=(0, GROUND)),
          Actor("ground_right", topleft=(416, GROUND)))
platforms = (Actor("platform", topleft=(96, 304)),
             Actor("platform", topleft=(544, 280)))
door = Actor("door", pos=(720, GROUND), anchor=("center", "bottom"))

music.set_volume(0.4)
music.play("theme")


def play_sound(name):
    if audio_on:
        getattr(sounds, name).play()


def toggle_audio():
    global audio_on
    audio_on = not audio_on
    if audio_on:
        music.unpause()
    else:
        music.pause()


def start_game():
    global state, lives, gems_left, hint_timer
    state, lives, gems_left, hint_timer = "play", 3, 3, 0
    for index, gem in enumerate(gems):
        taken[index], gem.pos = False, GEMS[index]
    player.respawn()
    player.stun = 0
    for enemy in enemies:
        enemy.reset()


def finish(result):
    global state, hint_timer
    state, hint_timer = result, 0
    play_sound(result)


def lose_life():
    global lives
    lives -= 1
    play_sound("hit")
    if lives <= 0:
        finish("lose")
    else:
        player.respawn()


def update_gems(dt):
    global gem_time, gems_left
    gem_time += dt
    for index, (x, y) in enumerate(GEMS):
        gem = gems[index]
        gem.image = f"gem_{int(gem_time * 12) % 5}"
        gem.y = y + math.sin(gem_time * 3 + index) * 5
        if not taken[index] and player.hitbox().colliderect(
                Rect(x - 18, gem.y - 18, 36, 36)):
            taken[index], gems_left = True, gems_left - 1
            play_sound("gem")


def update(dt):
    global hint, hint_timer
    if state != "play":
        return
    dt = min(dt, 0.05)
    hint_timer = max(0, hint_timer - dt)
    player.update(dt)
    for enemy in enemies:
        enemy.update(dt)
    update_gems(dt)

    if player.y > HEIGHT + 40:
        lose_life()
        return
    if player.stun == 0:
        for enemy in enemies:
            if player.hitbox().colliderect(enemy.hitbox()):
                lose_life()
                return
    if player.hitbox().colliderect(DOOR):
        if gems_left == 0:
            finish("win")
        elif hint_timer == 0:
            hint, hint_timer = "COLLECT ALL 3 GEMS TO OPEN THE DOOR!", 2


def text(message, y, size=10, color="white", x=384):
    screen.draw.text(message, center=(x, y), fontname=FONT,
                     fontsize=size, color=color)


def panel(rect):
    screen.draw.filled_rect(rect, BLACK)
    screen.draw.rect(rect, WHITE)
    screen.draw.rect(rect.inflate(-2, -2), WHITE)


def button(rect, label):
    screen.draw.filled_rect(rect, WHITE)
    screen.draw.text(label, center=rect.center, fontname=FONT,
                     fontsize=10, color="black")


def draw_menu():
    panel(Rect(190, 40, 388, 392))
    text("GEM QUEST", 82, 28, "white")
    text("A DELIBERATELY UGLY 1-BIT PLATFORMER.", 118, 8, "white")
    text("COLLECT 3 GEMS, THEN REACH THE DOOR.", 140, 9, "white")
    text("MOVE: ARROWS / A D     JUMP: SPACE", 170, 8, "white")
    labels = ("START GAME",
              f"MUSIC & SOUNDS: {'ON' if audio_on else 'OFF'}", "EXIT")
    for rect, label in zip(MENU, labels):
        button(rect, label)
    screen.draw.filled_rect(Rect(0, 438, WIDTH, 34), WHITE)
    text("ENTER TO START    ESC FOR MENU", 455, 8, "black")


def draw_hud():
    left = Rect(10, 10, 160, 44)
    right = Rect(598, 10, 160, 44)
    for rect in (left, right):
        screen.draw.filled_rect(rect, BLACK)
        screen.draw.rect(rect, WHITE)
        screen.draw.rect(rect.inflate(-2, -2), WHITE)
    screen.draw.text(f"LIVES {lives}", center=(90, 32), fontname=FONT,
                     fontsize=14, color="white")
    screen.draw.text(f"GEMS {3 - gems_left}/3", center=(678, 32),
                     fontname=FONT, fontsize=14, color="white")


def draw_end():
    panel(Rect(174, 120, 420, 250))
    win = state == "win"
    text("YOU WIN!" if win else "GAME OVER", 160, 26, "white")
    text("ALL GEMS FOUND. YOU ESCAPED!" if win else
         "OUT OF LIVES. TRY AGAIN!", 205, 9, "white")
    button(END[0], "PLAY AGAIN")
    button(END[1], "MAIN MENU")


def draw():
    background.draw()
    screen.draw.rect(Rect(0, 0, WIDTH, HEIGHT), WHITE)
    screen.draw.rect(Rect(1, 1, WIDTH - 2, HEIGHT - 2), WHITE)
    if state == "menu":
        draw_menu()
        return
    for actor in (*ground, *platforms, door):
        actor.draw()
    for index, gem in enumerate(gems):
        if not taken[index]:
            gem.draw()
    for character in (*enemies, player):
        character.actor.draw()
    draw_hud()
    if hint_timer > 0:
        screen.draw.filled_rect(Rect(180, 112, 408, 32), WHITE)
        text(hint, 128, 9, "black")
    if state in ("win", "lose"):
        draw_end()


def to_menu():
    global state
    state = "menu"


def quit_game():
    music.stop()
    exit()


def on_mouse_down(pos):
    if state == "menu":
        rects, actions = MENU, (start_game, toggle_audio, quit_game)
    elif state in ("win", "lose"):
        rects, actions = END, (start_game, to_menu)
    else:
        return
    for rect, action in zip(rects, actions):
        if rect.collidepoint(pos):
            play_sound("click")
            action()
            return


def on_key_down(key):
    if key == keys.RETURN and state in ("menu", "win", "lose"):
        start_game()
    elif key == keys.ESCAPE and state != "menu":
        to_menu()
