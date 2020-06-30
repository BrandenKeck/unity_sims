import pygame
import numpy as np

class player():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25*x
        self.pos_y = 25*y
        self.target_pos_x = 25*x
        self.target_pos_y = 25*y

    def decide_move(self):
        if np.random.random(1)[0] < 0.001:
            self.player.set_target(1, 0)

    def move(self):
        if (self.pos_x != self.target_pos_x or self.pos_y != self.target_pos_y):
            self.pos_x = self.pos_x + np.sign(self.target_pos_x - self.pos_x)
            self.pos_y = self.pos_y + np.sign(self.target_pos_y - self.pos_y)
        else:
            self.x = self.target_x
            self.y = self.target_y

    def set_target(self, dx, dy):
        self.target_pos_x = self.pos_x + 25 * dx
        self.target_x = self.x + 1 * dx

        self.target_pos_y = self.pos_y + 25 * dy
        self.target_y = self.y + 1 * dy

    def draw(self, window):
        pygame.draw.rect(window, (0,0,255), (self.pos_x, self.pos_y, 25, 25))

class goal():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos_x = 25*x
        self.pos_y = 25*y

    def draw(self, window):
        pygame.draw.rect(window, (50, 255, 50), (self.pos_x, self.pos_y, 25, 25))

class world():

    def __init__(self):
        players = []
        goals = []

    def add_player(self, x, y):
        self.players.append(player(x,y))

    def add_goal(self, x, y):
        self.players.append(goal(x,y))


if __name__ == "__main__":
    
    # Initialize game state
    run = True
    ticker = 0
    
    # Board size
    width = 1000
    height = 1000
    
    # Initialize game
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("grid game")

    # Initialize player
    p1 = player(1, 2)
    agent = agent(p1)
    
    # Start the game loop
    while run:

        # Refresh window
        pygame.time.delay(10)
        pygame.draw.rect(window, (0,0,0), (0, 0, width, height))

        # Show actions
        agent.decide_move()
        p1.move()
        p1.draw(window)

        # Iterate game ticker
        ticker = ticker + 1
        if ticker>60:
            ticker = 0
        

            
        pygame.display.update()        
                   
    pygame.quit()