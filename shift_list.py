from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        try:
            shifts = micro.shift_list(key=key, department_id=department.id)
        except:
            print("Key was expired")
            key = micro.login()
            print("Authenticated again")
            shifts = micro.shift_list(key=key, department_id=department.id)

        crud.add_shifts(db=session, shift_list=shifts, department_id=department.id)

    micro.logout(key=key)


if __name__ == '__main__':
    app()
