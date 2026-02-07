import pygame.midi
import time
import sys


def play_midi(file_path):
    # Initialize the MIDI module
    pygame.midi.init()

    # Open the default MIDI output device
    player = pygame.midi.Output(pygame.midi.get_default_output_id())
    print("player ", player)

    # Load the MIDI file
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)

    print(f"🎵 Playing: {file_path}")
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Clean up
    del player
    pygame.midi.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python play_midi.py <file.mid>")
        sys.exit(1)

    play_midi(sys.argv[1])
