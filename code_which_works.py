import pygame, sys, random
from pygame import QUIT, USEREVENT, K_UP, K_DOWN
from classes import Paddle, Ball

FPS = 200

WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 20

BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
# background_image = pygame.image.load('bg.jpg')
# background_image = pygame.transform.scale(background_image, (1000, 700))

get_random_color = lambda: tuple(random.sample(range(0, 256), 3))

def drawArena(DISPLAYSURF):
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2),0),(int(WINDOWWIDTH/2),WINDOWHEIGHT), int(LINETHICKNESS/4))

def main():
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')

    playerOnePosition = playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    paddle1 = Paddle(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = Paddle(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = Ball()

    drawArena(DISPLAYSURF)
    paddle1.draw(WHITE, DISPLAYSURF)
    paddle2.draw(WHITE, DISPLAYSURF)
    ball.draw(DISPLAYSURF)

    paddle1_color = paddle2_color = WHITE

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == USEREVENT and event.paddle==1:
                paddle1_color = get_random_color()
            elif event.type == USEREVENT and event.paddle==2:
                paddle2_color = get_random_color()

        if keys[ord("w")]:
            paddle1.y -= 2
        elif keys[ord("s")]:
            paddle1.y += 2

        if keys[K_UP]:
            paddle2.y -= 2
        elif keys[K_DOWN]:
            paddle2.y += 2

        drawArena(DISPLAYSURF)
        paddle1.draw(paddle1_color, DISPLAYSURF)
        paddle2.draw(paddle2_color, DISPLAYSURF)
        ball.draw(DISPLAYSURF)   
        ball.move(paddle1, paddle2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()