from sqlalchemy import and_
from sqlalchemy.orm import Session
import models
from sqlalchemy.exc import IntegrityError

from helpers.database import session


def add_departments(db: Session, department_list):
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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback() 


def add_stores(db: Session, store_list):
    for store in store_list:
        id = store['id'] if 'id' in store else None
        department_id = store['parentId'] if 'parentId' in store else None
        code = store['code'] if 'code' in store and store['code'] else None
        name = store['name'] if 'name' in store else None
        type = store['type'] if 'type' in store else None

        query = models.Stores(id=id,
                              department_id=department_id,
                              code=code,
                              name=name,
                              type=type
                              )
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction


def add_categories(db: Session, category_list):
    for category in category_list:
        query = models.Categories(id=category['id'],
                                  deleted=category['deleted'],
                                  name=category['name'])
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback() 


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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()


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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction


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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()


def add_employees(db: Session, employee_list, departments_dict):
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
        department_code = i.find('departmentCodes')
        department_id = departments_dict[department_code.text] if department_code is not None else None
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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction


def add_shifts(db: Session, shift_list, department_id):
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
                                 sum_write_off_orders=shift['sumWriteoffOrders'],
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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction


def add_shift_payments(db: Session, payment):
    order_id = payment['UniqOrderId.Id'] if payment['UniqOrderId.Id'] else None
    order_num = payment['OrderNum'] if payment['OrderNum'] else None
    payment_id = payment['PaymentTransaction.Id'] if payment['PaymentTransaction.Id'] else None
    created_at = payment['CloseTime'] if payment['CloseTime'] else None
    nomenclature_id = payment['DishId'] if payment['DishId'] else None
    nomenclature_name = payment['DishName'] if payment['DishName'] else None
    shift_id = payment['SessionID'] if payment['SessionID'] else None
    shift_num = payment['SessionNum'] if payment['SessionNum'] else None
    cashier_id = payment['Cashier.Id'] if payment['Cashier.Id'] else None
    soldwithdish_id = payment['SoldWithDish.Id'] if payment['SoldWithDish.Id'] else None
    soldwithitem_id = payment['SoldWithItem.Id'] if payment['SoldWithItem.Id'] else None
    department_id = payment['Department.Id'] if payment['Department.Id'] else None
    ordertype_id = payment['OrderType.Id'] if payment['OrderType.Id'] else None
    ordertype = payment['OrderType'] if payment['OrderType'] else None
    paymenttype_id = payment['PayTypes.GUID'] if payment['PayTypes.GUID'] else None
    paymenttype = payment['PayTypes'] if payment['PayTypes'] else None
    paymenttype_group = payment['PayTypes.Group'] if payment['PayTypes.Group'] else None
    measure_unit = payment['DishMeasureUnit'] if payment['DishMeasureUnit'] else None
    nomenclature_amount = payment['DishAmountInt'] if payment['DishAmountInt'] else None
    nomenclature_sum = payment['DishSumInt'] if payment['DishSumInt'] else None
    is_delivery = payment['Delivery.IsDelivery'] if payment['Delivery.IsDelivery'] else None
    guest_num = payment['GuestNum'] if payment['GuestNum'] else None
    guestcard_num = payment['OrderDiscount.GuestCard'] if payment['OrderDiscount.GuestCard'] else None
    guestcard_owner = payment['CardOwner'] if payment['CardOwner'] else None
    paymentcard_num = payment['CardNumber'] if payment['CardNumber'] else None
    bonuscard_num = payment['Bonus.CardNumber'] if payment['Bonus.CardNumber'] else None
    orderdiscount_type = payment['OrderDiscount.Type'] if payment['OrderDiscount.Type'] else None
    orderdiscount_type_id = payment['OrderDiscount.Type.IDs'] if payment['OrderDiscount.Type.IDs'] else None
    orderincrease_type = payment['OrderIncrease.Type'] if payment['OrderIncrease.Type'] else None
    orderincrease_type_id = payment['OrderIncrease.Type.IDs'] if payment['OrderIncrease.Type.IDs'] else None
    itemsalediscount_name = payment['ItemSaleEventDiscountType'] if payment['ItemSaleEventDiscountType'] else None
    fiscalcheque_num = payment['FiscalChequeNumber'] if payment['FiscalChequeNumber'] else None
    discountdish_num = payment['ItemSaleEventDiscountType.DiscountAmount'] if payment['ItemSaleEventDiscountType.DiscountAmount'] else None
    discount_percent = payment['DiscountPercent'] if payment['DiscountPercent'] else None
    discount_sum = payment['DiscountSum'] if payment['DiscountSum'] else None
    increase_percent = payment['IncreasePercent'] if payment['IncreasePercent'] else None
    increase_sum = payment['IncreaseSum'] if payment['IncreaseSum'] else None
    full_sum = payment['fullSum'] if payment['fullSum'] else None
    query = models.ShiftPayments(order_id=order_id,
                                 order_num=order_num,
                                 payment_id=payment_id,
                                 created_at=created_at,
                                 nomenclature_id=nomenclature_id,
                                 nomenclature_name=nomenclature_name,
                                 shift_id=shift_id,
                                 shift_num=shift_num,
                                 cashier_id=cashier_id,
                                 soldwithdish_id=soldwithdish_id,
                                 soldwithitem_id=soldwithitem_id,
                                 department_id=department_id,
                                 ordertype_id=ordertype_id,
                                 ordertype=ordertype,
                                 paymenttype_id=paymenttype_id,
                                 paymenttype=paymenttype,
                                 paymenttype_group=paymenttype_group,
                                 measure_unit=measure_unit,
                                 nomenclature_amount=nomenclature_amount,
                                 nomenclature_sum=nomenclature_sum,
                                 is_delivery=is_delivery,
                                 guest_num=guest_num,
                                 guestcard_num=guestcard_num,
                                 guestcard_owner=guestcard_owner,
                                 paymentcard_num=paymentcard_num,
                                 bonuscard_num=bonuscard_num,
                                 orderdiscount_type=orderdiscount_type,
                                 orderdiscount_type_id=orderdiscount_type_id,
                                 orderincrease_type=orderincrease_type,
                                 orderincrease_type_id=orderincrease_type_id,
                                 itemsalediscount_name=itemsalediscount_name,
                                 fiscalcheque_num=fiscalcheque_num,
                                 discountdish_num=discountdish_num,
                                 discount_percent=discount_percent,
                                 discount_sum=discount_sum,
                                 increase_percent=increase_percent,
                                 increase_sum=increase_sum,
                                 full_sum=full_sum
                                 )
    try:
        db.add(query)
        db.commit()
    except IntegrityError as e:
        db.rollback()


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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()


def add_product_expense(db: Session, product_expense_list, department, not_found_products):
    for i in product_expense_list:
        product_id = i.find('productId')
        product_id = product_id.text if product_id is not None else None
        try:
            product_details = get_product(db=session, id=product_id)
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
        try:
            db.add(query)
            db.commit()
        except IntegrityError as e:
            db.rollback()

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


def get_payment_item(db: Session, shift_id, payment_id, nomenclature_id):
    payment_item = db.query(models.ShiftPayments).filter(and_(models.ShiftPayments.shift_id == shift_id,
                                                              models.ShiftPayments.payment_id == payment_id,
                                                              models.ShiftPayments.nomenclature_id == nomenclature_id)
                                                         ).first()
    return payment_item


def get_last_added_payment(db: Session):
    last_payment = db.query(models.ShiftPayments).order_by(models.ShiftPayments.last_update.desc()).first()
    # last_added_shift = last_payment.shift_id
    return last_payment


def update_department(db: Session, id):
    obj = db.query(models.Departments).get(id)
    obj.is_added = 1
    db.commit()


def update_all_departments_is_added(db: Session, departments):
    for department in departments:
        obj = db.query(models.Departments).get(department.id)
        obj.is_added = 0
        db.commit()


def update_shift(db: Session, id):
    obj = db.query(models.ShiftList).get(id)
    obj.is_added = 1
    db.commit()
