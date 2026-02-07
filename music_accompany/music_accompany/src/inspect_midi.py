import mido
import sys


def inspect_midi(file_path):
    mid = mido.MidiFile(file_path)
    channel_instruments = {}

    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            if msg.type == "program_change":
                channel_instruments[msg.channel] = msg.program
                print(f"  Channel {msg.channel} -> Program {msg.program}")

    print("\nSummary of channels:")
    for ch, prog in channel_instruments.items():
        print(f"Channel {ch}: Instrument program {prog}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_midi.py <file.mid>")
        sys.exit(1)

    midi_file = sys.argv[1]
    inspect_midi(midi_file)
