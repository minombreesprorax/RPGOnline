"""
The resource manager for RPGOnline.
"""

import pygame
import os

def reference_image(path:str):
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    else:
        return None

def reference_audio(path:str):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        return None
    
class Res():
    def __init__(self) -> None:
        self.res = {"images": {}, "audio": {}}
        self.default_image_path = "data/textures/missing.png"
        self.default_audio_path = "data/sounds/missing.ogg"
        self.load_defaults()

    def load_defaults(self):
        if os.path.exists(self.default_image_path):
            self.default_image = pygame.image.load(self.default_image_path)
        else:
            print(f"Missing image file '{self.default_image_path}'")
            self.default_image = pygame.Surface((1, 1))  # Placeholder surface for missing images

        if os.path.exists(self.default_audio_path):
            self.default_audio = pygame.mixer.Sound(self.default_audio_path)
        else:
            print(f"Missing audio file '{self.default_audio_path}'")
            self.default_audio = None  # Placeholder for missing audio

    def append(self, content: any, id: str):
        if content is None:
            print(f"Skipped loading of None element '{id}'")
        elif isinstance(content, pygame.surface.Surface):
            if id in self.res["images"]:
                print(f"Skipped content, as it would overwrite element '{id}' of type '{type(content)}'.")
            else:
                print(f"Loaded image '{id}'.")
                self.res["images"][id] = content
        elif isinstance(content, pygame.mixer.Sound):
            if id in self.res["audio"]:
                print(f"Skipped content, as it would overwrite element '{id}' of type '{type(content)}'.")
            else:
                print(f"Loaded sound '{id}'.")
                self.res["audio"][id] = content

    def get(self, id:str, elementtype:str, IgnoreMissing:bool = False):
        try:
            return self.res[elementtype][id]
        except KeyError:
            if not IgnoreMissing:
                print(f"There is no such element as '{id}' of type '{elementtype}'! Use 'IgnoreMissing' to ignore this error.")
            if elementtype == "images":
                return self.default_image
            elif elementtype == "audio":
                return self.default_audio
