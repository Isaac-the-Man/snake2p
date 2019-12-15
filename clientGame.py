import sys
import pygame
from Snake import Snake
from pygame.locals import *
from ClientServer import ClientServer

class ClientGame:

    def __init__(self):
        self.FPS = 10
        self.TILE_SIZE = 10
        self.GAME_WIDTH = 40
        self.GAME_HEIGHT = 40
        self.WIDTH = (self.GAME_WIDTH)*self.TILE_SIZE
        self.HEIGHT = (self.GAME_HEIGHT)*self.TILE_SIZE
        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.COLOR_RED = (255,0,0)
        self.LIGHT_GREY = (180,180,180)
        self.COLOR_WHITE = (0,255,0)
        self.alias = {
            '0' : (180,180,180), # floor
            '1' : (0,255,0), # food
            '2' : (255,0,0), # snake 1 (red)
            '3' : (0,0,255), # snake 2 (blue)
        }
        self.server = None
        self.connectServer()

    def connectServer(self):
        hostname = input('Host Name: ')
        self.server = ClientServer(host = hostname, port = 12397)
        self.server.startServer()

    def startGame(self):
        # init game
        pygame.init()
        # Game loop.
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    dir = 0
                    step = 1
                    if event.key == pygame.K_LEFT:
                        dir = -2
                    elif event.key == pygame.K_RIGHT:
                        dir = 2
                    elif event.key == pygame.K_UP:
                        dir = 1
                    elif event.key == pygame.K_DOWN:
                        dir = -1
                    if event.key == pygame.K_SPACE:
                        step = 2
                    self.server.broadcast((dir, step))

            # Draw.
            self.drawFrame()

            pygame.display.flip()
            self.fpsClock.tick(self.FPS)

    def drawFrame(self):
        print('received')
        try:
            data = self.server.receiveInput()
            for y in range(self.GAME_HEIGHT):
                for x in range(self.GAME_WIDTH):
                    if (not data[y][x] == '0'):
                        rect = (x*self.TILE_SIZE, y*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                        pygame.draw.rect(self.screen, self.alias.get(data[y][x]), rect, 1)
        except EOFError as e:
            print(e)


if __name__ == "__main__":
    game = ClientGame()
    game.startGame()
    game.connectServer()
