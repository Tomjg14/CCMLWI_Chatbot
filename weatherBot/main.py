from weatherBot import WeatherBot
import time

def getHour():
    t = time.asctime(time.localtime(time.time()))
    time_elements = t.split()
    clock_time = time_elements[3]
    clock_time = clock_time.split(":")
    hour = clock_time[0]
    return hour


def main(wb):
    hour = getHour()
    last_update_id = None
    while True:
        print("getting updates")
        updates = wb.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = wb.get_last_update_id(updates) + 1
            wb.handle_updates(updates)
        new_hour = getHour()
        if new_hour is not hour:
            wb.updateWeatherNimma()
            wb.updateMood()
        time.sleep(0.5)

if __name__ == '__main__':
    wb = WeatherBot()
    main(wb)
