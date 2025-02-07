import pygame
import neat
import time
import os 
import random
pygame.font.init()

'''
This is an AI implementation of Flappy Bird using the NEAT algorithm.
Run this file by typing 'python flappy_AI.py' in the terminal.
Make sure your working directory is flappy-bird.
'''

# Window dimensions
WIN_WIDTH = 500
WIN_HEIGHT = 800
GENS = 0  # Track number of generations

# Load and scale bird animation images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))), 
             pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))), 
             pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

# Load and scale game assets
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

# Font for score display
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird():
    """
    Bird class that handles bird movement, animation and physics
    """
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
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        """Handle bird physics for movement"""
        self.tick_count += 1

        # Calculate displacement using physics equation
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        # Terminal velocity
        if d >= 16:
            d = 16
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
        """Draw bird with animation and rotation"""
        self.img_count += 1

        # Handle animation cycle
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

        # Don't flap wings when nose diving
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2                        
        
        # Rotate image around center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Get mask for collision detection"""
        return pygame.mask.from_surface(self.img)

class Pipe():
    """Class to represent obstacles (pipes)"""
    GAP = 200  # Gap between pipes
    VEL = 5    # Pipe movement speed

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
        """Move pipe left across screen"""
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
    """Class for moving ground/base"""
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
        self.x2 -= self.VEL

        # Reset positions when off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH  
    
    def draw(self, win):
        """Draw both ground images"""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
def draw_window(win, birds, pipes, base, score):
    """Draw all game elements to the window"""
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: "+ str(score), 1, (255, 255, 255))  
    gens = STAT_FONT.render("GEN: " + str(GENS), 1, (255, 255, 255))
    win.blit(gens, (5, 1))  
    win.blit(text, (WIN_WIDTH-10 - text.get_width(), 1))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes, config):
    """Main game loop and NEAT algorithm implementation"""
    global GENS
    GENS += 1
    
    # Setup neural networks and genomes
    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0
    add_pipe = False

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Find which pipe to focus on
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes)>1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
             run = False
             break       

        # Move birds and calculate fitness
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # Neural network input and decision making
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()     

        rem = []        
        for pipe in pipes:
            for x, bird in enumerate(birds):
                # Check collisions and remove birds
                if pipe.collide(bird):
                   ge[x].fitness -= 1
                   birds.pop(x)
                   nets.pop(x)
                   ge.pop(x)
                
                # Add score and new pipe when passed
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True  
                    score += 1 
                    ge[x].fitness += 5 
                    pipes.append(Pipe(700))    
            
            # Remove pipes that are off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                 
            pipe.move()
        
        if add_pipe:
            score += 1  
            pipes.append(Pipe(700))
        
        # Remove marked pipes
        for r in rem:
            pipes.remove(r) 

        # Remove birds that hit ground or go too high
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        bird.move()
        base.move()
        draw_window(win, birds, pipes, base, score)        

def run(config_path):
    """Setup and run NEAT algorithm"""
    config = neat.Config(neat.DefaultGenome,
                        neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, 
                        neat.DefaultStagnation, 
                        config_path)
   
    # Create population and add reporters
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations
    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
