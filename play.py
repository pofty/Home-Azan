import simpleaudio as sa
import os
import run_commands
import time as Time


currently_playing_AZAN = False

def play_azan():
    print("Playing azan")
    azan_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "AZAN.wav"))
    sa.stop_all()
    play_sound(azan_path)
    print("Azan finished playing")


def play_sound(path: str):
    Time.sleep(2)
    wave_obj = sa.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def play_welcome_message():
    print("Playing welcome message")
    run_commands.connect_to_google_mini()
    Time.sleep(5)
    run_commands.set_volume(60)
    Time.sleep(2)
    welcome_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "Welcome.wav"))
    play_sound(welcome_path)
    print("Welcome message finished playing")
    run_commands.disconnect_from_google_mini()

