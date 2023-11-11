import threading
import apps

threading_events = []


# apps.departments()  1
# apps.nomenclature_categories()  2
# apps.nomenclature_groups()  3
# apps.nomenclatures()  4
# apps.department_revenue()  5
# apps.employee_roles()  6
# apps.employees()  7
# apps.shift_list()  8
# apps.payments()  9
# apps.product_expense()  10


def departments_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.departments, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def nomenclature_categories_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.nomenclature_categories, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def nomenclature_groups_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.nomenclature_groups, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def nomenclatures_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.nomenclatures, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def department_revenue_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.department_revenue, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def employee_roles_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.employee_roles, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def employees_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.employees, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def shift_list_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.shift_list, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def payments_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.payments, args=(pill2kill, 'task'))
    t.start()
    threading_events.append((t, pill2kill))


def product_expense_starter():
    global pill2kill
    global t
    pill2kill = threading.Event()
    t = threading.Thread(target=apps.product_expense, args=(pill2kill, 'task'))
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
    # print("Job stopped")
    for t, stop_event in threading_events:
        stop_event.set()
        t.join()

