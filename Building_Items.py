from Container.imports_library import *

# build
class BuildingPanel:
    def __init__(self, grid, position=(10, 10), scale=(100, 100), item_size=(40, 40), color=pygame.Color('gray')):
        self.position = position
        self.scale = scale
        self.item_size = item_size
        self.color = color
        self.grid = grid
        self.rect = pygame.Rect(self.position, self.scale)
        # items
        self.items_per_row = 2
        self.padding = 10
        self.items = []
        self.selected_item = None
        self.dragged_instance = None
        self.update_panel_size()

    def update_panel_size(self):
        """Update the panel's size based on the number of items and layout."""
        total_items = len(self.items)
        rows = math.ceil(total_items / self.items_per_row)
        width = self.items_per_row * self.item_size[0] + (self.items_per_row + 1) * self.padding
        height = rows * self.item_size[1] + (rows + 1) * self.padding
        self.rect.size = (width, height)

    def add_item(self, item_class, **kwargs):
        self.items.append((item_class, kwargs))
        self.update_panel_size()
    
    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=1, border_radius=3)
        # Draw items in grid
        for index, (item_class, kwargs) in enumerate(self.items):
            row = index // self.items_per_row
            col = index % self.items_per_row
            x = self.rect.left + self.padding + col * (self.item_size[0] + self.padding)
            y = self.rect.top + self.padding + row * (self.item_size[1] + self.padding)
            icon_rect = pygame.Rect(x, y, *self.item_size)

            # Optional: Store icon_rect if needed for get_item_at_pos
            pygame.draw.rect(screen, self.darken_color(item_class, kwargs), icon_rect)
            
    def darken_color(self, item_class, kwargs):
        item_instance = item_class(**kwargs)
        r, g, b = item_instance.color[:3]
        return (int(r * 0.4), int(g * 0.4), int(b * 0.4))

    def get_item_at_pos(self, pos):
        for index, (item_class, kwargs) in enumerate(self.items):
            row = index // self.items_per_row
            col = index % self.items_per_row
            x = self.rect.left + self.padding + col * (self.item_size[0] + self.padding)
            y = self.rect.top + self.padding + row * (self.item_size[1] + self.padding)
            icon_rect = pygame.Rect(x, y, *self.item_size)

            if icon_rect.collidepoint(pos):
                return item_class, kwargs
        return None
    
    def handle_event(self, event, all_sprites, item_list):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = self.get_item_at_pos(event.pos)
                if result:
                    item_cls, kwargs = result
                    self.dragged_instance = item_cls(**kwargs)
                    all_sprites.add(self.dragged_instance)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragged_instance:
                snapped_x, snapped_y = self.dragged_instance.rect.center
                occupied = any(i.rect.center == (snapped_x, snapped_y) for i in item_list if i is not self.dragged_instance)
                if not occupied and not self.dragged_instance.placed:
                    self.dragged_instance.snap_to_grid((snapped_x, snapped_y))
                    item_list.add(self.dragged_instance)
                    self.dragged_instance.placed = True
                    self.dragged_instance = None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragged_instance:
                self.dragged_instance.rect.center = event.pos
                self.dragged_instance.x, self.dragged_instance.y = event.pos
                self.dragged_instance.snap_to_grid(self.dragged_instance.rect.center)

# sqaure item
class BuildingSegments(pygame.sprite.Sprite):
    def __init__(self, position, scale, grid, color=pygame.Color("red")):
        super().__init__()
        self.x, self.y = position
        self.base_width, self.base_height = scale
        self.width, self.height = scale
        self.grid = grid
        self.original_color = color
        self.color = color
        self.highlight_color = self.darken_color()
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.hovered = False
        self.placed = False
        self.snap_to_grid((self.x, self.y))

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        rect_width = min(self.width, self.grid.spacing[0] - 2)  # Subtract 2 for a small margin
        rect_height = min(self.height, self.grid.spacing[1] - 2)
        # Calculate the rectangle to be perfectly centered in the surface
        rect_x = (self.width - rect_width) // 2
        rect_y = (self.height - rect_height) // 2
        # Draw the rectangle centered on the surface
        pygame.draw.rect(self.image, self.color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(self.image, self.darken_color(), pygame.Rect(rect_x, rect_y, rect_width, rect_height), width=1)
    
    def snap_to_grid(self, position):
        """ Adjusts position to the nearest grid point. """
        grid_x = round((position[0] - self.grid.offset[0]) / self.grid.spacing[0]) * self.grid.spacing[0] + self.grid.offset[0]
        grid_y = round((position[1] - self.grid.offset[1]) / self.grid.spacing[1]) * self.grid.spacing[1] + self.grid.offset[1]
        self.x, self.y = grid_x, grid_y
        self.rect.center = (grid_x, grid_y)

    def update_transform(self, offset=None, zoom=None):
        if offset is not None:
            self.x += offset[0]
            self.y += offset[1]
        if zoom is not None:
            self.width = int(self.grid.spacing[0])
            self.height = int(self.grid.spacing[1])
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.draw()
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        self.snap_to_grid((self.x, self.y))
    
    def darken_color(self):
        r, g, b = self.color[:3]
        return (int(r * 0.4), int(g * 0.4), int(b * 0.4))
    
    def handle_event(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.highlight_color
            self.hovered = True
        else:
            self.hovered = False
            self.color = self.original_color
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)