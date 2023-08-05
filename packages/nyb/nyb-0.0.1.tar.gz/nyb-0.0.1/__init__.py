import pygame

class pgtext:
    def text(font, size, text, color):
        font = pygame.font.Font(font, size)
        text = font.render(text, True, color)

    def blit(screen, text, font, fontsize, color, textxy):
        """Text sample for pygame"""
        font = pygame.font.Font(font,fontsize)
        text = font.render(text, True, color)
        screen.blit(text, textxy)

    def default(screen, text):
        font = pygame.font.Font(None, 32)
        text = font.render(text, True, "white")
        screen.blit(text, (0, 0))
        