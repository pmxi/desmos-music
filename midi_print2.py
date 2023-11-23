# Updated to output beats not seconds (assumes 1 beat = 1 quarter note)
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

note_gain = {}  # Dictionary to store gain (velocity) for each note number

for track in midi_file.tracks:
    current_time_in_ticks = 0  # Current time in ticks
    for msg in track:
        current_time_in_ticks += msg.time  # Increment time by delta time of the message

        if msg.type == 'note_on':
            time_in_beats = current_time_in_ticks / midi_file.ticks_per_beat
            freq = midi_note_to_freq(msg.note)
            gain = msg.velocity / 127  # Normalizing velocity to a 0-1 range (Gain)
            note_gain[msg.note] = gain  # Store the gain for this note number
            start_time_in_beats = time_in_beats

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            end_time_in_beats = current_time_in_ticks / midi_file.ticks_per_beat
            gain = note_gain.get(msg.note, 0)  # Retrieve the stored gain for this note number
            if gain > 0:  # Only print if there was a valid note_on for this note
                print(f"\\operatorname{{tone}}\\left({freq:.2f},{gain:.2f}\\right)\\left\\{{{start_time_in_beats}<t<{end_time_in_beats}+k_{{1}}\\right\\}}")
