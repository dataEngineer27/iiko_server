import schedule
import time
from jobs import *


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


# List of jobs to start --- (You can give instead of day weekdays like wednesday)
# schedule.every().tuesday.at("12:48").do(departments_starter)  # 1
# schedule.every().day.at("08:00").do(nomenclature_categories_starter)  # 2
# schedule.every().day.at("08:00").do(nomenclature_groups_starter)  # 3
# schedule.every().day.at("13:05").do(nomenclatures_starter)  # 4
# schedule.every().day.at("10:14").do(department_revenue_starter)   # 5
# schedule.every().day.at("18:16").do(employee_roles_starter)   # 6
# schedule.every().day.at("18:16").do(employees_starter)   # 7
# schedule.every().day.at("10:50").do(shift_list_starter)   # 8
schedule.every().day.at("02:50").do(payments_starter)   # 9
# schedule.every().day.at("18:16").do(product_expense_starter)   # 10

# Stop all jobs
schedule.every().day.at('06:30').do(job_stopper)

while True:
    time.sleep(20)
    schedule.run_pending()
