from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.login()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        try:
            shifts = micro.shift_list(key=key, department_id=department.id)
        except:
            key = micro.login()
            shifts = micro.shift_list(key=key, department_id=department.id)

        crud.add_shifts(db=session, shift_list=shifts, department_id=department.id)

    micro.logout(key=key)


if __name__ == '__main__':
    app()
