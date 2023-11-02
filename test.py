import threading
import schedule
import time
import datetime
threading_events = []

# Function to perform the work
def doit(stop_event, arg):
    for i in range(1000):
        if stop_event.is_set():  # Check if stop event is set
            break
        time.sleep(3)
        dt = datetime.datetime.today()
        seconds = dt.timestamp()
        print(f"working on {seconds}")

    print('Ending of process')
# Function to start the job in a thread
def startit():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=doit, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t,pill2kill))


# Function to stop the job
def stopit():
    for t, stop_event in threading_events:
        stop_event.set()
        t.join() # Wait for the thread to finish gracefully

schedule.every().day.at("19:29").do(startit)
schedule.every().day.at("19:29").do(startit)
schedule.every().day.at("19:29").do(startit)
schedule.every().day.at("19:29").do(startit)
schedule.every().day.at("19:29").do(startit)
schedule.every().day.at('10:00').do(stopit)

while True:
    schedule.run_pending()
    time.sleep(1)
