from sqlalchemy.orm import Session
import models
from sqlalchemy.exc import IntegrityError

from helpers.database import session


def add_departments(db: Session, department_list):
    # department_dict = {}
    for department in department_list:
        id = department.find('id')
        id = id.text if id is not None else None
        parent_id = department.find('parentId')
        parent_id = parent_id.text if parent_id is not None else None
        code = department.find('code')
        code = code.text if code is not None else None
        name = department.find('name')
        name = name.text if name is not None else None
        type_n = department.find('type')
        type_n = type_n.text if type_n is not None else None
        tax_payer_id = department.find('taxpayerIdNumber')
        tax_payer_id = tax_payer_id.text if tax_payer_id is not None else None
        query = models.Departments(id=id,
                                   parent_id=parent_id,
                                   code=code,
                                   name=name,
                                   type=type_n,
                                   tax_payer_id=tax_payer_id)
        db.add(query)
        db.commit()
        # department_dict[code] = id
        print("Was added department: ", name)
    # return department_dict


def add_categories(db: Session, category_list):
    # category_dict = {}
    for category in category_list:
        query = models.Categories(id=category['id'],
                                  deleted=category['deleted'],
                                  name=category['name'])
        db.add(query)
        db.commit()
        print("Was added category: ", category['name'])
        # category_dict[category['name']] = category['id']
    # return category_dict


def add_groups(db: Session, group_list):
    for group in group_list:
        if group['visibilityFilter'] is not None:
            department_list = group['visibilityFilter']['departments']
        else:
            department_list = None
        query = models.Groups(id=group['id'],
                              deleted=group['deleted'],
                              parent_id=group['parent'],
                              name=group['name'],
                              num=group['num'],
                              code=group['code'],
                              category_id=group['category'],
                              accountingCategory_id=group['accountingCategory'],
                              departments_visibility=department_list)
        db.add(query)
        db.commit()
        print("Was added department: ", group['name'])
    return True


# def add_tools(db:Session, lst, new_dict):
#     for i in lst:
#         try:
#             id = i.find('id')
#             id = id.text if id is not None else None
#             parent_id = i.find('parentId')
#             parent_id = parent_id.text if parent_id is not None else None
#             num = i.find('num')
#             num = num.text if num is not None else None
#             code = i.find('code')
#             code = code.text if code is not None else None
#             name = i.find('name')
#             name = name.text if name is not None else None
#             product_type = i.find('productType')
#             product_type = product_type.text if product_type is not None else None
#             cooking_type_place = i.find('cookingPlaceType')
#             cooking_type_place = cooking_type_place.text if cooking_type_place is not None else None
#             main_unit = i.find('mainUnit')
#             main_unit = main_unit.text if main_unit is not None else None
#             category = i.find('productCategory')
#             category = new_dict[category.text] if category is not None else None
#             query = models.Nomenclatures(id= id,
#                                          parent_id=parent_id,
#                                          name=name,
#                                          num=num,
#                                          code=code,
#                                          product_type=product_type,
#                                          cooking_place_type=cooking_type_place,
#                                          main_unit=main_unit,
#                                          category_id=category)
#             db.add(query)
#             try:
#                 db.commit()
#             except IntegrityError as e:
#                 db.rollback()  # Rollback the transaction
#         except Exception as e:
#             pass
#     return True


def add_nomenclatures(db: Session, nomenclature_list):
    for nomenclature in nomenclature_list:
        id = nomenclature['id'] if 'id' in nomenclature else None
        group_id = nomenclature['parent'] if 'parent' in nomenclature else None
        category_id = nomenclature['category'] if 'category' in nomenclature else None
        accounting_category = nomenclature['accountingCategory'] if 'accountingCategory' in nomenclature else None
        name = nomenclature['name'] if 'name' in nomenclature else None
        num = nomenclature['num'] if 'num' in nomenclature else None
        code = nomenclature['code'] if 'code' in nomenclature and nomenclature['code'] else None
        main_unit = nomenclature['mainUnit'] if 'mainUnit' in nomenclature else None
        price = nomenclature['defaultSalePrice'] if 'defaultSalePrice' in nomenclature else None
        place_type = nomenclature['placeType'] if 'placeType' in nomenclature else None
        included_in_menu = nomenclature[
            'defaultIncludedInMenu'] if 'defaultIncludedInMenu' in nomenclature else None
        product_type = nomenclature['type'] if 'type' in nomenclature else None
        unit_weight = nomenclature['unitWeight'] if 'unitWeight' in nomenclature else None
        query = models.Nomenclatures(id=id,
                                     group_id=group_id,
                                     category_id=category_id,
                                     accounting_category=accounting_category,
                                     name=name,
                                     num=num,
                                     code=code,
                                     main_unit=main_unit,
                                     price=price,
                                     place_type=place_type,
                                     included_in_menu=included_in_menu,
                                     type=product_type,
                                     unit_weight=unit_weight)
        db.add(query)
        try:
            db.commit()
            print("Was added nomenclature: ", name)
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction
    return True


def add_roles(db: Session, role_list):
    for role in role_list:
        id = role.find('id')
        id = id.text if id is not None else None
        code = role.find('code')
        code = code.text if code is not None else None
        name = role.find('name')
        name = name.text if name is not None else None
        deleted = role.find('deleted')
        deleted = bool(deleted.text == 'true') if deleted is not None else False
        query = models.EmployeeRoles(id=id,
                                     code=code,
                                     name=name,
                                     deleted=deleted)
        db.add(query)
        db.commit()
        print("Was added employee role: ", name)
    return True


def add_employees(db: Session, employee_list, department_id):
    for i in employee_list:
        id = i.find('id')
        id = id.text if id is not None else None
        code = i.find('code')
        code = code.text if code is not None else None
        name = i.find('name')
        name = name.text if name is not None else None
        role_id = i.find('mainRoleId')
        role_id = role_id.text if role_id is not None else None
        roles = i.find('rolesIds')
        roles = [roles.text] if roles is not None else None
        role_codes = i.find('roleCodes')
        role_codes = role_codes.text if role_codes is not None else None
        role_code = i.find('mainRoleCode')
        role_code = role_code.text if role_code is not None else None
        # department_code = i.find('departmentCodes')
        # department_code = dict_department[department_code.text] if department_code is not None else None
        deleted = i.find('deleted')
        deleted = bool(deleted.text == 'true') if deleted is not None else False
        supplier = i.find('supplier')
        supplier = bool(supplier.text == 'true') if supplier is not None else False
        employee = i.find('employee')
        employee = bool(employee.text == 'true') if employee is not None else False
        client = i.find('client')
        client = bool(client.text == "true") if client is not None else False
        representstore = i.find('representsStore')
        representstore = bool(representstore.text == 'True') if representstore is not None else False
        query = models.Employees(id=id,
                                 code=code,
                                 name=name,
                                 role_id=role_id,
                                 roles=roles,
                                 role_codes=role_codes,
                                 role_code=role_code,
                                 department_id=department_id,
                                 deleted=deleted,
                                 supplier=supplier,
                                 employee=employee,
                                 client=client,
                                 representStore=representstore)
        db.add(query)
        try:
            db.commit()
            print(f"Was added employee of department: {name} of {department_id}")
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction
    return True


def add_shifts(db: Session, shift_list, department_id):
    # list_of_shifts = []
    for shift in shift_list:
        query = models.ShiftList(id=shift['id'],
                                 session_number=shift['sessionNumber'],
                                 fiscal_number=shift['fiscalNumber'],
                                 cash_reg_number=shift['cashRegNumber'],
                                 cash_reg_serial=shift['cashRegSerial'],
                                 open_date=shift['openDate'],
                                 close_date=shift['closeDate'],
                                 accepted_date=shift['acceptDate'],
                                 manager_id=shift['managerId'],
                                 responsible_user_id=shift['responsibleUserId'],
                                 session_start_cash=shift['sessionStartCash'],
                                 pay_orders=shift['payOrders'],
                                 sum_writeoff_orders=shift['sumWriteoffOrders'],
                                 sales_cash=shift['salesCash'],
                                 sales_credit=shift['salesCredit'],
                                 sales_card=shift['salesCard'],
                                 pay_in=shift['payIn'],
                                 pay_out=shift['payOut'],
                                 pay_income=shift['payIncome'],
                                 cash_remain=shift['cashRemain'],
                                 cash_diff=shift['cashDiff'],
                                 session_status=shift['sessionStatus'],
                                 conception_id=shift['conceptionId'],
                                 point_of_sale_id=shift['pointOfSaleId'],
                                 department_id=department_id
                                 )
        # list_of_shifts.append(shift['id'])
        db.add(query)
        try:
            db.commit()
            print(f"Was added shift of department: {shift['id']} of {department_id}")
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction
    # return list_of_shifts


def add_shift_payments(db: Session, shift_payments):
    department_dict = {}
    for payment in shift_payments['cashlessRecords']:
        query = models.ShiftPayments(id=payment['info']['id'],
                                     shift_id=shift_payments['sessionId'],
                                     date=payment['info']['creationDate'],
                                     group=payment['info']['group'],
                                     account_id=payment['info']['accountId'],
                                     counteragent_id=payment['info']['counteragentId'],
                                     payment_type_id=payment['info']['paymentTypeId'],
                                     type=payment['info']['paymentTypeId'],
                                     sum=payment['info']['sum'],
                                     user_id=payment['info']['auth']['user'],
                                     cause_event_id=payment['info']['causeEventId'],
                                     cashier_id=payment['info']['cashierId'],
                                     department_id=payment['info']['departmentId'],
                                     actual_sum=payment['actualSum'],
                                     original_sum=payment['originalSum'],
                                     edited_payaccount_id=payment["editedPayAccountId"],
                                     original_payaccount_id=payment['originalPayAccountId'],
                                     status=payment['status']
                                     )
        db.add(query)
        try:
            db.commit()
            print(f"Was added payment of shift: {payment['info']['id']} of {payment['info']['departmentId']}")
        except IntegrityError as e:
            db.rollback()

        # if shift_payments['sessionId'] not in department_dict.values():
        #     department_dict[shift_payments['sessionId']] = payment['info']['departmentId']

    # return department_dict
    return True


def add_department_revenue(db: Session, department_revenue_list, department):
    for revenue in department_revenue_list:
        date = revenue.find('date')
        date = date.text if date is not None else None
        product_id = revenue.find('productId')
        product_id = product_id.text if product_id is not None else None
        sum = revenue.find('value')
        sum = sum.text if sum is not None else None
        query = models.DepartmentRevenue(department_id=department,
                                         nomenclature_id=product_id,
                                         date=date,
                                         sum=sum)
        db.add(query)
        try:
            db.commit()
            print(f"Was added revenue of department: {department}")
        except IntegrityError as e:
            db.rollback()

    return True


def add_product_expense(db: Session, product_expense_list, department, not_found_products):
    for i in product_expense_list:
        product_id = i.find('productId')
        product_id = product_id.text if product_id is not None else None
        try:
            product_details = get_product(db=session, id=product_id)
            print("Product details type: ", type(product_details))
            group_id = product_details.group_id
            category_id = product_details.category_id
            main_unit = product_details.main_unit
        except:
            not_found_products[f"{department}"] = product_id
            group_id = None
            category_id = None
            main_unit = None
        date = i.find('date')
        date = date.text if date is not None else None
        name = i.find('productName')
        name = name.text if name is not None else None
        quantity = i.find('value')
        quantity = quantity.text if quantity is not None else None
        query = models.ProductExpense(nomenclature_id=product_id,
                                      category_id=category_id,
                                      group_id=group_id,
                                      department_id=department,
                                      date=date,
                                      name=name,
                                      quantity=quantity,
                                      main_unit=main_unit)
        db.add(query)
        try:
            db.commit()
            print(f"Was added product ({product_id}) expenses of department: ", department)
        except IntegrityError as e:
            db.rollback()
    print("\n ----------- Not found products -------------- \n", not_found_products)
    return not_found_products


def get_product(db: Session, id):
    query = db.query(models.Nomenclatures).get(id)
    return query


def get_all_departments(db: Session):
    query = db.query(models.Departments).all()
    return query


def get_all_shifts(db: Session):
    query = db.query(models.ShiftList).all()
    return query


def update_department(db: Session, id):
    # query = db.query(models.Departments).get(models.Departments.id == id).update({models.Departments.is_added: 1})
    obj = db.query(models.Departments).get(id)
    obj.is_added = 1
    db.commit()


def update_all_departments_is_added(db: Session, departments):
    for department in departments:
        db.query(models.Departments).get(department.id).update({models.Departments.is_added: 0})
        db.commit()
    return True


def update_shift(db: Session, id):
    query = db.query(models.ShiftList).filter(models.ShiftList.id == id).update({models.ShiftList.is_added: 1})
    db.commit()
    return True
