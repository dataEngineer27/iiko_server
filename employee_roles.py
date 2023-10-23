from helpers.database import session
from helpers import crud, micro


def app():
    print("Authenticated")
    key = micro.login()
    try:
        roles = micro.employee_roles(key=key)
    except:
        print("Key was expired")
        key = micro.login()
        print("Authenticated again")
        roles = micro.employee_roles(key=key)

    crud.add_roles(db=session, role_list=roles)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
