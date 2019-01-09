import pygame
from random import random, sample
from pygame import QUIT, USEREVENT, K_UP, K_DOWN

FPS = 200

WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

e1 = pygame.event.Event(pygame.USEREVENT, paddle=1)
e2 = pygame.event.Event(pygame.USEREVENT, paddle=2)


def drawArena(DISPLAYSURF):
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, WHITE,
                     ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2), 0),
                     (int(WINDOWWIDTH/2), WINDOWHEIGHT), int(LINETHICKNESS/4))


def get_random_color(): return tuple(sample(range(0, 256), 3))


class Game:

    def __init__(self):
        pygame.init()

        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Pong')

    def setup_game(self):
        playerOnePosition = playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2

        paddle1 = Paddle(self.DISPLAYSURF, PADDLEOFFSET, playerOnePosition,
                        LINETHICKNESS, PADDLESIZE)
        paddle2 = Paddle(self.DISPLAYSURF, WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS,
                        playerTwoPosition, LINETHICKNESS, PADDLESIZE)
        ball = Ball(self.DISPLAYSURF)
        score = Score(self.DISPLAYSURF)

        drawArena(self.DISPLAYSURF)
        paddle1.draw()
        paddle2.draw()
        ball.draw()

        return paddle1, paddle2, ball, score

    def update_game_screen(self, paddle1, paddle2, ball, score):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == USEREVENT and event.paddle == 1:
                paddle1.color = get_random_color()
            elif event.type == USEREVENT and event.paddle == 2:
                paddle2.color = get_random_color()

        if keys[ord("w")]:
            paddle1.y -= 2
        elif keys[ord("s")]:
            paddle1.y += 2

        if keys[K_UP]:
            paddle2.y -= 2
        elif keys[K_DOWN]:
            paddle2.y += 2

        drawArena(self.DISPLAYSURF)
        paddle1.draw()
        paddle2.draw()
        ball.draw()
        ball.move(paddle1, paddle2)

        score.update_score(paddle1, paddle2)

        pygame.display.update()
        self.FPSCLOCK.tick(FPS)

class Paddle(pygame.Rect):
    display = None

    def __init__(self, display, *props):
        self.score = 0
        self.color = WHITE
        self.display = display
        pygame.Rect.__init__(self, props[0], props[1], props[2], props[3])

    def draw(self):
        if self.bottom > WINDOWHEIGHT - LINETHICKNESS:
            self.bottom = WINDOWHEIGHT - LINETHICKNESS
        elif self.top < LINETHICKNESS:
            self.top = LINETHICKNESS

        pygame.draw.rect(self.display, self.color, self)


class Ball(pygame.Rect):
    display = None

    def __init__(self, display, *props):
        self.display = display
        self.pos_x = (WINDOWWIDTH - LINETHICKNESS)/2
        self.pos_y = (WINDOWHEIGHT - LINETHICKNESS)/2
        self.dir_x = self.dir_y = -1
        pygame.Rect.__init__(self, self.pos_x, self.pos_y,
                             LINETHICKNESS, LINETHICKNESS)

    def draw(self):
        pygame.draw.rect(self.display, WHITE, self)

    def move(self, *paddles):
        speed = random() + 1
        self.x += self.dir_x * speed
        self.y += self.dir_y * speed

        self.check_hitball(paddles[0], paddles[1])
        self.check_edge_collision()

    def check_edge_collision(self):
        if (self.x - LINETHICKNESS / 2 <= 0 and self.dir_x < 0) or (self.x + LINETHICKNESS/2 >= WINDOWWIDTH and self.dir_x > 0):
            self.dir_x *= -1
        elif (self.y - LINETHICKNESS / 2 <= 0 and self.dir_y < 0) or (self.y + LINETHICKNESS/2 >= WINDOWHEIGHT and self.dir_y > 0):
            self.dir_y *= -1

    def check_hitball(self, paddle1, paddle2):
        vector = 1

        if self.dir_x < 0:
            if abs(paddle1.right - self.left) <= 1.5 and paddle1.top <= self.top and paddle1.bottom >= self.bottom:
                pygame.event.post(e1)
                paddle1.score += 1
                vector = -1
            elif self.x - LINETHICKNESS / 2 <= 0:
                paddle1.score -= 1 if paddle1.score else 0

        if self.dir_x > 0:
            if abs(paddle2.left - self.right) <= 1.5 and paddle2.top <= self.top and paddle2.bottom >= self.bottom:
                pygame.event.post(e2)
                paddle2.score += 1
                vector = -1
            elif self.x + LINETHICKNESS/2 >= WINDOWWIDTH:
                paddle2.score -= 1 if paddle2.score else 0

        self.dir_x *= vector


class Score:
    display = None

    def __init__(self, display):
        self.display = display
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def update_score(self, *paddles):
        if len(paddles) == 2:
            for paddle in paddles:
                result = self.font.render(
                    f'Score = {paddle.score}', True, WHITE)
                rect = result.get_rect()
                rect.topright = (150, 50) if not paddles.index(
                    paddle) else (WINDOWWIDTH - 150 + rect.width, 50)

                self.display.blit(result, rect)
