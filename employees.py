import departments
import main
from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        try:
            employees = micro.employee_list(key=key, department_code=department.code)
        except:
            print("Key was expired")
            key = micro.login()
            print("Authenticated again")
            employees = micro.employee_list(key=key, department_code=department.code)

        # dict_department = main.dict_department
        crud.add_employees(db=session, employee_list=employees, department_id=department.id)

    micro.logout(key=key)


if __name__ == '__main__':
    app()
