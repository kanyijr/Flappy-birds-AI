import pygame
import neat
import time
import os 
import random
pygame.font.init()

'''
This is a player-controlled implementation of Flappy Bird using Pygame.
Run this file by typing 'python flappy_player.py' in the terminal.
Make sure your working directory is flappy-bird.

Controls:
- Press any key to make the bird jump
- Try to navigate through the pipes without hitting them
- Score increases as you successfully pass through pipes
- Game ends if you hit a pipe or the ground
'''

# Window dimensions
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Load and scale bird animation images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

# Load and scale game assets
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

# Font for score display
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird():
    """Bird class that handles bird movement, animation and physics"""
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # Maximum rotation angle
    ROT_VEL = 20      # Rotation velocity
    ANIMATION_TIME = 5 # How long each animation frame lasts

    def __init__(self, x, y):
        """Initialize bird at given position"""
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """Make bird jump by setting upward velocity"""
        self.vel = -7.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        """Handle bird physics for movement"""
        self.tick_count += 1

        # Calculate displacement using physics equation
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        if d >= 16:
            d =16
        elif d < 0:
            d -= 2           
        self.y += d

        # Handle bird tilt based on movement
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
               self.tilt = self.MAX_ROTATION   
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Handle bird animation and drawing"""
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < (self.ANIMATION_TIME*2):
            self.mg = self.IMGS[1]  
        elif self.img_count < (self.ANIMATION_TIME * 3):
            self.mg = self.IMGS[2]   
        elif self.img_count < (self.ANIMATION_TIME * 4):
            self.mg = self.IMGS[1]   
        elif self.img_count == ((self.ANIMATION_TIME * 4) + 1):
            self.mg = self.IMGS[0]
            self.img_count = 0               

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2                        
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Get mask for collision detection"""
        return pygame.mask.from_surface(self.img)

class Pipe():
    """Class representing the pipes obstacles"""
    GAP = 200  # Gap between top and bottom pipes
    VEL = 5    # Pipe movement velocity

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        
        self.top = 0
        self.bottom = 0    
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):
        """Randomly set pipe heights"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
  
    def move(self):
        """Move pipe towards the left"""
        self.x -= self.VEL 
    
    def draw(self, win):
        """Draw both top and bottom pipes"""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """Check if bird collides with pipes using mask collision"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    """Class representing the moving ground"""
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Move ground to create infinite scrolling effect"""
        self.x1 -= self.VEL
        self.x2 -=self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2  + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH  
    
    def draw(self, win):
        """Draw the ground"""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
def draw_window(win, bird, pipes, base, score):
    """Draw all game elements to the window"""
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: "+ str(score), 1, (255, 255, 255))    
    win.blit(text, (WIN_WIDTH-10 - text.get_width(), 1))
    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()

def main():
    """Main game loop"""
    nets = []
    ge = []
    bird = Bird(200, 350)
   
    base = Base(730)
    pipes = [Pipe(700)]
    win  = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run  = True
    score = 0
    add_pipe = False
    to_jump = True 

    while run:
        clock.tick(30)
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
              
            if  pygame.key.get_pressed and to_jump == True:
                bird.jump()    
       
        rem =[]  
            
        for pipe in pipes:
          
                if pipe.collide(bird) or bird.y + bird.img.get_height() >= 730:
                    score = "YOU FAILED"
                    to_jump = False

                if not pipe.passed and pipe.x < bird.x and bird.y + bird.img.get_height()  < 730:
                    pipe.passed = True  
                    score += 1 
                    
                    pipes.append(Pipe(700))    
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                  rem.append(pipe)
               
                pipe.move()
        
        if add_pipe:
            score += 1  
            pipes.append(Pipe(700))
        
        for r in rem:
            pipes.remove(r) 
       
        bird.move()
        base.move()
        draw_window(win, bird, pipes, base, score)        
   
main()
 