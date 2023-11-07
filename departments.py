from helpers.database import SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        departments = micro.department_list(key=key)
    except:
        key = micro.login()
        departments = micro.department_list(key=key)
    crud.add_departments(db=session, department_list=departments)
    micro.logout(key=key)


# if __name__ == '__main__':
#     app()