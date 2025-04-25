from Container.imports_library import *

# OptionItem
class OptionItem:
    def __init__(self, position, scale, text, font_size=16):
        self.position = position
        self.scale = scale
        self.text = text
        self.font_size = font_size
        self.textColor = pygame.Color("black")
        self.rect = pygame.Rect(self.position, self.scale)
        self.font = pygame.font.SysFont("Arial", self.font_size) if pygame.font.get_init() else None

# MenuOption
class MenuOption(OptionItem):
    def __init__(self, position, scale, text, active_color, inactive_color, font_size=16):
        super().__init__(position, scale, text, font_size)
        self.position = position
        self.scale = scale
        self.text = text
        self.font_size = font_size
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.text_color = pygame.Color("black")
        self.hover = False
        self.clicked = False
        self.locked = False

    def draw(self, screen):
        # Draw background with rounded corners
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        # Draw text
        if self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.position[0] + self.scale[0] // 2, self.position[1] + self.scale[1] // 2))
            screen.blit(text_surface, text_rect)
        # Draw highlight border if hovering
        if self.hover:
            pygame.draw.rect(screen, pygame.Color("white"), self.rect, width=1, border_radius=3)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
        if not self.locked:
            if self.hover:
                self.color = self.active_color
            else:
                self.color = self.inactive_color
        else:
            self.text_color = pygame.Color("gray50")
            self.color = pygame.Color("gray80")

    def handle_event(self, event):
        if self.locked:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            if event.button == 1:  # Left click
                self.clicked = True
                return True
        return False

# MenuHeader
class MenuHeader(OptionItem):
    """Category header for the menu"""
    def __init__(self, position, scale, text, bg_color=pygame.Color("black"), font_size=18):
        super().__init__(position, scale, text, font_size)
        self.position = position
        self.scale = scale
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = pygame.Color("white")
        self.font = pygame.font.SysFont("Arial", self.font_size, True) if pygame.font.get_init() else None
    
    def draw(self, screen):
        # Draw header background with rounded top corners
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=3)
        # Draw text
        if self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(
                self.position[0] + self.scale[0] // 2, 
                self.position[1] + self.scale[1] // 2
            ))
            screen.blit(text_surface, text_rect)

# ContextMenu
class ContextMenu:
    def __init__(self, initial_position=(0, 0)):
        self.position = initial_position
        self.padding = 9
        self.item_height = 28
        self.header_height = 32
        self.min_width = 180
        self.items = []
        self.sections = {}
        self.visible = False
        self.active_section = None
        self.bg_color = pygame.Color("dark gray")
        self.border_color = pygame.Color("gray60")
        self.item_active_color = pygame.Color("dodgerblue4")
        self.item_inactive_color = pygame.Color("gray90")
        self.section_colors = ["Game State", "Building Options", "Service Options"]
        self.game_speed = 1
        # Initialize menu structure
        self._init_menu_structure()
        # Calculate menu dimensions
        self._update_layout()

    def _init_menu_structure(self):
        """Initialize the menu structure with sections and items"""
        self.sections = {
            "Game State": [
                {"text": "Stop/Play"},
                {"text": f"Game Speed +{self.game_speed}"},
                {"text": "Settings"},
                {"text": "Exit"}
            ],
            "Building Options": [
                {"text": "Remove"},
                {"text": "Rename"},
                {"text": "Check Price"},
                {"text": "Move"},
                {"text": "Change Color"}
            ],
            "Service Options": [
                {"text": "Open/Close"}
            ]
        }

    def _update_layout(self):
        """Recalculate menu dimensions and item positions"""
        # Clear existing items
        self.items = []
        
        # Calculate width based on text length
        max_text_len = 0
        for section, options in self.sections.items():
            max_text_len = max(max_text_len, len(section))
            for option in options:
                max_text_len = max(max_text_len, len(option["text"]))
        
        # Width calculation (ensure minimum width)
        self.width = max(self.min_width, max_text_len * 10 + self.padding * 2)
        
        # Calculate total height
        total_items = sum(len(options) for options in self.sections.values())
        total_sections = len(self.sections)
        self.height = (total_items * self.item_height) + (total_sections * self.header_height) + (self.padding * 2)
        
        # Create the menu rect
        self.rect = pygame.Rect(self.position, (self.width, self.height))
        
        # Create headers and items with proper positioning
        y_offset = self.position[1] + self.padding
        
        for section_name, options in self.sections.items():
            # Add section header
            header = MenuHeader(
                position=(self.position[0] + self.padding, y_offset),
                scale=(self.width - self.padding * 2, self.header_height),
                text=section_name,
                bg_color=pygame.Color("black")
            )
            self.items.append(header)
            y_offset += self.header_height
            
            # Add section items
            for option in options:
                item = MenuOption(
                    position=(self.position[0] + self.padding, y_offset),
                    scale=(self.width - self.padding * 2, self.item_height),
                    text=option["text"],
                    active_color=self.item_active_color,
                    inactive_color=self.item_inactive_color
                )
                self.items.append(item)
                y_offset += self.item_height

    def show(self, position):
        """Show the menu at the specified position"""
        self.position = position
        
        # Ensure menu stays within screen bounds
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Adjust horizontal position if needed
        if self.position[0] + self.width > screen_width:
            self.position = (screen_width - self.width - self.padding, self.position[1])
            
        # Adjust vertical position if needed
        if self.position[1] + self.height > screen_height:
            self.position = (self.position[0], screen_height - self.height - self.padding)
        
        self._update_layout()
        self.visible = True

    def hide(self):
        """Hide the menu"""
        self.visible = False

    def draw(self, screen):
        """Draw the menu on the screen"""
        if not self.visible:
            return
        
        # Draw menu background with shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, pygame.Color("gray30"), shadow_rect, border_radius=5)
        
        # Draw main background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, width=1, border_radius=5)
        
        # Draw all items
        for item in self.items:
            try:
                item.update()
                item.draw(screen)
            except:
                item.draw(screen)
            finally:
                pass

    def handle_event(self, event):
        """Handle mouse events"""
        if not self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
                self.show(event.pos)
                return True
            return False
        # Handle clicks outside the menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                self.hide()
                return True
        return False
        
    
        