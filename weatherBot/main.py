from weatherBot import WeatherBot
import time

def main(wb):
    last_update_id = None
    while True:
        print("getting updates")
        updates = wb.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = wb.get_last_update_id(updates) + 1
            wb.handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    wb = WeatherBot()
    wb.initializeDB()
    main(wb)
