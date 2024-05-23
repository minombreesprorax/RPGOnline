"""The UI Handler for RPGOnline"""
import colorsys
import random
import pygame

if __name__ == "__main__":
    from resourcemanager import Res, reference_image
else:
    from modules.resourcemanager import Res, reference_image

def rainbow_hsv(hue):
    """
    Funny rainbow effect, why is it in UIHandler? Yes.
    """
    # Ensure hue is in the range [0, 360]
    hue %= 360

    # Convert hue to the range [0, 1] as expected by Pygame
    hue /= 360.0

    # Convert HSV color to RGB
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 1)

    # Scale RGB values from [0, 1] to [0, 255]
    rgba_color = (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

    return rgba_color

class UIElement(pygame.sprite.Sprite):
    def __init__(self, position, size, rotation=0):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.default_color = (0, 0, 0, 0)
        self.active_color = (0, 0, 0, 0)
        self.selected_color = (0, 0, 0, 0)
        self.current_color = self.default_color
        self.rotation = rotation
        self.update_rotation()

    def hsva(self, h, s, v, a=255):
        self.current_color.hsva = (h, s, v, a)

    def set_colors(self, default_color = None, active_color = None, selected_color = None):
        if default_color != None:
            self.default_color = default_color
        if active_color != None:
            self.active_color = active_color
        if selected_color != None:
            self.selected_color = selected_color
        self.current_color = self.default_color
        self.image.fill(self.current_color)
        self.original_image = self.image.copy()
        self.update_rotation()

    def set_active(self):
        self.current_color = self.active_color
        self.image.fill(self.current_color)
        self.original_image = self.image.copy()
        self.update_rotation()

    def set_selected(self):
        self.current_color = self.selected_color
        self.image.fill(self.current_color)
        self.original_image = self.image.copy()
        self.update_rotation()

    def set_default(self):
        self.current_color = self.default_color
        self.image.fill(self.current_color)
        self.original_image = self.image.copy()
        self.update_rotation()

    def set_rotation(self, angle):
        self.rotation = angle
        self.update_rotation()

    def update_rotation(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def render(self, surface):
        surface.blit(self.image, self.rect.topleft)

class UITextButton(UIElement):
    def __init__(self, text, font, position, width, height, on_click,
                 default_color=(0, 0, 0, 0), active_color=(100, 100, 100, 0), selected_color=(255, 0, 0, 0),
                 hover_color=(150, 150, 150, 0), border_color=(255, 255, 255), border_active_color=(255, 255, 0),
                 border_selected_color=(0, 255, 0)):
        super().__init__(position, (width, height))
        self.text = text
        self.font = font
        self.position = position
        self.width = width
        self.height = height
        self.on_click = on_click
        self.selected = False

        # Set up button properties
        self.border_color = border_color
        self.border_active_color = border_active_color
        self.border_selected_color = border_selected_color
        self.border_width = 5

        # Set colors
        self.set_colors(default_color, active_color, selected_color)

        # Additional color for hover
        self.hover_color = hover_color

        # Initial rendering
        self.create_image()

    def create_image(self):
        # Render text
        text_surface = self.font.render(self.text, True, self.border_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))

        # Draw button border
        pygame.draw.rect(self.image, self.border_color, pygame.Rect((0, 0), (self.width, self.height)), self.border_width)

        # Draw text on the button
        self.image.blit(text_surface, text_rect)

        # Set button rectangle
        self.rect = self.image.get_rect(topleft=self.position)
        self.original_image = self.image.copy()
        self.update_rotation()

    def update_image(self, color, border_color):
        # Create button surface with the given color
        if color is not None:
            self.image.fill(color)

        # Render text
        if border_color is not None:
            text_surface = self.font.render(self.text, True, border_color)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))

            # Draw button border
            pygame.draw.rect(self.image, border_color, pygame.Rect((0, 0), (self.width, self.height)), self.border_width)

            # Draw text on the button
            self.image.blit(text_surface, text_rect)

        self.original_image = self.image.copy()
        self.update_rotation()

    def set_active(self):
        super().set_active()
        self.update_image(self.active_color, self.border_active_color)
        self.selected = True

    def set_selected(self):
        super().set_selected()
        self.update_image(self.selected_color, self.border_selected_color)
        self.selected = True

    def set_default(self):
        super().set_default()
        self.update_image(self.default_color, self.border_color)
        self.selected = False

    def render(self, surface):
        super().render(surface)
    
    def set_colors(self, default_color = None, active_color = None, selected_color = None, default_border_color = None, active_border_color = None, selected_border_color = None,):
        if default_color != None:
            self.default_color = default_color
        if active_color != None:
            self.active_color = active_color
        if selected_color != None:
            self.selected_color = selected_color
        if default_border_color != None:
            self.border_color = default_border_color
        if active_border_color != None:
            self.border_active_color = active_border_color
        if selected_border_color != None:
            self.border_selected_color = selected_border_color
        self.update_image(self.default_color if default_color != None else None, self.border_color if default_border_color != None else None)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.set_selected()
            else:
                self.set_default()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_click()
                self.set_selected()
                self.set_active()  # Update the active state immediately after click
            else:
                self.set_default()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected:
                if self.rect.collidepoint(event.pos):
                    self.set_selected()
                else:
                    self.set_default()

class UIImageButton(UIElement):
    """This tool is deperecated, and won't be updated, meaning it's very buggy, and probably doesn't even work anymore thanks to updates. This class will be removed next update."""
    def __init__(self, position, image_path, action):
        print("Warning! Class UIImageButton is depercated and will be removed on the next update of the UIHandler.")
        image = pygame.image.load(image_path)
        size = image.get_size()
        super().__init__(position, size)
        self.image = image
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

class UILabel(UIElement):
    def __init__(self, position, text, font, color):
        text_surface = font.render(text, True, color)
        size = text_surface.get_size()
        super().__init__(position, size)
        self.text = text
        self.font = font
        self.color = color
        self.render_text()

    def render_text(self):
        self.image = self.font.render(self.text, True, self.color)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.update_rotation()

class UIImage(UIElement):
    def __init__(self, position, image_id, res_manager):
        image = res_manager.get(image_id, "images", IgnoreMissing=True)
        size = image.get_size()
        super().__init__(position, size)
        self.res_manager = res_manager
        self.image = image
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.update_rotation()

class UIAlignmentHandler:
    @staticmethod
    def align_center_x(element, container_rect):
        element.rect.centerx = container_rect.centerx

    @staticmethod
    def align_center_y(element, container_rect):
        element.rect.centery = container_rect.centery

    @staticmethod
    def align_center(element, container_rect):
        element.rect.center = container_rect.center

class UIListHandler:
    def __init__(self, elements=None):
        self.elements = elements or []
        self.spacing = 10
        self.alignment = "left"  # Default alignment

    def add_element(self, element):
        self.elements.append(element)

    def set_spacing(self, spacing):
        self.spacing = spacing

    def set_alignment(self, alignment):
        self.alignment = alignment

    def align_elements(self, container_rect):
        total_height = sum(element.rect.height + self.spacing for element in self.elements)
        if self.alignment == "left":
            current_y = container_rect.top
            for element in self.elements:
                element.rect.topleft = (container_rect.left, current_y)
                current_y += element.rect.height + self.spacing
        elif self.alignment == "center":
            current_y = container_rect.centery - total_height // 2
            for element in self.elements:
                element.rect.centerx = container_rect.centerx
                element.rect.top = current_y
                current_y += element.rect.height + self.spacing
        elif self.alignment == "right":
            current_y = container_rect.bottom - total_height
            for element in self.elements:
                element.rect.bottomright = (container_rect.right, current_y)
                current_y += element.rect.height + self.spacing

    def render_all(self, surface):
        for element in self.elements:
            element.render(surface)

    def handle_event(self, event):
        for element in self.elements:
            if hasattr(element, 'handle_event'):
                element.handle_event(event)

class UIGroupStepper(UIElement):
    def __init__(self, position, size, elements=None):
        super().__init__(position, size)
        self.elements = elements or []

    def add_element(self, element):
        self.elements.append(element)

    def render_all(self, surface):
        for element in self.elements:
            element.render(surface)

    def handle_event(self, event):
        for element in self.elements:
            if hasattr(element, 'handle_event'):
                element.handle_event(event)



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    res_manager = Res()
    # Load images using resource manager
    res_manager.append(reference_image("data/textures/fwog.png"), "fwog")

    # Example callback function for button click
    def button_clicked():
        button.text = "What did you expect?"

    # Example callback function for button click
    def button_clicked2():
        image.set_rotation(random.random()*359)

    # Example UI elements
    image = UIImage((450, 200), "fwog", res_manager)
    label1 = UILabel((100, 100), "UIEngine!", pygame.font.SysFont("comicsansms", 36), (255, 255, 255))
    label2 = UILabel((100, 160), "Spin", pygame.font.SysFont("comicsansms", 36), (127, 255, 127))
    button = UITextButton("A button that does nothing.", pygame.font.Font("data/fonts/Body.ttf", 18),(100, 300), 250, 50, button_clicked,default_color=(0, 0, 0),active_color=(100, 100, 100),selected_color=(0, 0, 0),border_color=(255, 255, 255),border_active_color=(0, 255, 0),border_selected_color=(0, 200, 0))
    button2 = UITextButton("Frog.", pygame.font.Font("data/fonts/Body.ttf", 18),(100, 375), 250, 50, button_clicked2)
    group_stepper = UIGroupStepper((0, 0), (800, 600))
    group_stepper.add_element(image)
    group_stepper.add_element(label1)
    group_stepper.add_element(label2)

    button_row = UIListHandler()
    button_row.add_element(button)
    button_row.add_element(button2)

    i = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            group_stepper.handle_event(event)
        

        i += 1
        label2.set_rotation(i)
        button2.set_colors(None, None, None, rainbow_hsv(i), rainbow_hsv(i), rainbow_hsv(i))
        group_stepper.render_all(screen)
        button_row.render_all(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
