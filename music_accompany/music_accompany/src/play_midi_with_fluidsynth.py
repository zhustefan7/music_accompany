import mido
import time
import sys
import subprocess
import os
import tempfile

# Path to your FluidSynth soundfont
SOUNDFONT_PATH = (
    "/Users/zheyaozhu/repo/music_accompany/asset/FluidR3_GM.sf2"  # Update if needed
)


def print_msg(input_path):
    mid = mido.MidiFile(input_path)

    for track in mid.tracks:
        for msg in track:
            print("time ", msg.time)


def filter_midi(input_path, keep_channels):
    """Filter a MIDI file to only include the given channels."""
    mid = mido.MidiFile(input_path)
    new_mid = mido.MidiFile(ticks_per_beat=mid.ticks_per_beat)

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        time_accum = 0
        for msg in track:
            if msg.is_meta:
                # Meta events just pass through
                new_track.append(msg)
            else:
                if msg.channel in keep_channels:
                    # Add any accumulated skipped time to this event
                    new_msg = msg.copy(time=msg.time + time_accum)
                    new_track.append(new_msg)
                    time_accum = 0
                else:
                    # Accumulate skipped time
                    time_accum += msg.time

        new_mid.tracks.append(new_track)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mid")
    new_mid.save(tmp.name)
    return tmp.name


def play_midi(file_path, keep_channels=None, soundfont_path=SOUNDFONT_PATH):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"MIDI file not found: {file_path}")
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"SoundFont file not found: {soundfont_path}")

    print_msg(file_path)
    if keep_channels is not None:
        file_path = filter_midi(file_path, keep_channels)

    print(f"🎵 Playing MIDI via FluidSynth: {file_path}")
    process = subprocess.Popen(
        ["fluidsynth", "-i", "-a", "coreaudio", "-g", "0.5", soundfont_path, file_path]
    )

    # Wait until playback finishes
    try:
        process.wait()
    except KeyboardInterrupt:
        print("Stopping playback...")
        process.terminate()
        process.wait()

    print("✅ Playback finished")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python play_midi_fluidsynth.py <file.mid> [channels...]")
        sys.exit(1)

    midi_file = sys.argv[1]
    keep_channels = list(map(int, sys.argv[2:])) if len(sys.argv) > 2 else None

    play_midi(midi_file, keep_channels)
