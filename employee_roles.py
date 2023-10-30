from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.login()
    try:
        roles = micro.employee_roles(key=key)
    except:
        key = micro.login()
        roles = micro.employee_roles(key=key)

    crud.add_roles(db=session, role_list=roles)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
