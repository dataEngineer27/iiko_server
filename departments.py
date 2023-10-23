from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    try:
        departments = micro.department_list(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        departments = micro.department_list(key=key)

    # department_dict = crud.add_departments(db=session, department_list=departments)
    crud.add_departments(db=session, department_list=departments)
    micro.logout(key=key)
    # return department_dict


if __name__ == '__main__':
    app()
    # dict_department = app()
