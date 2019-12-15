# The Snake Object for each player

class Snake:

    def __init__(self, coord = [0,0], bound = [40, 40], color = 3):
        self.body = [coord]
        self.isAlive = True
        self.lastDir = 1 # last direction
        self.MAX_WIDTH = bound[0]
        self.MAX_HEIGHT = bound[1]
        self.pendingGrowth = 0 # undigesetd food
        self.step = 1
        self.color = color

    # walk toward certain direction at certain height (update body array)
    # directinon:
    # up:1 ; right:2 ; down:-1 ; left:-2
    def walk(self, direction):
        # print(self.body)
        # check if go back
        if (direction + self.lastDir == 0):
            # don't change direction
            direction = self.lastDir
        if (direction == 1):
            # move up
            for i in range(self.step):
                newCoord = self.body[0].copy()
                newCoord[1] -= 1
                self.body.insert(0, newCoord)
        if (direction == -1):
            # move down
            for i in range(self.step):
                newCoord = self.body[0].copy()
                newCoord[1] += 1
                self.body.insert(0, newCoord)
        if (direction == 2):
            # move right
            for i in range(self.step):
                newCoord = self.body[0].copy()
                newCoord[0] += 1
                self.body.insert(0, newCoord)
        if (direction == -2):
            # move left
            for i in range(self.step):
                newCoord = self.body[0].copy()
                newCoord[0] -= 1
                self.body.insert(0, newCoord)
        # print(self.body)

        # kill tail and digest food
        if (self.pendingGrowth > self.step):
            for i in range(step):
                del self.body[-1]
            self.pendingGrowth -= self.step
        else:
            for i in range(self.step - self.pendingGrowth):
                del self.body[-1]
            self.pendingGrowth = 0

        self.lastDir = direction
        # print(self.body)
        print('')

    # increase length when eat
    def eat(self, score = 1):
        self.pendingGrowth += score

    # check for wall collision
    def isWallCrash(self):
        if (self.body[0][0] < 0 or self.body[0][1] < 0 or self.body[0][0] > (self.MAX_WIDTH-1) or self.body[0][1] > (self.MAX_HEIGHT-1)):
            return True
        else:
            return False

    def getLength(self):
        return(len(self.body))
