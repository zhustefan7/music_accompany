import pygame.midi

pygame.midi.init()

for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    (interf, name, is_input, is_output, opened) = info
    print(f"ID {i}: {name.decode()}  input:{is_input}  output:{is_output}")

pygame.midi.quit()
