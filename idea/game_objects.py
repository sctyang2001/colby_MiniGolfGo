from turtle import width
import pygame
import math
import random


class Thing():
    def __init__(self, image, x, y, width, height):
        self.rect = pygame.Rect((x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2

    def get_center_x(self):
        return self.x + self.width / 2

    def get_center_y(self):
        return self.y + self.height / 2

    def get_x(self):
        return self.rect.x

    def set_x(self, x):
        self.x = x
        self.rect.x = x

    def get_y(self):
        return self.rect.y

    def set_y(self, y):
        self.y = y
        self.rect.y = y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_rect(self):
        return self.rect

class MovingThing(Thing):
    def __init__(self, image, x, y, width, height, arrow):
        super().__init__(image, x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.acc = 1
        self.angle = 0
        self.launchF = 0
        self.arrow = arrow
        self.mass = 1
        self.max_power = 10
        self.turn_angle = 15
        self.powermult = 1

    def set_rot(self, rot_img, rot_rect):
        self.rot_img = rot_img
        self.rot_rect = rot_rect

    def set_vel(self, vel):
        angleInRadian = math.radians(self.angle)
        self.vel_x = vel * math.cos(angleInRadian)
        self.vel_y = vel * math.sin(angleInRadian)
    
    def set_acc(self, acc):
        self.acc = acc

    def get_xy_velocities(self):
        return [self.vel_x, self.vel_y]

    def get_vel(self):
        return math.hypot(self.vel_x, self.vel_y)
    
    def move(self):
        vel = self.get_vel()

        if abs(vel) < 2:
            if vel > 0:
                self.reset()
            self.set_vel(0)
        else:
            angleInRadian = math.radians(self.angle)
            acc_x = self.acc * math.cos(angleInRadian)

            acc_y = self.acc * math.sin(angleInRadian)

            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.vel_x -= acc_x
            self.vel_y -= acc_y
            self.x = self.rect.x
            self.y = self.rect.y

    def update_pos(self):
        vel = self.get_vel()
        if abs(vel) < 2:
            if vel > 0:
                self.reset()
            self.set_vel(0)

        else:
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.x = self.rect.x
            self.y = self.rect.y
            angleInRadian = math.radians(self.angle)
            acc_x = self.acc * math.cos(angleInRadian)
            acc_y = self.acc * math.sin(angleInRadian)
            self.vel_x -= acc_x
            self.vel_y -= acc_y

    def advance(self, step):
        '''allows the ball to take a step forward without changing its speed. Only used in collision detection'''

        self.x = self.x + self.vel_x/step
        self.y = self.y + self.vel_y/step

    def traceback(self, step):
        self.x = self.x - self.vel_x/step
        self.y = self.y - self.vel_y/step

    def set_new_pos(self):
        '''allows the ball to take a step back. Only used in collision detection'''
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        self.x = self.rect.x
        self.y = self.rect.y


    def left(self, angle):
        self.angle -= angle

    def right(self, angle):
        self.angle += angle

    def get_angle(self):
        return self.angle

    def increase_launchF(self):
        if self.launchF < self.max_power:
            self.launchF += 1

    def decrease_launchF(self):
        if self.launchF > 0:
            self.launchF -= 1

    def reflect_x(self):
        self.angle = -self.angle
        self.vel_y = -self.vel_y

    def reflect_y(self):
        self.angle = 180 - self.angle
        self.vel_x = -self.vel_x

    def launch(self, velocity):
        """set initial speed when player launches ball"""
        vel = velocity*(1+self.launchF*self.powermult/2)
        angleInRadian = math.radians(self.angle)
        self.vel_x = vel * math.cos(angleInRadian)
        self.vel_y = vel * math.sin(angleInRadian)

    def update_angle(self):
        self.angle = math.degrees(math.atan2(self.vel_y, self.vel_x))

    def reset(self):
        self.vel_x = 0
        self.vel_y = 0
        self.acc = 1
        self.angle = 0
        self.launchF = 0
        self.mass = 1
        self.max_power = 10
        self.turn_angle = 15
        self.powermult = 1


class Ball(MovingThing):
    def __init__(self, image, x, y, width, height, id, arrow):
        super().__init__(image, x, y, width, height, arrow)
        self.RADIUS = 15
        self.consumables = []
        self.projectiles = []
        self.opponent = None
        self.need_to_display = False
        self.score = 0
        self.id = id

    def display(self):
        # this list stores tuples ((x, y), consumable)
        displayList = []
        # display consumables
        if len(self.consumables) == 1:
            c0 = self.consumables[0]
            displayList.append( (c0, (self.x, self.y-c0.height)) )
        elif len(self.consumables) == 2:
            c0 = self.consumables[0]
            displayList.append( (c0, (self.x-c0.width/2 , self.y-c0.height)) )
            c1 = self.consumables[1]
            displayList.append( (c1, (self.x+c0.width/2 , self.y-c1.height)) )
        
        # display projectile
        if len(self.projectiles) == 1:
            p0 = self.projectiles[0]
            displayList.append( (p0, (self.x-p0.width/3, self.y+p0.height/1.8)) )
        
        return displayList



    def get_projectiles(self):
        return self.projectiles
    
    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def set_opponent(self, opponent):
        self.opponent = opponent

    def get_consumables(self):
        return self.consumables

    def add_consumable(self, consumable):
        self.consumables.append(consumable)
        
    def remove_consumable(self, consumable):
        self.consumables.remove(consumable)

    def get_radius(self):
        return self.RADIUS


class Projectile(MovingThing):
    def __init__(self, image, x, y, width, height, arrow):
        super().__init__(image, x, y, width, height, arrow)
        self.need_arrow = False
        self.is_moving = False
        self.need_to_set = False


class GolfClub(Projectile):
    def __init__(self, image, x, y, width, height, arrow):
        super().__init__(image, x, y, width, height, arrow)
        self.id = "golfClub"
        self.attack_object = None

    def prepare(self, plr):
        self.need_arrow = True
        plr.add_projectile(self)

    def setPosition(self, plr):
        self.set_x(plr.x - 10)
        self.set_y(plr.y - 10)
        self.attack_object = plr.opponent
        self.is_moving = True


class Arrow(Thing):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.rot_img = image
        self.rot_rect = self.rect.copy()
        self.is_visible = True
        self.ball = None

    def set_rot(self, rot_img, rot_x, rot_y):
        self.rot_img = rot_img
        self.rot_rect.x = rot_x
        self.rot_rect.y = rot_y

    def track(self):
        self.x = self.ball.rect.x-self.ball.width
        self.y = self.ball.rect.y-self.ball.height
        
    def reset(self, ball):
        self.ball = ball
        self.x = ball.rect.x-ball.width
        self.y = ball.rect.y-ball.height
        self.rot_img = self.image.copy()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rot_rect = self.rect.copy()
        self.is_visible = True


class Consumable(Thing):
    def __init__(self, duration, image, x, y, width, height, id):
        super().__init__(image, x, y, width, height)
        self.duration = duration
        self.id = id

    def get_duration(self):
        return self.duration
    
    def set_duration(self, new_duration):
        self.duration = new_duration

    def need_to_deactivate(self):
        if self.duration == 0:
            return True
        else:
            self.duration -= 1
            return False

    def activate(self, plr):
        '''activate the item's effect'''
        pass

    def deactivate(self, plr):
        '''deactivate the item's effect'''
        pass


class MassUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(3, image, x, y, width, height, "massUp")

    def activate(self, plr):
        plr.mass = 5*plr.mass
        plr.add_consumable(self)

    def deactivate(self, plr):
        plr.mass = plr.mass/5


class PowerUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(2, image, x, y, width, height, "powerUp")

    def activate(self, plr):
        plr.powermult = 2
        plr.add_consumable(self)

    def deactivate(self, plr):
        plr.powermult = 1


class SpeedUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(2, image, x, y, width, height, "speedUp")

    def activate(self, plr):
        plr.acc /= 3
        plr.add_consumable(self)

    def deactivate(self, plr):
        plr.acc *= 3


class RandomAngle(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(0, image, x, y, width, height, "randomAngle")

    def activate(self, plr):
        plr.opponent.turn_angle = 0
        plr.opponent.angle = random.randint(0, 359)
        # add current consumable into the plr's consumables list
        plr.add_consumable(self)

    def deactivate(self, plr):
        plr.opponent.turn_angle = 15


class ExchangePosition(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(0, image, x, y, width, height, "exchangePosition")

    def activate(self, plr):
        print("Exchange")
        plr_x = plr.x
        plr_y = plr.y
        opponent_x = plr.opponent.x + 6
        opponent_y = plr.opponent.y + 6
        plr.set_x(opponent_x)
        plr.set_y(opponent_y)
        plr.opponent.set_x(plr_x)
        plr.opponent.set_y(plr_y)
        plr.opponent.arrow.reset(plr.opponent)
        plr.add_consumable(self)

    def deactivate(self, plr):
        pass


class Terrain(Thing):
    def __init__(self, image, x, y, width, height, id, color):
        super().__init__(image, x, y, width, height)
        self.id = id
        self.color = color

class SandPit(Terrain):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height, "sand", (253, 223, 119))


class BoostPad(Terrain):
    def __init__(self, image, x, y, width, scale, angle):
        super().__init__( image, x, y, width, width, "boost", (126, 200, 80))
        #orientation is a tuple
        self.scale = scale
        self.angle = angle
        self.orientation = (1, 0)
        self.update_ori()
        self.image = pygame.transform.rotate(self.image, self.angle)

    def right(self):
        self.angle -= 90
        if self.angle < 0:
            self.angle += 360
        self.update_ori()
        self.image = pygame.transform.rotate(self.image, -90)

    def left(self):
        self.angle += 90
        if self.angle >= 360:
            self.angle = 360 - self.angle
        self.update_ori()
        self.image = pygame.transform.rotate(self.image, 90)

    def update_ori(self):
        if self.angle == 0:
            self.orientation = (1, 0)
        if self.angle == 90:
            self.orientation = (0, -1)
        if self.angle == 180:
            self.orientation = (-1, 0)
        if self.angle == 270:
            self.orientation = (0, 1)


class Tornado(Terrain):
    def __init__(self, image, x, y, width, height):
        super().__init__( image, x, y, width, height, "tor", (255, 0, 80))
        #orientation is a tuple
        self.scale = 2


class RandomBox(Consumable):
    def __init__(self, image, x, y, images):
        # images is a list storing all icons RandomBox needs
        # index 0: speedUp; index 1: powerUp; index 2: massUp
        super().__init__(1, image, x, y, 40, 40, "RandomBox")
        # self.consumable = MassUp(self.image, self.x, self.y, self.width, self.height)
        self.images = images
        self.consumable = self.generate_consumable()

    def generate_consumable(self):
        randNum = random.randint(1, 100)
        random_consumable = None

        # SpeedUp: 20%
        if 1 <= randNum <= 20:
            random_consumable = SpeedUp(self.images[0], self.x, self.y, self.width, self.height)
        # PowerUp: 25%
        elif 21 <= randNum <= 45:
            random_consumable = PowerUp(self.images[1], self.x, self.y, self.width, self.height)
        # RandomAngle: 15%
        elif 46 <= randNum <= 60:
            random_consumable = RandomAngle(self.images[3], self.x, self.y, self.width, self.height)
        # ExchangePosition: 15%
        elif 61 <= randNum <= 75:
            random_consumable = ExchangePosition(self.images[4], self.x, self.y, self.width, self.height)
        # MassUp: 25%
        else:
            random_consumable = MassUp(self.images[2], self.x, self.y, self.width, self.height)
            
        # activate consumable
        return random_consumable

    def reset(self):
        self.consumable = self.generate_consumable()
        self.image = self.consumable.image
        self.id = self.consumable.id


    def activate(self, plr):
        self.consumable.activate(plr)

    def deactivate(self, plr):
        pass


        




        



