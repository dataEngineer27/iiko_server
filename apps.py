import json

from helpers.database import SessionLocal, session
from helpers import crud, micro


def departments(stop_event, arg):
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


def nomenclature_categories(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        categories = micro.category_list(key=key)
    except:
        key = micro.login()
        categories = micro.category_list(key=key)

    crud.add_categories(db=session, category_list=categories)
    micro.logout(key=key)


def nomenclature_groups(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        group_list = micro.nomenclature_groups(key=key)
    except:
        key = micro.login()
        group_list = micro.nomenclature_groups(key=key)

    crud.add_groups(db=session, group_list=group_list)
    micro.logout(key=key)


def nomenclatures(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        nomenclature_list = micro.nomenclature_list(key=key)
    except:
        key = micro.login()
        nomenclature_list = micro.nomenclature_list(key=key)

    crud.add_nomenclatures(db=session, nomenclature_list=nomenclature_list)
    micro.logout(key=key)


def department_revenue(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        if stop_event.is_set():  # Check if stop event is set
            break
        if department.is_added == 0:
            try:
                revenue_list = micro.department_revenue(key=key, department=department.id)
            except:
                key = micro.login()
                try:
                    revenue_list = micro.department_revenue(key=key, department=department.id)
                except SyntaxError as e:
                    crud.update_department(db=session, id=department.id)
                    continue
            crud.add_department_revenue(db=session, department_revenue_list=revenue_list, department=department.id)
            crud.update_department(db=session, id=department.id)

    micro.logout(key=key)


def employee_roles(stop_event, arg):
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


def employees(stop_event, arg):
    departments_dict = {}
    session = SessionLocal()
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        departments_dict[f"{department.code}"] = department.id
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        employee_list = micro.employee_list(key=key)
    except:
        key = micro.login()
        employee_list = micro.employee_list(key=key)

    crud.add_employees(db=session, employee_list=employee_list, departments_dict=departments_dict)
    micro.logout(key=key)


def shift_list(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        if stop_event.is_set():  # Check if stop event is set
            break
        try:
            shifts = micro.shift_list(key=key, department_id=department.id)
        except:
            key = micro.login()
            shifts = micro.shift_list(key=key, department_id=department.id)

        crud.add_shifts(db=session, shift_list=shifts, department_id=department.id)

    micro.logout(key=key)


def payments(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    shifts = crud.get_all_shifts(db=session)
    for shift in shifts:
        if stop_event.is_set():  # Check if stop event is set
            break
        if shift.is_added == 0:
            try:
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            except:
                key = micro.login()
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)

            crud.add_shift_payments(db=session, shift_payments=shift_payments)
            crud.update_shift(db=session, id=shift.id)

    micro.logout(key=key)


def product_expense():
    not_found_products = {}
    key = micro.login()
    department_list = crud.get_all_departments(db=session)
    for department in department_list:
        if department.is_added == 0:
            try:
                product_expense_list = micro.product_expenses(key=key, department=department.id)
            except:
                key = micro.login()
                product_expense_list = micro.product_expenses(key=key, department=department.id)

            not_found_products = crud.add_product_expense(db=session,
                                                          product_expense_list=product_expense_list,
                                                          department=department.id,
                                                          not_found_products=not_found_products)
            crud.update_department(db=session, id=department.id)
            with open("not_found_products(product_expense).json", "w+") as json_file:
                json.dump(not_found_products, json_file)

    crud.update_all_departments_is_added(db=session, departments=department_list)
    micro.logout(key=key)
