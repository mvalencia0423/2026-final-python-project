import pygame
import math
import random

class Defender:
    def __init__(self, x, y, role="guard", number=None, customization=None):
        self.x = x
        self.y = y
        self.role = role  # "guard", "forward", "center"
        self.width = 30
        self.height = 60
        self.speed = 2.5 if role == "guard" else 2.0 if role == "forward" else 1.5
        
        # Use customization if provided, otherwise use enemy team defaults
        if customization:
            self.skin_tone = customization.get('skin_color', (255, 220, 177))
            self.hair_color = (0, 0, 0)  # Default black hair
            self.shoes_color = customization.get('shoe_color', (50, 50, 50))
            # Enemy team - different jersey color but same style
            self.jersey_color = (50, 50, 200)  # Blue enemy team
            self.shorts_color = (50, 50, 200)
        else:
            # Default enemy team appearance
            skin_tones = [(255, 220, 177), (255, 195, 140), (235, 170, 120), (180, 120, 80), (120, 80, 50)]
            hair_colors = [(0, 0, 0), (50, 30, 0), (100, 60, 30)]
            
            self.skin_tone = random.choice(skin_tones)
            self.hair_color = random.choice(hair_colors)
            self.jersey_color = (200, 50, 50)  # Red team
            self.shorts_color = (200, 50, 50)
            self.shoes_color = (50, 50, 50)
        
        self.number = number or str(random.randint(1, 99))
        
        # Defensive AI behavior
        self.target_x = x
        self.target_y = y
        self.state = "defending"  # "defending", "stealing", "blocking", "recovering"
        self.marked_player = None
        self.running_frame = random.randint(0, 19)
        self.arm_swing = 0
        self.defensive_stance = False
        self.reaction_time = 0
        self.steal_cooldown = 0
        self.block_cooldown = 0
        
    def update_ai(self, player, teammates, ball, hoop):
        """Smart defensive AI decision making"""
        self.reaction_time += 1
        self.steal_cooldown = max(0, self.steal_cooldown - 1)
        self.block_cooldown = max(0, self.block_cooldown - 1)
        
        # Update animation
        if abs(self.x - self.target_x) > 2 or abs(self.y - self.target_y) > 2:
            self.running_frame = (self.running_frame + 1) % 20
            self.arm_swing = math.sin(self.running_frame * 0.5) * 15
            self.defensive_stance = True
        else:
            self.running_frame = 0
            self.arm_swing *= 0.8
            self.defensive_stance = False
        
        # Find player to mark based on role
        self.find_mark(player, teammates)
        
        # Defensive decision tree
        if ball.held and ball.held_by == player:
            # Player has ball - play tight defense
            self.defend_ball_handler(player, ball, hoop)
        elif not ball.held:
            # Ball is loose - try to get it
            self.target_x = ball.x
            self.target_y = ball.y
            self.state = "recovering"
        elif self.marked_player:
            # Mark assigned player
            self.mark_opponent(self.marked_player, ball)
        else:
            # Zone defense
            self.play_zone_defense(hoop)
        
        # Move towards target
        self.move_to_target()
        
        # Attempt steals and blocks
        self.try_steal(player, ball)
        self.try_block(ball, hoop)
        
    def find_mark(self, player, teammates):
        """Find appropriate player to mark based on defensive role"""
        all_opponents = [player] + teammates
        
        if self.role == "guard":
            # Guard marks the ball handler or closest guard
            ball_handler = self.find_ball_handler(all_opponents)
            if ball_handler:
                self.marked_player = ball_handler
            else:
                # Mark closest opponent
                self.marked_player = min(all_opponents, 
                                       key=lambda p: math.hypot(p.x - self.x, p.y - self.y))
                                       
        elif self.role == "forward":
            # Forward marks wing players
            forwards = [p for p in all_opponents if p != player]
            if forwards:
                self.marked_player = min(forwards, 
                                       key=lambda p: math.hypot(p.x - self.x, p.y - self.y))
            else:
                self.marked_player = player
                
        elif self.role == "center":
            # Center marks players in the paint
            paint_players = [p for p in all_opponents 
                           if abs(p.x - 850) < 150 and abs(p.y - 300) < 100]
            if paint_players:
                self.marked_player = min(paint_players, 
                                       key=lambda p: math.hypot(p.x - self.x, p.y - self.y))
            else:
                self.marked_player = player
                
    def find_ball_handler(self, players):
        """Find who has the ball"""
        for player in players:
            if hasattr(player, 'ball') and player.ball:
                return player
        return None
        
    def defend_ball_handler(self, player, ball, hoop):
        """Defend against player with ball"""
        # Position between ball handler and hoop
        hoop_x, hoop_y = hoop.rim_x, hoop.rim_y
        
        # Calculate defensive position
        dx = hoop_x - player.x
        dy = hoop_y - player.y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            # Position between player and hoop with more distance
            defend_distance = 60 if self.role == "guard" else 70 if self.role == "forward" else 80
            self.target_x = player.x + (dx / dist) * defend_distance
            self.target_y = player.y + (dy / dist) * defend_distance
            
        # Stay in defensive stance
        self.defensive_stance = True
        self.state = "defending"
        
        # Try to steal if close enough
        dist_to_ball = math.hypot(self.x - ball.x, self.y - ball.y)
        if dist_to_ball < 30 and self.steal_cooldown == 0:
            self.state = "stealing"
            
    def mark_opponent(self, opponent, ball):
        """Stay between assigned opponent and hoop"""
        hoop_x, hoop_y = 850, 300  # Hoop position
        
        # Calculate marking position
        dx = opponent.x - hoop_x
        dy = opponent.y - hoop_y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            # Stay between opponent and hoop with more distance
            mark_distance = 50 if self.role == "guard" else 60
            self.target_x = opponent.x - (dx / dist) * mark_distance
            self.target_y = opponent.y - (dy / dist) * mark_distance
            
        self.state = "defending"
        
    def play_zone_defense(self, hoop):
        """Zone defense positioning"""
        if self.role == "guard":
            # Guard zone - top of key
            self.target_x = hoop.rim_x - 100
            self.target_y = hoop.rim_y - 100
        elif self.role == "forward":
            # Forward zone - wings
            side = 1 if self.x < hoop.rim_x else -1
            self.target_x = hoop.rim_x + side * 120
            self.target_y = hoop.rim_y
        elif self.role == "center":
            # Center zone - paint
            self.target_x = hoop.rim_x - 50
            self.target_y = hoop.rim_y
            
    def try_steal(self, player, ball):
        """Attempt to steal the ball"""
        if self.state == "stealing" and self.steal_cooldown == 0:
            dist_to_ball = math.hypot(self.x - ball.x, self.y - ball.y)
            
            if dist_to_ball < 25 and random.random() < 0.1:  # 10% steal chance
                # Successful steal - this would be handled in main game logic
                self.steal_cooldown = 60  # 1 second cooldown
                return True
                
        return False
        
    def try_block(self, ball, hoop):
        """Attempt to block a shot"""
        if self.block_cooldown == 0:
            dist_to_hoop = math.hypot(self.x - hoop.rim_x, self.y - hoop.rim_y)
            dist_to_ball = math.hypot(self.x - ball.x, self.y - ball.y)
            
            # If close to hoop and ball is being shot
            if dist_to_hoop < 80 and dist_to_ball < 60 and not ball.held:
                if random.random() < 0.15:  # 15% block chance
                    self.block_cooldown = 60
                    self.state = "blocking"
                    return True
                    
        return False
        
    def move_to_target(self):
        """Smooth movement towards target"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist > 2:
            # Normalize and apply speed
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            
            self.x += move_x
            self.y += move_y
            
    def draw(self, screen, camera_x=0, camera_y=0):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw shadow
        shadow_ellipse = (draw_x - 15, draw_y + 55, 30, 8)
        pygame.draw.ellipse(screen, (20, 20, 30), shadow_ellipse)
        
        # Draw realistic defender (enemy team colors)
        
        # Shoes (dark)
        shoe_y = draw_y + 50
        pygame.draw.ellipse(screen, self.shoes_color, (draw_x - 12, shoe_y, 12, 8))
        pygame.draw.ellipse(screen, self.shoes_color, (draw_x + 2, shoe_y, 12, 8))
        
        # Legs
        leg_top = draw_y + 30
        pygame.draw.rect(screen, self.skin_tone, (draw_x - 8, leg_top, 6, 20))
        pygame.draw.rect(screen, self.skin_tone, (draw_x + 2, leg_top, 6, 20))
        
        # Shorts (red team)
        shorts_y = draw_y + 25
        pygame.draw.rect(screen, self.shorts_color, (draw_x - 10, shorts_y, 20, 15))
        
        # Jersey (red team)
        jersey_y = draw_y + 10
        pygame.draw.rect(screen, self.jersey_color, (draw_x - 8, jersey_y, 16, 18))
        pygame.draw.rect(screen, self.jersey_color, (draw_x - 12, jersey_y + 2, 4, 8))
        pygame.draw.rect(screen, self.jersey_color, (draw_x + 8, jersey_y + 2, 4, 8))
        
        # Jersey number
        font = pygame.font.Font(None, 12)
        number_text = font.render(self.number, True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(draw_x, jersey_y + 9))
        screen.blit(number_text, number_rect)
        
        # Arms (defensive stance)
        shoulder_y = draw_y + 12
        
        if self.defensive_stance:
            # Arms up in defensive stance
            pygame.draw.rect(screen, self.skin_tone, (draw_x - 12, shoulder_y - 5, 4, 15))
            pygame.draw.rect(screen, self.skin_tone, (draw_x + 8, shoulder_y - 5, 4, 15))
        else:
            # Normal arms with animation
            arm_swing_offset = int(self.arm_swing)
            left_arm_x = draw_x - 10 + arm_swing_offset // 3
            right_arm_x = draw_x + 6 - arm_swing_offset // 3
            
            pygame.draw.rect(screen, self.skin_tone, (left_arm_x, shoulder_y + 2, 4, 15))
            pygame.draw.rect(screen, self.skin_tone, (right_arm_x, shoulder_y + 2, 4, 15))
        
        # Head
        head_y = draw_y - 5
        head_size = 12
        pygame.draw.ellipse(screen, self.skin_tone, 
                          (draw_x - head_size//2, head_y, head_size, head_size + 2))
        
        # Hair
        if self.hair_color != (255, 220, 177):
            pygame.draw.arc(screen, self.hair_color, 
                          (draw_x - head_size//2 - 1, head_y - 2, head_size + 2, head_size), 
                          0, 3.14, 3)
        
        # Face (focused expression)
        eye_y = head_y + 4
        pygame.draw.circle(screen, (0, 0, 0), (draw_x - 3, eye_y), 1)
        pygame.draw.circle(screen, (0, 0, 0), (draw_x + 3, eye_y), 1)
        
        # Show defensive role indicator
        role_colors = {"guard": (255, 0, 0), "forward": (255, 165, 0), "center": (128, 0, 128)}
        pygame.draw.circle(screen, role_colors.get(self.role, (255, 0, 0)), 
                         (draw_x + 15, draw_y - 10), 3)
        
        # Show state indicator
        if self.state == "stealing":
            pygame.draw.circle(screen, (255, 255, 0), (draw_x, draw_y - 20), 3)
        elif self.state == "blocking":
            pygame.draw.rect(screen, (255, 0, 0), (draw_x - 2, draw_y - 22, 4, 4))


class DefenderManager:
    def __init__(self, customization=None):
        self.defenders = []
        self.customization = customization
        self.create_defense()
        
    def create_defense(self):
        """Create a balanced defensive team"""
        # Starting positions (defensive setup)
        positions = [
            (700, 250, "guard", "24"),   # Point guard
            (750, 200, "forward", "32"),  # Small forward  
            (750, 400, "forward", "44"),  # Power forward
            (800, 300, "center", "55"),   # Center
        ]
        
        for x, y, role, number in positions:
            self.defenders.append(Defender(x, y, role, number, self.customization))
            
    def update(self, player, teammates, ball, hoop):
        """Update all defenders AI"""
        for defender in self.defenders:
            defender.update_ai(player, teammates, ball, hoop)
            
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw all defenders"""
        for defender in self.defenders:
            defender.draw(screen, camera_x, camera_y)
            
    def check_steals(self, player, ball):
        """Check if any defender successfully stole the ball"""
        for defender in self.defenders:
            if defender.try_steal(player, ball):
                return True
        return False
        
    def check_blocks(self, ball, hoop):
        """Check if any defender successfully blocked the shot"""
        for defender in self.defenders:
            if defender.try_block(ball, hoop):
                return True
        return False
