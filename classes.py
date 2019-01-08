import pygame

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
        self.x += self.dir_x * 1.2
        self.y += self.dir_y * 1.2

        self.check_hitball(paddles[0], paddles[1])
        self.check_edge_collision()


    def check_edge_collision(self):
        if (self.x - LINETHICKNESS / 2 <= 0 and self.dir_x < 0) or (self.x + LINETHICKNESS/2 >= WINDOWWIDTH and self.dir_x > 0):
            self.dir_x *= -1
        elif (self.y - LINETHICKNESS / 2 <= 0 and self.dir_y < 0) or (self.y + LINETHICKNESS/2 >= WINDOWHEIGHT and self.dir_y > 0):
            self.dir_y *= -1

    def check_hitball(self, paddle1, paddle2):
        vector = 1
        if self.dir_x < 0 and paddle1.right == self.left and paddle1.top < self.top and paddle1.bottom > self.bottom:
            pygame.event.post(e1)
            vector = -1
        elif self.dir_x > 0 and paddle2.left == self.right and paddle2.top < self.top and paddle2.bottom > self.bottom:
            pygame.event.post(e2)
            vector = -1

        self.dir_x *= vector