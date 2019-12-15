# Game state of the Game
# Stores All Player Information and Game Time Instances

import sys
from Snake import Snake
from random import randint
from Food import Food


class Slither:

    # configuration
    def __init__(self):
        self.WIDTH = 40
        self.HEIGHT = 40
        self.TILE_SIZE = 20
        self.playerDict = {}
        self.foodList = []
        self.alias = {
            '0' : (0,0,0), # floor
            '1' : (0,255,0), # food
            '2' : (255,0,0), # snake 1 (red)
            '3' : (0,0,255), # snake 2 (blue)
        }

    # add Player
    def addPlayer(self, id):
        snake = Snake(coord = [randint(5, self.WIDTH-5), randint(5, self.HEIGHT-5)], color = str(len(self.playerDict) + 2))
        print('SNAKE {} ADDED'.format(snake.color))
        self.playerDict[id] = snake

    # spawn food
    def addFood(self):
        flag = True
        x,y = 0,0
        while(flag):
            flag = False
            x = randint(1, self.WIDTH-1)
            y = randint(1, self.HEIGHT-1)
            # check player
            for player in self.playerDict:
                if (self.playerDict.get(player).body in [x,y]):
                    flag = True
            # check food
            for food in self.foodList:
                if (food.coord == [x,y]):
                    flag = True
        self.foodList.append(Food(coord = [x,y]))

    # control snake
    def moveSnake(self, port, direction, speed):
        snake = self.playerDict.get(port)
        snake.step = speed
        if (not direction == 0):
            snake.walk(direction=direction)
        else:
            snake.walk(snake.lastDir)

    # check wall crash
    def checkWallCrash(self):
        for player in self.playerDict:
            snake = self.playerDict.get(player)
            if (snake.isWallCrash()):
                return True
        return False

    # check if eat food
    def checkEatFood(self):
        for player in self.playerDict:
            snake = self.playerDict.get(player)
            for food in self.foodList:
                if (food.coord in snake.body):
                    snake.eat(food.score)
                    food.isEaten = True
        self._removeFood()

    # check snake collision
    def checkSnakeCollision(self):
        for player in self.playerDict:
            snake = self.playerDict.get(player)
            for otherPlayer in self.playerDict:
                if (not otherPlayer == player):
                    otherSnake = self.playerDict.get(otherSnake)
                    if (len(snake.body) > 1): # check both head and head2
                        if (snake[0] in otherSnake.body or snake[1] in otherSnake.body):
                            return True
                    else:
                        if (snake[0] in otherSnake.body):
                            return True

    # remove eaten Food
    def _removeFood(self):
        for food in self.foodList:
            if (food.isEaten):
                self.foodList.remove(food)

    # format to 2d array for transport
    def getOutput(self):
        row = '0.'*(self.WIDTH - 1) + '0'
        packet = []
        for i in range(self.HEIGHT):
            packet.append(row.split('.'))
        # draw food
        print('FOODS {}'.format(self.foodList))
        for food in self.foodList:
            print(food.coord)
            packet[food.coord[1]][food.coord[0]] = '1'
        # draw snake
        for player in self.playerDict:
            snake = self.playerDict.get(player)
            for seg in snake.body:
                print('SNAKE {}'.format(seg))
                packet[seg[1]][seg[0]] = snake.color

        return packet
