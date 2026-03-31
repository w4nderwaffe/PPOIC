from pathlib import Path
import pygame


class SilentSound:
    def play(self):
        pass


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.music_enabled = True
        self.current_music = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            self.music_enabled = False

        self.load_defaults()

    def load_sound(self, name, path):
        if not self.enabled:
            self.sounds[name] = SilentSound()
            return

        file_path = Path(path)

        if not file_path.exists():
            self.sounds[name] = SilentSound()
            return

        try:
            self.sounds[name] = pygame.mixer.Sound(str(file_path))
        except pygame.error:
            self.sounds[name] = SilentSound()

    def load_defaults(self):
        self.load_sound("shoot", "assets/sounds/shoot.wav")
        self.load_sound("enemy_hit", "assets/sounds/enemy_hit.wav")
        self.load_sound("player_dead", "assets/sounds/player_dead.wav")
        self.load_sound("menu_move", "assets/sounds/menu_move.mp3")

    def play(self, name):
        sound = self.sounds.get(name)

        if sound is None:
            return

        try:
            sound.play()
        except pygame.error:
            pass

    def play_music(self, path, loops=-1, volume=0.45):
        if not self.music_enabled:
            return

        file_path = Path(path)

        if not file_path.exists():
            return

        normalized = str(file_path)

        if self.current_music == normalized:
            return

        try:
            pygame.mixer.music.load(normalized)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
            self.current_music = normalized
        except pygame.error:
            pass

    def stop_music(self):
        if not self.music_enabled:
            return

        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except pygame.error:
            pass