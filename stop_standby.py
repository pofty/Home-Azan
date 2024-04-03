import os
import play
import run_commands


def run_empty_sound():
    print("Playing silence")
    run_commands.set_volume(50)
    silence_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "silence.wav"))
    play.play_sound(silence_path)
    print("Silence finished playing")

