import pygame
import math

class Ball:
    GRAVITY = 0.3

    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255,140,0)
        self.speed_x = 0
        self.speed_y = 0
        self.held = True
        self.held_by = None  # Track which player is holding the ball
        self.can_score = False
        self.perfect_shot = False
        self.target_hoop_x = 0
        self.target_hoop_y = 0

    def shoot(self, perfect_shot: bool, power: float, hoop_x=None, hoop_y=None):
        if not self.held:
            return
        
        # Release the ball
        self.held = False
        self.held_by = None
        self.perfect_shot = perfect_shot
        self.can_score = perfect_shot
        
        if perfect_shot and hoop_x is not None and hoop_y is not None:
            # Perfect shot - calculate controlled trajectory to hoop
            self.target_hoop_x = hoop_x
            self.target_hoop_y = hoop_y
            
            # Calculate distance to hoop
            dx = hoop_x - self.x
            dy = hoop_y - self.y
            
            # Set moderate velocities - much lower power
            self.speed_x = dx / 40  # Much slower horizontal speed
            self.speed_y = -8  # Fixed upward arc for all distances
            
            # Ensure reasonable minimum power
            if abs(self.speed_x) < 3:
                self.speed_x = 3 if self.speed_x >= 0 else -3
            
        else:
            # Regular shot - much weaker power
            base_x = 4  # Much lower
            base_y = -6  # Much lower
            multiplier = max(0.2, min(power, 0.8))  # Reduced max power
            self.speed_x = base_x * multiplier
            self.speed_y = base_y * multiplier

    def reset(self):
        self.held = True
        self.held_by = None
        self.can_score = False
        self.perfect_shot = False
        self.x = self.start_x
        self.y = self.start_y
        self.speed_x = 0
        self.speed_y = 0

    def move(self):
        if self.held:
            return
            
        # Apply gravity
        self.speed_y += self.GRAVITY
        
        # Update position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Perfect shot correction - gently guide to hoop
        if self.perfect_shot:
            dx = self.target_hoop_x - self.x
            dy = self.target_hoop_y - self.y
            
            # Gentle correction
            self.speed_x += dx * 0.02
            self.speed_y += dy * 0.01

    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y)
        pygame.draw.circle(screen, self.color, (draw_x, draw_y), self.radius)
        
        # Add basketball texture lines
        pygame.draw.arc(screen, (200, 100, 0), (draw_x - self.radius, draw_y - self.radius, 
                        self.radius * 2, self.radius * 2), 0, math.pi, 2)
        pygame.draw.line(screen, (200, 100, 0), (draw_x - self.radius, draw_y), 
                        (draw_x + self.radius, draw_y), 2)
        pygame.draw.line(screen, (200, 100, 0), (draw_x, draw_y - self.radius), 
                        (draw_x, draw_y + self.radius), 2)