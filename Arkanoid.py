import pygame
import random
import time
import sys

# Define constants for the screen width and height
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

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
        self.bricks = []
        self.running = False

    def do_game_loop(self):
        while self.running == True:
            self.tick()

    def start_game(self):
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        pygame.init()
##        pygame.mouse.set_visible(False)
        self.running = True
        self.do_game_loop( )

    def spawn_ball(self):
        self.ball = Ball(SCREEN_WIDTH/2,
                         SCREEN_HEIGHT-100)

    def destroy_ball(self):
        self.ball = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEMOTION:
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
                    elif self.ball == None:
                        self.spawn_ball()
                elif event.button == 3:
                    print ("right click")

    def handle_the_ball(self):
        if self.ball:
            self.ball.update()
            self.screen.blit(self.ball.image, (self.ball.x,
                                               self.ball.y))
            if self.ball.thrown == False:
                self.ball.x = self.paddle.x + self.paddle.center_x/2
            elif self.ball.thrown == True:
                if self.ball.x < self.bounds.left or self.ball.x + self.ball.image.get_width() > self.bounds.right:
                    self.ball.vx *= -1
                elif self.ball.y - self.ball.center_y < self.bounds.top:
                    self.ball.vy *= -1
                elif self.ball.y + self.ball.center_y > self.bounds.bottom:
                    self.destroy_ball()
                    print ("You lost the ball!")

    def tick(self):
        ## DISPLAY CURRENT BACKGROUND
        self.screen.fill((0,0,100))
        
        ## EVENT LOOP
        self.handle_events()

        ## DISPLAY THE paddle
        self.screen.blit(self.paddle.image, (self.paddle.x,
                                             self.paddle.y))
        ## DISPLAY THE BALL
        if self.ball:
            self.handle_the_ball()

##        for brick in self.bricks:
##            brick.update()

        ## HANDLE COLLISIONS
        if self.ball:
            if self.ball.is_collided_with(self.paddle):
                self.ball.vy *= -1
        pygame.display.flip()
        time.sleep(0.01)

class Paddle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.load_image()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def get_rect(self):
        self.rect = self.image.get_rect()
        return self.rect

    def set_pos(self, pos):
        if pos[0] <= 0 + self.center_x:
            self.x = 0
        elif pos[0] >= SCREEN_WIDTH - self.center_x:
            self.x = SCREEN_WIDTH - self.image.get_width()
        elif pos[0] > 0 and pos[0] < SCREEN_WIDTH - self.center_x:
            self.x = pos[0] - self.center_x
##        self.y = pos[1] - self.center_y
        
    def load_image(self):
        image = pygame.image.load("images/arkanoid_paddle.png")
        self.image = pygame.transform.scale(image, (100, 50))
        
class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.thrown = False
        self.load_image()
        self.center_x = (self.image.get_width()/2)
        self.center_y = (self.image.get_height()/2)

    def throw_ball(self):
        self.thrown = True
        self.vx = 5
        self.vy = -5

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def get_rect(self):
        self.rect = self.image.get_rect()
        return self.rect
    
    def load_image(self):
        image = pygame.image.load("images/arkanoid_ball.png")
        self.image = pygame.transform.scale(image, (50, 50))

    def is_collided_with(self, target):
        rect1 = self.image.get_rect()
        rect1.topleft = (self.x,self.y)
        rect2 = target.image.get_rect()
        rect2.topleft = (target.x, target.y)
        return rect1.colliderect(rect2)

def test_game():
    print ("Game was test.")
    game = Arkanoid_Game_Manager()
    game.start_game()

if __name__ == "__main__":
    test_game()
