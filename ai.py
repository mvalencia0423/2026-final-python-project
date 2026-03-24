import pygame
import random

class AI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = (100, 100, 200)  # Modern blue jersey
        self.skin_color = (255, 195, 140)  # Medium skin tone
        self.speed = 3

    def move(self):
        direction = random.choice(["up","down","left","right"])

        if direction == "up":
            self.y -= self.speed
        if direction == "down":
            self.y += self.speed
        if direction == "left":
            self.x -= self.speed
        if direction == "right":
            self.x += self.speed

    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Modern 2026 Xbox basketball player appearance
        
        # Modern basketball shoes (detailed)
        pygame.draw.ellipse(screen, (0, 0, 0), (draw_x + 5, draw_y + 50, 12, 8))
        pygame.draw.ellipse(screen, (255, 255, 255), (draw_x + 5, draw_y + 50, 12, 2))  # Shoe stripe
        pygame.draw.ellipse(screen, (0, 0, 0), (draw_x + 23, draw_y + 50, 12, 8))
        pygame.draw.ellipse(screen, (255, 255, 255), (draw_x + 23, draw_y + 50, 12, 2))  # Shoe stripe
        
        # Modern basketball shorts (longer, baggier)
        pygame.draw.rect(screen, self.color, (draw_x + 8, draw_y + 30, 24, 25))
        pygame.draw.rect(screen, (255, 255, 255), (draw_x + 8, draw_y + 30, 24, 2))  # Shorts trim
        # Shorts side stripes
        pygame.draw.rect(screen, (255, 255, 255), (draw_x + 10, draw_y + 32, 2, 20))
        pygame.draw.rect(screen, (255, 255, 255), (draw_x + 28, draw_y + 32, 2, 20))
        
        # Modern basketball jersey (tank top style)
        pygame.draw.rect(screen, self.color, (draw_x + 10, draw_y + 15, 20, 20))
        # Jersey arm holes (rounded)
        pygame.draw.ellipse(screen, (64, 64, 64), (draw_x + 5, draw_y + 17, 8, 10))  # Left armhole
        pygame.draw.ellipse(screen, (64, 64, 64), (draw_x + 27, draw_y + 17, 8, 10))  # Right armhole
        
        # Jersey number
        font = pygame.font.SysFont("arial", 12, bold=True)
        number_text = font.render("45", True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(draw_x + 20, draw_y + 25))
        screen.blit(number_text, number_rect)
        
        # Muscular arms
        # Left arm
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 2, draw_y + 18, 8, 20))
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 1, draw_y + 35, 6, 10))  # Forearm
        # Right arm
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 30, draw_y + 18, 8, 20))
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 33, draw_y + 35, 6, 10))  # Forearm
        
        # Modern hands with fingers
        # Left hand
        pygame.draw.ellipse(screen, self.skin_color, (draw_x, draw_y + 42, 8, 8))
        for i, offset in enumerate([-3, -1, 1]):
            pygame.draw.ellipse(screen, self.skin_color, (draw_x + offset, draw_y + 47, 2, 3))
        # Right hand
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 32, draw_y + 42, 8, 8))
        for i, offset in enumerate([-3, -1, 1]):
            pygame.draw.ellipse(screen, self.skin_color, (draw_x + 34 + offset, draw_y + 47, 2, 3))
        
        # Detailed head (realistic proportions)
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 12, draw_y + 5, 16, 12))
        
        # Modern hair (short fade)
        pygame.draw.ellipse(screen, (0, 0, 0), (draw_x + 11, draw_y + 3, 18, 10))
        pygame.draw.ellipse(screen, self.skin_color, (draw_x + 13, draw_y + 5, 14, 8))  # Fade effect
        
        # Facial features
        pygame.draw.ellipse(screen, (50, 50, 50), (draw_x + 15, draw_y + 8, 2, 2))  # Left eye
        pygame.draw.ellipse(screen, (50, 50, 50), (draw_x + 23, draw_y + 8, 2, 2))   # Right eye
        
        # Modern basketball accessories
        # Wristbands
        pygame.draw.rect(screen, (255, 0, 0), (draw_x, draw_y + 38, 6, 2))
        pygame.draw.rect(screen, (255, 0, 0), (draw_x + 34, draw_y + 38, 6, 2))
        # Headband
        pygame.draw.rect(screen, (0, 0, 0), (draw_x + 12, draw_y + 4, 16, 2))