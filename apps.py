import datetime
import json
from helpers.database import SessionLocal
from helpers import crud, micro


def departments(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        department_list = micro.department_list(key=key)
    except:
        key = micro.login()
        department_list = micro.department_list(key=key)
    crud.add_departments(db=session, department_list=department_list)
    micro.logout(key=key)


def stores(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        store_list = micro.store_list(key=key)
    except:
        key = micro.login()
        store_list = micro.store_list(key=key)
    crud.add_stores(db=session, store_list=store_list)
    micro.logout(key=key)


def store_remains(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    last_processed_item = crud.get_last_added_store_remaining(db=session)
    current_datetime = datetime.datetime.now()
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time().strftime("%H:%M:%S")
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    try:
        remains_list = micro.store_remainings(key=key, date=current_date, time=current_time)
    except:
        key = micro.login()
        remains_list = micro.store_remainings(key=key, date=current_date, time=current_time)
    i = 0
    if last_processed_item is not None:
        if current_date > last_processed_item.date:
            for item in remains_list:
                i += 1
                crud.add_store_remainings(db=session, item=item, current_datetime=current_datetime)
                print(f"Was inserted {i}-item")
        else:
            for item in remains_list:
                i += 1
                available_store_item = crud.get_store_remaining_item(db=session,
                                                                     store_id=item['store'] if item['store'] else None,
                                                                     nomenclature_id=item['product'] if item[
                                                                         'product'] else None,
                                                                     datetime=current_datetime)
                if available_store_item:
                    print(f"Was skipped existing {i}-item")
                    continue
                else:
                    crud.add_store_remainings(db=session, item=item, current_datetime=current_datetime)
                    print(f"Was inserted {i}-product")
    else:
        for item in remains_list:
            i += 1
            crud.add_store_remainings(db=session, item=item, current_datetime=current_datetime)
            print(f"Was inserted {i}-product")

    micro.logout(key=key)


def store_incomings(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    today = datetime.datetime.now().date()
    incoming_list = micro.store_incomings(key=key, date=today)
    incoming_list = incoming_list['data']
    print(incoming_list)
    # store_list = crud.get_all_stores(db=session)
    last_incoming = crud.get_last_added_incoming(db=session)
    i = 0
    if last_incoming is not None:
        if today > last_incoming.last_update.date():
            for item in incoming_list:
                i += 1
                if stop_event.is_set():  # Check if stop event is set
                    break
                crud.add_store_incoming(db=session, item=item)
        else:
            for item in incoming_list:
                print("ITEM: ", item)
                store_name = item['Store'] if 'Store' in item and item['Store'] is not None else None
                print(store_name, item['Store'])
                nomenclature_id = item['Product.Id'] if 'Product.Id' in item and item[
                    'Product.Id'] is not None else None
                doc_number = item['Document'] if 'Document' in item and item['Document'] is not None else None
                i += 1
                available_store_item = crud.get_store_incoming_item(db=session,
                                                                    store_name=store_name,
                                                                    nomenclature_id=nomenclature_id,
                                                                    doc_number=doc_number
                                                                    )
                if available_store_item:
                    print(f"Was skipped existing {i}-item")
                    continue
                else:
                    crud.add_store_incoming(db=session, item=item)
                    print(f"Was inserted {i}-item")
    else:
        for item in incoming_list:
            i += 1
            crud.add_store_incoming(db=session, item=item)
            print(f"Was inserted {i}-item")

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
    department_list = crud.get_all_departments(db=session)
    d = 0
    for department in department_list:
        key = micro.login()
        d += 1
        department_id = department.id
        if stop_event.is_set():  # Check if stop event is set
            break
        if department.is_added == 0:
            try:
                revenue_list = micro.department_revenue(key=key, department=department_id)['dayDishValues'][
                    'dayDishValue']
            except:
                crud.update_department(db=session, id=department_id)
                continue
            for item in revenue_list:
                date = item['date'] if "date" in item and item['date'] else None
                nomenclature_id = item['productId'] if "productId" in item and item['productId'] else None
                crud.add_department_revenue(db=session, item=item, department_id=department_id)
                print(f"Was inserted department №{d} - {department_id}: product-{nomenclature_id} in {date}")
            crud.update_department(db=session, id=department_id)
            # for item in revenue_list:
            #     date = item['date'] if "date" in item and item['date'] else None
            #     nomenclature_id = item['productId'] if "productId" in item and item['productId'] else None
            #     available_item = crud.get_revenue_item(db=session, date=date, department_id=department_id,
            #                                            nomenclature_id=nomenclature_id)
            #     if available_item:
            #         print(f"Exist item of department №{d} ({department_id}) in {date}: product - {nomenclature_id}")
            #         continue
            #     else:
            #         crud.add_department_revenue(db=session, item=item, department_id=department_id)
            #         crud.update_department(db=session, id=department_id)
            #         print(f"Was inserted department №{d} - {department_id}: in {date}")

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
    last_processed_payment = crud.get_last_added_payment(db=session)
    for shift in shifts:
        if stop_event.is_set():  # Check if stop event is set
            break
        if shift.is_added == 0:
            try:
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            except:
                key = micro.login()
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)

            if last_processed_payment is not None:
                if shift.id == last_processed_payment.shift_id:
                    for payment in shift_payments['data']:
                        payment_id = payment['PaymentTransaction.Id'] if payment['PaymentTransaction.Id'] else None
                        nomenclature_id = payment['DishId'] if payment['DishId'] else None
                        available_payment_item = crud.get_payment_item(db=session,
                                                                       shift_id=shift.id,
                                                                       payment_id=payment_id,
                                                                       nomenclature_id=nomenclature_id)
                        if available_payment_item:
                            continue
                        else:
                            crud.add_shift_payments(db=session, payment=payment)
                else:
                    for payment in shift_payments['data']:
                        crud.add_shift_payments(db=session, payment=payment)
            else:
                for payment in shift_payments['data']:
                    crud.add_shift_payments(db=session, payment=payment)
            crud.update_shift(db=session, id=shift.id)

    micro.logout(key=key)


def product_expense():
    session = SessionLocal()
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


def reference_units(stop_event, arg):
    session = SessionLocal()
    key = micro.login()
    root_type_list = ["Account", "AccountingCategory", "AlcoholClass", "AllergenGroup", "AttendanceType", "Conception",
                      "CookingPlaceType", "DiscountType", "MeasureUnit", "OrderType", "PaymentType", "ProductCategory",
                      "ProductScale", "ProductSize", "ScheduleType", "TaxCategory"]
    if stop_event.is_set():  # Check if stop event is set
        micro.logout(key=key)
        return
    for root_type in root_type_list:
        try:
            unit_list = micro.unit_list(root_type=root_type, key=key)
        except:
            key = micro.login()
            unit_list = micro.unit_list(root_type=root_type, key=key)
        crud.add_units(db=session, unit_list=unit_list)

    micro.logout(key=key)
