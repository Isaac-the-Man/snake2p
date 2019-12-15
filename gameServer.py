from Mechanics import Slither
from SocketServer import SocketServer
import pygame
from pygame.locals import *
import sys
from time import sleep


# constants
FPS = 10
PLAYER = 1
MAX_FOOD_COUNT = 3

# config
fpsClock = pygame.time.Clock()
engine = Slither()

server = SocketServer(maxPlayer = PLAYER, host = '', port = 12397)
server.startServer()
input('Press Enter When Connection Done')
server.closeConnection()

# add player and initialize
for client in server.clientList:
    engine.addPlayer(client.get('port'))
    server.commandDict[client.get('port')] = (1,1)

server.startListening()

for i in range(3):
    sleep(1)
    print(3-i)
print('START')

pygame.init()
# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # update game
    print(server.commandDict)

        # initialize food
    if (len(engine.foodList) <= 0):
        for i in range(MAX_FOOD_COUNT):
            engine.addFood()

    # broadcast data
    server.broadcast(engine.getOutput())

        # move
    for client in server.commandDict:
        engine.moveSnake(client, server.commandDict.get(client)[0], server.commandDict.get(client)[1])

    # eat food
    engine.checkEatFood()

    # check wall crash
    if (engine.checkWallCrash()):
        print('DEAD')
        pygame.quit()
        sys.exit()

    # check snake crash
    if (engine.checkSnakeCollision()):
        print('COLLISION DEAD')
        pygame.quit()
        sys.exit()


    # tick time
    fpsClock.tick(FPS)

server.endServer()
