import get_prayer_times
import schedule
import time
import play
import run_commands
import stop_standby


def stop_standby_thread():
    print("Stop standby triggered")
    stop_standby.run_empty_sound()


def get_desired_times() -> list:
    return get_prayer_times.get_prayer_times()


def AzanHandler(name_of_azan: str):
    run_commands.connect_to_google_mini()

    if name_of_azan == "Fajar" or name_of_azan == "Sunrise":
        run_commands.set_volume(38)
        print("Volume set to 38%")
    else:
        run_commands.set_volume(55)

    # triggered
    print("Azan {} triggered".format(name_of_azan))
    if name_of_azan == "Fajar":
        play.play_azan_fajar()
    else:
        play.play_azan()
    run_commands.disconnect_from_google_mini()


# Schedule the function to run at the desired time every day
def schedule_function():
    prayer_times = get_desired_times()
    Fajar = prayer_times[0]
    Sunrise = prayer_times[1]
    Dhuhr = prayer_times[2]
    Asr = prayer_times[3]
    Maghrib = prayer_times[4]
    Isha = prayer_times[5]
    schedule.every().day.at(Fajar).do(AzanHandler, "Fajar")
    # schedule.every().day.at(Sunrise).do(AzanHandler, "Sunrise")
    schedule.every().day.at(Dhuhr).do(AzanHandler, "Dhuhr")
    schedule.every().day.at(Asr).do(AzanHandler, "Asr")
    schedule.every().day.at(Maghrib).do(AzanHandler, "Maghrib")
    schedule.every().day.at(Isha).do(AzanHandler, "Isha")

    # this is used to keep the speaker on
    # schedule.every(1).to(3).minutes.do(stop_standby_thread)


# Initial scheduling
schedule_function()
print("Welcome message will be played in 3 seconds")
time.sleep(3)
play.play_welcome_message()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
    current_time = time.strftime("%H:%M")  # Get current time in "HH:MM" format
    if current_time == "00:10":
        # Refresh the scheduling every 24 hours
        schedule.clear()
        schedule_function()
