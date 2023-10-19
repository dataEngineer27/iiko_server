from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    try:
        roles = micro.employee_roles(key=key)
    except:
        key = micro.authiiko()
        roles = micro.employee_roles(key=key)

    crud.add_roles(db=session, role_list=roles)


if __name__ == '__main__':
    app()
