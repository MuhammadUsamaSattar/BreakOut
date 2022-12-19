import pygame
import Objects
import Constants
import random

class Interface:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
        self.bricks = []
        self.restart = True

        while self.restart:
            self.gameLoop()

        pygame.quit()

    def gameLoop(self):
        self.won = None
        self.restart = False
        self.running = True
        pressed_left = False
        pressed_right = False
        clock = pygame.time.Clock()
        score = 0

        Player = Objects.Player([int(Constants.SCREEN_SIZE[0]/2) - Constants.PLAYER_SIZE[0]/2, int(9*Constants.SCREEN_SIZE[1]/10)], [255,255,255], Constants.PLAYER_SIZE)
        Ball = Objects.Ball([int(Constants.SCREEN_SIZE[0]/2 - (Constants.BALL_SIZE/2)), int(6*Constants.SCREEN_SIZE[1]/10)], [255, 255, 255], Constants.BALL_SIZE)
        self.bricks = self.setBricks()
        prev_time = pygame.time.get_ticks()
        curr_time = pygame.time.get_ticks()

        while self.running:
            curr_time = pygame.time.get_ticks()
            self.screen.fill([0,0,0])

            if (curr_time - prev_time) >= (1000/Constants.FPS):
                temp = curr_time
                curr_time = pygame.time.get_ticks()
                prev_time = temp

                self.drawPlayer(Player, self.screen)
                self.drawBricks(self.bricks, self.screen)
                self.drawBall(Ball, self.screen)

                self.textHandler(self.screen, self.won, score)
                pygame.display.flip()
            self.won, score = self.checkWin(Ball, self.bricks, score, self.won)

            pressed_left, pressed_right = self.EventHandler(pressed_left, pressed_right, Player)
            Player.resolveMechanics()
            Ball.resolveMechanics(Ball.getPos(), Ball.getVel(), Ball.size, Player, self.bricks)    


    def drawPlayer(self, Player, screen):
        self.drawRect([int(Player.pos[0]), int(Player.pos[1])], Player.size, Player.color, screen)

    def drawBrick(self, Brick, screen):
        self.drawRect(Brick.pos, Brick.size, Brick.color, screen)

    def drawBall(self, Ball, screen):
        self.drawCircle([int(Ball.pos[0]),int(Ball.pos[1])], Ball.size, Ball.color, screen)

    def drawRect(self, pos, size, color, screen):
        pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], size[0], size[1],))

    def drawCircle(self, pos, size, color, screen):
        pygame.draw.circle(screen, color, pos, size)

    def goLeft(self, Player):
        Player.setAcc(-Constants.PLAYER_ACC)

    def goRight(self, Player):
        Player.setAcc(Constants.PLAYER_ACC)

    def setBricks(self):
        bricks = []
        random.seed(Constants.SEED)
        for j in range(Constants.NUM_VERT):
            bricks.append([])
            for i in range(Constants.NUM_HORIZ):
                pos = [Constants.BRICK_SIZE[0]*i, Constants.BRICK_SIZE[1]*j]

                if i > 0 and j > 1 and i < (Constants.NUM_HORIZ - 2) and not bricks[j-1][i-1].Dest and not bricks[j-1][i+1].Dest and not bricks[j-2][i].Dest:
                    bricks[-1].append(Objects.Brick(pos, Constants.BRICK_SIZE))
                else:
                    if random.random() < Constants.CHANCE_INDEST_BRICKS:
                        bricks[-1].append(Objects.Brick(pos, Constants.BRICK_SIZE, Dest = False))
                    else:
                        bricks[-1].append(Objects.Brick(pos, Constants.BRICK_SIZE))

        temp = []
        for j in range(len(bricks)):
            temp.append(bricks[len(bricks)-1-j])
        bricks = temp

        return bricks

    def drawBricks(self, bricks, screen):
        for j in bricks:
            for i in j:
                if not i.dead:
                    self.drawBrick(i, screen)
                    pygame.draw.rect(screen, [0,0,0], pygame.Rect(i.pos[0], i.pos[1], i.size[0], i.size[1],), Constants.BORDER_SIZE)

    def EventHandler(self, pressed_left, pressed_right, Player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True

                elif event.key == pygame.K_RIGHT:
                    pressed_right = True

                elif event.key == pygame.K_r:
                    self.setRestart()

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pressed_left = False

                elif event.key == pygame.K_RIGHT:
                    pressed_right = False

        if pressed_left:
            self.goLeft(Player)
        elif pressed_right:
            self.goRight(Player)
        else:
            Player.friction()

        return pressed_left, pressed_right

    def setRestart(self):
        self.restart = True
        self.running = False
    
    def checkWin(self, Ball, bricks, score, won):
        if won == None:
            if Ball.pos[1] < Constants.SCREEN_SIZE[1]:
                score = 0
                won = True
                for j in bricks:
                    for i in j:
                        if i.Dest:
                            if not i.dead:
                                won = None
                            else:
                                score += 1
            else:
                won = False
            
        return won, score

    def textHandler(self, screen, won, score):
        if won != None:
            if won:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('You Won!', True, [255,255,255])
                textRect = text.get_rect()
                textRect.center = (Constants.SCREEN_SIZE[0] // 2, Constants.SCREEN_SIZE[1] // 2)
                screen.blit(text, textRect)

            else:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('You Lost!', True, [255,255,255])
                textRect = text.get_rect()
                textRect.center = (Constants.SCREEN_SIZE[0] // 2, Constants.SCREEN_SIZE[1] // 2)
                screen.blit(text, textRect)
        
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('R to restart', True, [255,255,255])
            textRect = text.get_rect()
            textRect.center = (Constants.SCREEN_SIZE[0] // 2, int(5.5*Constants.SCREEN_SIZE[1] // 10))
            screen.blit(text, textRect)
            
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Escape to quit', True, [255,255,255])
            textRect = text.get_rect()
            textRect.center = (Constants.SCREEN_SIZE[0] // 2, int(6*Constants.SCREEN_SIZE[1] // 10))
            screen.blit(text, textRect)
            
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(score), True, [255,255,255])
        textRect = text.get_rect()
        textRect.center = (int(9.5*Constants.SCREEN_SIZE[0] // 10), int(9.5*Constants.SCREEN_SIZE[1] // 10))
        screen.blit(text, textRect)
