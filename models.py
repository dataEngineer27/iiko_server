from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table,REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from datetime import datetime
import uuid
import pytz
timezonetash = pytz.timezone("Asia/Tashkent")
Base = declarative_base()

Base = declarative_base()


class Categories(Base):
    __tablename__='user_categories'
    id=Column(UUID(as_uuid=True),primary_key=True)
    deleted=Column(Boolean)
    name=Column(String)
    groups = relationship('Groups',back_populates='category')
    last_update = Column(DateTime(timezone=True),default=func.now())
    user_tool = relationship('Tools',back_populates='user_category')


class Groups(Base):
    __tablename__='nomenclature_groups'
    id = Column(UUID(as_uuid=True),primary_key=True)
    deleted = Column(Boolean,nullable=True)
    parent_id = Column(UUID(as_uuid=True),nullable=True)
    name = Column(String,nullable=True)
    num = Column(String,nullable=True)
    code = Column(String,nullable=True)
    category_id = Column(UUID(as_uuid=True),ForeignKey('user_categories.id'),nullable=True)
    category = relationship('Categories',back_populates='groups')
    accountingCategory_id = Column(UUID(as_uuid=True),nullable=True)
    tools = relationship('Tools',back_populates='groups')
    departments_visibility = Column(ARRAY(UUID(as_uuid=True)),nullable=True)
    last_update = Column(DateTime(timezone=True),default=func.now())
    


class Tools(Base):
    __tablename__='products'
    id =Column(UUID(as_uuid=True),primary_key=True)
    parent_id = Column(UUID(as_uuid=True),ForeignKey('nomenclature_groups.id'))
    groups = relationship('Groups',back_populates='tools')
    name = Column(String)
    num = Column(String,nullable=True)
    code  = Column(String,nullable=True)
    product_type = Column(String,nullable=True)
    cooking_place_type = Column(String,nullable=True)
    main_unit = Column(String,nullable=True)
    category_id = Column(UUID(as_uuid=True),ForeignKey('user_categories.id'),nullable=True)
    user_category = relationship('Categories',back_populates='user_tool')
    last_update = Column(DateTime(timezone=True),default=func.now())


class Departments(Base):
    __tablename__='departments'
    id = Column(UUID(as_uuid=True),primary_key=True)
    parent_id = Column(UUID(as_uuid=True),nullable=True)
    code = Column(String,nullable=True)
    name = Column(String,nullable=True)
    type = Column(String,nullable=True)
    tax_payer_id = Column(String,nullable=True)
    last_update = Column(DateTime(timezone=True),default=func.now())
    employee_depart = relationship('Employees',back_populates='department')
    department_shift = relationship('ShiftPaymentWithd',back_populates='shift_pay_dep')
    is_added = Column(Integer,default=0)



class DepartmentRavenue(Base):
    __tablename__= 'department_revenue'
    id = Column(Integer,primary_key=True,index=True)
    department_id = Column(UUID(as_uuid=True),nullable=True)
    product_id = Column(UUID(as_uuid=True),nullable=True)
    date = Column(String,nullable=True)
    sum = Column(REAL,nullable=True)
    last_add = Column(DateTime(timezone=True),default=func.now())

    


class EmployeeRoles(Base):
    __tablename__ = 'employee_roles'
    id = Column(UUID(as_uuid=True),primary_key=True)
    code = Column(String,nullable=True)
    name = Column(String)
    deleted = Column(Boolean)
    last_update = Column(DateTime(timezone=True),default=func.now())
    employee = relationship('Employees',back_populates='employeerole')



class Employees(Base):
    __tablename__='employees'
    id = Column(UUID(as_uuid=True),primary_key=True)
    code = Column(String,nullable=True)
    name = Column(String)
    role_id = Column(UUID(as_uuid=True),ForeignKey('employee_roles.id'),nullable=True)
    employeerole = relationship('EmployeeRoles',back_populates='employee')
    roles = Column(ARRAY(UUID(as_uuid=True)))
    role_codes = Column(String,nullable=True)
    role_code = Column(String,nullable=True)
    department_id = Column(UUID(as_uuid=True),ForeignKey('departments.id'))
    department = relationship('Departments',back_populates='employee_depart')
    deleted = Column(Boolean,nullable=True)
    supplier = Column(Boolean,nullable=True)
    employee = Column(Boolean,nullable=True)
    client = Column(Boolean,nullable=True)
    representStore = Column(Boolean,nullable=True)
    last_update = Column(DateTime(timezone=True),default=func.now())
    shift_list_employee = relationship('Shift_list',back_populates='shift_employee')







class Shift_list(Base):
    __tablename__ = 'shift_list'
    id = Column(UUID(as_uuid=True),primary_key=True)
    session_number = Column(Integer,nullable=True)
    fiscal_number = Column(Integer,nullable=True)
    cash_reg_number = Column(Integer,nullable=True)
    cash_reg_serial = Column(String,nullable=True)
    open_date = Column(DateTime)
    close_date = Column(DateTime)
    accepted_date = Column(DateTime)
    manager_id = Column(UUID(as_uuid=True),ForeignKey('employees.id'),nullable=True)
    shift_employee = relationship('Employees',back_populates='shift_list_employee')
    responsible_user_id = Column(UUID(as_uuid=True),nullable=True)
    session_start_cash = Column(REAL,nullable=True)
    pay_orders = Column(BIGINT,nullable=True)
    sum_writeoff_orders  = Column(BIGINT,nullable=True)
    sales_cash = Column(REAL,nullable=True)
    sales_credit = Column(REAL,nullable=True)
    sales_card = Column(REAL,nullable=True)
    pay_in = Column(REAL,nullable=True)
    pay_out = Column(REAL,nullable=True)
    pay_income = Column(REAL,nullable=True)
    cash_remain = Column(REAL,nullable=True)
    cash_diff = Column(REAL,nullable=True)
    session_status = Column(String,nullable=True)
    conception_id = Column(UUID(as_uuid=True),nullable=True)
    point_of_sale_id = Column(UUID(as_uuid=True),nullable=True)
    last_add = Column(DateTime(timezone=True),default=func.now())
    shiftlst = relationship('ShiftPaymentWithd',back_populates='shift_pay')
    is_added = Column(Integer,default=0)





class ShiftPaymentWithd(Base):
    __tablename__ = 'shift_payments_deposits'
    id =  Column(UUID(as_uuid=True),primary_key=True)
    shift_id =Column(UUID(as_uuid=True),ForeignKey('shift_list.id'),nullable=True)
    shift_pay = relationship('Shift_list',back_populates='shiftlst')
    date = Column(DateTime,nullable=True)
    group = Column(String,nullable=True)
    account_id = Column(UUID(as_uuid=True),nullable=True)
    counteragent_id = Column(UUID(as_uuid=True),nullable=True)
    payment_type_id = Column(UUID(as_uuid=True),nullable=True)
    type = Column(String,nullable=True)
    sum = Column(Float,nullable=True)
    user_id = Column(UUID(as_uuid=True),nullable=True)
    cause_event_id = Column(UUID(as_uuid=True),nullable=True)
    cashier_id  = Column(UUID(as_uuid=True),nullable=True)
    department_id = Column(UUID(as_uuid=True),ForeignKey('departments.id'),nullable=True)
    shift_pay_dep = relationship('Departments',back_populates='department_shift')
    actual_sum = Column(Float,nullable=True)
    original_sum = Column(Float,nullable=True)
    edited_payaccount_id = Column(UUID(as_uuid=True),nullable=True)
    original_payaccount_id = Column(UUID(as_uuid=True),nullable=True)
    status  = Column(String,nullable=True)
    last_add = Column(DateTime(timezone=True),default=func.now())




