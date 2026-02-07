from music21 import converter, midi
import sys
import os


def musicxml_to_midi(xml_path, midi_path=None):
    """
    Convert a MusicXML file to MIDI.

    Parameters:
        xml_path (str): Path to input MusicXML file
        midi_path (str, optional): Path to output MIDI file. Defaults to same name as XML.
    """
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"MusicXML file not found: {xml_path}")

    # Parse MusicXML
    score = converter.parse(xml_path)

    # Default output file
    if midi_path is None:
        midi_path = os.path.splitext(xml_path)[0] + ".mid"

    # Write to MIDI
    mf = midi.translate.music21ObjectToMidiFile(score)
    mf.open(midi_path, "wb")
    mf.write()
    mf.close()

    print(f"✅ Converted {xml_path} → {midi_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python musicxml_to_midi.py <input.musicxml> [output.mid]")
        sys.exit(1)

    input_xml = sys.argv[1]
    output_midi = sys.argv[2] if len(sys.argv) > 2 else None

    musicxml_to_midi(input_xml, output_midi)
