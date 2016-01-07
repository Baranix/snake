import pygame
import random


clock = pygame.time.Clock()
win = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
pygame.display.set_caption('Snake')

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class snake:
    image = pygame.image.load("blip.gif")
    direction = UP
    def __init__(self, pos):
        self.pos = [pos]
        win.blit(snake.image, pos)


class food:
    image = pygame.image.load("blip.gif")
    def __init__(self, pos):
        self.pos = pos
        win.blit(food.image, pos)


class billboard:
    def __init__(self, player):
        self.score = "0000"
        #self.score2 = score1
        self.image = pygame.image.load("player" + str(player) + ".png")
        self.pos = (10,5)
        self.scoreImg = [ pygame.image.load(self.score[0] + ".png"),
            pygame.image.load(self.score[1] + ".png"),
            pygame.image.load(self.score[2] + ".png"),
            pygame.image.load(self.score[3] + ".png") ]
        self.scorePos = [(12, 30), (27, 30), (42, 30), (57, 30)]

    def addScore(self):
        self.score = str(int(self.score)+1).zfill(4)
        print self.score
        print self.score[1]
        self.scoreImg = [ pygame.image.load(self.score[0] + ".png"),
            pygame.image.load(self.score[1] + ".png"),
            pygame.image.load(self.score[2] + ".png"),
            pygame.image.load(self.score[3] + ".png") ]


def roundToFive(x):
    return int(5.0 * round(float(x)/5.0))

def generateFood(playerPos):
    foodPos = ( roundToFive(random.randint(5,495)), roundToFive(random.randint(55,495)) )
    while foodPos in playerPos: # Prevent food from spawning over the snake
        foodPos = ( roundToFive(random.randint(5,495)), roundToFive(random.randint(55,495)) )
    return food( foodPos )  

def gameOn():
    running = True
    growFlag = False
    growpos = []
    player1 = snake((250,250))
    food1 = generateFood(player1.pos)
    scoreboard1 = billboard(1)
    while running:
        win.fill( (0,0,0) )

        for i in range(len(player1.pos)): # redraw
            win.blit( player1.image, player1.pos[i] )
            win.blit( food1.image, food1.pos )
            win.blit( scoreboard1.image, scoreboard1.pos )
            for j in range(4):
                win.blit( scoreboard1.scoreImg[j], scoreboard1.scorePos[j] )
            win.blit( pygame.image.load("border.gif"), (0,50) )

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
            if key[pygame.K_LEFT] and not player1.direction == RIGHT:
                player1.direction = LEFT
            if key[pygame.K_RIGHT] and not player1.direction == LEFT:
                player1.direction = RIGHT
            if key[pygame.K_UP] and not player1.direction == DOWN:
                player1.direction = UP
            if key[pygame.K_DOWN] and not player1.direction == UP:
                player1.direction = DOWN

        pos = []
        for i in range(len(player1.pos)):
            pos.append(player1.pos[i])

        if player1.direction == UP:
            player1.pos[0] = player1.pos[0][:1] + (player1.pos[0][1]-5,)
            #print player1.pos[0]
            for j in range(1, len(player1.pos)):
                player1.pos[j] = pos[j-1]
                #print "going up"

        elif player1.direction == DOWN:
            player1.pos[0] = player1.pos[0][:1] + (player1.pos[0][1]+5,)
            #print player1.pos[0]
            for j in range(1, len(player1.pos)):
                player1.pos[j] = pos[j-1]
                #print "going down"

        elif player1.direction == LEFT:
            player1.pos[0] = (player1.pos[0][0]-5,) + player1.pos[0][1:]
            #print player1.pos[0]
            for j in range(1, len(player1.pos)):
                player1.pos[j] = pos[j-1]
                #print "going left"

        elif player1.direction == RIGHT:
            player1.pos[0] = (player1.pos[0][0]+5,) + player1.pos[0][1:]
            #print player1.pos[0]
            for j in range(1, len(player1.pos)):
                player1.pos[j] = pos[j-1]
                #print "going right"

        if player1.pos[0][0] > 495 or player1.pos[0][1] > 495 or player1.pos[0][0] < 0 or player1.pos[0][1] < 55:
            break # Game Over if hit edge
        if player1.pos[0] in player1.pos[1:]:
            break # Game Over if eat itself

        if food1.pos in player1.pos:
            growpos.append(food1.pos)
            food1 = generateFood(player1.pos)
            growFlag = True
            scoreboard1.addScore()
        elif growFlag and not growpos in player1.pos:
            player1.pos.append(growpos[0])
            growFlag = False
            growpos = []

        pygame.display.flip()
        clock.tick(25)

def gameOver():
    while True:
        #print "Game Over"
        gameOver = pygame.image.load("gameover.png")
        win.blit( gameOver, (27, 220) )

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE] or key[pygame.K_n]:
                return False
            elif key[pygame.K_y]:
                return True

        pygame.display.flip()
        clock.tick(25)


def main():

    pygame.key.set_repeat(1,1)
    
    continueGame = True

    while continueGame:
        gameOn()
        continueGame = gameOver()

    
main()
