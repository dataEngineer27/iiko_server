import json
from helpers.database import session
from helpers import crud, micro


def app():
    not_found_products = {}
    print("Authenticated")
    key = micro.login()
    departments = crud.get_all_departments(db=session)
    for department in departments:
        if department.is_added == 0:
            try:
                get_product_expense = micro.product_expenses(key=key, department=department.id)
            except:
                print("Key was expired")
                key = micro.login()
                print("Authenticated again")
                get_product_expense = micro.product_expenses(key=key, department=department.id)

            not_found_products = crud.add_product_expense(db=session,
                                                          product_expense_list=get_product_expense,
                                                          department=department.id,
                                                          not_found_products=not_found_products)
            crud.update_department(db=session, id=department.id)

    print("\n //////////// NOT FOUND PRODUCTS ///////////// \n", not_found_products)
    with open("not_found_products(product_expense).json", "w+") as json_file:
        json.dump(not_found_products, json_file)
    crud.update_all_departments_is_added(db=session, departments=departments)
    micro.logout(key=key)


if __name__ == '__main__':
    app()
