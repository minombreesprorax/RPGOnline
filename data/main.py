import subprocess
import sys
import pygame
import os
import modules.resourcemanager as ResourceManager
import modules.UIHandler as UI

def load_assets():
    assets = ResourceManager.Res()
    
    # Define directories for images and audio
    image_dir = 'data/textures'
    sound_effects_dir = 'data/sounds'
    music_dir = 'data/soundtrack'

    # Load images
    for filename in os.listdir(image_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_name = filename.rsplit(".", 1)[0]
            assets.append(ResourceManager.reference_image(os.path.join(image_dir, filename)), image_name)
    
    # Load sound effects
    for filename in os.listdir(sound_effects_dir):
        if filename.endswith(('.wav', '.mp3', '.ogg')):
            sound_name = filename.rsplit(".", 1)[0]
            assets.append(ResourceManager.reference_audio(os.path.join(sound_effects_dir, filename)), sound_name)
    
    # Load music
    for filename in os.listdir(music_dir):
        if filename.endswith(('.wav', '.mp3', '.ogg')):
            music_name = filename.rsplit(".", 1)[0]
            assets.append(ResourceManager.reference_audio(os.path.join(music_dir, filename)), music_name)
    
    return assets

# Function to display loading screen
def display_loading_screen(screen):
    font = pygame.font.Font(None, 74)
    text = font.render('Loading...', True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()

# Function to scale image without anti-aliasing
def scale_image(image, scale_factor):
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
state = "mainmenu"
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RPGOnline")

# Display loading screen
display_loading_screen(screen)

# Load assets
assets = load_assets()

# Define button click functions
def singleplayer_clicked():
    print("Singleplayer clicked")

def multiplayer_clicked():
    print("Multiplayer clicked")

def avatar_clicked():
    print("Avatar clicked")

def settings_clicked():
    print("Settings clicked")

def exit_clicked():
    print("Exit clicked")
    pygame.quit()
    quit()

# Create UI elements
main_menu_group = UI.UIGroupStepper((50, 0), (200, screen_height))
main_menu_background = UI.UIElement((0, 0), (260, screen_height))
main_menu_background_titler = UI.UIElement((260, 0), (75, 75))
main_menu_background.image.fill((0, 0, 0, 150))  # Transparent black background
main_menu_background_titler.image.fill((0, 0, 0, 150))  # Transparent black background
main_menu_group.add_element(main_menu_background)
main_menu_group.add_element(main_menu_background_titler)

# Create and add buttons
buttons = [
    ("Singleplayer", singleplayer_clicked),
    ("Multiplayer", multiplayer_clicked),
    ("Avatar", avatar_clicked),
    ("Settings", settings_clicked),
    ("Exit", exit_clicked)
]

button_height = 50
spacing = 15
total_button_height = (button_height + spacing) * len(buttons) - spacing
start_y = (screen_height - total_button_height) // 2

title = UI.UILabel((10, 10), "RPGONLINE", pygame.font.Font("data\\fonts\\Titles.ttf", 50), (255, 255, 255))
main_menu_group.add_element(title)

# Adjust the position of buttons
for text, click_handler in buttons:
    button = UI.UITextButton(text, pygame.font.Font("data\\fonts\\Body.ttf", 24), (spacing, start_y), 225, button_height, click_handler)
    main_menu_group.add_element(button)
    start_y += button_height + spacing

subprocess.Popen(['notepad.exe', 'data/README.txt'])

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        main_menu_group.handle_event(event)
    
    # Fill the screen with a color (e.g., black)
        screen.fill((255, 255, 255))
    
    if state == "mainmenu":
        # Get the background image
        bg = assets.get('background', 'images', True)
        
        # Calculate scaling factors
        scale_width = screen_width / bg.get_width()
        scale_height = screen_height / bg.get_height()
        
        # Choose the larger scale factor to cover the entire window
        scale_factor = max(scale_width, scale_height)
        
        # Scale the background image
        bg_scaled = scale_image(bg, scale_factor)
        
        # Get the rect of the scaled image and center it
        bg_rect = bg_scaled.get_rect()
        bg_rect.center = (screen_width // 2, screen_height // 2)

        # Blit the scaled and centered background image
        screen.blit(bg_scaled, bg_rect.topleft)

        main_menu_group.render_all(screen)
        
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
