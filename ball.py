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

    def shoot(self, perfect_shot: bool, power: float, hoop_x=None, hoop_y=None):
        print(f"Ball.shoot called with perfect_shot={perfect_shot}, power={power}, hoop_x={hoop_x}, hoop_y={hoop_y}")
        if not self.held:
            print("Ball not held, cannot shoot")
            return
        
        # Release the ball
        self.held = False
        self.held_by = None
        self.perfect_shot = perfect_shot
        self.can_score = perfect_shot
        self.shot_protection_timer = 60  # 1 second of protection at 60 FPS
        
        if perfect_shot and hoop_x is not None and hoop_y is not None:
            print("Executing perfect shot trajectory")
            # Perfect shot - guaranteed to score
            self.target_hoop_x = hoop_x
            self.target_hoop_y = hoop_y
            
            # For perfect shots, just teleport to hoop area for guaranteed scoring
            self.x = hoop_x
            self.y = hoop_y
            self.speed_x = 0
            self.speed_y = 2  # Slight downward motion
            print(f"Perfect shot teleported to hoop: ({hoop_x}, {hoop_y})")
                
        else:
            print("Executing imperfect shot (backboard)")
            # Imperfect shot - aim for backboard
            # Target backboard position
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
        
        print(f"Ball velocities set: speed_x={self.speed_x}, speed_y={self.speed_y}")

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
            
        # Apply gravity
        self.speed_y += self.GRAVITY
        
        # Update position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Perfect shot correction - strongly guide to hoop
        if self.perfect_shot:
            dx = self.target_hoop_x - self.x
            dy = self.target_hoop_y - self.y
            distance = math.hypot(dx, dy)
            
            # Only print every 10 frames to avoid spam
            if hasattr(self, 'frame_count'):
                self.frame_count += 1
            else:
                self.frame_count = 0
                
            if self.frame_count % 10 == 0:
                print(f"Perfect shot guidance: distance={distance:.1f}, ball pos=({self.x:.1f}, {self.y:.1f})")
            
            # Strong correction when close to hoop
            if distance < 100:
                # Strong guidance to ensure scoring
                correction_x = dx * 0.05
                correction_y = dy * 0.03
                self.speed_x += correction_x
                self.speed_y += correction_y
                
                # Ensure ball goes through hoop
                if distance < 30:
                    self.speed_y = max(self.speed_y, 2)  # Downward motion through hoop
                    print("Ball very close to hoop, forcing downward motion")
            else:
                # Gentle correction at distance
                correction_x = dx * 0.02
                correction_y = dy * 0.01
                self.speed_x += correction_x
                self.speed_y += correction_y
            
            # Ensure ball is always moving (prevent getting stuck)
            if abs(self.speed_x) < 1:
                self.speed_x = 1 if self.target_hoop_x > self.x else -1
            if abs(self.speed_y) < 0.5:
                self.speed_y = 0.5

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