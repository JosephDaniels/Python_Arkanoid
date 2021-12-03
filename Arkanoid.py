import pygame
import random
import time
import sys
import tkinter

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

PONG_SOUND = "sounds/noisecollector_pongblip_f-5.wav"
LEVEL_COMPLETE_SOUND = "sounds/game-level-completed.wav"
LOSE_A_LIFE_SOUND = "sounds/failure_alert.wav"
GAME_OVER_SOUND = "sounds/game-over.wav"
POWER_UP_SOUND = "sounds/power-up.wav"

VALID_BRICK_TYPES = ["1","2","3","4","5","6","X","S"]

BRICK_HEIGHT, BRICK_WIDTH = (40, 80)

NORMAL_BALL_SIZE, SMALL_BALL_SIZE = (15,7)

BRICK_TYPE_IMAGES = {
    "1"   :   "light_brick.png",
    "2"   :   "dark_brick.png",
    "3"   :   "blue_brick.png",
    "4"   :   "green_brick.png",
    "5"   :   "purple_brick.png",
    "6"   :   "red_brick.png",
    "X"   :   "black_brick.png",
    "S"   :   "special_brick.png"
    }

class Arkanoid_Game_Manager(object):
    """ Handles all the game objects,
        and manages all the game stuff!!!"""
    def __init__(self):

        ## Add Game Objects
        self.paddle = Paddle(SCREEN_WIDTH/2,
                             SCREEN_HEIGHT-20)
        self.ball = None
        self.spawn_ball()
        self.power_ups = []

        ## Game Data
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bounds = self.screen.get_rect()
        self.running = False
        self.game_over = True

        ## Sound Data
        pygame.mixer.init()
        self.power_up_sound = pygame.mixer.Sound(POWER_UP_SOUND)
        self.pong_sound = pygame.mixer.Sound(PONG_SOUND)
        self.level_complete_sound = pygame.mixer.Sound(LEVEL_COMPLETE_SOUND)
        self.lose_a_life_sound = pygame.mixer.Sound(LOSE_A_LIFE_SOUND)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

        ## Level Data
        self.current_level = 0
        self.bricks = []

        ## Player Data
        self.score = 0
        self.score_text = "Welcome to Python Arkanoid"
        self.lives = 3  # Three lives then its game over!
        self.continues = 0  # The number of times the player had to restart

        pygame.init()
        pygame.display.set_caption("Python Arkanoid by Jordan Vo")

    def load_level(self):
        filename = "levels/level%i.txt" % (self.current_level)
        level_file = open(filename, mode="r")
        rows = 0
        columns = 3
        for line in level_file:
            line = line.strip()
            for brick in line:
                if brick == "0":
                    rows+=1
                elif brick in VALID_BRICK_TYPES:
                    brick = Brick(rows*BRICK_WIDTH,
                                  columns*BRICK_HEIGHT,
                                  brick)
                    self.add_brick(brick)
                    rows+=1
            rows=0
            columns+=1
        print ("Level finished loading.")

    def do_game_loop(self):
        while self.running == True:
            self.tick()

    def start_game(self):
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        pygame.mouse.set_visible(False)
        ## Make the First level
        self.game_over = False
        self.running = True
        self.do_game_loop()

    def destroy_level(self):
        self.bricks = []

    def restart(self):
        self.game_over = False
        self.continues += 1
        self.score = 0
        self.lives = 3
        self.update_score()
        self.destroy_level()
        self.load_level()
        self.paddle = Paddle(SCREEN_WIDTH/2,
                             SCREEN_HEIGHT-50)
        self.running = True
        self.do_game_loop()

    def spawn_ball(self):
        self.ball = Ball(SCREEN_WIDTH/2,
                         SCREEN_HEIGHT-80)

    def add_brick(self, brick):
        self.bricks.append(brick)

    def remove_brick(self, brick):
        if brick in self.bricks:
            self.bricks.remove(brick)

    def update_score(self):
        self.score_text = str(self.score)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print ("Thanks for playing!!!")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    self.paddle.move_right()
                if event.key == pygame.K_LEFT:
                    self.paddle.move_left()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.do_throw_ball()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.paddle.stop_move_right()
                if event.key == pygame.K_LEFT:
                    self.paddle.stop_move_left()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                self.paddle.set_pos(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print ("left click")
                    self.do_throw_ball()
                elif event.button == 3:
                    print ("right click")
                    self.next_level()

    def show_win_screen(self):
        self.paddle.disabled = True
        win_game_text = "You have won the game!!! Score was: %i"% (self.score)
        sub_text = "It only took you %i continues to beat the game." % (self.continues)
        main_font = pygame.font.Font('freesansbold.ttf', 72)
        sub_font = pygame.font.Font('freesansbold.ttf', 32)
        
        main_text = main_font.render(win_game_text, True, green, blue)
        main_textRect = main_text.get_rect()
        main_textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        
        text = sub_font.render(sub_text, True, green, blue)
        sub_textRect = text.get_rect()
        sub_textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + main_textRect.height)
        
        self.screen.blit(main_text, main_textRect)
        self.screen.blit(text, sub_textRect)

    def show_game_over_screen(self):
        self.paddle.disabled = True
        game_over_text = "Game over!!! Score was: %i"% (self.score)
        sub_text = "Left click to restart..."
        main_font = pygame.font.Font('freesansbold.ttf', 72)
        sub_font = pygame.font.Font('freesansbold.ttf', 32)
        
        main_text = main_font.render(game_over_text, True, green, blue)
        main_textRect = main_text.get_rect()
        main_textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        
        text = sub_font.render(sub_text, True, green, blue)
        sub_textRect = text.get_rect()
        sub_textRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + main_textRect.height)
        
        self.screen.blit(main_text, main_textRect)
        self.screen.blit(text, sub_textRect)

    def lose_a_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.game_over = True
            self.game_over_sound.play()

    def do_throw_ball(self):
        if self.ball:
            if self.ball.thrown == True:
                pass
            else:
                self.ball.throw_ball()
                self.update_score()
        elif self.ball == None:
            if self.game_over == True:
                self.restart()
            else:
                self.spawn_ball()

    def handle_the_ball(self):
        if self.ball:
            self.ball.update()
            self.screen.blit(self.ball.image, (self.ball.x,
                                               self.ball.y))
            if self.ball.thrown == False:
                self.ball.x = self.paddle.x + self.paddle.center_x - self.ball.center_x
            elif self.ball.thrown == True:
                if self.ball.x < self.bounds.left or self.ball.x + self.ball.image.get_width() > self.bounds.right:
                    self.ball.vx *= -1
                elif self.ball.y - self.ball.center_y < self.bounds.top:
                    self.ball.vy *= -1
                elif self.ball.y + self.ball.center_y > self.bounds.bottom:
                    self.ball = None
                    self.lose_a_life()
                    self.lose_a_life_sound.play()
                    print ("You lost the ball!")

    def display_score(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.score_text, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH/2, 50)
        self.screen.blit(text, textRect)

    def display_lives(self):
        _str = "Lives: %i" % (self.lives)
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(_str, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH-100, 50)
        self.screen.blit(text, textRect)

    def next_level(self):
        self.level_complete_sound.play()
        self.current_level += 1
        self.destroy_level()
        self.load_level()

    def drop_powerup(self, position):
        choices = ["power_up","power_down"]
        #drop_type = random.choice(choices)
        drop_type = "power_down"
        if drop_type == "power_up":
            power_up = PowerUp(position[0],position[1])
            self.power_ups.append(power_up)
        elif drop_type == "power_down":
            power_down = PowerDown(position[0],position[1])
            self.power_ups.append(power_down)

    def handle_brick_collision(self, brick):
        if brick.brick_type == "1":
            self.remove_brick(brick)
        elif brick.brick_type == "X":
            pass
        elif brick.brick_type == "S":
            self.remove_brick(brick)
            pos = brick.x+brick.image.get_width()/2, brick.y+brick.image.get_height()/2
            self.drop_powerup(pos)
        elif int(brick.brick_type) in [2,3,4,5,6]:
            new_brick_type = int(brick.brick_type)-1
            brick.set_brick_type(str(new_brick_type))
        self.ball.vy *= -1

    def power_up(self):
        self.paddle.grow_bigger()
        self.power_up_sound.play()
        
    def tick(self):
        ## DISPLAY CURRENT BACKGROUND
        self.screen.fill((0,0,100))
        
        ## EVENT LOOP
        self.handle_events()

        ## DISPLAY THE paddle
        self.paddle.update()
        self.screen.blit(self.paddle.image, (self.paddle.x,
                                             self.paddle.y))

        ## DISPLAY THE BALL
        if self.ball:
            self.handle_the_ball()

        ## DISPLAY THE BRICKS
        for brick in self.bricks:
            self.screen.blit(brick.image,
                             (brick.x, brick.y))

        ## DISPLAY THE POWERUPS
        for power_up in self.power_ups:
            power_up.update()
            self.screen.blit(power_up.image,
                             (power_up.x, power_up.y))

        ## DISPLAY LIVES
        self.display_lives()

        ## DISPLAY THE SCORE
        self.display_score()

        ## DISPLAY THE GAME OVER SCREEN
        if self.game_over == True:
            self.show_game_over_screen()
            self.paddle.disabled = True
            
        ## HANDLE COLLISIONS
        if self.ball:
            if self.ball.is_collided_with(self.paddle):
                self.ball.vy *= -1
            for brick in self.bricks:
                if self.ball.is_collided_with(brick):
                    self.handle_brick_collision(brick)
                    self.score += 500
                    self.update_score()
                    self.pong_sound.play()
                    if self.bricks == []:
                        self.next_level()
        if self.power_ups != []:
            for power_up in self.power_ups:
                if power_up.is_collided_with(self.paddle):
                    self.power_ups.remove(power_up)
                    print ("POWER UP!")
                    self.power_up()
        pygame.display.flip()
        time.sleep(0.01)

class Game_Object(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_file = ""

    def get_rect(self):
        self.rect = self.image.get_rect()
        return self.rect

    def load_image(self):
        self.image = pygame.image.load(self.image_file)

    def is_collided_with(self, target):
        rect1 = self.image.get_rect()
        rect1.topleft = (self.x,self.y)
        rect2 = target.image.get_rect()
        rect2.topleft = (target.x, target.y)
        return rect1.colliderect(rect2)

class PowerUp(Game_Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image_file = "images/powerup.png"
        self.load_image()
        self.vy = 9.8
        self.image = pygame.transform.scale(self.image, (80, 30))

    def update(self):
        self.y += self.vy

class PowerDown(Game_Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image_file = "images/powerdown.png"
        self.load_image()
        self.vy = 9.8
        self.image = pygame.transform.scale(self.image, (80, 30))

    def update(self):
        self.y += self.vy

class Brick(Game_Object):
    def __init__(self, x, y, brick_type):
        super().__init__(x, y)
        self.brick_type = brick_type
        self.brick_images = {}
        self.load_all_brick_images()
        self.image = self.brick_images[self.brick_type]
        
    def __str__(self):
        return ("Brick Object @ (%i, %i)" % (self.x, self.y))

    def set_brick_type(self, new_brick_type):
        prev_brick_type = self.brick_type
        self.brick_type = new_brick_type
        self.image = self.brick_images[self.brick_type]

    def load_all_brick_images(self):
        for brick_type in BRICK_TYPE_IMAGES.keys():
            filename = "images/"+BRICK_TYPE_IMAGES[brick_type]
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (BRICK_WIDTH, BRICK_HEIGHT))
            self.brick_images[brick_type] = image

class Paddle(Game_Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_positions = []  # A list with the last 5 positions
        self.disabled = False
        self.dx = 0  # Calculates on update
        self.vx = 0
        self.image_file = "images/arkanoid_paddle.png"
        self.load_image()
        self.image = pygame.transform.scale(self.image, (100, 25))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def shrink_smaller(self):
        self.image = pygame.transform.scale(self.image, (50, 25))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def grow_bigger(self):
        self.image = pygame.transform.scale(self.image, (150, 25))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def move_right(self):
        self.vx += 15

    def move_left(self):
        self.vx -= 15

    def stop_move_right(self):
        self.vx -= 15

    def stop_move_left(self):
        self.vx += 15

    def set_pos(self, pos):
        if self.disabled != True:
            if pos[0] <= 0 + self.center_x:
                self.x = 0
            elif pos[0] >= SCREEN_WIDTH - self.center_x:
                self.x = SCREEN_WIDTH - self.image.get_width()
            elif pos[0] > 0 and pos[0] < SCREEN_WIDTH - self.center_x:
                self.x = pos[0] - self.center_x
##        self.y = pos[1] - self.center_y

    def update(self):
        if self.disabled != True:
            self.x += self.vx
        
class Ball(Game_Object):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.vx = 0
        self.vy = 0
        self.thrown = False
        self.image_file = "images/arkanoid_ball.png"
        self.load_image()
        self.image = pygame.transform.scale(self.image, (NORMAL_BALL_SIZE, NORMAL_BALL_SIZE))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def throw_ball(self):
        self.thrown = True
        self.vx = 7
        self.vy = -7

    def update(self):
        self.x += self.vx
        self.y += self.vy

def test_1(): # Test a single brick
    game = Arkanoid_Game_Manager()
    brick = Brick(0,0)
    game.add_brick(brick)
    game.start_game()

def test_2(): # Level testing
    game = Arkanoid_Game_Manager()
    game.load_level()
    game.start_game()

if __name__ == "__main__":
    test_2()
