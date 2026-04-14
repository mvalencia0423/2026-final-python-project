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
        self.shot_protection_timer = 0  # Prevent immediate reset after shooting
        self.has_scored = False  # Prevent duplicate scoring
        
        # Dribbling animation
        self.dribble_height = 0  # Current dribble offset
        self.dribble_speed = 0  # Dribble animation speed
        self.dribble_frame = 0  # Dribble animation frame
        self.is_dribbling = False  # Whether currently dribbling

    def shoot(self, perfect_shot, power, hoop_x=0, hoop_y=0):
        """Shoot the ball towards the hoop"""
        if not self.held:
            return
        
        self.held = False
        self.perfect_shot = perfect_shot
        self.can_score = perfect_shot
        self.shot_protection_timer = 30  # Prevent catching for 30 frames
        
        if perfect_shot:
            # Perfect shot - start from current position and move toward hoop
            self.target_hoop_x = hoop_x
            self.target_hoop_y = hoop_y
            
            # Calculate initial velocity toward hoop with more power
            dx = hoop_x - self.x
            dy = hoop_y - self.y
            distance = math.hypot(dx, dy)
            
            # Set initial velocity toward hoop with stronger power
            if distance > 0:
                self.speed_x = (dx / distance) * 12  # Increased speed
                self.speed_y = (dy / distance) * 12 - 8  # Higher arc
            else:
                self.speed_x = 0
                self.speed_y = -12
        else:
            # Imperfect shot - aim for backboard
            backboard_x = hoop_x + 20 if hoop_x else self.x + 200
            backboard_y = hoop_y if hoop_y else self.y - 50
            
            dx = backboard_x - self.x
            dy = backboard_y - self.y
            
            # Set velocities to hit backboard
            self.speed_x = dx / 25
            self.speed_y = -10
            
            # Ensure it has enough power to reach backboard
            if abs(self.speed_x) < 5:
                self.speed_x = 5 if self.speed_x >= 0 else -5

    def reset(self):
        if self.shot_protection_timer > 0:
            self.shot_protection_timer -= 1
            return
        
        self.held = True
        self.held_by = None
        self.can_score = False
        self.perfect_shot = False
        self.has_scored = False  # Reset scored flag
        self.x = self.start_x
        self.y = self.start_y
        self.speed_x = 0
        self.speed_y = 0

    def move(self):
        if self.held:
            return
            
        # Decrease shot protection timer
        if self.shot_protection_timer > 0:
            self.shot_protection_timer -= 1
            
        # Apply gravity
        self.speed_y += self.GRAVITY
        
        # Update position
        old_x, old_y = self.x, self.y
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Perfect shot correction - strongly guide to hoop
        if self.perfect_shot:
            dx = self.target_hoop_x - self.x
            dy = self.target_hoop_y - self.y
            distance = math.hypot(dx, dy)
            
            # Very aggressive correction to ensure scoring
            if distance < 150:
                # Strong guidance to ensure scoring
                correction_x = dx * 0.08  # Increased correction
                correction_y = dy * 0.05  # Increased correction
                self.speed_x += correction_x
                self.speed_y += correction_y
                
                # Ensure ball goes through hoop
                if distance < 50:
                    self.speed_y = max(self.speed_y, 3)  # Stronger downward motion
                    # Force ball toward hoop center
                    self.x += dx * 0.1
                    self.y += dy * 0.1
            else:
                # Gentle correction at distance
                correction_x = dx * 0.03
                correction_y = dy * 0.02
                self.speed_x += correction_x
                self.speed_y += correction_y
            
            # Ensure ball is always moving aggressively toward hoop
            if abs(self.speed_x) < 2:
                self.speed_x = 2 if self.target_hoop_x > self.x else -2
            if abs(self.speed_y) < 1:
                self.speed_y = 1

    def update_dribble(self, player_is_moving=False):
        """Update dribbling animation"""
        if self.held and player_is_moving:
            self.is_dribbling = True
            self.dribble_frame += 1
            
            # Dribble animation - ball bounces up and down
            if self.dribble_frame % 20 < 10:
                # Ball going down
                self.dribble_height = min(15, self.dribble_height + 2)
            else:
                # Ball coming up
                self.dribble_height = max(0, self.dribble_height - 2)
        else:
            # Stop dribbling when not moving
            self.is_dribbling = False
            self.dribble_height = 0
            self.dribble_frame = 0

    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y + self.dribble_height)  # Add dribble offset
        pygame.draw.circle(screen, self.color, (draw_x, draw_y), self.radius)
        
        # Add basketball texture lines
        pygame.draw.arc(screen, (200, 100, 0), (draw_x - self.radius, draw_y - self.radius, 
                        self.radius * 2, self.radius * 2), 0, math.pi, 2)
        pygame.draw.line(screen, (200, 100, 0), (draw_x - self.radius, draw_y), 
                        (draw_x + self.radius, draw_y), 2)
        pygame.draw.line(screen, (200, 100, 0), (draw_x, draw_y - self.radius), 
                        (draw_x, draw_y + self.radius), 2)