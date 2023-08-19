import pygame

# Initializing pygame for audio
pygame.mixer.init()

class SoundController():
    
    def __init__(self):
        pygame.mixer.init()
        
        
    def play_sound(self, sound_filename):
        pygame.mixer.music.load(sound_filename)
        pygame.mixer.music.play()
        
        
    def is_playing(self):
        return pygame.mixer.music.get_busy()
    
    
    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.quit()