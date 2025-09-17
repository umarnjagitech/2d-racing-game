import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Test")
    
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Fill the screen with white
        screen.fill(WHITE)
        
        # Draw a red rectangle
        pygame.draw.rect(screen, RED, (350, 250, 100, 100))
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
