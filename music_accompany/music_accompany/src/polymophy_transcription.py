import pyaudio
import numpy as np
from essentia.standard import (
    PitchYinFFT,
    OnsetDetection,
    Windowing,
    FrameGenerator,
    FFT,
    CartesianToPolar,
    MultiPitchKlapuri,
    Spectrum,
)


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(midi_note):
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    return f"{NOTE_NAMES[note_index]}{octave}"


# ----------------------------
# Audio Settings
# ----------------------------
BUFFER_SIZE = 8192
HOP_SIZE = 2048
SAMPLE_RATE = 44100

# ----------------------------
# Essentia Algorithms
# ----------------------------

window = Windowing(type="hann")
onset_detector = OnsetDetection(method="complex")

# ----------------------------
# PyAudio Stream
# ----------------------------
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=HOP_SIZE,
)

fft = FFT()  # Outputs a complex FFT vector.
c2p = CartesianToPolar()  # Converts it into a pair of magnitude and phase vectors.

print("Listening... Press Ctrl+C to stop.")

try:
    while True:
        pitch_detector = MultiPitchKlapuri(
            frameSize=BUFFER_SIZE, sampleRate=SAMPLE_RATE
        )
        audio_chunk = stream.read(HOP_SIZE, exception_on_overflow=False)
        samples = np.frombuffer(audio_chunk, dtype=np.float32)

        # Break audio into overlapping frames
        for frame in FrameGenerator(
            samples, frameSize=BUFFER_SIZE, hopSize=HOP_SIZE, startFromZero=True
        ):
            frame_win = window(frame)

            # --- Onset detection ---
            magnitude, phase = c2p(fft(frame_win))
            onset_strength = onset_detector(magnitude, phase)
            # print(onset_strength)
            if onset_strength > 0.3:  # threshold
                print(f"Onset detected! Strength: {onset_strength:.3f}")

                # --- Pitch detection ---
                spectrum = Spectrum()(frame)

                pitches = pitch_detector(frame)
                print("pitch detection output ")
                print(pitches)

                # for pitch in pitches:
                #     print("one output")
                #     for note in pitch:
                #         # print("pitch ", pitch)
                #         midi_note = int(round(69 + 12 * np.log2(note / 440.0)))
                #         note_name = midi_to_note_name(midi_note)
                #         print(
                #             f"Pitch: {note:.2f} Hz, MIDI: {midi_note}, Note: {note_name}"
                #         )


except KeyboardInterrupt:
    print("Stopping...")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
