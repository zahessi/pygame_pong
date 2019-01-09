import pygame
from random import random

WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 20

BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

e1 = pygame.event.Event(pygame.USEREVENT, paddle=1)
e2 = pygame.event.Event(pygame.USEREVENT, paddle=2)

class Paddle(pygame.Rect):

    def __init__(self, *props):
        self.score = 0
        pygame.Rect.__init__(self, props[0], props[1], props[2], props[3])
    
    def draw(self, color, DISPLAYSURF):
        if self.bottom > WINDOWHEIGHT - LINETHICKNESS:
            self.bottom = WINDOWHEIGHT - LINETHICKNESS
        elif self.top < LINETHICKNESS:
            self.top = LINETHICKNESS
        
        pygame.draw.rect(DISPLAYSURF, color, self)


class Ball(pygame.Rect):

    def __init__(self, *props):
        self.pos_x = (WINDOWWIDTH - LINETHICKNESS)/2
        self.pos_y = (WINDOWHEIGHT - LINETHICKNESS)/2
        self.dir_x = self.dir_y = -1
        pygame.Rect.__init__(self, self.pos_x, self.pos_y, LINETHICKNESS, LINETHICKNESS)

    def draw(self, display):
        pygame.draw.rect(display, WHITE, self)

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

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def update_score(self, display, *paddles):
        if len(paddles) == 2:
            for paddle in paddles:
                result = self.font.render(f'Score = {paddle.score}', True, WHITE)
                rect = result.get_rect()
                rect.topright = (150, 50) if not paddles.index(paddle) else (WINDOWWIDTH - 150 + rect.width, 50)

                display.blit(result, rect) 
