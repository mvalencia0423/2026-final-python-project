import math
import pygame
from player import Player
from ball import Ball
from ai import AI
from hoop import Hoop
from locker_room import LockerRoom
from teammates import TeammateManager
from defenders import DefenderManager
from crowd import Crowd

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Hoops")

clock = pygame.time.Clock()

# Game states
STATE_LOCKER_ROOM = "locker_room"
STATE_PLAYING = "playing"
current_state = STATE_LOCKER_ROOM

# Initialize locker room
locker_room = LockerRoom(screen)

# Initialize game objects (will be configured after locker room)
player = None
ai = None
ball = None
hoop = None
teammates = None
defenders = None
controlled_player = None  # Who we're currently controlling

font = pygame.font.SysFont(None, 40)

player_score = 0
ai_score = 0

# Shot meter state (moves back and forth while ball is held)
meter_pos = 0.0
meter_dir = 1
meter_speed = 0.015
meter_green_zone = (0.4, 0.6)

# Camera for first-person view
camera_x = 0
camera_y = 0

def draw_court(screen, camera_x, camera_y):
    # 2026 Xbox-style basketball arena with realistic graphics
    
    # Arena background (dark, professional)
    screen.fill((20, 20, 30))
    
    # Court boundaries
    court_left = -camera_x
    court_top = -camera_y
    court_width = 1200
    court_height = 700
    
    # Draw professional basketball court (hardwood)
    # Main court surface with wood grain effect
    court_color = (205, 170, 125)  # Professional hardwood color
    pygame.draw.rect(screen, court_color, 
                     (court_left, court_top, court_width, court_height))
    
    # Wood grain lines for realism
    for i in range(0, court_width, 40):
        grain_x = court_left + i
        pygame.draw.line(screen, (195, 160, 115), 
                        (grain_x, court_top), (grain_x, court_top + court_height), 1)
    
    # Court lines (professional white, slightly thicker)
    line_color = (255, 255, 255)
    line_width = 4
    
    # Outer court boundary
    pygame.draw.rect(screen, line_color, 
                     (court_left, court_top, court_width, court_height), line_width)
    
    # Center line
    center_x = court_left + court_width // 2
    pygame.draw.line(screen, line_color, 
                     (center_x, court_top), (center_x, court_top + court_height), line_width)
    
    # Center circle (professional size)
    pygame.draw.circle(screen, line_color, 
                      (center_x, court_top + court_height // 2), 60, line_width)
    
    # Three-point line (NBA regulation)
    three_point_radius = 180  # Scaled for game
    three_point_x = court_left + court_width - 80
    pygame.draw.arc(screen, line_color, 
                   (three_point_x - three_point_radius, court_top + court_height // 2 - three_point_radius, 
                    three_point_radius * 2, three_point_radius * 2), 
                   -1.57, 1.57, line_width)
    
    # Free throw line
    free_throw_distance = 120
    free_throw_x = court_left + court_width - 80 - free_throw_distance
    pygame.draw.line(screen, line_color, 
                     (free_throw_x, court_top + 180), 
                     (free_throw_x, court_top + court_height - 180), line_width)
    
    # Free throw circle
    pygame.draw.circle(screen, line_color, 
                      (free_throw_x, court_top + court_height // 2), 45, line_width)
    
    # Paint area (key)
    paint_width = 80
    paint_height = 190
    paint_left = court_left + court_width - 80 - paint_width
    paint_top = court_top + (court_height - paint_height) // 2
    pygame.draw.rect(screen, line_color, 
                     (paint_left, paint_top, paint_width, paint_height), line_width)
    
    # Backboard and hoop area
    backboard_x = court_left + court_width - 80
    pygame.draw.line(screen, line_color,
                     (backboard_x, court_top + 200),
                     (backboard_x, court_top + court_height - 200), line_width)
    
    # Baseline
    baseline_x = court_left + court_width - 60
    pygame.draw.line(screen, line_color,
                     (baseline_x, court_top),
                     (baseline_x, court_top + court_height), line_width + 3)
    
    # Arena lighting effects
    draw_arena_lighting(screen, camera_x, camera_y, court_left, court_top, court_width, court_height)
    
    # Court logos and markings
    draw_court_logos(screen, camera_x, camera_y, center_x, court_top, court_height)

def draw_arena_fans(screen, camera_x, camera_y, court_left, court_top, court_width, court_height):
    # Draw realistic fans in the stands
    
    # Background stands (dark)
    stand_color = (40, 40, 50)
    
    # Top stands
    pygame.draw.rect(screen, stand_color, 
                     (court_left - 100, court_top - 150, court_width + 200, 140))
    
    # Side stands (left)
    pygame.draw.rect(screen, stand_color, 
                     (court_left - 150, court_top, 140, court_height))
    
    # Side stands (right)
    pygame.draw.rect(screen, stand_color, 
                     (court_left + court_width + 10, court_top, 140, court_height))
    
    # Draw individual realistic fans
    import random
    random.seed(42)  # Consistent fan positions
    
    # Top stand fans
    for row in range(8):
        for col in range(30):
            fan_x = court_left - 80 + col * 40
            fan_y = court_top - 130 + row * 15
            
            # Random fan appearance
            skin_tones = [(255, 220, 177), (255, 195, 140), (235, 170, 120), (180, 120, 80), (120, 80, 50)]
            shirt_colors = [(200, 50, 50), (50, 50, 200), (50, 200, 50), (255, 255, 255), (100, 100, 100), (255, 165, 0)]
            hair_colors = [(0, 0, 0), (50, 30, 0), (255, 255, 255), (200, 150, 100)]
            
            skin_color = random.choice(skin_tones)
            shirt_color = random.choice(shirt_colors)
            hair_color = random.choice(hair_colors)
            
            # Draw realistic fan person
            # Head
            pygame.draw.ellipse(screen, skin_color, (fan_x - 3, fan_y - 8, 6, 8))
            # Hair
            if random.random() > 0.3:  # 70% have hair
                pygame.draw.arc(screen, hair_color, (fan_x - 3, fan_y - 10, 6, 6), 0, 3.14, 2)
            # Body/torso
            pygame.draw.rect(screen, shirt_color, (fan_x - 4, fan_y, 8, 10))
            # Arms
            pygame.draw.rect(screen, skin_color, (fan_x - 6, fan_y + 2, 2, 6))
            pygame.draw.rect(screen, skin_color, (fan_x + 4, fan_y + 2, 2, 6))
    
    # Left stand fans
    for row in range(15):
        for col in range(8):
            fan_x = court_left - 130 + col * 15
            fan_y = court_top + 50 + row * 40
            
            skin_tones = [(255, 220, 177), (255, 195, 140), (235, 170, 120), (180, 120, 80), (120, 80, 50)]
            shirt_colors = [(200, 50, 50), (50, 50, 200), (50, 200, 50), (255, 255, 255), (100, 100, 100), (255, 165, 0)]
            hair_colors = [(0, 0, 0), (50, 30, 0), (255, 255, 255), (200, 150, 100)]
            
            skin_color = random.choice(skin_tones)
            shirt_color = random.choice(shirt_colors)
            hair_color = random.choice(hair_colors)
            
            # Draw realistic fan person (side view)
            # Head
            pygame.draw.ellipse(screen, skin_color, (fan_x - 4, fan_y - 6, 8, 10))
            # Hair
            if random.random() > 0.3:
                pygame.draw.arc(screen, hair_color, (fan_x - 4, fan_y - 8, 8, 8), 0, 3.14, 3)
            # Body/torso
            pygame.draw.rect(screen, shirt_color, (fan_x - 5, fan_y + 4, 10, 12))
            # Arms
            pygame.draw.rect(screen, skin_color, (fan_x - 8, fan_y + 6, 3, 8))
            pygame.draw.rect(screen, skin_color, (fan_x + 5, fan_y + 6, 3, 8))
    
    # Right stand fans
    for row in range(15):
        for col in range(8):
            fan_x = court_left + court_width + 30 + col * 15
            fan_y = court_top + 50 + row * 40
            
            skin_tones = [(255, 220, 177), (255, 195, 140), (235, 170, 120), (180, 120, 80), (120, 80, 50)]
            shirt_colors = [(200, 50, 50), (50, 50, 200), (50, 200, 50), (255, 255, 255), (100, 100, 100), (255, 165, 0)]
            hair_colors = [(0, 0, 0), (50, 30, 0), (255, 255, 255), (200, 150, 100)]
            
            skin_color = random.choice(skin_tones)
            shirt_color = random.choice(shirt_colors)
            hair_color = random.choice(hair_colors)
            
            # Draw realistic fan person (side view)
            # Head
            pygame.draw.ellipse(screen, skin_color, (fan_x - 4, fan_y - 6, 8, 10))
            # Hair
            if random.random() > 0.3:
                pygame.draw.arc(screen, hair_color, (fan_x - 4, fan_y - 8, 8, 8), 0, 3.14, 3)
            # Body/torso
            pygame.draw.rect(screen, shirt_color, (fan_x - 5, fan_y + 4, 10, 12))
            # Arms
            pygame.draw.rect(screen, skin_color, (fan_x - 8, fan_y + 6, 3, 8))
            pygame.draw.rect(screen, skin_color, (fan_x + 5, fan_y + 6, 3, 8))

def draw_arena_lighting(screen, camera_x, camera_y, court_left, court_top, court_width, court_height):
    # Professional arena lighting effects
    
    # Light fixtures (top)
    for i in range(8):
        light_x = court_left + 100 + i * 130
        light_y = court_top - 100
        
        # Light glow effect
        for radius in range(30, 5, -5):
            alpha = 50 - radius
            light_color = (255, 255, 200, alpha) if alpha > 0 else (255, 255, 200)
            pygame.draw.circle(screen, light_color[:3], (light_x, light_y), radius)
        
        # Light fixture
        pygame.draw.rect(screen, (100, 100, 100), (light_x - 15, light_y - 5, 30, 10))
    
    # Court lighting effect (subtle overlay)
    overlay = pygame.Surface((court_width, court_height))
    overlay.set_alpha(30)
    overlay.fill((255, 255, 200))
    screen.blit(overlay, (court_left, court_top))

def draw_court_logos(screen, camera_x, camera_y, center_x, court_top, court_height):
    # Professional court logos and markings
    
    # Center court logo
    logo_font = pygame.font.SysFont("impact", 48, bold=True)
    logo_text = logo_font.render("NBA", True, (150, 150, 150))
    logo_rect = logo_text.get_rect(center=(center_x, court_top + court_height // 2))
    
    # Logo shadow for depth
    shadow_text = logo_font.render("NBA", True, (50, 50, 50))
    shadow_rect = shadow_text.get_rect(center=(center_x + 2, court_top + court_height // 2 + 2))
    screen.blit(shadow_text, shadow_rect)
    screen.blit(logo_text, logo_rect)
    
    # Court sponsor text
    sponsor_font = pygame.font.SysFont("arial", 16, bold=True)
    sponsor_text = sponsor_font.render("BASKETBALL", True, (100, 100, 100))
    sponsor_rect = sponsor_text.get_rect(center=(center_x, court_top + court_height // 2 + 30))
    screen.blit(sponsor_text, sponsor_rect)
    
    # Team name on baseline
    team_font = pygame.font.SysFont("impact", 24, bold=True)
    team_text = team_font.render("HOME", True, (200, 200, 200))
    team_rect = team_text.get_rect(center=(center_x - 200, court_top + 50))
    screen.blit(team_text, team_rect)
    
    team_text2 = team_font.render("AWAY", True, (200, 200, 200))
    team_rect2 = team_text2.get_rect(center=(center_x + 200, court_top + 50))
    screen.blit(team_text2, team_rect2)

def find_nearest_teammate(current_player, teammates_list):
    """Find the nearest teammate to pass to"""
    if not teammates_list:
        return None
    
    nearest = None
    min_distance = float('inf')
    
    for teammate in teammates_list:
        if teammate != current_player:
            dist = math.hypot(teammate.x - current_player.x, teammate.y - current_player.y)
            if dist < min_distance and dist < 200:  # Only pass if within range
                min_distance = dist
                nearest = teammate
    
    return nearest

def pass_ball_to_teammate(from_player, to_player):
    """Pass the ball from one player to another"""
    global ball
    
    # Calculate pass trajectory
    dx = to_player.x - from_player.x
    dy = to_player.y - from_player.y
    distance = math.hypot(dx, dy)
    
    # Set ball velocity for pass
    pass_speed = distance / 30  # Adjust speed based on distance
    ball.speed_x = dx / 30
    ball.speed_y = dy / 30
    
    # Release ball from current player
    ball.held = False
    ball.perfect_shot = False
    ball.can_score = False

def start_game():
    global player, ai, ball, hoop, teammates, defenders, controlled_player, player_score, ai_score, meter_pos, meter_dir, current_state, crowd
    
    # Get customization from locker room
    customization = locker_room.get_customization()
    
    # Map customization parameters to Player class parameters
    player_params = {
        'skin_tone': customization.get('skin_color', (255, 220, 177)),
        'hair_color': (0, 0, 0),  # Default black hair
        'jersey_color': customization.get('jersey_color', (200, 50, 50)),
        'shorts_color': customization.get('jersey_color', (200, 50, 50)),
        'shoes_color': customization.get('shoe_color', (255, 255, 255)),
        'number': "23"
    }
    
    # Initialize game objects with customization
    player = Player(100, 300, **player_params)
    ai = AI(600, 300)
    ball = Ball(player.x, player.y)
    hoop = Hoop(1180, 300)  # Position at the actual end of the court (1200 - backboard width)
    
    # Initialize AI teammates and defenders
    teammates = TeammateManager()
    defenders = DefenderManager()
    
    # Initialize ultra-realistic crowd system
    crowd = Crowd(WIDTH, HEIGHT)
    
    # Start by controlling the main player
    controlled_player = player
    
    # Reset scores and meter
    player_score = 0
    ai_score = 0
    meter_pos = 0.0
    meter_dir = 1
    
    # Change state to playing
    current_state = STATE_PLAYING

running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_state == STATE_LOCKER_ROOM:
            result = locker_room.handle_event(event)
            if result == "start_game":
                start_game()
        
        elif current_state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot using the shot meter if ball is currently held
                    if ball.held and controlled_player:
                        meter_good = meter_green_zone[0] <= meter_pos <= meter_green_zone[1]
                        
                        # Distance affects shot power (farther = less power)
                        player_center_x = controlled_player.x + controlled_player.width // 2
                        player_center_y = controlled_player.y + controlled_player.height // 2
                        dist = math.hypot(player_center_x - hoop.rim_x, player_center_y - hoop.rim_y)
                        power = max(0.4, 1 - min(dist / 400, 1))
                        
                        # Pass hoop coordinates for perfect shots
                        ball.shoot(meter_good, power, hoop.rim_x, hoop.rim_y)
                
                elif event.key == pygame.K_p:
                    # Pass ball to nearest teammate
                    if ball.held and controlled_player and teammates:
                        nearest_teammate = find_nearest_teammate(controlled_player, teammates.teammates)
                        if nearest_teammate:
                            pass_ball_to_teammate(controlled_player, nearest_teammate)
                            # Switch control to the teammate receiving the pass
                            controlled_player = nearest_teammate
                
                elif event.key == pygame.K_TAB:
                    # Switch control to next teammate
                    if teammates:
                        current_index = -1
                        if controlled_player in teammates.teammates:
                            current_index = teammates.teammates.index(controlled_player)
                        elif controlled_player == player:
                            current_index = -1
                        
                        # Switch to next player in cycle
                        next_index = (current_index + 1) % (len(teammates.teammates) + 1)
                        if next_index < len(teammates.teammates):
                            controlled_player = teammates.teammates[next_index]
                        else:
                            controlled_player = player
    
    if current_state == STATE_LOCKER_ROOM:
        locker_room.draw()
        pygame.display.update()
    
    elif current_state == STATE_PLAYING:
        keys = pygame.key.get_pressed()
        
        # Only move the controlled player
        if controlled_player:
            controlled_player.move(keys)
        
        ai.move()
        
        # Update AI teammates and defenders
        if teammates and defenders:
            # Update teammates with current controlled player as the "main" player
            teammates.update(controlled_player, ball, defenders.defenders, hoop)
            defenders.update(controlled_player, teammates.teammates, ball, hoop)
            
            # Check for steals and blocks
            if defenders.check_steals(controlled_player, ball):
                # Ball was stolen - reset to defender
                ball.reset()
                meter_pos = 0.0
                meter_dir = 1
                
            if defenders.check_blocks(ball, hoop):
                # Shot was blocked - reset ball
                ball.reset()
                meter_pos = 0.0
                meter_dir = 1
        
        # Update ultra-realistic crowd system
        if crowd:
            # Update crowd based on ball position and game action
            ball_action = ball.held and controlled_player
            crowd.update((ball.x, ball.y), ball_action)
        
        # Update hoop animations
        hoop.update(ball_action and ball_action)
        
        # Update camera to follow controlled player
        if controlled_player:
            camera_x = controlled_player.x + controlled_player.width // 2 - WIDTH // 2
            camera_y = controlled_player.y + controlled_player.height // 2 - HEIGHT // 2
        
        # Shot meter movement (only while ball is held)
        if ball.held:
            meter_pos += meter_dir * meter_speed
            if meter_pos <= 0:
                meter_pos = 0
                meter_dir = 1
            elif meter_pos >= 1:
                meter_pos = 1
                meter_dir = -1
        
        # Move the ball first
        ball.move()
        
        # Check for pass reception
        if not ball.held and controlled_player:
            # Check if controlled player is near the ball
            dist_to_ball = math.hypot(controlled_player.x - ball.x, controlled_player.y - ball.y)
            if dist_to_ball < 30:
                # Catch the ball
                ball.held = True
                ball.held_by = controlled_player
                ball.x = controlled_player.x + controlled_player.width // 2
                ball.y = controlled_player.y + controlled_player.height // 2
                meter_pos = 0.0
                meter_dir = 1
        
        # Keep the ball attached to the controlled player until shot
        if ball.held and controlled_player:
            ball.held_by = controlled_player
            ball.x = controlled_player.x + controlled_player.width // 2
            ball.y = controlled_player.y + controlled_player.height // 2
        
        # Reset the ball if it goes off-screen
        if ball.y > HEIGHT + 50 or ball.x > WIDTH + 50 or ball.x < -50:
            ball.reset()
            meter_pos = 0.0
            meter_dir = 1
        
        # Score when the ball passes through the rim from above
        if hoop.check_score(ball):
            player_score += 1
            ball.reset()
            meter_pos = 0.0
            meter_dir = 1
            # Trigger crowd celebration on score
            if crowd:
                crowd.trigger_celebration()
            # Trigger hoop animation
            hoop.update(True)
        
        # Draw street basketball court
        draw_court(screen, camera_x, camera_y)
        
        # Draw ultra-realistic crowd
        if crowd:
            crowd.draw(screen, camera_x, camera_y)
        
        # Draw the shot meter
        if ball.held:
            meter_color = (0, 255, 0) if meter_green_zone[0] <= meter_pos <= meter_green_zone[1] else (255, 255, 255)
            meter_x = 50
            meter_y = 550
            meter_width = 200
            meter_height = 15
            pygame.draw.rect(screen, (100, 100, 100), (meter_x, meter_y, meter_width, meter_height))
            fill_width = int(meter_pos * meter_width)
            pygame.draw.rect(screen, meter_color, (meter_x, meter_y, fill_width, meter_height))
        
        # Draw game objects with camera offset
        hoop.draw(screen, camera_x, camera_y)
        
        # Draw teammates and defenders
        if teammates and defenders:
            teammates.draw(screen, camera_x, camera_y)
            defenders.draw(screen, camera_x, camera_y)
        
        # Draw all players
        player.draw(screen, camera_x, camera_y)
        ai.draw(screen, camera_x, camera_y)
        
        # Draw control indicator above controlled player
        if controlled_player:
            control_x = controlled_player.x + controlled_player.width // 2 - camera_x
            control_y = controlled_player.y - 20 - camera_y
            
            # Draw arrow indicator
            pygame.draw.polygon(screen, (255, 255, 0), [
                (control_x, control_y),
                (control_x - 8, control_y - 10),
                (control_x + 8, control_y - 10)
            ])
            pygame.draw.polygon(screen, (255, 200, 0), [
                (control_x, control_y + 2),
                (control_x - 6, control_y - 8),
                (control_x + 6, control_y - 8)
            ])
            
            # Draw "YOU" text
            font_small = pygame.font.Font(None, 16)
            you_text = font_small.render("YOU", True, (255, 255, 0))
            you_rect = you_text.get_rect(center=(control_x, control_y - 15))
            screen.blit(you_text, you_rect)
        
        ball.draw(screen, camera_x, camera_y)
        
        # Draw controls help
        font_small = pygame.font.Font(None, 20)
        controls = [
            "Arrow Keys: Move",
            "SPACE: Shoot", 
            "P: Pass to teammate",
            "TAB: Switch player"
        ]
        for i, text in enumerate(controls):
            control_text = font_small.render(text, True, (200, 200, 200))
            screen.blit(control_text, (10, 10 + i * 20))
        
        score_text = font.render(f"{player_score} - {ai_score}", True, (255, 255, 255))
        screen.blit(score_text, (370, 20))
        
        pygame.display.update()

pygame.quit()