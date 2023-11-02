from helpers.database import session
from helpers import crud, micro


def app(stop_event, arg):
    key = micro.login()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        if stop_event.is_set():  # Check if stop event is set
            break
        if department.is_added == 0:
            try:
                department_revenue = micro.department_revenue(key=key, department=department.id)
            except:
                key = micro.login()
                try:
                    department_revenue = micro.department_revenue(key=key, department=department.id)
                except SyntaxError as e:
                    continue
            crud.add_department_revenue(db=session, department_revenue_list=department_revenue, department=department.id)
            crud.update_department(db=session, id=department.id)

    micro.logout(key=key)


if __name__ == '__main__':
    app()
