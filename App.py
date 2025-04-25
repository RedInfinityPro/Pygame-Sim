from Container.imports_library import *
import Building_Items, UI_Items
screenWidth, screenHeight = 700, 700

# Grid
class CreateGrid:
    def __init__(self, spacing=(40, 40), offset=(0, 0), width=1, color=pygame.Color("gray")):
        self.base_spacing = spacing
        self.spacing = list(spacing)
        self.offset = list(offset)
        self.width = width
        self.color = color

    def pan(self, dx, dy):
        self.offset[0] += dx
        self.offset[1] += dy

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        for x in range(-self.spacing[0], screen_width + self.spacing[0], self.spacing[0]):
            draw_x = x + self.offset[0] % self.spacing[0]
            pygame.draw.line(screen, self.color, (draw_x, 0), (draw_x, screen_height), self.width)

        for y in range(-self.spacing[1], screen_height + self.spacing[1], self.spacing[1]):
            draw_y = y + self.offset[1] % self.spacing[1]
            pygame.draw.line(screen, self.color, (0, draw_y), (screen_width, draw_y), self.width)

# application
class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dragging = False
        self.start_offset = (0, 0)
        # objects
        self.all_sprites = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.grid = CreateGrid()
        self.build_panel = Building_Items.BuildingPanel(grid=self.grid, position=(10, 10), scale=(100, 200))
        self.build_panel.add_item(Building_Items.BuildingSegments, position=(10, 10), scale=(40, 40), grid=self.grid)
        self.build_panel.add_item(Building_Items.BuildingSegments, position=(10, 10), scale=(40, 40), grid=self.grid, color=pygame.Color("green"))
        self.cursor_options = UI_Items.ContextMenu(initial_position=(0,0))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Objects
                self.build_panel.handle_event(event=event, all_sprites=self.all_sprites, item_list=self.item_list)
                # Grad
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        self.dragging = True
                        self.start_offset = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        dx = event.pos[0] - self.start_offset[0]
                        dy = event.pos[1] - self.start_offset[1]
                        for item in self.item_list:
                            item.update_transform((dx, dy))
                        self.grid.pan(dx, dy)
                        self.start_offset = event.pos
                # --->
                for i in self.item_list:
                    i.handle_event(event)
                self.cursor_options.handle_event(event)

            self.screen.fill(pygame.Color("white"))
            self.grid.draw(self.screen)
            
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.cursor_options.draw(screen=self.screen)

            self.build_panel.draw(screen=self.screen)
            # This is to update the scene
            self.clock.tick(64)
            pygame.display.flip()
            pygame.display.update()

if __name__ == "__main__":
    Application().run()
