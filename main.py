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

job_start_time = str(input("Enter start time of job:  "))
jobs_end_time = str(input("Enter end time of all jobs:  "))

# List of jobs to start --- (You can give instead of day weekdays like wednesday)
# schedule.every().day.at(job_start_time).do(departments_starter)  # 1
# schedule.every().day.at(job_start_time).do(nomenclature_categories_starter)  # 2
# schedule.every().day.at(job_start_time).do(nomenclature_groups_starter)  # 3
# schedule.every().day.at(job_start_time).do(nomenclatures_starter)  # 4
# schedule.every().day.at(job_start_time).do(department_revenue_starter)   # 5
# schedule.every().day.at("18:16").do(employee_roles_starter)   # 6
# schedule.every().day.at("18:16").do(employees_starter)   # 7
# schedule.every().day.at("10:50").do(shift_list_starter)   # 8
# schedule.every().day.at("00:30").do(payments_starter)   # 9
schedule.every().thursday.at(job_start_time).do(product_expense_starter)   # 10
# schedule.every().day.at(job_start_time).do(stores_starter)   # 11
# schedule.every().day.at(job_start_time).do(store_remains_starter)   # 12
# schedule.every().day.at(job_start_time).do(store_incomings_starter)   # 13
# schedule.every().day.at(job_start_time).do(store_remains_starter)   # 14
# schedule.every().day.at(job_start_time).do(referenceunits_starter)   # 15
# schedule.every().day.at("06:30").do(product_expense_starter)   # 16

# Stop all jobs
# schedule.every().day.at('22:30').do(job_stopper)
schedule.every().monday.at(jobs_end_time).do(job_stopper)

while True:
    time.sleep(10)
    schedule.run_pending()
