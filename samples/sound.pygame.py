import pygame

reso_destroyed = "../audio/resonator_destroyed1.wav"
reso_deployed = "../audio/resonator_deployed1.wav"

print("pygame init:")
pygame.init()
print("pygame mixer init:")
pygame.mixer.init()
print("pygame music load:")
sounda = pygame.mixer.music.load(reso_destroyed)
print("pygame music play:")
sounda.play()
print("pygame soun play")

