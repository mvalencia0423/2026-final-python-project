import pygame
import math
import random

class Hoop:
    def __init__(self, x, y):
        # Backboard position (top-left) - larger, more realistic
        self.backboard_x = x
        self.backboard_y = y
        self.backboard_width = 20  # Thicker backboard
        self.backboard_height = 160  # Taller backboard

        # Rim position (center of rim) - positioned to touch backboard
        self.rim_radius = 20  # Larger rim
        self.rim_x = x - 40  # Closer to backboard so net touches
        self.rim_y = y + 45  # Much lower for realistic height

        # Animation properties
        self.net_sway = 0
        self.rim_vibration = 0
        self.backboard_shake = 0

        # Scoring zone (ball must pass downward through this rectangle)
        self.score_zone = pygame.Rect(self.rim_x - self.rim_radius,
                                      self.rim_y - 5,
                                      self.rim_radius * 2,
                                      10)

    def update(self, ball_scored=False):
        """Update hoop animations"""
        if ball_scored:
            self.rim_vibration = 1  # Almost no shake
            self.backboard_shake = 0  # No shake
            self.net_sway = 3  # Minimal sway
        
        # Decay animations
        self.rim_vibration *= 0.9
        self.backboard_shake *= 0.85
        self.net_sway *= 0.95

    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = self.backboard_x - camera_x + int(random.randint(-int(self.backboard_shake), int(self.backboard_shake)))
        draw_y = self.backboard_y - camera_y + int(random.randint(-int(self.backboard_shake), int(self.backboard_shake)))
        rim_x = self.rim_x - camera_x + int(random.randint(-int(self.rim_vibration), int(self.rim_vibration)))
        rim_y = self.rim_y - camera_y + int(random.randint(-int(self.rim_vibration), int(self.rim_vibration)))
        
        # Draw ultra-realistic 2026 Xbox basketball hoop
        
        # Backboard shadow (for depth)
        shadow_offset = 8
        pygame.draw.rect(screen, (5, 5, 15), 
                        (draw_x + shadow_offset, draw_y + shadow_offset, 
                         self.backboard_width, self.backboard_height))
        
        # Backboard support structure (metal pole)
        pole_x = draw_x + self.backboard_width + 15
        pygame.draw.rect(screen, (40, 40, 50), 
                        (pole_x, draw_y + self.backboard_height - 50, 15, 400))
        # Pole highlight
        pygame.draw.rect(screen, (60, 60, 70), 
                        (pole_x + 2, draw_y + self.backboard_height - 50, 3, 400))
        # Pole shadow
        pygame.draw.rect(screen, (30, 30, 40), 
                        (pole_x + 10, draw_y + self.backboard_height - 50, 3, 400))
        
        # Backboard (main structure - realistic materials)
        # Outer frame (thick metal)
        pygame.draw.rect(screen, (50, 50, 70), 
                        (draw_x - 4, draw_y - 4, 
                         self.backboard_width + 8, self.backboard_height + 8))
        
        # Inner frame border
        pygame.draw.rect(screen, (80, 80, 100), 
                        (draw_x - 2, draw_y - 2, 
                         self.backboard_width + 4, self.backboard_height + 4))
        
        # Main backboard (tempered glass effect)
        pygame.draw.rect(screen, (230, 240, 250), 
                        (draw_x, draw_y, self.backboard_width, self.backboard_height))
        
        # Glass reflection layers (realistic lighting)
        for i in range(4):
            reflection_alpha = 100 - i * 20
            reflection_x = draw_x + 3 + i * 2
            reflection_y = draw_y + 10 + i * 25
            reflection_height = 30 - i * 5
            
            # Create gradient effect
            for j in range(reflection_height):
                gradient_alpha = reflection_alpha - j * 2
                if gradient_alpha > 0:
                    color = (255, 255, 255, min(255, gradient_alpha))
                    pygame.draw.line(screen, color[:3], 
                                   (reflection_x, reflection_y + j), 
                                   (reflection_x + self.backboard_width - 6, reflection_y + j), 1)
        
        # Shooting square (regulation NBA markings)
        square_width = 30
        square_height = 22
        square_x = draw_x + self.backboard_width - square_width - 8
        square_y = draw_y + (self.backboard_height - square_height) // 2
        
        # Square outline (thick, professional NBA style)
        pygame.draw.rect(screen, (220, 50, 50), 
                        (square_x, square_y, square_width, square_height), 4)
        
        # Square inner detail (double line effect)
        pygame.draw.rect(screen, (180, 40, 40), 
                        (square_x + 3, square_y + 3, square_width - 6, square_height - 6), 2)
        
        # Backboard branding area (NBA logo style)
        brand_rect = (draw_x + 5, draw_y + 10, self.backboard_width - 10, 25)
        pygame.draw.rect(screen, (40, 40, 60), brand_rect)
        pygame.draw.rect(screen, (60, 60, 80), brand_rect, 2)
        
        # Support brackets (realistic engineering)
        # Top mounting bracket
        pygame.draw.rect(screen, (70, 70, 90), 
                        (draw_x + self.backboard_width // 2 - 10, 
                         draw_y - 20, 20, 20))
        # Diagonal support braces
        pygame.draw.polygon(screen, (60, 60, 80), [
            (draw_x + self.backboard_width // 2 - 10, draw_y),
            (draw_x + self.backboard_width // 2 - 15, draw_y - 20),
            (draw_x + self.backboard_width // 2 + 15, draw_y - 20),
            (draw_x + self.backboard_width // 2 + 10, draw_y)
        ])
        
        # Rim mounting system
        mounting_plate_x = draw_x + self.backboard_width - 8
        mounting_plate_y = draw_y + (self.backboard_height - 12) // 2
        
        # Mounting plate (thick metal)
        pygame.draw.rect(screen, (90, 90, 110), 
                        (mounting_plate_x, mounting_plate_y, 12, 12))
        # Mounting bolts
        for i in range(4):
            bolt_x = mounting_plate_x + 2 + (i % 2) * 8
            bolt_y = mounting_plate_y + 2 + (i // 2) * 8
            pygame.draw.circle(screen, (40, 40, 50), (bolt_x, bolt_y), 2)
            pygame.draw.circle(screen, (60, 60, 70), (bolt_x, bolt_y), 1)
        
        # Rim arm (connects rim to backboard)
        arm_start_x = mounting_plate_x + 12
        arm_start_y = mounting_plate_y + 6
        arm_end_x = rim_x + self.rim_radius - 5
        arm_end_y = rim_y
        
        # Draw arm with thickness
        pygame.draw.line(screen, (100, 100, 120), 
                       (arm_start_x, arm_start_y), (arm_end_x, arm_end_y), 6)
        pygame.draw.line(screen, (120, 120, 140), 
                       (arm_start_x, arm_start_y), (arm_end_x, arm_end_y), 4)
        
        # Rim (ultra-realistic NBA specification)
        # Outer rim (thick orange metal)
        pygame.draw.circle(screen, (255, 120, 0), 
                          (int(rim_x), int(rim_y)), self.rim_radius, 5)
        
        # Inner rim (bright orange)
        pygame.draw.circle(screen, (255, 140, 0), 
                          (int(rim_x), int(rim_y)), self.rim_radius - 3, 3)
        
        # Rim highlights (metallic shine effect)
        for angle in range(0, 360, 45):
            highlight_angle = math.radians(angle)
            highlight_x = rim_x + math.cos(highlight_angle) * (self.rim_radius - 4)
            highlight_y = rim_y + math.sin(highlight_angle) * (self.rim_radius - 4)
            pygame.draw.circle(screen, (255, 180, 50), 
                             (int(highlight_x), int(highlight_y)), 2)
        
        # Rim shadow (depth effect)
        pygame.draw.circle(screen, (200, 80, 0), 
                          (int(rim_x + 3), int(rim_y + 3)), self.rim_radius, 2)
        
        # Net attachment clips (realistic metal chain links)
        clip_positions = 12
        for i in range(clip_positions):
            angle = (2 * math.pi * i) / clip_positions
            clip_x = rim_x + math.cos(angle) * (self.rim_radius - 3)
            clip_y = rim_y + math.sin(angle) * (self.rim_radius - 3)
            # Clip detail
            pygame.draw.circle(screen, (140, 140, 160), 
                             (int(clip_x), int(clip_y)), 3)
            pygame.draw.circle(screen, (160, 160, 180), 
                             (int(clip_x), int(clip_y)), 2)
        
        # Draw ultra-realistic net with physics
        self.draw_ultra_realistic_net(screen, rim_x, rim_y, draw_x, draw_y)
        
        # Breakaway rim mechanism detail
        rim_spring_x = rim_x - self.rim_radius - 10
        rim_spring_y = rim_y
        pygame.draw.rect(screen, (80, 80, 100), 
                        (rim_spring_x, rim_spring_y - 5, 10, 10))
        # Spring coils
        for i in range(5):
            coil_y = rim_spring_y - 4 + i * 2
            pygame.draw.line(screen, (100, 100, 120), 
                           (rim_spring_x + 2, coil_y), 
                           (rim_spring_x + 8, coil_y), 1)

    def draw_ultra_realistic_net(self, screen, rim_x, rim_y, backboard_x, backboard_y):
        """Draw ultra-realistic basketball net with advanced physics and sway"""
        
        # Net parameters
        net_segments = 16  # More segments for realism
        net_depth = 35
        chain_width = 2
        
        # Net color (realistic white with slight gray tint)
        net_color = (245, 245, 250)
        shadow_color = (200, 200, 210)
        highlight_color = (255, 255, 255)
        
        # Calculate sway effect
        sway_offset = math.sin(pygame.time.get_ticks() * 0.001) * self.net_sway
        
        # Draw net chains with advanced physics
        for i in range(net_segments):
            angle = (2 * math.pi * i) / net_segments
            next_angle = (2 * math.pi * (i + 1)) / net_segments
            
            # Top attachment points on rim
            x1 = rim_x + math.cos(angle) * (self.rim_radius - 3)
            y1 = rim_y + math.sin(angle) * (self.rim_radius - 3)
            x2 = rim_x + math.cos(next_angle) * (self.rim_radius - 3)
            y2 = rim_y + math.sin(next_angle) * (self.rim_radius - 3)
            
            # Draw vertical net chains with realistic sag
            for depth in range(0, net_depth, 3):
                # Calculate funnel effect (narrower as it goes down)
                funnel_factor = 1 - (depth / net_depth) * 0.7
                current_radius = (self.rim_radius - 6) * funnel_factor
                
                # Add physics-based sway (more sway at bottom)
                current_sway = sway_offset * (depth / net_depth) * 1.5
                sag = math.sin(depth * 0.2) * 2  # Natural sag effect
                
                # Alternate chain pattern for realistic weave
                if (depth // 3) % 2 == 0:
                    left_x = rim_x + math.cos(angle) * current_radius + current_sway
                    left_y = rim_y + depth + sag
                    right_x = rim_x + math.cos(next_angle) * current_radius + current_sway
                    right_y = rim_y + depth + sag
                else:
                    # Cross-over pattern
                    left_x = rim_x + math.cos(angle + 0.15) * current_radius + current_sway
                    left_y = rim_y + depth + sag
                    right_x = rim_x + math.cos(next_angle - 0.15) * current_radius + current_sway
                    right_y = rim_y + depth + sag
                
                # Draw net chains with 3D effect (shadow + main + highlight)
                # Shadow layer
                pygame.draw.line(screen, shadow_color, 
                               (x1 + 1, y1 + 1), (left_x + 1, left_y + 1), chain_width + 1)
                pygame.draw.line(screen, shadow_color, 
                               (x2 + 1, y2 + 1), (right_x + 1, right_y + 1), chain_width + 1)
                
                # Main chain
                pygame.draw.line(screen, net_color, 
                               (x1, y1), (left_x, left_y), chain_width)
                pygame.draw.line(screen, net_color, 
                               (x2, y2), (right_x, right_y), chain_width)
                
                # Highlight for 3D effect
                if depth % 6 == 0:  # Periodic highlights
                    pygame.draw.line(screen, highlight_color, 
                                   (x1 - 1, y1), (left_x - 1, left_y), 1)
                    pygame.draw.line(screen, highlight_color, 
                                   (x2 - 1, y2), (right_x - 1, right_y), 1)
                
                # Horizontal connecting chains
                if depth > 0 and depth % 3 == 0:
                    # Shadow
                    pygame.draw.line(screen, shadow_color, 
                                   (left_x + 1, left_y + 1), (right_x + 1, right_y + 1), chain_width + 1)
                    # Main
                    pygame.draw.line(screen, net_color, 
                                   (left_x, left_y), (right_x, right_y), chain_width)
                    # Highlight
                    if depth % 6 == 0:
                        pygame.draw.line(screen, highlight_color, 
                                       (left_x - 1, left_y - 1), (right_x - 1, right_y - 1), 1)
                
                # Update for next segment
                x1, y1 = left_x, left_y
                x2, y2 = right_x, right_y
        
        # Bottom net opening with realistic chain detail
        bottom_radius = 10
        bottom_y = rim_y + net_depth
        bottom_sway = sway_offset * 2
        
        # Draw bottom chain ring
        for i in range(12):
            angle = (2 * math.pi * i) / 12
            chain_x = rim_x + math.cos(angle) * bottom_radius + bottom_sway
            chain_y = bottom_y
            pygame.draw.circle(screen, shadow_color, 
                             (int(chain_x + 1), int(chain_y + 1)), 4)
            pygame.draw.circle(screen, net_color, 
                             (int(chain_x), int(chain_y)), 3)
            pygame.draw.circle(screen, highlight_color, 
                             (int(chain_x - 1), int(chain_y - 1)), 1)
        
        # Add some loose chain ends for realism
        for i in range(4):
            angle = (math.pi * i) / 2 + math.pi / 4
            loose_x = rim_x + math.cos(angle) * bottom_radius + bottom_sway
            loose_y = bottom_y
            pygame.draw.line(screen, shadow_color, 
                           (loose_x, loose_y), (loose_x + random.randint(-3, 3), loose_y + 5), 2)
            pygame.draw.line(screen, net_color, 
                           (loose_x, loose_y), (loose_x + random.randint(-3, 3), loose_y + 5), 1)

    def draw_realistic_net(self, screen, rim_x, rim_y, backboard_x, backboard_y):
        """Draw ultra-realistic basketball net with proper physics"""
        
        # Net parameters
        net_segments = 12
        net_depth = 25
        chain_width = 1
        
        # Net color (realistic white)
        net_color = (240, 240, 245)
        shadow_color = (200, 200, 210)
        
        # Draw net chains (zigzag pattern)
        for i in range(net_segments):
            angle = (2 * math.pi * i) / net_segments
            next_angle = (2 * math.pi * (i + 1)) / net_segments
            
            # Top attachment points on rim
            x1 = rim_x + math.cos(angle) * (self.rim_radius - 2)
            y1 = rim_y + math.sin(angle) * (self.rim_radius - 2)
            x2 = rim_x + math.cos(next_angle) * (self.rim_radius - 2)
            y2 = rim_y + math.sin(next_angle) * (self.rim_radius - 2)
            
            # Draw zigzag net pattern
            for depth in range(0, net_depth, 4):
                # Calculate funnel effect (narrower as it goes down)
                funnel_factor = 1 - (depth / net_depth) * 0.6
                current_radius = (self.rim_radius - 5) * funnel_factor
                
                # Alternate zigzag points
                if (depth // 4) % 2 == 0:
                    left_x = rim_x + math.cos(angle) * current_radius
                    left_y = rim_y + depth
                    right_x = rim_x + math.cos(next_angle) * current_radius
                    right_y = rim_y + depth
                else:
                    left_x = rim_x + math.cos(angle + 0.1) * current_radius
                    left_y = rim_y + depth
                    right_x = rim_x + math.cos(next_angle - 0.1) * current_radius
                    right_y = rim_y + depth
                
                # Draw net chains with shadow effect
                pygame.draw.line(screen, shadow_color, 
                               (x1, y1), (left_x, left_y), chain_width + 1)
                pygame.draw.line(screen, net_color, 
                               (x1, y1), (left_x, left_y), chain_width)
                
                pygame.draw.line(screen, shadow_color, 
                               (x2, y2), (right_x, right_y), chain_width + 1)
                pygame.draw.line(screen, net_color, 
                               (x2, y2), (right_x, right_y), chain_width)
                
                # Horizontal chains
                if depth > 0:
                    pygame.draw.line(screen, shadow_color, 
                                   (left_x, left_y), (right_x, right_y), chain_width + 1)
                    pygame.draw.line(screen, net_color, 
                                   (left_x, left_y), (right_x, right_y), chain_width)
                
                # Update for next segment
                x1, y1 = left_x, left_y
                x2, y2 = right_x, right_y
        
        # Bottom net opening (funnel effect)
        bottom_radius = 8
        bottom_y = rim_y + net_depth
        pygame.draw.circle(screen, shadow_color, 
                          (int(rim_x), int(bottom_y)), bottom_radius, 2)
        pygame.draw.circle(screen, net_color, 
                          (int(rim_x), int(bottom_y)), bottom_radius - 1, 1)
        
        # Net attachment to backboard (realistic connection)
        attach_y = rim_y + 8
        attach_points = 4
        for i in range(attach_points):
            offset = (i - 1.5) * 4
            pygame.draw.line(screen, shadow_color, 
                           (backboard_x + self.backboard_width, attach_y + offset),
                           (rim_x - self.rim_radius + 3, rim_y + 10 + offset), 2)
            pygame.draw.line(screen, net_color, 
                           (backboard_x + self.backboard_width, attach_y + offset),
                           (rim_x - self.rim_radius + 3, rim_y + 10 + offset), 1)
        
        # Inner rim (darker orange for depth)
        pygame.draw.circle(screen, (200, 100, 0),
                           (int(rim_x), int(rim_y)), self.rim_radius - 2, 2)

    def draw_net(self, screen, rim_x, rim_y, backboard_x, backboard_y):
        # Draw realistic basketball net that touches the backboard
        
        # Net attachment points on rim (8 points around the rim)
        net_points = []
        for angle in range(0, 360, 45):
            import math
            point_x = rim_x + int(self.rim_radius * math.cos(math.radians(angle)))
            point_y = rim_y + int(self.rim_radius * math.sin(math.radians(angle)))
            net_points.append((point_x, point_y))
        
        # Net chains (zigzag pattern)
        net_length = 40
        chain_count = 8
        
        for i in range(chain_count):
            # Calculate chain positions
            angle = (360 / chain_count) * i
            
            # Top attachment point on rim
            import math
            top_x = rim_x + int(self.rim_radius * math.cos(math.radians(angle)))
            top_y = rim_y + int(self.rim_radius * math.sin(math.radians(angle)))
            
            # Bottom of net (funnel shape - narrower at bottom)
            bottom_radius = self.rim_radius - 15
            bottom_x = rim_x + int(bottom_radius * math.cos(math.radians(angle)))
            bottom_y = rim_y + net_length
            
            # Draw chain with zigzag pattern
            segments = 6
            for j in range(segments):
                progress = j / segments
                
                # Calculate current position with slight zigzag
                current_x = top_x + (bottom_x - top_x) * progress
                current_y = top_y + (bottom_y - top_y) * progress
                
                # Add zigzag effect
                if j % 2 == 0:
                    current_x += 3
                else:
                    current_x -= 3
                
                # Connect to next segment
                if j < segments - 1:
                    next_progress = (j + 1) / segments
                    next_x = top_x + (bottom_x - top_x) * next_progress
                    next_y = top_y + (bottom_y - top_y) * next_progress
                    
                    if (j + 1) % 2 == 0:
                        next_x += 3
                    else:
                        next_x -= 3
                    
                    pygame.draw.line(screen, (255, 255, 255),
                                   (current_x, current_y), (next_x, next_y), 2)
        
        # Horizontal net strings (connect chains)
        for level in range(1, 5):
            level_progress = level / 5
            level_y = rim_y + int(net_length * level_progress)
            level_radius = self.rim_radius - int(12 * level_progress)
            
            # Draw horizontal connections
            for i in range(chain_count):
                angle1 = (360 / chain_count) * i
                angle2 = (360 / chain_count) * ((i + 1) % chain_count)
                
                import math
                x1 = rim_x + int(level_radius * math.cos(math.radians(angle1)))
                x2 = rim_x + int(level_radius * math.cos(math.radians(angle2)))
                
                # Add slight curve to horizontal strings
                mid_x = (x1 + x2) // 2
                mid_y = level_y - 2
                
                pygame.draw.line(screen, (255, 255, 255),
                               (x1, level_y), (mid_x, mid_y), 1)
                pygame.draw.line(screen, (255, 255, 255),
                               (mid_x, mid_y), (x2, level_y), 1)
        
        # Net touches backboard - draw attachment strings
        backboard_attach_y = rim_y + 10
        pygame.draw.line(screen, (255, 255, 255),
                       (backboard_x + self.backboard_width, backboard_attach_y),
                       (rim_x - self.rim_radius + 5, rim_y + 15), 2)
        pygame.draw.line(screen, (255, 255, 255),
                       (backboard_x + self.backboard_width, backboard_attach_y + 10),
                       (rim_x + self.rim_radius - 5, rim_y + 15), 2)

    def check_score(self, ball):
        # Only perfect shots can score - and only if they haven't scored yet
        if ball.perfect_shot and not ball.has_scored:
            distance = math.hypot(ball.x - self.rim_x, ball.y - self.rim_y)
            print(f"Perfect shot check: ball pos=({ball.x}, {ball.y}), hoop pos=({self.rim_x}, {self.rim_y}), distance={distance}")
            # Much much larger scoring area for perfect shots - almost guaranteed
            if distance < self.rim_radius + 35:  # Increased from 15 to 35
                print("PERFECT SHOT SCORED!")
                return True
        
        # No other scoring allowed
        return False
