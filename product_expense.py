from database import session
import crud
import micro


def app():
    key = micro.authiiko()
    departments = crud.get_all_department(db=session)
    for department in departments:
        product_details = crud.get_product(db=session, id=department.id)

        if department.is_added == 0:
            try:
                get_product_expense = micro.get_product_expense(key=key, department=department.id)
            except:
                key = micro.authiiko()
                get_product_expense = micro.get_product_expense(key=key, department=department.id)

            crud.add_product_expense(db=session,
                                     product_expense_list=get_product_expense,
                                     department=department.id,
                                     product_details=product_details)
            crud.update_shift_ids(db=session, id=department.id)


if __name__ == '__main__':
    app()
