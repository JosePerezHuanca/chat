import pygame;

class Sound:
    pygame.mixer.init();
    def connectSound(self):
        sound=pygame.mixer.Sound('sounds/connect.ogg');
        sound.play();

    def disconnectSound(self):
        sound=pygame.mixer.Sound('sounds/disconnect.ogg');
        sound.play();

    def chatSound(self):
        sound=pygame.mixer.Sound('sounDS/chat.ogg');
        sound.play();
