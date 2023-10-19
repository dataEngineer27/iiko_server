from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    try:
        departments = micro.department_list(key=key)
    except:
        key = micro.authiiko()
        departments = micro.department_list(key=key)

    department_dict = crud.add_departments(db=session, department_list=departments)
    return department_dict


if __name__ == '__main__':
    # app()
    dict_department = app()
