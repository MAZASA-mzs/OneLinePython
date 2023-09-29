#IMPORT
import pygame as pg;
from random import randint as ri;
rect = pg.rect.Rect;
pg.init();
#CONFIG
FPS = 60;
SCREEN_W, SCREEN_H = 500, 500;
SCREEN_BG_COLOR = (0, 0, 0, 0);
SCREEN_FONT_SIZE = 25;
SCREEN_FONT_COLOR = (127, 127, 127);

OUT_TIME = 10;

GAME_TIMEOUT = 10;

PLAYER_SIZE = 50;
PLAYER_SPEED = 100;
PLAYER_START_HEALTH = 50;
PLAYER_COLOR = (56, 73, 19);

APPLES_CNT = 50;
APPLE_MIN_SIZE = 5;
APPLE_MAX_SIZE = 15;

# VARS
screen = pg.display.set_mode((SCREEN_W, SCREEN_H));
clock = pg.time.Clock();
font = pg.font.SysFont(pg.font.get_default_font(), SCREEN_FONT_SIZE);

# (SCORE, RUN)
game = rect(0, 1, 0, 0);

# (HEALTH, none), (RECT)
player = [
        rect(PLAYER_START_HEALTH, 0, 0, 0),
        rect(PLAYER_SIZE//2, PLAYER_SIZE//2, PLAYER_SIZE, PLAYER_SIZE)
        ];

# (COLOR, none) (RECT)
apples = [
    (
        rect(
            ri(3, 256),
            ri(0, 3),
            0, 0
        ),
        rect(
            ri(2*PLAYER_SIZE, SCREEN_W-2*PLAYER_SIZE),
            ri(2*PLAYER_SIZE, SCREEN_W-2*PLAYER_SIZE),
            ri(APPLE_MIN_SIZE, APPLE_MAX_SIZE),
            ri(APPLE_MIN_SIZE, APPLE_MAX_SIZE),
        )
    )
    for _ in range(APPLES_CNT)
];

# LOGIC
logic_apples_remove = lambda: [apples.append(apple)
                                    if not(apple[-1].colliderect(player[-1]))
                                    else game.move_ip(1, 0)
                                for apple in [apples.pop() for _ in range(len(apples))] ];
logic_apples_add = lambda: [apples.append(
                                            (
                                                rect(
                                                    ri(3, 256),
                                                    ri(0, 3),
                                                    0, 0
                                                ),
                                                rect(
                                                    ri(2*PLAYER_SIZE, SCREEN_W-2*PLAYER_SIZE),
                                                    ri(2*PLAYER_SIZE, SCREEN_W-2*PLAYER_SIZE),
                                                    ri(APPLE_MIN_SIZE, APPLE_MAX_SIZE),
                                                    ri(APPLE_MIN_SIZE, APPLE_MAX_SIZE),
                                                )
                                            )
                                        ) for _ in range(APPLES_CNT - len(apples))];
update_logic = lambda: (logic_apples_remove(), logic_apples_add());

# INPUT

input_down = lambda: [game.move_ip(0, -1) for ev in pg.event.get() if ev.type == pg.QUIT];

input_key_d = lambda lst: player[-1].move_ip(PLAYER_SPEED/FPS,  0) if lst[pg.K_d] else None;
input_key_s = lambda lst: ((player[-1].move_ip(0,  PLAYER_SPEED/FPS) if lst[pg.K_s] else None), input_key_d(lst));
input_key_a = lambda lst: ((player[-1].move_ip(-PLAYER_SPEED/FPS, 0) if lst[pg.K_a] else None), input_key_s(lst));
input_key_w = lambda lst: ((player[-1].move_ip(0, -PLAYER_SPEED/FPS) if lst[pg.K_w] else None), input_key_a(lst));
input_pressed = lambda: input_key_w(pg.key.get_pressed());

update_input = lambda: (input_pressed(), input_down());

# DRAW

draw_apples = lambda: [pg.draw.rect(screen, (
                                                (2 ** apple[0][0]) % 256,
                                                (3 ** apple[0][0]) % 256,
                                                (4 ** apple[0][0]) % 256,
                                            ), apple[-1])
                        for apple in apples];
draw_player = lambda: (pg.draw.rect(screen, PLAYER_COLOR, player[1]));
draw_score = lambda: pg.display.set_caption(f'Score: {game[0]}');

update_screen = lambda: (screen.fill(SCREEN_BG_COLOR), draw_apples(), draw_player(), draw_score(), pg.display.update(), clock.tick(FPS));

# UPDATE
global_update = lambda time: (update_screen(), update_logic(), update_input());

# START
[global_update(time) for time in range(GAME_TIMEOUT * FPS) if game[1]];
text = f'Your score: {game[0]}. Thank you for playing!';
text = font.render(text, True, SCREEN_FONT_COLOR);
screen.blit(text, rect(SCREEN_W//2-text.get_rect().w//2, SCREEN_H//2-text.get_rect().h//2, text.get_rect().w, text.get_rect().h));
game.move_ip(0, 1);
[(pg.display.update(), clock.tick(FPS), [[game.move_ip(0, -1) for ev in pg.event.get() if ev.type == pg.QUIT]]) for time in range(OUT_TIME*FPS) if game[1]];
pg.quit();