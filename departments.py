from helpers.database import session,SessionLocal
from helpers import crud, micro


def app(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    try:
        departments = micro.department_list(key=key)
    except:
        key = micro.login()
        departments = micro.department_list(key=key)
    crud.add_departments(db=session, department_list=departments)
    micro.logout(key=key)


if __name__ == '__main__':
    app()