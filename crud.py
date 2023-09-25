from sqlalchemy.orm import Session
import models
import pytz
from typing import Optional
from sqlalchemy.exc import IntegrityError



def add_departments(db:Session,lst):
    department_dict = {}
    for i in lst:

        id = i.find('id')
        id = id.text if id is not None else None
        parent_id = i.find('parentId')
        parent_id = parent_id.text if parent_id is not None else None
        code = i.find('code')
        code = code.text if code is not None else None
        name = i.find('name')
        name = name.text if name is not None else None
        type_n =  i.find('type')
        type_n = type_n.text if type_n is not None else None
        tax_payer_id = i.find('taxpayerIdNumber')
        tax_payer_id = tax_payer_id.text if tax_payer_id is not None else None
        query= models.Departments(id = id,parent_id=parent_id,code =code,name=name,type = type_n,tax_payer_id=tax_payer_id)
        db.add(query)
        db.commit()
        department_dict[code]=id
    return department_dict



def add_categories(db:Session,lst):
    new_dict = {}
    for i in lst:
        query = models.Categories(id=i['id'],deleted=i['deleted'],name=i['name'])
        db.add(query)
        db.commit()
        new_dict[i['name']]=i['id']
    return new_dict



def add_groups(db:Session,lst):
    
    for i in lst:
        if i['visibilityFilter'] is not None:
            dep_list = i['visibilityFilter']['departments']
        else:
            dep_list = None
        query = models.Groups(id=i['id'],deleted=i['deleted'],parent_id=i['parent'],name=i['name'],num=i['num'],code=i['code'],category_id=i['category'],accountingCategory_id=i['accountingCategory'],departments_visibility=dep_list)
        db.add(query)
        db.commit()
        

    return True

def add_tools(db:Session,lst,new_dict):

    for i in lst:
        try:
            id = i.find('id')
            id = id.text if id is not None else None
            parent_id = i.find('parentId')
            parent_id = parent_id.text if parent_id is not None else None
            num = i.find('num')
            num = num.text if num is not None else None
            code = i.find('code')
            code = code.text if code is not None else None
            name = i.find('name')
            name = name.text if name is not None else None
            product_type = i.find('productType')
            product_type= product_type.text if product_type is not None else None
            cooking_type_place = i.find('cookingPlaceType')
            cooking_type_place = cooking_type_place.text if cooking_type_place is not None else None
            main_unit = i.find('mainUnit')
            main_unit = main_unit.text if main_unit is not None else None
            category = i.find('productCategory')
            category = new_dict[category.text] if category is not None else None
            query  = models.Tools(id= id,parent_id=parent_id,name=name,num=num,code=code,product_type=product_type,cooking_place_type=cooking_type_place,main_unit=main_unit,category_id=category)
            db.add(query)
            try:
                db.commit()
            except IntegrityError as e:
                db.rollback()  # Rollback the transaction
        except Exception as e:
            pass
    return True


def add_roles(db:Session,lst):
    for i in lst:
        id = i.find('id')
        id = id.text if id is not None else None
        code =i.find('code')
        code = code.text if code is not None else None
        name = i.find('name')
        name = name.text if name is not None else None
        deleted = i.find('deleted')
        deleted = bool(deleted.text == 'true') if deleted is not None else False
        query = models.EmployeeRoles(id=id,code = code,name =name,deleted=deleted)
        db.add(query)
        db.commit()
    return True


def add_employees(db:Session,lst,dict_department):
    for i in lst:

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
        department_code = dict_department[department_code.text] if department_code is not None else None
        deleted = i.find('deleted')
        deleted = bool(deleted.text == 'true') if deleted is not None else False
        supplier = i.find('supplier')
        supplier = bool(supplier.text == 'true') if supplier is not None else False
        employee = i.find('employee')
        employee = bool(employee.text=='true') if employee is not None else False
        client = i.find('client')
        client = bool(client.text=="true") if client is not None else False
        representstore = i.find('representsStore')
        representstore = bool(representstore.text =='True') if representstore is not None else False
        query = models.Employees(id=id,code=code,name=name,role_id=role_id,roles=roles,role_codes=role_codes,role_code=role_code,department_id=department_code,deleted=deleted,supplier=supplier,employee=employee,client=client,representStore=representstore)
        db.add(query)
        db.commit()
    return True



def add_employee_shifts(db:Session,lst):
    list_of_shifts = []
    for i in lst:
        query = models.Shift_list(id=i['id'],
                                  session_number = i['sessionNumber'],
                                  fiscal_number = i['fiscalNumber'],
                                  cash_reg_number = i['cashRegNumber'],
                                  cash_reg_serial = i['cashRegSerial'],
                                  open_date = i['openDate'],
                                  close_date = i['closeDate'],
                                  accepted_date = i['acceptDate'],
                                  manager_id = i['managerId'],
                                  responsible_user_id = i['responsibleUserId'],
                                  session_start_cash = i['sessionStartCash'],
                                  pay_orders = i['payOrders'],
                                  sum_writeoff_orders = i['sumWriteoffOrders'],
                                  sales_cash = i['salesCash'],
                                  sales_credit = i['salesCredit'],
                                  sales_card = i['salesCard'],
                                  pay_in = i['payIn'],
                                  pay_out = i['payOut'],
                                  pay_income = i['payIncome'],
                                  cash_remain = i['cashRemain'],
                                  cash_diff = i['cashDiff'],
                                  session_status = i['sessionStatus'],
                                  conception_id = i['conceptionId'],
                                  point_of_sale_id = i['pointOfSaleId']
                                  )
        list_of_shifts.append(i['id'])
        db.add(query)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()  # Rollback the transaction
    return list_of_shifts


def add_withdraw_shifts(db:Session,lst):
    for i in lst['cashlessRecords']:
        query = models.ShiftPaymentWithd(id=i['info']['id'],
                                         shift_id =lst['sessionId'],
                                         date = i['info']['creationDate'],
                                         group = i['info']['group'],
                                         account_id = i['info']['accountId'],
                                         counteragent_id = i['info']['counteragentId'],
                                         payment_type_id = i['info']['paymentTypeId'],
                                         type = i['info']['paymentTypeId'],
                                         sum = i['info']['sum'],
                                         user_id = i['info']['auth']['user'],
                                         cause_event_id = i['info']['causeEventId'],
                                         cashier_id = i['info']['cashierId'],
                                         department_id = i['info']['departmentId'],
                                         actual_sum = i['actualSum'],
                                         original_sum = i['originalSum'],
                                         edited_payaccount_id = i["editedPayAccountId"],
                                         original_payaccount_id  = i['originalPayAccountId'],
                                         status = i['status']
                                         )
        db.add(query)
        try:
            db.commit()

        except IntegrityError as e:
            db.rollback()
    return True


def add_department_ravenue(db:Session,lst,department):
    for i in lst:
        date = i.find('date')
        date = date.text if date is not None else None
        product_id = i.find('productId')
        product_id = product_id.text if product_id is not None else None
        sum = i.find('value')
        sum = sum.text  if sum is not None else None
        query = models.DepartmentRavenue(date=date,product_id=product_id,department_id=department,sum=sum)
        db.add(query)
        try:
            db.commit()

        except IntegrityError as e:
            db.rollback()

    return True









def get_all_department(db:Session):
    query = db.query(models.Departments).all()
    return query


def get_all_payment_shifts(db:Session):
    query = db.query(models.Shift_list).all()
    return query




def update_department_renenue(db:Session,id):
    query  = db.query(models.Departments).filter(models.Departments.id==id).update({models.Departments.is_added:1})
    db.commit()
    db.refresh(query)
    return True



def update_shift_ids(db:Session,id):
    query  = db.query(models.Shift_list).filter(models.Shift_list.id==id).update({models.Shift_list.is_added:1})
    db.commit()
    db.refresh(query)
    return True