import department_revenue
import departments
import employee_roles
import employees
import nomenclature_categories
import nomenclature_groups
import nomenclatures
import payments
import product_expense
import shift_list

import threading
import schedule
import time
import datetime

threading_events = []


# 1 # departments.app()

# 2 # nomenclature_categories.app()

# 3 # nomenclature_groups.app()

# 4 # nomenclatures.app()

# 5 # department_revenue.app()

# 6 # employee_roles.app()

# 7 # employees.app()

# 8 # shift_list.app()

# 9 # payments.app()

# 10 # product_expense.app()


def department_revenue_starter():
    print("Job started for department_revenue")
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=department_revenue.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def departments_starter():
    print("Job started")
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=departments.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def nomenclature_categories_starter():
    print("Job started")
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=nomenclature_categories.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def nomenclatures_starter():
    print("Job started for nomenclatures")
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=nomenclatures.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def job_starter(app):
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def job_stopper():
    print("Job stopped")
    for t, stop_event in threading_events:
        stop_event.set()
        t.join()


# List of jobs to start --- (You can give instead of day weekdays like wednesday)
# schedule.every().tuesday.at("12:48").do(departments_starter)  # 1
# schedule.every().day.at("08:00").do(nomenclature_categories_starter)  # 2
# schedule.every().day.at("13:05").do(nomenclatures_starter)  # 4
schedule.every().day.at("14:35").do(department_revenue_starter)   # 5

# Stop all jobs
schedule.every().day.at('18:00').do(job_stopper)

while True:
    time.sleep(20)
    schedule.run_pending()
