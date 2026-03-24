import pygame
import math
import random

def safe_color(color, subtract=0):
    """Ensure color values stay within valid RGB range (0-255)"""
    return tuple(max(0, min(255, c - subtract)) for c in color)

class Player:
    def __init__(self, x, y, skin_tone=(255, 220, 177), hair_color=(0, 0, 0), 
                 jersey_color=(200, 50, 50), shorts_color=(200, 50, 50), 
                 shoes_color=(255, 255, 255), number="23"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 60
        self.speed = 5
        
        # Appearance customization
        self.skin_tone = skin_tone
        self.hair_color = hair_color
        self.jersey_color = jersey_color
        self.shorts_color = shorts_color
        self.shoes_color = shoes_color
        self.number = number
        
        # Enhanced animation states
        self.running_frame = 0
        self.is_running = False
        self.arm_swing = 0
        self.leg_swing = 0
        self.breathing_offset = 0
        self.sweat_drops = []
        self.muscle_flex = 0
        
        # Dynamic effects
        self.exertion_level = 0.0  # How tired the player looks
        self.adrenaline = 0.0  # Boosts animations during intense moments
        
    def move(self, keys):
        old_x, old_y = self.x, self.y
        self.is_running = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.is_running = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.is_running = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.is_running = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.is_running = True
            
        # Update animation
        if self.is_running:
            self.running_frame = (self.running_frame + 1) % 20
            self.arm_swing = math.sin(self.running_frame * 0.5) * 15
        else:
            self.running_frame = 0
            self.arm_swing *= 0.8  # Smooth return to center

    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw ultra-realistic 2026 Xbox NBA 2K style player
        
        # Enhanced shadow with realistic blur effect
        shadow_ellipse = (draw_x - 18, draw_y + 58, 36, 10)
        pygame.draw.ellipse(screen, (10, 10, 15), shadow_ellipse)
        shadow_inner = (draw_x - 15, draw_y + 56, 30, 8)
        pygame.draw.ellipse(screen, (20, 20, 25), shadow_inner)
        
        # Draw legs with muscular definition
        # Left leg (quadriceps, calves)
        pygame.draw.rect(screen, self.skin_tone, (draw_x - 8, draw_y + 25, 6, 20))  # Upper thigh
        pygame.draw.rect(screen, safe_color(self.skin_tone, 15), 
                        (draw_x - 8, draw_y + 25, 6, 3))  # Muscle highlight
        pygame.draw.rect(screen, self.skin_tone, (draw_x - 7, draw_y + 45, 5, 12))  # Lower leg
        pygame.draw.rect(screen, safe_color(self.skin_tone, 10), 
                        (draw_x - 7, draw_y + 45, 5, 2))  # Shin highlight
        
        # Right leg (quadriceps, calves)
        pygame.draw.rect(screen, self.skin_tone, (draw_x + 2, draw_y + 25, 6, 20))  # Upper thigh
        pygame.draw.rect(screen, safe_color(self.skin_tone, 15), 
                        (draw_x + 2, draw_y + 25, 6, 3))  # Muscle highlight
        pygame.draw.rect(screen, self.skin_tone, (draw_x + 2, draw_y + 45, 5, 12))  # Lower leg
        pygame.draw.rect(screen, safe_color(self.skin_tone, 10), 
                        (draw_x + 2, draw_y + 45, 5, 2))  # Shin highlight
        
        # Draw ultra-realistic NBA shorts with details
        shorts_main = (draw_x - 12, draw_y + 20, 24, 18)
        pygame.draw.rect(screen, self.shorts_color, shorts_main)
        
        # Shorts side panels (NBA style)
        shorts_panel_color = tuple(max(0, min(255, c - 30)) for c in self.shorts_color)
        pygame.draw.rect(screen, shorts_panel_color, 
                        (draw_x - 12, draw_y + 20, 4, 18))  # Left panel
        pygame.draw.rect(screen, shorts_panel_color, 
                        (draw_x + 8, draw_y + 20, 4, 18))  # Right panel
        
        # Shorts waistband with realistic detail
        pygame.draw.rect(screen, (50, 50, 50), (draw_x - 12, draw_y + 20, 24, 3))
        pygame.draw.rect(screen, (100, 100, 100), (draw_x - 12, draw_y + 20, 24, 1))
        
        # Draw muscular torso with abs definition
        torso_main = (draw_x - 10, draw_y + 5, 20, 18)
        pygame.draw.rect(screen, self.skin_tone, torso_main)
        
        # Ab lines (realistic 6-pack)
        for i in range(3):
            abs_y = draw_y + 8 + i * 4
            pygame.draw.line(screen, safe_color(self.skin_tone, 20), 
                           (draw_x - 5, abs_y), (draw_x + 5, abs_y), 1)
        
        # Chest muscle definition
        pygame.draw.arc(screen, safe_color(self.skin_tone, 15), 
                       (draw_x - 8, draw_y + 5, 16, 12), 0, 3.14, 2)
        
        # Draw ultra-realistic NBA jersey with advanced details
        jersey_main = (draw_x - 11, draw_y + 3, 22, 20)
        pygame.draw.rect(screen, self.jersey_color, jersey_main)
        
        # Jersey armholes with realistic curves
        pygame.draw.ellipse(screen, self.skin_tone, (draw_x - 13, draw_y + 5, 6, 8))  # Left armhole
        pygame.draw.ellipse(screen, self.skin_tone, (draw_x + 7, draw_y + 5, 6, 8))   # Right armhole
        
        # Jersey collar (NBA style)
        pygame.draw.ellipse(screen, (255, 255, 255), (draw_x - 5, draw_y + 2, 10, 6))
        pygame.draw.ellipse(screen, (200, 200, 200), (draw_x - 4, draw_y + 3, 8, 4))
        
        # Jersey side panels (realistic NBA design)
        jersey_panel_color = tuple(max(0, min(255, c - 40)) for c in self.jersey_color)
        pygame.draw.rect(screen, jersey_panel_color, 
                        (draw_x - 11, draw_y + 3, 3, 20))  # Left panel
        pygame.draw.rect(screen, jersey_panel_color, 
                        (draw_x + 8, draw_y + 3, 3, 20))  # Right panel
        
        # Draw ultra-realistic arms with muscle definition
        # Left arm with bicep/tricep details
        left_arm_x = draw_x - 10 + int(self.arm_swing * 0.3)
        pygame.draw.rect(screen, self.skin_tone, (left_arm_x - 3, draw_y + 8, 6, 15))  # Bicep
        pygame.draw.rect(screen, (self.skin_tone[0]-12, self.skin_tone[1]-12, self.skin_tone[2]-12), 
                        (left_arm_x - 3, draw_y + 8, 2, 15))  # Bicep highlight
        pygame.draw.rect(screen, self.skin_tone, (left_arm_x - 2, draw_y + 23, 5, 12))  # Forearm
        pygame.draw.rect(screen, (self.skin_tone[0]-8, self.skin_tone[1]-8, self.skin_tone[2]-8), 
                        (left_arm_x - 2, draw_y + 23, 2, 12))  # Forearm highlight
        
        # Right arm with bicep/tricep details  
        right_arm_x = draw_x + 10 + int(self.arm_swing * 0.3)
        pygame.draw.rect(screen, self.skin_tone, (right_arm_x - 3, draw_y + 8, 6, 15))  # Bicep
        pygame.draw.rect(screen, (self.skin_tone[0]-12, self.skin_tone[1]-12, self.skin_tone[2]-12), 
                        (right_arm_x + 1, draw_y + 8, 2, 15))  # Bicep highlight
        pygame.draw.rect(screen, self.skin_tone, (right_arm_x - 2, draw_y + 23, 5, 12))  # Forearm
        pygame.draw.rect(screen, (self.skin_tone[0]-8, self.skin_tone[1]-8, self.skin_tone[2]-8), 
                        (right_arm_x + 1, draw_y + 23, 2, 12))  # Forearm highlight
        
        # Draw ultra-realistic hands with fingers
        # Left hand
        pygame.draw.ellipse(screen, self.skin_tone, (left_arm_x - 4, draw_y + 33, 8, 6))
        # Fingers on left hand
        for i in range(4):
            finger_x = left_arm_x - 3 + i * 2
            pygame.draw.rect(screen, self.skin_tone, (finger_x, draw_y + 35, 1, 3))
        
        # Right hand
        pygame.draw.ellipse(screen, self.skin_tone, (right_arm_x - 4, draw_y + 33, 8, 6))
        # Fingers on right hand
        for i in range(4):
            finger_x = right_arm_x - 3 + i * 2
            pygame.draw.rect(screen, self.skin_tone, (finger_x, draw_y + 35, 1, 3))
        
        # Draw ultra-realistic head with facial features
        head_x = draw_x
        head_y = draw_y - 8
        
        # Head shape with realistic jawline
        pygame.draw.ellipse(screen, self.skin_tone, (head_x - 10, head_y - 5, 20, 18))
        pygame.draw.ellipse(screen, (self.skin_tone[0]-10, self.skin_tone[1]-10, self.skin_tone[2]-10), 
                           (head_x - 8, head_y - 3, 16, 14))  # Inner face shading
        
        # Jawline definition
        pygame.draw.arc(screen, (self.skin_tone[0]-15, self.skin_tone[1]-15, self.skin_tone[2]-15), 
                       (head_x - 10, head_y + 5, 20, 8), 0, 3.14, 2)
        
        # Ultra-realistic hair with texture
        if self.hair_color != (255, 255, 255):  # Not bald
            # Hair base with realistic shape
            pygame.draw.ellipse(screen, self.hair_color, (head_x - 11, head_y - 10, 22, 15))
            # Hair texture strands with safe color calculation
            for i in range(8):
                strand_x = head_x - 8 + i * 2
                strand_y = head_y - 8 + (i % 2) * 2
                # Safe color calculation - ensure values stay within 0-255
                hair_shade = tuple(max(0, min(255, c - 20)) for c in self.hair_color)
                pygame.draw.line(screen, hair_shade, 
                               (strand_x, strand_y), (strand_x, strand_y + 3), 1)
        
        # Ultra-realistic facial features
        # Eyes with pupils and expression
        left_eye_x = head_x - 4
        right_eye_x = head_x + 4
        eye_y = head_y + 2
        
        # Eye whites
        pygame.draw.ellipse(screen, (255, 255, 255), (left_eye_x - 2, eye_y - 1, 4, 2))
        pygame.draw.ellipse(screen, (255, 255, 255), (right_eye_x - 2, eye_y - 1, 4, 2))
        # Pupils
        pygame.draw.circle(screen, (50, 50, 50), (left_eye_x, eye_y), 1)
        pygame.draw.circle(screen, (50, 50, 50), (right_eye_x, eye_y), 1)
        
        # Realistic nose with bridge
        pygame.draw.polygon(screen, (self.skin_tone[0]-20, self.skin_tone[1]-20, self.skin_tone[2]-20), [
            (head_x, head_y + 4),
            (head_x - 2, head_y + 7),
            (head_x + 2, head_y + 7)
        ])
        # Nose bridge line
        pygame.draw.line(screen, (self.skin_tone[0]-15, self.skin_tone[1]-15, self.skin_tone[2]-15), 
                       (head_x, head_y), (head_x, head_y + 4), 1)
        
        # Realistic mouth with lips
        mouth_y = head_y + 10
        pygame.draw.arc(screen, (180, 100, 100), (head_x - 4, mouth_y - 2, 8, 6), 0, 3.14, 2)
        pygame.draw.arc(screen, (150, 70, 70), (head_x - 3, mouth_y - 1, 6, 4), 0, 3.14, 1)
        
        # NBA jersey number with shadow effect
        number_font = pygame.font.Font(None, 14)
        number_shadow = number_font.render(self.number, True, (0, 0, 0))
        number_text = number_font.render(self.number, True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(draw_x, draw_y + 13))
        shadow_rect = number_shadow.get_rect(center=(draw_x + 1, draw_y + 14))
        screen.blit(number_shadow, shadow_rect)
        screen.blit(number_text, number_rect)
        
        # Ultra-realistic NBA shoes with details
        # Left shoe
        left_shoe_x = draw_x - 8 + int(self.arm_swing * 0.2)
        pygame.draw.ellipse(screen, self.shoes_color, (left_shoe_x - 4, draw_y + 55, 12, 8))
        # Shoe sole
        pygame.draw.ellipse(screen, (50, 50, 50), (left_shoe_x - 4, draw_y + 58, 12, 3))
        # Shoe laces
        for i in range(3):
            lace_x = left_shoe_x - 2 + i * 2
            pygame.draw.circle(screen, (255, 255, 255), (lace_x, draw_y + 56), 1)
        # Nike logo style detail
        pygame.draw.arc(screen, (255, 255, 255), (left_shoe_x + 2, draw_y + 54, 4, 4), 1.57, 4.71, 1)
        
        # Right shoe
        right_shoe_x = draw_x + 8 + int(self.arm_swing * 0.2)
        pygame.draw.ellipse(screen, self.shoes_color, (right_shoe_x - 4, draw_y + 55, 12, 8))
        # Shoe sole
        pygame.draw.ellipse(screen, (50, 50, 50), (right_shoe_x - 4, draw_y + 58, 12, 3))
        # Shoe laces
        for i in range(3):
            lace_x = right_shoe_x - 2 + i * 2
            pygame.draw.circle(screen, (255, 255, 255), (lace_x, draw_y + 56), 1)
        # Nike logo style detail
        pygame.draw.arc(screen, (255, 255, 255), (right_shoe_x + 2, draw_y + 54, 4, 4), 1.57, 4.71, 1)
        
        # NBA accessories - wristbands
        # Left wristband
        pygame.draw.rect(screen, (255, 0, 0), (left_arm_x - 2, draw_y + 30, 6, 3))
        pygame.draw.rect(screen, (200, 0, 0), (left_arm_x - 2, draw_y + 30, 6, 1))
        # Right wristband  
        pygame.draw.rect(screen, (255, 0, 0), (right_arm_x - 2, draw_y + 30, 6, 3))
        pygame.draw.rect(screen, (200, 0, 0), (right_arm_x - 2, draw_y + 30, 6, 1))
        
        # Headband (NBA style)
        pygame.draw.rect(screen, (255, 0, 0), (head_x - 12, head_y - 2, 24, 4))
        pygame.draw.rect(screen, (200, 0, 0), (head_x - 12, head_y - 2, 24, 2))
        
        # Sweat details (realistic NBA player effect)
        if self.is_running:
            # Sweat drops on face
            for i in range(3):
                sweat_x = head_x - 4 + i * 4
                sweat_y = head_y + 8
                pygame.draw.circle(screen, (200, 200, 255), (sweat_x, sweat_y), 1)
            # Sweat on arms
            pygame.draw.circle(screen, (200, 200, 255), (left_arm_x, draw_y + 20), 1)
            pygame.draw.circle(screen, (200, 200, 255), (right_arm_x, draw_y + 20), 1)
        
        # Muscle flexing effect when running
        if self.is_running and self.running_frame % 10 < 5:
            # Enhanced muscle definition during movement
            pygame.draw.rect(screen, (self.skin_tone[0]-25, self.skin_tone[1]-25, self.skin_tone[2]-25), 
                            (draw_x - 8, draw_y + 25, 6, 2))  # Left quad flex
            pygame.draw.rect(screen, (self.skin_tone[0]-25, self.skin_tone[1]-25, self.skin_tone[2]-25), 
                            (draw_x + 2, draw_y + 25, 6, 2))  # Right quad flex