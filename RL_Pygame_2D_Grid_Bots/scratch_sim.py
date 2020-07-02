import pygame
from gridworld import world

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
    thisWorld = world(width, height)
    thisWorld.add_player(2, 4)
    thisWorld.add_player(2, 6)
    thisWorld.add_player(2, 10)
    thisWorld.add_goal(8, 8)
    
    # Start the game loop
    while run:

        # Refresh window
        pygame.time.delay(10)
        pygame.draw.rect(window, (0, 0, 0), (0, 0, width, height))

        # Agent Actions
        thisWorld.learn()
        thisWorld.draw(window)

        # Update Display
        pygame.display.update()

        # Exit on Esc
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False


    pygame.quit()