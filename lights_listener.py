from datetime import datetime
import threading


def checkTime():
    # This function runs periodically every 1 second
    timer = threading.Timer(1, checkTime)
    timer.start()

    now = datetime.now()

    current_time = now.strftime("%I:%M")
    print("Current Time =", current_time)

    if(current_time == '11:06'):  # check if matches with the desired time
        print('success')
        timer.cancel()



# checkTime()