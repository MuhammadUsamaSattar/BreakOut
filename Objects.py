import pygame
import Constants

class Object:
    def __init__(self, pos, color, size):
        self.pos = pos
        self.color = color
        self.size = size

class Player(Object):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
        self.vel = [0, 0]
        self.acc = [0, 0]

    def changePos(self, delta):
        self.pos[0] += delta
        if (self.pos[0] + (self.size[0])) > (Constants.SCREEN_SIZE[0]): 
            self.pos[0] = Constants.SCREEN_SIZE[0] - (self.size[0])
        elif (self.pos[0] ) < 0: 
            self.pos[0] = 0

    def changeVel(self, delta):
        if abs(self.vel[0]) < Constants.PLAYER_MAX_VEL or self.vel[0] > 0 and self.acc[0] < 0 or self.vel[0] < 0 and self.acc[0] > 0:
            self.vel[0] += delta

    def setVel(self, val):
        self.vel = val

        return self.vel

    def setAcc(self, val):
        self.acc[0] = val

    def getPos(self):
        return self.pos

    def getVel(self):
        return self.vel

    def friction(self):
        self.acc[0] = -self.vel[0]/3
        if abs(self.vel[0]) < 0.05:
            self.vel[0] = 0

    def resolveMechanics(self):
        self.changeVel(self.acc[0])

        self.changePos(self.vel[0])


class Brick(Object):
    def __init__(self, pos, size, Dest = True):
        if Dest:
            color = [0,0,255]
        else:
            color = [255,0,0]
        super().__init__(pos, color, size)
        self.Dest = Dest
        self.dead = False

class Ball(Player):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
        self.vel = Constants.PLAYER_START_VEL

    def changePos(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

        self.pos[0] = self.pos[0]
        self.pos[1] = self.pos[1]

    def setVel(self, val):
        self.vel = val

    def changeVel(self, delta):
        self.vel[0] += delta[0]/4
        self.vel[1] += delta[1]/4

        if abs(self.vel[0]) > Constants.BALL_MAX_VEL:
            if self.vel[0] > 0:
                self.vel[0] = Constants.BALL_MAX_VEL
            else:
                self.vel[0] = -Constants.BALL_MAX_VEL

        if abs(self.vel[1]) > Constants.BALL_MAX_VEL:
            if self.vel[1] > 0:
                self.vel[1] = Constants.BALL_MAX_VEL
            else:
                self.vel[1] = -Constants.BALL_MAX_VEL

    def resolveMechanics(self, pos, vel, size, Player, bricks):
        player_collided = False

        ball_x_low = pos[0] - (size/2)
        ball_x_high = pos[0] + (size/2)
        ball_y_low = pos[1] - (size/2)
        ball_y_high = pos[1] + (size/2)


        if pos[1] >= Constants.SCREEN_SIZE[1]//2:
            player_x_low = Player.pos[0]
            player_x_high = Player.pos[0] + Player.size[0]
            player_y_low = Player.pos[1]
            player_y_high = Player.pos[1] + Player.size[1]

            top_cond = ball_y_high >= player_y_low and pos[0] >= player_x_low and pos[0] <= player_x_high and ((ball_y_high < player_y_high) or (ball_y_low<player_y_high))
            left_cond = ball_x_high >= player_x_low and pos[1] >= player_y_low and pos[1] <= player_y_high
            right_cond = ball_x_low <= player_x_high and pos[1] >= player_y_low and pos[1] <= player_y_high

            if top_cond:
                self.setVel([vel[0], -abs(vel[1])])
                player_collided = True
        else:
            for j in bricks:
                for i in j:
                    if not i.dead:
                        brick_x_low = i.pos[0]
                        brick_x_high = i.pos[0] + i.size[0]
                        brick_y_low = i.pos[1]
                        brick_y_high = i.pos[1] + i.size[1]
            
                        top_cond = ball_y_high >= brick_y_low and pos[0] >= brick_x_low and pos[0] <= brick_x_high and ball_y_high < brick_y_high
                        bottom_cond = ball_y_low <= brick_y_high and pos[0] >= brick_x_low and pos[0] <= brick_x_high and ball_y_low > brick_y_low
                        left_cond = ball_x_high >= brick_x_low and pos[1] >= brick_y_low and pos[1] <= brick_y_high and ball_x_high < brick_x_high
                        right_cond = ball_x_low <= brick_x_high and pos[1] >= brick_y_low and pos[1] <= brick_y_high and ball_x_low > brick_x_low
            
                        if bottom_cond or top_cond or right_cond or left_cond:
                            if i.Dest:
                                i.dead = True
                            break
            
                if (bottom_cond):
                    self.setVel([vel[0], abs(vel[1])])
                    break
                elif (top_cond):
                    self.setVel([vel[0], -abs(vel[1])])
                    break
                elif (left_cond):
                    self.setVel([-abs(vel[0]), vel[1]])
                    break
                elif (right_cond):
                    self.setVel([abs(vel[0]), vel[1]])
                    break

        bottom_cond = ball_y_low <= 0
        left_cond = ball_x_high >= Constants.SCREEN_SIZE[0]
        right_cond = ball_x_low <= 0
        
        if (right_cond):
            self.setVel([abs(vel[0]), vel[1]])
        elif (left_cond):
            self.setVel([-abs(vel[0]), vel[1]])
        elif (bottom_cond):
            self.setVel([vel[0], abs(vel[1])])

        if player_collided:
            self.changeVel(Player.vel)

        self.changePos(vel)