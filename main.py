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
#departments.app()

# nomenclature_categories.app()

nomenclature_groups.app()

nomenclatures.app()
#
#department_revenue.app()

employee_roles.app()

employees.app()

shift_list.app()

payments.app()
#
product_expense.app()


def startdepartmentravenue():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=department_revenue.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t,pill2kill))

def startdepartment():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=departments.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t,pill2kill))



def nomenclature_category():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=nomenclature_categories.app, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t,pill2kill))



def stopit():
    for t, stop_event in threading_events:
        stop_event.set()
        t.join()


# you can give instead of day weekdays like wednesdays
schedule.every().wednesday.at("08:00").do(startdepartment)
schedule.every().day.at("08:00").do(nomenclature_category)
schedule.every().day.at("08:00").do(startdepartmentravenue)



schedule.every().day.at('10:00').do(stopit)



while True:
    schedule.run_pending()
    time.sleep(20)