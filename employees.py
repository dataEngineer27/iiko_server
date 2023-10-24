from helpers.database import session
from helpers import crud, micro


def app():
    departments_dict = {}
    print("Authenticated")
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        departments_dict[f"{department.code}"] = department.id
    try:
        employees = micro.employee_list(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        employees = micro.employee_list(key=key)

    # dict_department = main.dict_department
    crud.add_employees(db=session, employee_list=employees, departments_dict=departments_dict)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
