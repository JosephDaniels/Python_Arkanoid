import pygame
import random
import time
import sys
import tkinter

# Define constants for the screen width and height
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

PONG_SOUND = "sounds/noisecollector_pongblip_f-5.wav"
LEVEL_COMPLETE_SOUND = "sounds/game-level-completed.wav"
LOSE_A_LIFE_SOUND = "sounds/failure_alert.wav"
GAME_OVER_SOUND = "sounds/game-over.wav"

class Arkanoid_Game_Manager(object):
    """ Handles all the game objects,
        and manages all the game stuff!!!"""
    def __init__(self):
        self.paddle = Paddle(SCREEN_WIDTH/2,
                             SCREEN_HEIGHT-50)
        self.ball = None
        self.spawn_ball()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bounds = self.screen.get_rect()

        pygame.init()
        pygame.display.set_caption("Python Arkanoid by Jordan Vo")


        ## Game Data
        self.running = False
        self.game_over = True

        ## Sound Data
        pygame.mixer.init()
        self.pong_sound = pygame.mixer.Sound(PONG_SOUND)
        self.level_complete_sound = pygame.mixer.Sound(LEVEL_COMPLETE_SOUND)
        self.lose_a_life_sound = pygame.mixer.Sound(LOSE_A_LIFE_SOUND)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

        ## Level Data
        self.current_level = 0
        self.bricks = []

        ## Player Data
        self.score = 0
        self.score_text = "Welcome to Pygame Arkanoid"
        self.lives = 3  # Three lives then its game over!

    def load_level(self):
        filename = "levels/level%i.txt" % (self.current_level)
        level_file = open(filename, mode="r")
        rows = 0
        columns = 0
        for line in level_file:
            line = line.strip()
            for brick in line:
                if brick == "0":
                    rows+=1
                elif brick == "1":
                    brick = Brick(rows*125, columns*62)
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
            elif event.type == pygame.MOUSEMOTION:
                if self.paddle:
                    mouse_pos = event.pos
                    self.paddle.set_pos(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print ("left click")
                    if self.ball:
                        if self.ball.thrown == True:
                            pass
                        else:
                            self.ball.throw_ball()
                            self.update_score()
                    elif self.ball == None:
                        if self.paddle == None:
                            self.restart()
                        else:
                            self.spawn_ball()
                elif event.button == 3:
                    print ("right click")
                    self.next_level()

    def show_game_over_screen(self):
        self.paddle = None
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

    def next_level(self):
        self.level_complete_sound.play()
        self.current_level += 1
        self.load_level()

    def tick(self):
        ## DISPLAY CURRENT BACKGROUND
        self.screen.fill((0,0,100))
        
        ## EVENT LOOP
        self.handle_events()

        ## DISPLAY THE paddle
        if self.paddle:
            self.screen.blit(self.paddle.image, (self.paddle.x,
                                                 self.paddle.y))
        ## DISPLAY THE BALL
        if self.ball:
            self.handle_the_ball()

        ## DISPLAY THE BRICKS
        for brick in self.bricks:
            self.screen.blit(brick.image, (brick.x,
                                           brick.y))

        ## DISPLAY THE SCORE
        self.display_score()

        if self.game_over == True:
            self.show_game_over_screen()
            self.paddle = None
            
        ## HANDLE COLLISIONS
        if self.ball:
            if self.ball.is_collided_with(self.paddle):
                self.ball.vy *= -1
            for brick in self.bricks:
                if self.ball.is_collided_with(brick):
                    self.remove_brick(brick)
                    self.ball.vy *= -1
                    print ("Hit a brick!")
                    self.score += 500
                    self.update_score()
                    self.pong_sound.play()
                    if self.bricks == []:
                        self.next_level()
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

class Brick(Game_Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image_file = "images/arkanoid_brick.png"
        self.load_image()
        self.image = pygame.transform.scale(self.image, (125, 62))

    def __str__(self):
        return ("Brick Object @ (%i, %i)" % (self.x, self.y))

class Paddle(Game_Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image_file = "images/arkanoid_paddle.png"
        self.load_image()
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def set_pos(self, pos):
        if pos[0] <= 0 + self.center_x:
            self.x = 0
        elif pos[0] >= SCREEN_WIDTH - self.center_x:
            self.x = SCREEN_WIDTH - self.image.get_width()
        elif pos[0] > 0 and pos[0] < SCREEN_WIDTH - self.center_x:
            self.x = pos[0] - self.center_x
##        self.y = pos[1] - self.center_y
        
class Ball(Game_Object):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.vx = 0
        self.vy = 0
        self.thrown = False
        self.image_file = "images/arkanoid_ball.png"
        self.load_image()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.get_rect()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def throw_ball(self):
        self.thrown = True
        self.vx = 10
        self.vy = -10

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
