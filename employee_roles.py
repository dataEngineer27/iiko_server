from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        roles = micro.employee_roles(key=key)
    except:
        key = micro.login()
        roles = micro.employee_roles(key=key)

    crud.add_roles(db=session, role_list=roles)
    micro.logout(key=key)


# if __name__ == '__main__':
#     app()
