from weatherBot import WeatherBot
import time


'''
description: getHour() function will collect the current hour as two character int.
:hour: returns hours as int
'''
def getHour():
    t = time.asctime(time.localtime(time.time()))
    time_elements = t.split()
    clock_time = time_elements[3]
    clock_time = clock_time.split(":")
    hour = clock_time[0]
    return hour


'''
description: main(wb) is the main function that is used to run the weatherbot.
:wb: weatherBot object, this is a weatherBot object that is used to obtain certain functions from the weatherbot.
'''
def main(wb):
    wb.updateWeatherNimma()
    wb.updateMood()
    hour = getHour()
    last_update_id = None
    while True:
        print("updating..")
        updates = wb.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = wb.get_last_update_id(updates) + 1
            wb.handle_updates(updates,)
        new_hour = getHour()
        if new_hour is not hour:
            wb.updateWeatherNimma()
            wb.updateMood()
        time.sleep(0.5)

if __name__ == '__main__':
    wb = WeatherBot()
    main(wb)
