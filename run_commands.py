import os


def run_command(command: str):
    os.system(command)

def set_volume(volume: int):
    print(f"Setting volume to {volume}%")
    run_command(f"amixer -D pulse sset Master {volume}%")


def connect_to_google_mini():
    print("Connecting to Google")
    run_command("bluetoothctl connect F8:0F:F9:A0:7C:3F")


def disconnect_from_google_mini():
    print("Google mini is disconnected now")
    run_command("bluetoothctl disconnect F8:0F:F9:A0:7C:3F")
