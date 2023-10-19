import departments
from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    try:
        employees = micro.employee_list(key=key)
    except:
        key = micro.authiiko()
        employees = micro.employee_list(key=key)

    dict_department = departments.dict_department
    crud.add_employees(db=session, employee_list=employees, dict_department=dict_department)


if __name__ == '__main__':
    app()
