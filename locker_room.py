import pygame

class LockerRoom:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Customization options
        self.skin_colors = [
            (255, 220, 177),  # Light
            (255, 195, 140),  # Medium-light
            (235, 170, 120),  # Medium
            (180, 120, 80),   # Medium-dark
            (120, 80, 50)     # Dark
        ]
        self.hair_styles = ["short", "long", "bald"]
        self.jersey_colors = [
            (255, 0, 0),     # Red
            (0, 0, 255),     # Blue
            (0, 255, 0),     # Green
            (255, 255, 0),   # Yellow
            (255, 0, 255),   # Magenta
            (0, 255, 255),   # Cyan
            (255, 165, 0),   # Orange
            (128, 128, 128)  # Gray
        ]
        self.shoe_colors = [
            (0, 0, 0),       # Black
            (255, 255, 255), # White
            (255, 0, 0),     # Red
            (0, 0, 255)      # Blue
        ]
        
        # Current selections
        self.current_skin = 0
        self.current_hair = 0
        self.current_jersey = 0
        self.current_shoes = 0
        
        # UI elements
        self.start_button = pygame.Rect(self.width//2 - 75, self.height - 100, 150, 50)
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Preview character
        self.preview_x = self.width // 2
        self.preview_y = self.height // 2 - 50
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check start button
            if self.start_button.collidepoint(mouse_pos):
                return "start_game"
            
            # Check skin color buttons
            for i, color in enumerate(self.skin_colors):
                button_rect = pygame.Rect(50, 100 + i * 40, 30, 30)
                if button_rect.collidepoint(mouse_pos):
                    self.current_skin = i
            
            # Check hair style buttons
            for i, style in enumerate(self.hair_styles):
                button_rect = pygame.Rect(150, 100 + i * 40, 80, 30)
                if button_rect.collidepoint(mouse_pos):
                    self.current_hair = i
            
            # Check jersey color buttons
            for i, color in enumerate(self.jersey_colors):
                button_rect = pygame.Rect(self.width - 200, 100 + i * 40, 30, 30)
                if button_rect.collidepoint(mouse_pos):
                    self.current_jersey = i
            
            # Check shoe color buttons
            for i, color in enumerate(self.shoe_colors):
                button_rect = pygame.Rect(self.width - 100, 100 + i * 40, 30, 30)
                if button_rect.collidepoint(mouse_pos):
                    self.current_shoes = i
        
        return None
    
    def draw(self):
        # Background
        self.screen.fill((139, 69, 19))  # Brown locker room
        
        # Title
        title = self.font.render("LOCKER ROOM - CUSTOMIZE YOUR PLAYER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width//2, 30))
        self.screen.blit(title, title_rect)
        
        # Skin color section
        skin_text = self.small_font.render("Skin Color:", True, (255, 255, 255))
        self.screen.blit(skin_text, (50, 70))
        for i, color in enumerate(self.skin_colors):
            button_rect = pygame.Rect(50, 100 + i * 40, 30, 30)
            pygame.draw.rect(self.screen, color, button_rect)
            if i == self.current_skin:
                pygame.draw.rect(self.screen, (255, 255, 0), button_rect, 3)
        
        # Hair style section
        hair_text = self.small_font.render("Hair Style:", True, (255, 255, 255))
        self.screen.blit(hair_text, (150, 70))
        for i, style in enumerate(self.hair_styles):
            button_rect = pygame.Rect(150, 100 + i * 40, 80, 30)
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            if i == self.current_hair:
                pygame.draw.rect(self.screen, (255, 255, 0), button_rect, 3)
            text = self.small_font.render(style, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        # Jersey color section
        jersey_text = self.small_font.render("Jersey:", True, (255, 255, 255))
        self.screen.blit(jersey_text, (self.width - 200, 70))
        for i, color in enumerate(self.jersey_colors):
            button_rect = pygame.Rect(self.width - 200, 100 + i * 40, 30, 30)
            pygame.draw.rect(self.screen, color, button_rect)
            if i == self.current_jersey:
                pygame.draw.rect(self.screen, (255, 255, 0), button_rect, 3)
        
        # Shoe color section
        shoe_text = self.small_font.render("Shoes:", True, (255, 255, 255))
        self.screen.blit(shoe_text, (self.width - 100, 70))
        for i, color in enumerate(self.shoe_colors):
            button_rect = pygame.Rect(self.width - 100, 100 + i * 40, 30, 30)
            pygame.draw.rect(self.screen, color, button_rect)
            if i == self.current_shoes:
                pygame.draw.rect(self.screen, (255, 255, 0), button_rect, 3)
        
        # Preview area
        preview_text = self.small_font.render("Preview:", True, (255, 255, 255))
        self.screen.blit(preview_text, (self.preview_x - 40, self.preview_y - 100))
        
        # Draw preview character
        self._draw_preview_character()
        
        # Start button
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)
        start_text = self.font.render("START GAME", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_rect)
    
    def _draw_preview_character(self):
        # Get current selections
        skin_color = self.skin_colors[self.current_skin]
        hair_style = self.hair_styles[self.current_hair]
        jersey_color = self.jersey_colors[self.current_jersey]
        shoe_color = self.shoe_colors[self.current_shoes]
        
        # Modern 2026 Xbox basketball player preview
        scale = 3  # Larger for better detail
        x = self.preview_x
        y = self.preview_y
        
        # Modern basketball shoes (detailed)
        shoe_width = 30
        shoe_height = 15
        # Left shoe with details
        pygame.draw.ellipse(self.screen, shoe_color, (x - 25, y + 100, shoe_width, shoe_height))
        pygame.draw.ellipse(self.screen, (255, 255, 255), (x - 25, y + 100, shoe_width, 2))  # Shoe stripe
        # Right shoe with details
        pygame.draw.ellipse(self.screen, shoe_color, (x - 5, y + 100, shoe_width, shoe_height))
        pygame.draw.ellipse(self.screen, (255, 255, 255), (x - 5, y + 100, shoe_width, 2))  # Shoe stripe
        
        # Modern basketball shorts (longer, baggier)
        pygame.draw.rect(self.screen, jersey_color, (x - 25, y + 50, 50, 55))
        pygame.draw.rect(self.screen, (255, 255, 255), (x - 25, y + 50, 50, 2))  # Shorts trim
        # Shorts side stripes
        pygame.draw.rect(self.screen, (255, 255, 255), (x - 20, y + 55, 3, 45))
        pygame.draw.rect(self.screen, (255, 255, 255), (x + 17, y + 55, 3, 45))
        
        # Modern basketball jersey (tank top style)
        pygame.draw.rect(self.screen, jersey_color, (x - 20, y + 10, 40, 45))
        # Jersey arm holes (rounded)
        pygame.draw.ellipse(self.screen, (139, 69, 19), (x - 28, y + 15, 15, 20))  # Left armhole
        pygame.draw.ellipse(self.screen, (139, 69, 19), (x + 13, y + 15, 15, 20))  # Right armhole
        
        # Jersey number with modern styling
        font = pygame.font.SysFont("arial", 20, bold=True)
        number_text = font.render("23", True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(x, y + 32))
        # Number shadow
        shadow_text = font.render("23", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(x + 1, y + 33))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(number_text, number_rect)
        
        # Muscular arms (detailed)
        # Left arm
        pygame.draw.ellipse(self.screen, skin_color, (x - 30, y + 20, 12, 35))
        pygame.draw.ellipse(self.screen, skin_color, (x - 32, y + 50, 8, 15))  # Forearm
        # Right arm
        pygame.draw.ellipse(self.screen, skin_color, (x + 18, y + 20, 12, 35))
        pygame.draw.ellipse(self.screen, skin_color, (x + 24, y + 50, 8, 15))  # Forearm
        
        # Modern hands with fingers
        # Left hand
        pygame.draw.ellipse(self.screen, skin_color, (x - 33, y + 60, 10, 12))
        for i, offset in enumerate([-4, -2, 0, 2]):
            pygame.draw.ellipse(self.screen, skin_color, (x - 32 + offset, y + 68, 2, 4))
        # Right hand
        pygame.draw.ellipse(self.screen, skin_color, (x + 23, y + 60, 10, 12))
        for i, offset in enumerate([-4, -2, 0, 2]):
            pygame.draw.ellipse(self.screen, skin_color, (x + 24 + offset, y + 68, 2, 4))
        
        # Detailed head (more realistic proportions)
        pygame.draw.ellipse(self.screen, skin_color, (x - 15, y - 10, 30, 25))
        
        # Modern hair styles
        if hair_style == "short":
            # Short fade/crew cut
            pygame.draw.ellipse(self.screen, (0, 0, 0), (x - 14, y - 15, 28, 20))
            pygame.draw.ellipse(self.screen, skin_color, (x - 10, y - 12, 20, 15))  # Fade effect
        elif hair_style == "long":
            # Long braids/dreads
            for i, offset in enumerate([-8, -4, 0, 4, 8]):
                pygame.draw.ellipse(self.screen, (0, 0, 0), (x + offset - 3, y - 20, 6, 25))
        # bald - no hair
        
        # Facial features (subtle)
        pygame.draw.ellipse(self.screen, (100, 100, 100), (x - 8, y - 5, 3, 2))  # Left eye
        pygame.draw.ellipse(self.screen, (100, 100, 100), (x + 5, y - 5, 3, 2))   # Right eye
        pygame.draw.arc(self.screen, (200, 150, 150), (x - 5, y, 10, 8), 0, 3.14, 2)  # Smile
        
        # Modern basketball accessories
        # Wristbands
        pygame.draw.rect(self.screen, (0, 0, 0), (x - 35, y + 55, 8, 4))
        pygame.draw.rect(self.screen, (0, 0, 0), (x + 27, y + 55, 8, 4))
        # Headband
        pygame.draw.rect(self.screen, (255, 0, 0), (x - 15, y - 12, 30, 4))
    
    def get_customization(self):
        return {
            'skin_color': self.skin_colors[self.current_skin],
            'hair_style': self.hair_styles[self.current_hair],
            'jersey_color': self.jersey_colors[self.current_jersey],
            'shoe_color': self.shoe_colors[self.current_shoes]
        }
