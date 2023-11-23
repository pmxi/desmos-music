import mido
import sys

def midi_note_to_freq(note_number):
    """ Convert MIDI note number to frequency in Hz. """
    return 440 * 2 ** ((note_number - 69) / 12)

# Check if a filename argument was provided
if len(sys.argv) < 2:
    print("Usage: python script_name.py path_to_your_midi_file.mid")
    sys.exit(1)

midi_file_path = sys.argv[1]
midi_file = mido.MidiFile(midi_file_path)

for track in midi_file.tracks:
    current_time = 0  # Current time in ticks
    for msg in track:
        current_time += msg.time  # Increment time by delta time of the message

        if msg.type == 'note_on' or msg.type == 'note_off':
            # Convert tick to second
            time_in_seconds = mido.tick2second(current_time, midi_file.ticks_per_beat, mido.bpm2tempo(120))  # Using a default tempo of 120 BPM

            # Extract note information
            freq = midi_note_to_freq(msg.note)
            gain = msg.velocity / 127  # Normalizing velocity to a 0-1 range (Gain)
            if msg.type == 'note_on' and msg.velocity > 0:
                start_time = time_in_seconds
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                end_time = time_in_seconds
                # Print in the specified format
                print(f"\\operatorname{{tone}}\\left({freq:.5f},g\\right)\\left\\{{{start_time:.5f}<t<{end_time:.5f}+k_1\\right\\}}")

