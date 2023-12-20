import uuid

from sqlalchemy import and_, null
from sqlalchemy.orm import Session
import models
from sqlalchemy.exc import IntegrityError

from helpers.database import session


def add_departments(db: Session, department_list):
    department_list = department_list['corporateItemDtoes']['corporateItemDto']
    i = 0
    for department in department_list:
        i += 1
        id = department['id'] if 'id' in department else None
        parent_id = department['parentId'] if 'parentId' in department else None
        code = department['code'] if 'code' in department else None
        name = department['name'] if 'name' in department else None
        object_type = department['type'] if 'type' in department else None
        tax_payer_id = department['taxpayerIdNumber'] if 'taxpayerIdNumber' in department else None
        query = models.Departments(id=id,
                                   parent_id=parent_id,
                                   code=code,
                                   name=name,
                                   type=object_type,
                                   tax_payer_id=tax_payer_id)
        try:
            db.add(query)
            db.commit()
            print(f"Was inserted {i}-department:  {name}")
        except IntegrityError as e:
            print(f"Was occured error on {i}-department")
            db.rollback()
    print("Length of departments: ", len(department_list))


def add_stores(db: Session, store_list):
    store_list = store_list['corporateItemDtoes']['corporateItemDto']
    i = 0
    for store in store_list:
        i += 1
        id = store['id'] if 'id' in store else None
        department_id = store['parentId'] if 'parentId' in store else None
        code = store['code'] if 'code' in store and store['code'] is not None else None
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
            print(f"Was inserted {i}-store:  {name}")
        except IntegrityError as e:
            print(f"Was occured error on {i}-store")
            db.rollback()  # Rollback the transaction
    print("Length of stores: ", len(store_list))


def add_store_remainings(db: Session, item, current_datetime):
    store_id = item['store'] if 'store' in item else None
    product_id = item['product'] if 'product' in item else None
    amount = item['amount'] if 'amount' in item else None
    sum = item['name'] if 'name' in item else None

    query = models.StoreRemains(store_id=store_id,
                                nomenclature_id=product_id,
                                datetime=current_datetime,
                                amount=amount,
                                sum=sum
                                )
    try:
        db.add(query)
        db.commit()
        print(f"Was inserted item:  {product_id} to {store_id}")
    except IntegrityError as e:
        print(f"Was occured error")
        db.rollback()  # Rollback the transaction


def add_categories(db: Session, category_list):
    for category in category_list:
        query = models.Categories(id=category['id'],
                                  deleted=category['deleted'],
                                  name=category['name'])
        try:
            db.add(query)
            db.commit()
            print(f"Was added category: ", category['name'])
        except IntegrityError as e:
            print(f"Error of category: ", e)
            db.rollback()


def add_groups(db: Session, group_list):
    i = 0
    for group in group_list:
        i += 1
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
            print(f"Was added group-{i}: ", group['name'])
        except IntegrityError as e:
            print(f"Error of group-{i}: ", e)
            db.rollback()
    print("Length of groups: ", len(group_list))


def add_nomenclatures(db: Session, nomenclature_list):
    i = 0
    for nomenclature in nomenclature_list:
        i += 1
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
            print(f"Was added {i}-product: ", name)
        except IntegrityError as e:
            print(f"Error of {i}-product: ", e)
            db.rollback()  # Rollback the transaction

    print(f"Amount of products: {i}")


def add_units(db: Session, unit_list):
    global type
    i = 0
    for unit in unit_list:
        i += 1
        id = unit['id'] if 'id' in unit else None
        type = unit['rootType'] if 'rootType' in unit else None
        deleted = unit['deleted'] if 'deleted' in unit else None
        code = unit['code'] if 'code' in unit else None
        name = unit['name'] if 'name' in unit else None
        query = models.ReferenceUnits(id=id,
                                      type=type,
                                      deleted=deleted,
                                      code=code,
                                      name=name
                                      )
        try:
            db.add(query)
            db.commit()
            print(f"Was added {i}-unit: ", name)
        except IntegrityError as e:
            print(f"Error of {i}-unit: ", e)
            db.rollback()  # Rollback the transaction
    print(f"Added {i} units for this unit_type: {type}")


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
    order_id = payment['UniqOrderId.Id'] if 'UniqOrderId.Id' in payment and payment['UniqOrderId.Id'] else None
    order_num = payment['OrderNum'] if 'OrderNum' in payment and payment['OrderNum'] else None
    payment_id = payment['PaymentTransaction.Id'] if 'PaymentTransaction.Id' in payment and payment[
        'PaymentTransaction.Id'] else None
    created_at = payment['CloseTime'] if 'CloseTime' in payment and payment['CloseTime'] else None
    nomenclature_id = payment['DishId'] if 'DishId' in payment and payment['DishId'] else None
    nomenclature_name = payment['DishName'] if 'DishName' in payment and payment['DishName'] else None
    shift_id = payment['SessionID'] if 'SessionID' in payment and payment['SessionID'] else None
    shift_num = payment['SessionNum'] if 'SessionNum' in payment and payment['SessionNum'] else None
    cashier_id = payment['Cashier.Id'] if 'Cashier.Id' in payment and payment['Cashier.Id'] else None
    soldwithdish_id = payment['SoldWithDish.Id'] if 'SoldWithDish.Id' in payment and payment[
        'SoldWithDish.Id'] else None
    soldwithitem_id = payment['SoldWithItem.Id'] if 'SoldWithItem.Id' in payment and payment[
        'SoldWithItem.Id'] else None
    department_id = payment['Department.Id'] if 'Department.Id' in payment and payment['Department.Id'] else None
    ordertype_id = payment['OrderType.Id'] if 'OrderType.Id' in payment and payment['OrderType.Id'] else None
    ordertype = payment['OrderType'] if 'OrderType' in payment and payment['OrderType'] else None
    paymenttype_id = payment['PayTypes.GUID'] if 'PayTypes.GUID' in payment and payment['PayTypes.GUID'] else None
    paymenttype = payment['PayTypes'] if 'PayTypes' in payment and payment['PayTypes'] else None
    paymenttype_group = payment['PayTypes.Group'] if 'PayTypes.Group' in payment and payment['PayTypes.Group'] else None
    measure_unit = payment['DishMeasureUnit'] if 'DishMeasureUnit' in payment and payment['DishMeasureUnit'] else None
    nomenclature_amount = payment['DishAmountInt'] if 'DishAmountInt' in payment and payment['DishAmountInt'] else None
    nomenclature_sum = payment['DishSumInt'] if 'DishSumInt' in payment and payment['DishSumInt'] else None
    is_delivery = payment['Delivery.IsDelivery'] if 'Delivery.IsDelivery' in payment and payment[
        'Delivery.IsDelivery'] else None
    guest_num = payment['GuestNum'] if 'GuestNum' in payment and payment['GuestNum'] else None
    guestcard_num = payment['OrderDiscount.GuestCard'] if 'OrderDiscount.GuestCard' in payment and payment[
        'OrderDiscount.GuestCard'] else None
    guestcard_owner = payment['CardOwner'] if 'CardOwner' in payment and payment['CardOwner'] else None
    paymentcard_num = payment['CardNumber'] if 'CardNumber' in payment and payment['CardNumber'] else None
    bonuscard_num = payment['Bonus.CardNumber'] if 'Bonus.CardNumber' in payment and payment[
        'Bonus.CardNumber'] else None
    orderdiscount_type = payment['OrderDiscount.Type'] if 'OrderDiscount.Type' in payment and payment[
        'OrderDiscount.Type'] else None
    orderdiscount_type_id = [uuid.UUID(item) for item in
                             payment['OrderDiscount.Type.IDs'].split(", ")] if 'OrderDiscount.Type.IDs' in payment and \
                                                                               payment[
                                                                                   'OrderDiscount.Type.IDs'] else None
    orderincrease_type = payment['OrderIncrease.Type'] if 'OrderIncrease.Type' in payment and payment[
        'OrderIncrease.Type'] else None
    orderincrease_type_id = [uuid.UUID(item) for item in
                             payment['OrderIncrease.Type.IDs'].split(", ")] if 'OrderIncrease.Type.IDs' in payment and \
                                                                               payment[
                                                                                   'OrderIncrease.Type.IDs'] else None
    itemsalediscount_name = payment['ItemSaleEventDiscountType'] if 'ItemSaleEventDiscountType' in payment and payment[
        'ItemSaleEventDiscountType'] else None
    fiscalcheque_num = payment['FiscalChequeNumber'] if 'FiscalChequeNumber' in payment and payment[
        'FiscalChequeNumber'] else None
    discountdish_num = payment[
        'ItemSaleEventDiscountType.DiscountAmount'] if 'ItemSaleEventDiscountType.DiscountAmount' in payment and \
                                                       payment['ItemSaleEventDiscountType.DiscountAmount'] else None
    discount_percent = payment['DiscountPercent'] if 'DiscountPercent' in payment and payment[
        'DiscountPercent'] else None
    discount_sum = payment['DiscountSum'] if 'DiscountSum' in payment and payment['DiscountSum'] else None
    increase_percent = payment['IncreasePercent'] if 'IncreasePercent' in payment and payment[
        'IncreasePercent'] else None
    increase_sum = payment['IncreaseSum'] if 'IncreaseSum' in payment and payment['IncreaseSum'] else None
    full_sum = payment['fullSum'] if 'fullSum' in payment and payment['fullSum'] else None

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
        print(f"ERROR of {shift_id}: \n{e}\n\n")
        db.rollback()


def add_store_incoming(db: Session, item):
    doc_number = item['Document'] if 'Document' in item and item['Document'] else None
    incoming_date = item['DateTime.Typed'] if 'DateTime.Typed' in item and item['DateTime.Typed'] else None
    transaction_date = item['DateSecondary.DateTimeTyped'] if 'DateSecondary.DateTimeTyped' in item and item['DateSecondary.DateTimeTyped'] else None
    counteragent_id = item['Counteragent.Id'] if 'Counteragent.Id' in item and item['Counteragent.Id'] else None
    counteragent_type = item['Account.CounteragentType'] if 'Account.CounteragentType' in item and item['Account.CounteragentType'] else None
    store_name = item['Store'] if 'Store' in item and item['Store'] else None
    sum = item['Sum.Incoming'] if 'Sum.Incoming' in item and item['Sum.Incoming'] else None
    measureunit = item['Product.MeasureUnit'] if 'Product.MeasureUnit' in item and item['Product.MeasureUnit'] else None
    nomenclature_id = item['Product.Id'] if 'Product.Id' in item and item['Product.Id'] else None
    amount = item['Amount.In'] if 'Amount.In' in item and item['Amount.In'] else None

    query = models.StoreIncomings(doc_number=doc_number,
                                  incoming_date=incoming_date,
                                  transaction_date=transaction_date,
                                  counteragent_id=counteragent_id,
                                  counteragent_type=counteragent_type,
                                  store_name=store_name,
                                  sum=sum,
                                  measureunit=measureunit,
                                  nomenclature_id=nomenclature_id,
                                  amount=amount)
    try:
        db.add(query)
        db.commit()
        print("Добавлен вещь в склад")
    except IntegrityError as e:
        print("ERROR : \n", e)
        db.rollback()


def add_department_revenue(db: Session, item, department_id):
    date = item['date'] if "date" in item and item['date'] else None
    nomenclature_id = item['productId'] if "productId" in item and item['productId'] else None
    sum = item['value'] if "value" in item and item['value'] else None
    query = models.DepartmentRevenue(department_id=department_id,
                                     nomenclature_id=nomenclature_id,
                                     date=date,
                                     sum=sum)
    db.add(query)
    db.commit()


def add_product_expense(db: Session, product_expense_list, department):  # not_found_products
    for i in product_expense_list:
        product_id = i['productId'] if "productId" in i and i['productId'] else None
        # try:
        product_details = get_product(db=session, id=product_id)
        group_id = product_details.group_id
        category_id = product_details.category_id
        main_unit = product_details.main_unit
        # except:
        #     not_found_products[f"{department}"] = product_id
        #     group_id = None
        #     category_id = None
        #     main_unit = None
        date = i['date'] if "date" in i and i['date'] else None
        name = i['productName'] if "productName" in i and i['productName'] else None
        quantity = i['value'] if "value" in i and i['value'] else None
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
            # print("Added expense: ", product_id, date)
        except IntegrityError as e:
            db.rollback()
            # print("ERROR: \n", e)

    # return not_found_products


def get_product(db: Session, id):
    query = db.query(models.Nomenclatures).get(id)
    return query


def get_all_departments(db: Session):
    query = db.query(models.Departments).all()
    return query


def get_all_shifts(db: Session):
    query = db.query(models.ShiftList).all()
    return query


def get_all_stores(db: Session):
    query = db.query(models.Stores).all()
    return query


def get_payment_item(db: Session, shift_id, payment_id, nomenclature_id):
    payment_item = db.query(models.ShiftPayments).filter(and_(models.ShiftPayments.shift_id == shift_id,
                                                              models.ShiftPayments.payment_id == payment_id,
                                                              models.ShiftPayments.nomenclature_id == nomenclature_id)
                                                         ).first()
    return payment_item


def get_store_remaining_item(db: Session, store_id, nomenclature_id, datetime):
    remaining_item = db.query(models.StoreRemains).filter(and_(models.StoreRemains.store_id == store_id,
                                                               models.StoreRemains.nomenclature_id == nomenclature_id,
                                                               models.StoreRemains.datetime == datetime)
                                                          ).first()
    return remaining_item


def get_store_incoming_item(db: Session, store_name, nomenclature_id, doc_number):
    incoming_item = db.query(models.StoreIncomings).filter(and_(models.StoreIncomings.store_name == store_name,
                                                                models.StoreIncomings.nomenclature_id == nomenclature_id,
                                                                models.StoreIncomings.doc_number == doc_number)
                                                           ).first()
    return incoming_item


def get_revenue_item(db: Session, date, department_id, nomenclature_id):
    revenue_item = db.query(models.DepartmentRevenue).filter(and_(models.DepartmentRevenue.date == date,
                                                                  models.DepartmentRevenue.department_id == department_id,
                                                                  models.DepartmentRevenue.nomenclature_id == nomenclature_id)
                                                             ).first()
    return revenue_item



def get_last_added_payment(db: Session):
    last_payment = db.query(models.ShiftPayments).order_by(models.ShiftPayments.last_update.desc()).first()
    # last_added_shift = last_payment.shift_id
    return last_payment


def get_last_added_incoming(db: Session):
    last_incoming = db.query(models.StoreIncomings).order_by(models.StoreIncomings.last_update.desc()).first()
    return last_incoming


def get_last_added_store_remaining(db: Session):
    last_item = db.query(models.StoreRemains).order_by(models.StoreRemains.last_update.desc()).first()
    return last_item


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
