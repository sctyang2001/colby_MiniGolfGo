#Yiheng Su, Blitzen Wang, Scottie Yang, Chloe Zhang
#Jan, 10, 2022

####################### Setup #########################
# useful imports
from dis import dis
import sys
import random
import math
from turtle import width
import numpy as np
import os.path

# import pygame
import pygame
from pygame.locals import *
from pygame import mixer

import game_objects as go
import sound as s


#global variables
debug_mode = True if sys.argv.__len__()>=2 and sys.argv[1].lower()=="--debug" else False
debug_x = 1220

# initialize pygame
pygame.init()

# initialize bgm
mixer.init()
sound = s.Sound(mixer)

# Frames per second
FPS = 30

# set RGB of colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (126, 200, 80)
YELLOW = (253, 223, 119)
RED =  (255, 0, 80)
CARAMEL = (255, 174, 105)
BLUE = (0, 0, 255)
HIGHLIGHT = (255,242,0)



#initial velocity when force scale is 0
VELOCITY = 8

tracing = False
show_rule = False
editing = False
current_tracing = pygame.Rect((0, 0), (0, 0))
trace_color = BLACK

current_player = 0

# initialize the fonts
try:
    pygame.font.init()
except:
    print("Fonts unavailable")
    sys.exit()

# create font for displaying debug info
INFO_FONT = pygame.font.SysFont("comicsans", 15)

# create a game clock
gameClock = pygame.time.Clock()

# create a screen and set its width and height
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
current_level = 1


# create caption for the screen
pygame.display.set_caption("Hole In One")

####################### Making Content #########################

# load some images
# set the size of the image

BALL_WIDTH, BALL_HEIGHT = 30, 30
ARROW_WIDTH, ARROW_HEIGHT = BALL_WIDTH*3, BALL_HEIGHT*3
ball_img1 = pygame.image.load( "../pictures/player1ball.png" ).convert_alpha() # put the name of ball image here
ball_img2 = pygame.image.load( "../pictures/player2ball.png" ).convert_alpha()
arrow_img = pygame.image.load( "../pictures/black_arrow.png" ).convert_alpha()
hole_img = pygame.image.load("../pictures/hole.png").convert_alpha()
massUp_img = pygame.image.load("../pictures/massUp.png").convert_alpha()
powerUp_img = pygame.image.load("../pictures/powerUp.png").convert_alpha()
speedUp_img = pygame.image.load("../pictures/speedUp.png").convert_alpha()
randomAngle_img = pygame.image.load("../pictures/randomAngle.png").convert_alpha()
exchangePosition_img = pygame.image.load("../pictures/exchangePosition.png").convert_alpha()
golfClub_img = pygame.image.load("../pictures/golfClub.png").convert_alpha()
boost_img = pygame.image.load("../pictures/acceleration_2.png").convert_alpha()
tornado_img = pygame.image.load("../pictures/tornado.png").convert_alpha()
random_img = pygame.image.load("../pictures/randomAngle.png").convert_alpha()
images = [speedUp_img, powerUp_img, massUp_img, randomAngle_img, exchangePosition_img]
obstacle_img = pygame.image.load("../pictures/brick_wall_3.png")
sand_img = pygame.image.load("../pictures/sandpit3_small.png")
edit_rule = pygame.image.load(os.path.join('../rules', 'level_editor_rule.png'))
game_item_rule = pygame.image.load(os.path.join('../rules', 'game_items_rule.png'))

# background scenes
BACKGROUND = pygame.transform.scale(pygame.image.load("../pictures/background.png").convert_alpha(), (WIDTH, HEIGHT))
STARTSCREEN = pygame.transform.scale(pygame.image.load("../pictures/startScreen.png").convert_alpha(), (WIDTH, HEIGHT))

# set up arrow and hole
arrow = go.Arrow(arrow_img, 0, 0, BALL_WIDTH*3, BALL_HEIGHT*3)
hole = go.Ball(hole_img, WIDTH - 75, HEIGHT / 2 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, 0, arrow)

# set up players
player1 = go.Ball(ball_img1, debug_x if debug_mode else 75, HEIGHT / 2 - 50 - BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, 1, arrow)
player2 = go.Ball(ball_img2, debug_x if debug_mode else 75, HEIGHT / 2 + 50 + BALL_WIDTH / 2, BALL_WIDTH, BALL_HEIGHT, 2, arrow)
player1.set_opponent(player2)
player2.set_opponent(player1)

arrow.reset(player1)
player_list = [player1, player2]

ICON_SIZE = 55
# set projectiles
golfClub = go.GolfClub(golfClub_img, 500, 600, ICON_SIZE, ICON_SIZE, arrow)
projectileList = []

# set consumables
massUp = go.MassUp(massUp_img, 700, 100, 40, 40)
speedUp = go.SpeedUp(speedUp_img, 400, 400, 40, 40)
powerUp = go.PowerUp(powerUp_img, 500, 500, 120, 120)
#randomAngle = go.RandomAngle(randomAngle_img, 650, 300, 40, 40)
exchangePosition = go.ExchangePosition(exchangePosition_img, 800, 250, 40, 40)
exchangePosition = go.MassUp(exchangePosition_img, 800, 250, 40, 40)
randomBox = go.RandomBox(random_img, 650, 300, images)
#consumableList = [speedUp, massUp, powerUp, randomAngle, exchangePosition]
consumableList = [exchangePosition]

# player2 have a golf club projectile at the beginning of the game
player2.add_projectile(golfClub)
golfClub.prepare(player2)

# create a font
afont = pygame.font.SysFont( "comicsans", 32, bold=True )
button_font = pygame.font.SysFont( "comicsans", 22, bold=True )
# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

# put rectangles on the boundaries
UPPERBOUND_RECT = pygame.Rect( (0, -35), (WIDTH, 60) )
LOWERBOUND_RECT = pygame.Rect( (0, HEIGHT - 25), (WIDTH, 60) )
LEFTBOUND_RECT = pygame.Rect( (-30, 0), (60, HEIGHT) )
RIGHTBOUND_RECT = pygame.Rect( (WIDTH - 30, 0), (60, HEIGHT) )

BOUNDARY = [UPPERBOUND_RECT, LOWERBOUND_RECT, LEFTBOUND_RECT, RIGHTBOUND_RECT]

# adding terrain
boost1 = go.BoostPad(boost_img, 100, 100, 80, 2, 0)
sand1 = go.SandPit(sand_img, 100, 550, 60, 60)

tor1 = go.Tornado(tornado_img, 700, 500, 120, 120)
TERRAIN_LIST = [boost1, sand1, tor1]

# testing stuff
test_rect = pygame.Rect((300,300), (100,100))
BOUNDARY.append(test_rect)

#stgae booleans
start_screen = False
tutorial_screen = False
game_running = True
replay_game = False
game_paused = False

####################### Filling the Screen #########################
def draw_window(scale):
    global tracing, current_tracing, trace_color
    # clear the screen with background
    screen.blit(BACKGROUND, (0,0))

    # now draw the surfaces to the screen using the blit function
    
    force_text = INFO_FONT.render("Launch force: " + str(scale), 1, BLACK)
    pygame.draw.rect(screen,HIGHLIGHT,pygame.Rect(5,HEIGHT-force_text.get_height()-10,force_text.get_width()+10,force_text.get_height()+10))
    screen.blit(force_text, (10, HEIGHT-force_text.get_height()-5))


    if tracing:
        pygame.draw.rect(screen, trace_color, current_tracing)


    for i in range(4, len(BOUNDARY)):
        # pygame.draw.rect(screen, BLACK, BOUNDARY[i])
        screen.blit(obstacle_img,BOUNDARY[i][0:2],BOUNDARY[i])

    # draw terrians
    for tr in TERRAIN_LIST:
        if tr.id == "sand":
            screen.blit(sand_img, (tr.get_x(), tr.get_y()), tr.get_rect())
        elif tr.id == "boost":
            pygame.draw.rect(screen, tr.color, tr.rect)
            screen.blit(tr.image, (tr.get_x(), tr.get_y()))
        if tr.id == "tor":
            screen.blit(tr.image, (tr.get_x(), tr.get_y()))
    for consumable in consumableList:
        screen.blit(consumable.image, (consumable.get_x(), consumable.get_y()))

    # if show_rule:
        # editing_rule_cover = pygame.Surface((WIDTH, HEIGHT))
        # editing_rule_cover.set_alpha(130)
        # editing_rule_cover.fill(WHITE)
        # screen.blit(editing_rule_cover, (0,0))
        # print(editing)
        # if editing:
            # screen.blit(edit_rule, (0, 0))
        # else:
            # screen.blit(game_item_rule, (0, 0))
        


def draw_players(player_list, current_player, hole, arrow):
    # draw consumable on the screen

    if arrow.is_visible:
        arrow.track();
        screen.blit(arrow.rot_img, (arrow.rot_rect.x, arrow.rot_rect.y))

    screen.blit(hole.image, (hole.get_x(), hole.get_y()))
    for plr in player_list:
        # draw players
        screen.blit(plr.image, (plr.get_x(), plr.get_y()))
        # check if need to show play's items
        if plr.need_to_display:
            displayList = plr.display()
            for info_tuple in displayList:
                screen.blit(info_tuple[0].image, (info_tuple[1][0], info_tuple[1][1]))


        # draw projectile on the screen
    for projectile in projectileList:
        screen.blit(projectile.image, (projectile.get_x(), projectile.get_y()))

    # update the screen
    pygame.display.update()

####################### Add Movement #########################

def handle_collision_ball_ball(ball1, ball2):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y

    distance = math.hypot(dx, dy)
    if distance <= ball1.RADIUS + ball2.RADIUS:
        print("Collision!")
        # play sound
        sound.collision_ball_ball()
        if ball1.get_vel() == 0 and ball2.get_vel() == 0:
            ball1.vel_x = 1
            ball1.vel_y = 1
        m1, m2 = ball1.mass, ball2.mass
        M = m1 + m2
        r1, r2 = np.array((ball1.x+ball1.RADIUS, ball1.y+ball1.RADIUS)), np.array((ball2.x+ball2.RADIUS, ball2.y+ball2.RADIUS))
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = np.array((ball1.vel_x, ball1.vel_y)), np.array((ball2.vel_x, ball2.vel_y))
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        ball1.vel_x, ball1.vel_y = u1[0], u1[1]
        ball2.vel_x, ball2.vel_y = u2[0], u2[1]
        ball1.update_angle()
        ball2.update_angle()
        ball1.advance(10)
        ball2.advance(10)


def handle_collision_ball_rect(ball, rect):
    """handles collision between a ball object and a rectangle"""
    # add sound
    sound.collision_ball_wall()

    orig_x = ball.x
    orig_y = ball.y
    collisions = []
    ball.x  = orig_x - abs(ball.vel_x)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.x  = orig_x + abs(ball.vel_x)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.y  = orig_y + abs(ball.vel_y)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.y  = orig_y - abs(ball.vel_y)
    collisions.append(check_collision_ball_rect(ball, rect))

    ball.x = orig_x
    ball.y = orig_y

    #0 vertical 1 horizontal 2 corner


    if collisions[0] != collisions[1]:
        return 0

    if collisions[2] != collisions[3]:
        return 1



def check_collision_v(ball, rect):
    '''check if the next advance of ball will result in a vertical collision'''
    if ball.x + ball.RADIUS > rect.x and ball.x + ball.RADIUS < rect.x + rect.width:
        return True

    elif round(ball.x + 2*ball.RADIUS) < rect.x or ball.x > rect.x + rect.width:
        return False

    elif ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height:
        return ball.x + 2*ball.RADIUS > rect.x and ball.x < rect.x + rect.width

    else:
        return check_corner_collision(ball, rect)


def check_corner_collision(ball, rect):
    x = ball.x + ball.RADIUS
    y = ball.y + ball.RADIUS
    if math.hypot(abs(x-rect.topleft[0]), abs(y-rect.topleft[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.bottomleft[0]), abs(y-rect.bottomleft[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.bottomright[0]), abs(y-rect.bottomright[1])) <= ball.RADIUS:
        return True
    elif math.hypot(abs(x-rect.topright[0]), abs(y-rect.topright[1])) <= ball.RADIUS:
        return True
    else:
        return False


def check_collision_h(ball, rect):
    '''check if the next advance of ball will result in a horizontal collision'''
    if ball.y + ball.RADIUS > rect.y and ball.y + ball.RADIUS < rect.y + rect.height:
        return True
    elif ball.y + 2*ball.RADIUS < rect.y or ball.y > rect.y + rect.height:
        return False
    elif ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height:
        return ball.y + 2*ball.RADIUS > rect.y and ball.y < rect.y + rect.height
    else:
        return check_corner_collision(ball, rect)


def handle_collision_ball_hole(ball, holeRect):
    """If collide, add GOAL to the event list"""
    if check_collision_ball_rect(ball, holeRect):
        if abs(ball.get_vel())<2:
            print("goal!")
            handle_next_level(ball)


def handle_collision_ball_consumables(ball, consumables_list):
    for consumable in consumables_list:
        if len(ball.get_consumables()) < 2 and check_collision_ball_rect(ball, consumable.get_rect()):
            print("Collide with consumable %s"%consumable)
            if hasattr(consumable, "consumable"): print("Sub-consumable %s"%consumable.consumable)
            print(consumable.id)
            # play sounds
            if consumable.id == "randomAngle":
                sound.randomAngle()

            elif consumable.id == "speedUp":
                sound.speedUp()

            elif consumable.id == "massUp":
                sound.massUp()


            # activate the consumable
            consumable.activate(ball)
            # remove consumable from the list and screen
            consumables_list.remove(consumable)


def handle_plr_consumables(plr):
    for consumable in plr.consumables:
        if consumable.need_to_deactivate():
            print("Deactivate: " + consumable.id)
            consumable.deactivate(plr)
            plr.consumables.remove(consumable)


def handle_conllision_ball_projectiles(ball, projectiles_list):
    for projectile in projectiles_list:
        if len(ball.get_projectiles()) < 1 and check_collision_ball_rect(ball, projectile.get_rect()):
            print("Collide with projectile")
            projectile.prepare(ball)
            projectiles_list.remove(projectile)
            

def handle_golfClub_function(golfClub, ball):
    for wall in BOUNDARY:
        if wall.colliderect(golfClub.get_rect()):
            golfClub.is_moving = False

    if check_collision_ball_rect(ball, golfClub.get_rect()):
        ball.angle = golfClub.angle
        ball.vel_x = golfClub.vel_x * 2
        ball.vel_y = golfClub.vel_y * 2
        golfClub.is_moving = False


def check_sand(plr):
    for tr in TERRAIN_LIST:
        if tr.id == "sand":
            if tr.rect.colliderect(plr.rect):
                return True
        else:
            continue


def handle_terrain():
    for plr in player_list:
        if check_sand(plr) and plr.acc != 1/3:
            plr.acc = 3
        elif plr.acc != 1/3:
            plr.acc = 1

        for tr in TERRAIN_LIST:
            if tr.rect.colliderect(plr.rect):
                if tr.id == "boost":
                    sound.acclpad()
                    plr.vel_x += tr.orientation[0] * tr.scale
                    plr.vel_y += tr.orientation[1] * tr.scale
                    plr.update_angle()

                if tr.id == "tor":
                    # deal with tornado
                    sound.tornado()
                    dx = plr.x - tr.center_x
                    dy = plr.y - tr.center_y
                    
                    angle = math.atan2(dy, dx)
                    if dx > 0:
                        plr.vel_x += tr.scale * math.cos(angle)
                    else:
                        plr.vel_x -= tr.scale * math.cos(angle)
                    if dy > 0:
                        plr.vel_y += tr.scale * math.sin(angle)
                    else:
                        plr.vel_y -= tr.scale * math.sin(angle)
                    plr.update_angle()


def rot_image(rect, image, angle):
    rotated_img = pygame.transform.rotate(image, angle)
    return rotated_img, rect.x + rect.width/2 - (rotated_img.get_width()/2), rect.y + rect.height/2 - (rotated_img.get_height()/2)

####################### Handle Screens #########################

def handle_startScreen():
    """Implement start screen"""
    pass

def check_collision_ball_rect(ball, rect):
    col_v = check_collision_v(ball, rect)
    col_h = check_collision_h(ball, rect)
    return col_v and col_h


def move(plr):
    '''Moves the player and handles collision with obstacles'''

    steps = 20
    for i in range(steps):
        plr.advance(steps)
        for wall in BOUNDARY:
            if check_collision_ball_rect(plr, wall):
                col_type = handle_collision_ball_rect(plr, wall)
                plr.traceback(steps)
                plr.traceback(steps)
                #plr.traceback(steps)
                if col_type == 0:
                    print("vertical")
                    plr.reflect_y()

                if col_type == 1:
                    print("horizontal")
                    plr.reflect_x()




        handle_collision_ball_ball(plr, plr.opponent)

    plr.update_pos()


def handle_next_level(plr):
    """Takes player to the next level"""
    global current_level, replay_game
    goal_text = afont.render( "Player %d scored!" %plr.id, True, BLUE )
    plr.score += 1
    tr_cover = pygame.Surface((WIDTH, HEIGHT))
    tr_cover.set_alpha(130)
    tr_cover.fill(WHITE)
    screen.blit(tr_cover, (0,0))
    # blit the text surface onto the screen
    screen.blit( goal_text, (WIDTH /2 - 100, HEIGHT / 2 - 50) )
    pygame.display.update()
    if current_level == 3:
        replay_game = True
        game_running = False
    else:
        print(1)
        pygame.time.wait(1500)
        current_level += 1
        read_level("level %d.txt" %current_level)
        game_reset()




def handle_endScreen():
    """Implement end screen"""
    screen.blit(STARTSCREEN, (0,0))

    button = pygame.Rect( (180, 80), (280, 80) )
    # pygame.draw.rect( screen, (70, 210, 80), button )
    pygame.display.update()

    print("Entering end screen")
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_clicked(button):
                    pygame.event.clear()
                    main()


def read_level(filename):
    global BOUNDARY, TERRAIN_LIST, consumableList
    BOUNDARY = BOUNDARY[:4]
    TERRAIN_LIST = []
    consumableList = []
    if len(filename) == 0:
        return
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'levels', filename))
    try:
        with open(path) as f:
            lines = f.readlines()
            for l in lines:
                l = l.split(",")
                if l[0] == "w":
                    #wall
                    wall = pygame.Rect((int(l[1]), int(l[2])), (int(l[3]), int(l[4])))
                    BOUNDARY.append(wall)
                if l[0] == "b":
                    #boost
                    boost = go.BoostPad(boost_img, int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]))
                    TERRAIN_LIST.append(boost)
                if l[0] == "s":
                    #sand
                    sand = go.SandPit(sand_img, int(l[1]), int(l[2]), int(l[3]), int(l[4]))
                    TERRAIN_LIST.append(sand)
                if l[0] == "t":
                    #tornado
                    tornado = go.Tornado(tornado_img, int(l[1]), int(l[2]), int(l[3]), int(l[4]))
                    TERRAIN_LIST.append(tornado)
                if l[0] == "i":
                    #item box
                    box = go.RandomBox(random_img, int(l[1]), int(l[2]), images)
                    box.reset()
                    consumableList.append(box)
        f.close()
    except FileNotFoundError:
        print("Level does not exist")


def save_level():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'levels', "new level.txt"))
    lvl = ""
    for i in range(4, len(BOUNDARY)):
        line = "w," + str(BOUNDARY[i].x)+"," + str(BOUNDARY[i].y)+"," + str(BOUNDARY[i].width)+"," + str(BOUNDARY[i].height)+"\n"
        lvl += line
    for tr in TERRAIN_LIST:
        if tr.id == "boost":
            line = "b," + str(tr.x)+"," + str(tr.y)+"," + str(tr.width)+"," + str(tr.scale)+"," + str(tr.angle)+"\n"
        if tr.id == "sand":
            line = "s," + str(tr.x)+"," + str(tr.y)+"," + str(tr.width)+"," + str(tr.height)+"\n"
        if tr.id == "tor":
            line = "t," + str(tr.x)+"," + str(tr.y)+"," + str(tr.width)+"," + str(tr.height)+"\n"
        lvl += line
    for item in consumableList:
        if type(item) is go.RandomBox:
            line = "i," + str(item.x)+"," + str(item.y)+"\n"
        lvl += line
    with open(path, 'w') as f:
        f.write(lvl)
        f.close
    print("level saved as \"new level.txt\"")


def check_button_clicked(button) -> bool:
    """Check if player click the button"""
    mousePos = pygame.mouse.get_pos()
    if button.left < mousePos[0] < button.right and button.top < mousePos[1] < button.bottom:
        return True
    else:
        return False

def check_ball_clicked(ball) -> bool:
    """Check if player click the ball"""
    mousePos = pygame.mouse.get_pos()
    dx = ball.get_center_x() - mousePos[0]
    dy = ball.get_center_y() - mousePos[1]
    distance = math.hypot(dx, dy)

    if distance <= ball.RADIUS:
        return True
    else:
        return False


def game_reset(reset_score = False):
    global current_player
    current_player = 0
    if reset_score:
        player1.score = 0
        player2.score = 0
        player_list[:]=[player1,player2]
    else:
        player_list[:]=[player_list[i] for i in range(1-player_list.__len__(), 1)]

    for plr in player_list:
        plr.consumables = []
        plr.projectiles = []
        plr.angle = 0
        plr.set_vel(0)
    player1.set_x(debug_x if debug_mode else 75)
    player1.set_y(HEIGHT / 2 - 50 - BALL_WIDTH / 2)
    player2.set_x(debug_x if debug_mode else 75)
    player2.set_y(HEIGHT / 2 + 50 + BALL_WIDTH / 2)
    player1.set_opponent(player2)
    player2.set_opponent(player1)
    arrow.reset(player_list[0])
    player1.reset()
    player2.reset()
    player1.arrow.reset(player_list[0])

####################### Main Event Loop #########################

def main(argv):
    global current_player, tracing, current_tracing, projectileList, trace_color, current_level, game_running, game_paused, tutorial_screen, replay_game, show_rule, editing

    read_level("level 1.txt")
    draw_window(0)
    draw_players(player_list, current_player, hole, arrow)

    # show the start screen
    handle_startScreen()

    # play bgm
    sound.bgm()

    print("Entering main loop")
    force_scale = 0
    topleft = (0, 0)
    wh = (0, 0)
    current_projectile = None


    replay_text_1 = afont.render( "You finished all the levels!", True, BLUE)
    replay_text_2 = afont.render( "Press \"R\" to replay, \"Q\" to quit", True, BLUE )


    while True:

        # When the game is running
        if game_running:
            
            if tracing:
                bottomright = pygame.mouse.get_pos()
                wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
                if trace_color == GREEN or trace_color == RED:
                    mn = min(wh[0], wh[1])
                    wh = (mn, mn)
                current_tracing = pygame.Rect(topleft, wh)

            if current_projectile is None:
                plr = player_list[current_player]
            else:
                if projectile.need_arrow:
                    plr = current_projectile
                    current_projectile.acc = 0
                    projectileList.append(current_projectile)
                    projectile.need_arrow = False

            #updating display
            force_scale = plr.launchF
            draw_window(force_scale)

            # Check every event in the event list
            for event in pygame.event.get():
                # click quit button, then quit
                if event.type == pygame.QUIT:
                    sys.exit()

                # display game items a ball have
                if event.type == pygame.MOUSEBUTTONDOWN and check_ball_clicked(player_list[current_player]):
                    player_list[current_player].need_to_display = True
                if event.type == pygame.MOUSEBUTTONUP and player_list[current_player].need_to_display:
                    player_list[current_player].need_to_display = False


                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_LSHIFT:
                        # show_rule = not show_rule

                    if event.key == pygame.K_UP:
                        plr.increase_launchF()

                    if event.key == pygame.K_DOWN:
                        plr.decrease_launchF()

                    if event.key == pygame.K_LEFT:
                        if editing:
                            mp = pygame.mouse.get_pos()
                            for tr in TERRAIN_LIST:
                                if tr.id == "boost":
                                    if mp[0] > tr.x and mp[0] < tr.x + tr.width and mp[1] > tr.y and mp[1] < tr.y + tr.height:
                                        tr.left()
                                        break

                        else:
                            plr.left(player_list[current_player].turn_angle)
                            rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())
                            arrow.set_rot(rot_img, rot_x, rot_y)


                    if event.key == pygame.K_RIGHT:
                        if editing:
                            mp = pygame.mouse.get_pos()
                            for tr in TERRAIN_LIST:
                                if tr.id == "boost":
                                    if mp[0] > tr.x and mp[0] < tr.x + tr.width and mp[1] > tr.y and mp[1] < tr.y + tr.height:
                                        tr.right()
                                        break

                        else:
                            plr.right(player_list[current_player].turn_angle)
                            rot_img, rot_x, rot_y = rot_image(arrow.rect, arrow.image, -plr.get_angle())
                            arrow.set_rot(rot_img, rot_x, rot_y)

                    if event.key == pygame.K_SPACE:
                        # Add sound
                        if current_projectile is None:
                            sound.normal_hit()
                        else:
                            sound.hard_hit()

                        if editing:
                            if tracing:
                                print(trace_color)
                                bottomright = pygame.mouse.get_pos()
                                wh = (bottomright[0] -  topleft[0], bottomright[1] -  topleft[1])
                                if trace_color == BLACK:
                                    BOUNDARY.append(pygame.Rect(topleft, wh))
                                elif trace_color == GREEN:
                                    mn = min(wh[0], wh[1])
                                    boost = go.BoostPad(boost_img, topleft[0], topleft[1], mn, 2, 0)
                                    TERRAIN_LIST.append(boost)
                                elif trace_color == YELLOW:
                                    sand = go.SandPit(hole_img, topleft[0], topleft[1], wh[0], wh[1])
                                    TERRAIN_LIST.append(sand)
                                elif trace_color == RED:
                                    mn = min(wh[0], wh[1])
                                    tornado = go.Tornado(tornado_img, topleft[0], topleft[1], mn, mn)
                                    TERRAIN_LIST.append(tornado)

                            tracing = False

                        else:
                            # Add sound
                            if current_projectile is None:
                                sound.normal_hit()
                            else:
                                sound.hard_hit()


                            plr.launch(VELOCITY)
                            arrow.is_visible = False
                            current_player = (current_player+1)%player_list.__len__()
                            nxt_p = player_list[current_player]

                            # check if we need to delet the consumables
                            handle_plr_consumables(nxt_p)

                            if random.randint(1, 10) <= 3:
                                random_projectile = go.GolfClub(golfClub_img, 0, 0, ICON_SIZE, ICON_SIZE, arrow)
                                random_projectile.prepare(nxt_p)

                            if nxt_p.get_vel() < 1:
                                plr = player_list[current_player]
                                arrow.reset(nxt_p)


                    if event.key == pygame.K_e:
                        editing = not editing
                        print("editing: "+ str(editing))


                    if event.key == pygame.K_RETURN:
                        if editing:
                            player_list[0].set_x(75)
                            player_list[0].set_y(HEIGHT / 2 - 50 - BALL_WIDTH / 2)
                            player_list[1].set_x(75)
                            player_list[1].set_y(HEIGHT / 2 + 50 - BALL_WIDTH / 2)
                            player_list[0].arrow.reset(player_list[0])
                        elif current_projectile is None:
                            for projectile in player_list[current_player].projectiles:
                                # if the player have golfClub projectile
                                projectile.setPosition(player_list[current_player])
                                current_projectile = projectile
                                arrow.reset(player_list[current_player])


                    if event.key == pygame.K_t:
                        game_running = False
                        replay_game = True

                    #level editing
                    if editing:
                        if event.key == pygame.K_1:
                            tracing = True
                            trace_color = BLACK
                            topleft = pygame.mouse.get_pos()

                        if event.key == pygame.K_2:
                            tracing = True
                            trace_color = GREEN
                            topleft = pygame.mouse.get_pos()

                        if event.key == pygame.K_3:
                            tracing = True
                            trace_color = YELLOW
                            topleft = pygame.mouse.get_pos()

                        if event.key == pygame.K_4:
                            tracing = True
                            trace_color = RED
                            topleft = pygame.mouse.get_pos()

                        if event.key == pygame.K_0:
                            center = pygame.mouse.get_pos()
                            box = go.RandomBox(random_img, center[0]-20, center[1]-20, images)
                            consumableList.append(box)

                        if event.key == pygame.K_BACKSPACE:
                            mp = pygame.mouse.get_pos()
                            for i in range(4, len(BOUNDARY)):
                                if mp[0] > BOUNDARY[i].x and mp[0] < BOUNDARY[i].right and mp[1] > BOUNDARY[i].y and mp[1] < BOUNDARY[i].bottom:
                                    del BOUNDARY[i]
                                    break
                            for tr in TERRAIN_LIST:
                                if mp[0] > tr.x and mp[0] < tr.x + tr.width and mp[1] > tr.y and mp[1] < tr.y + tr.height:
                                    TERRAIN_LIST.remove(tr)
                                    break
                            for item in consumableList:
                                if mp[0] > item.x and mp[0] < item.x + item.width and mp[1] > item.y and mp[1] < item.y + item.height:
                                    consumableList.remove(item)
                                    break

                        if event.key == pygame.K_s:
                            #save
                            save_level()

                        if event.key == pygame.K_r:
                            #reads level file
                            level_name = input("Please input level file name: ")
                            read_level(level_name)

                    draw_players(player_list, current_player, hole, arrow)

            # update the screen
            draw_window(force_scale)
            # set movement of projectile
            if current_projectile != None:
                if current_projectile.is_moving:
                    handle_golfClub_function(current_projectile, current_projectile.attack_object)
                    current_projectile.move()
                else:
                    if current_projectile in projectileList:
                        projectileList.remove(current_projectile)
                    current_projectile = None


            for i in range(len(player_list)):
                handle_collision_ball_consumables(player_list[i], consumableList)
                handle_terrain()
                if current_projectile is None:
                    handle_conllision_ball_projectiles(player_list[i], projectileList)
                handle_collision_ball_ball(player_list[0], player_list[1])
                move(player_list[i])

                handle_collision_ball_hole(player_list[i], hole.get_rect())


            if plr.get_vel() < 2 and plr.get_vel() != 0:
                arrow.reset(plr)
            elif plr.get_vel() > 1:
                arrow.is_visible = False

            draw_players(player_list, current_player, hole, arrow)


        if replay_game:
            if player_list[0].id == 1:
                p1 = player_list[0]
            else:
                p1 = player_list[0]
            p2 = p1.opponent
            score_1_text  = afont.render( "player 1 score: %d" %p1.score, True, BLUE)
            score_2_text = afont.render( "player 2 score: %d" %p2.score, True, BLUE )


            tr_cover = pygame.Surface((WIDTH, HEIGHT))
            tr_cover.set_alpha(130)
            tr_cover.fill(WHITE)
            screen.blit(tr_cover, (0,0))
            screen.blit(replay_text_1, (WIDTH/2 - 200, HEIGHT/2 ))
            screen.blit(replay_text_2, (WIDTH/2 - 240, HEIGHT/2 + 100))
            screen.blit(score_1_text, (WIDTH/2 - 350, HEIGHT/2 - 100))
            screen.blit(score_2_text, (WIDTH/2 + 100, HEIGHT/2 - 100))


            while replay_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            sys.exit()
                        if event.key == pygame.K_r:
                            replay_game = False
                            game_running = True
                            current_level = 1
                            current_player = 0
                            current_projectile = None

                            game_reset(True)
                            read_level("level 1.txt")
                pygame.display.update()
                gameClock.tick(FPS)



        # set FPS
        gameClock.tick(FPS)

if __name__ == "__main__":
    main(sys.argv)