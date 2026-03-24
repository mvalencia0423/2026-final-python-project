import pygame
import random
import math

class Fan:
    def __init__(self, x, y, row, seat):
        self.x = x
        self.y = y
        self.row = row
        self.seat = seat
        self.base_y = y
        
        # Fan appearance variety
        self.skin_tone = random.choice([
            (255, 220, 177), (245, 200, 150), (220, 180, 140),
            (180, 140, 100), (150, 120, 80), (255, 190, 150)
        ])
        self.hair_color = random.choice([
            (50, 30, 20), (100, 60, 30), (200, 150, 100),
            (255, 255, 255), (200, 200, 200), (255, 200, 100)
        ])
        self.shirt_color = random.choice([
            (200, 50, 50), (50, 100, 200), (50, 150, 50),
            (255, 100, 50), (150, 50, 200), (100, 100, 100)
        ])
        
        # Animation states
        self.animation_frame = random.randint(0, 60)
        self.standing = random.choice([True, False])
        self.cheering = random.choice([True, False])
        self.arm_raise = random.uniform(0, 15)
        self.lean_direction = random.uniform(-5, 5)
        
        # Excitement level (affects animation)
        self.excitement = random.uniform(0.3, 1.0)
        
    def update(self, game_action_intensity=0.5):
        """Update fan animation based on game action"""
        self.animation_frame += 1
        
        # Increase excitement during game action
        if random.random() < game_action_intensity * 0.1:
            self.excitement = min(1.0, self.excitement + 0.2)
        else:
            self.excitement = max(0.3, self.excitement - 0.01)
        
        # Update animations
        if self.animation_frame % 60 == 0:
            self.standing = random.choice([True, False]) if self.excitement < 0.7 else True
            self.cheering = random.random() < self.excitement
        
        # Arm movement
        if self.cheering:
            self.arm_raise = 10 + math.sin(self.animation_frame * 0.2) * 8
        else:
            self.arm_raise *= 0.9
        
        # Body movement
        self.lean_direction = math.sin(self.animation_frame * 0.1) * 3 * self.excitement
        self.y = self.base_y + math.sin(self.animation_frame * 0.15) * 2 * self.excitement
    
    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Skip if off screen
        if draw_x < -20 or draw_x > 820 or draw_y < -20 or draw_y > 620:
            return
        
        # Draw shadow
        pygame.draw.ellipse(screen, (20, 20, 30), 
                          (draw_x - 8, draw_y + 12, 16, 4))
        
        # Body
        body_height = 20 if self.standing else 15
        pygame.draw.rect(screen, self.shirt_color, 
                        (draw_x - 6, draw_y - body_height, 12, body_height))
        
        # Head
        head_y = draw_y - body_height - 8
        pygame.draw.circle(screen, self.skin_tone, (draw_x, head_y), 6)
        
        # Hair
        if self.hair_color != (255, 255, 255):
            pygame.draw.arc(screen, self.hair_color, 
                          (draw_x - 6, head_y - 8, 12, 10), 0, math.pi, 3)
        
        # Arms
        if self.arm_raise > 2:
            # Left arm raised
            arm_y = draw_y - body_height + 5
            pygame.draw.line(screen, self.skin_tone, 
                           (draw_x - 6, arm_y), 
                           (draw_x - 8 - self.lean_direction, arm_y - self.arm_raise), 2)
            # Right arm raised
            pygame.draw.line(screen, self.skin_tone, 
                           (draw_x + 6, arm_y), 
                           (draw_x + 8 - self.lean_direction, arm_y - self.arm_raise), 2)
            
            # Hands
            pygame.draw.circle(screen, self.skin_tone, 
                             (draw_x - 8 - self.lean_direction, arm_y - self.arm_raise), 2)
            pygame.draw.circle(screen, self.skin_tone, 
                             (draw_x + 8 - self.lean_direction, arm_y - self.arm_raise), 2)
        
        # Face details (draw for all fans)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (draw_x - 2, head_y - 1), 1)
        pygame.draw.circle(screen, (0, 0, 0), (draw_x + 2, head_y - 1), 1)
        
        # Mouth (open if cheering)
        if self.cheering:
            pygame.draw.arc(screen, (100, 50, 50), 
                          (draw_x - 2, head_y + 2, 4, 3), 0, math.pi, 1)

class Crowd:
    def __init__(self, court_width=800, court_height=600):
        self.fans = []
        self.court_width = court_width
        self.court_height = court_height
        
        # Create stadium sections
        self.create_crowd_sections()
        
        # Crowd atmosphere
        self.noise_level = 0.5
        self.wave_active = False
        self.wave_position = 0
        
    def create_crowd_sections(self):
        """Create fans in stadium sections (exactly at court edges, no overlap)"""
        # Top stands (above court) - exactly at court top edge
        self.create_section(100, -150, 6, 20, 25)  # Top stands
        self.create_section(self.court_width - 600, -150, 6, 20, 25)  # Top stands right
        
        # Bottom stands (below court) - exactly at court bottom edge
        self.create_section(100, self.court_height + 50, 6, 20, 25)  # Bottom stands
        self.create_section(self.court_width - 600, self.court_height + 50, 6, 20, 25)  # Bottom stands right
        
        # Left stands (left of court) - exactly at court left edge
        self.create_section(-150, 100, 15, 8, 20)  # Left stands upper
        self.create_section(-150, 400, 15, 8, 20)  # Left stands lower
        
        # Right stands (right of court) - starts after the hoop area
        self.create_section(self.court_width + 100, 100, 15, 8, 20)  # Right stands upper
        self.create_section(self.court_width + 100, 400, 15, 8, 20)  # Right stands lower
        
        # Corner sections - updated for new right stand position
        self.create_section(-150, -150, 4, 8, 20)  # Top-left corner
        self.create_section(self.court_width + 100, -150, 4, 8, 20)  # Top-right corner
        self.create_section(-150, self.court_height + 50, 4, 8, 20)  # Bottom-left corner
        self.create_section(self.court_width + 100, self.court_height + 50, 4, 8, 20)  # Bottom-right corner
        
    def create_section(self, start_x, start_y, rows, seats_per_row, spacing):
        """Create a section of fans"""
        for row in range(rows):
            for seat in range(seats_per_row):
                x = start_x + seat * spacing + random.randint(-5, 5)
                y = start_y + row * spacing + random.randint(-3, 3)
                
                # Add variety to positioning
                if row % 2 == 1:
                    x += spacing // 2
                
                fan = Fan(x, y, row, seat)
                self.fans.append(fan)
    
    def update(self, ball_position=None, game_action=False):
        """Update all fans based on game action"""
        # Calculate game action intensity
        action_intensity = 0.3
        if game_action:
            action_intensity = 0.8
        elif ball_position:
            # Fans closer to ball are more excited
            for fan in self.fans:
                distance = math.sqrt((fan.x - ball_position[0])**2 + 
                                   (fan.y - ball_position[1])**2)
                if distance < 200:
                    action_intensity = max(action_intensity, 0.6)
        
        # Update all fans
        for fan in self.fans:
            fan.update(action_intensity)
        
        # Update wave
        if self.wave_active:
            self.wave_position += 5
            if self.wave_position > 100:
                self.wave_active = False
                self.wave_position = 0
        
        # Random chance to start wave
        if random.random() < 0.001 and not self.wave_active:
            self.wave_active = True
            self.wave_position = 0
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw all fans"""
        # Draw stadium background
        self.draw_stadium_background(screen, camera_x, camera_y)
        
        # Sort fans by Y position for proper layering
        sorted_fans = sorted(self.fans, key=lambda f: f.y)
        
        # Draw fans
        for fan in sorted_fans:
            fan.draw(screen, camera_x, camera_y)
        
        # Draw stadium elements
        self.draw_stadium_elements(screen, camera_x, camera_y)
    
    def draw_stadium_background(self, screen, camera_x, camera_y):
        """Draw stadium structure exactly at court edges (no overlap)"""
        # Court boundaries
        stand_color = (40, 40, 50)
        
        # Top stands (above court) - starts exactly at court top edge
        pygame.draw.rect(screen, stand_color, 
                        (0 - camera_x, -200 - camera_y, self.court_width, 200))
        
        # Bottom stands (below court) - starts exactly at court bottom edge
        pygame.draw.rect(screen, stand_color, 
                        (0 - camera_x, self.court_height - camera_y, 
                         self.court_width, 200))
        
        # Left stands (left of court) - starts exactly at court left edge
        pygame.draw.rect(screen, stand_color, 
                        (-200 - camera_x, -200 - camera_y, 200, self.court_height + 400))
        
        # Right stands (right of court) - starts after the hoop area
        pygame.draw.rect(screen, stand_color, 
                        (self.court_width + 50 - camera_x, -200 - camera_y, 
                         200, self.court_height + 400))
        
        # Add stand details
        detail_color = (60, 60, 70)
        # Top stand rows
        for row in range(6):
            row_y = -180 + row * 30
            pygame.draw.line(screen, detail_color, 
                           (0 - camera_x, row_y - camera_y), 
                           (self.court_width - camera_x, row_y - camera_y), 2)
        
        # Side stand vertical lines
        for col in range(7):
            col_x_left = -180 + col * 30
            col_x_right = self.court_width + 70 + col * 30  # Updated for new right stand position
            pygame.draw.line(screen, detail_color, 
                           (col_x_left - camera_x, -200 - camera_y), 
                           (col_x_left - camera_x, self.court_height + 200 - camera_y), 2)
            pygame.draw.line(screen, detail_color, 
                           (col_x_right - camera_x, -200 - camera_y), 
                           (col_x_right - camera_x, self.court_height + 200 - camera_y), 2)
    
    def draw_stadium_elements(self, screen, camera_x, camera_y):
        """Draw stadium details like scoreboards, banners"""
        # Simple scoreboard
        scoreboard_x = 400 - camera_x
        scoreboard_y = 60 - camera_y
        
        pygame.draw.rect(screen, (50, 50, 50), 
                        (scoreboard_x - 80, scoreboard_y - 20, 160, 40))
        pygame.draw.rect(screen, (200, 200, 200), 
                        (scoreboard_x - 78, scoreboard_y - 18, 156, 36))
        
        # Score text (simplified)
        font = pygame.font.Font(None, 24)
        score_text = font.render("HOME 0 - 0 AWAY", True, (0, 0, 0))
        text_rect = score_text.get_rect(center=(scoreboard_x, scoreboard_y))
        screen.blit(score_text, text_rect)
        
        # Team banners
        for i in range(3):
            banner_x = 100 + i * 250 - camera_x
            pygame.draw.rect(screen, (random.randint(100, 255), 
                                    random.randint(100, 255), 
                                    random.randint(100, 255)), 
                           (banner_x, 35 - camera_y, 80, 15))
    
    def trigger_celebration(self):
        """Trigger crowd celebration"""
        for fan in self.fans:
            fan.excitement = 1.0
            fan.cheering = True
            fan.standing = True
