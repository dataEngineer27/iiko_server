from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        if department.is_added == 0:
            try:
                department_revenue = micro.department_revenue(key=key, department=department.id)
            except:
                key = micro.authiiko()
                department_revenue = micro.department_revenue(key=key, department=department.id)

            crud.add_department_revenue(db=session, department_revenue_list=department_revenue, department=department.id)
            crud.update_department_revenue(db=session, id=department.id)


if __name__ == '__main__':
    app()
