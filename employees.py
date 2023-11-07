from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    departments_dict = {}
    session = SessionLocal()
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        departments_dict[f"{department.code}"] = department.id
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        employees = micro.employee_list(key=key)
    except:
        key = micro.login()
        employees = micro.employee_list(key=key)

    crud.add_employees(db=session, employee_list=employees, departments_dict=departments_dict)
    micro.logout(key=key)


# if __name__ == '__main__':
#     app()
