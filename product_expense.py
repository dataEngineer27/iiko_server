from helpers.database import session
from helpers import crud, micro


def app():
    key = micro.authiiko()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        product_details = crud.get_product(db=session, id=department.id)

        if department.is_added == 0:
            try:
                get_product_expense = micro.product_expenses(key=key, department=department.id)
            except:
                key = micro.authiiko()
                get_product_expense = micro.product_expenses(key=key, department=department.id)

            crud.add_product_expense(db=session,
                                     product_expense_list=get_product_expense,
                                     department=department.id,
                                     product_details=product_details)
            crud.update_shift(db=session, id=department.id)


if __name__ == '__main__':
    app()
