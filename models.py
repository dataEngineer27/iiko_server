from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, Boolean, BIGINT, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid
import pytz

timezonetash = pytz.timezone("Asia/Tashkent")

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'nomenclature_categories'
    id = Column(UUID(as_uuid=True), primary_key=True)
    deleted = Column(Boolean)
    name = Column(String)
    last_update = Column(DateTime(timezone=True), default=func.now())
    groups = relationship('Groups', back_populates='category')
    nomenclatures = relationship('Nomenclatures', back_populates='category')
    product_expense = relationship('ProductExpense', back_populates='category')


class Groups(Base):
    __tablename__ = 'nomenclature_groups'
    id = Column(UUID(as_uuid=True), primary_key=True)
    deleted = Column(Boolean, nullable=True)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_categories.id'), nullable=True)
    accountingCategory_id = Column(UUID(as_uuid=True), nullable=True)
    departments_visibility = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    category = relationship('Categories', back_populates='groups')
    nomenclatures = relationship('Nomenclatures', back_populates='groups')
    product_expense = relationship('ProductExpense', back_populates='groups')


# class Tools(Base):
#     __tablename__ = 'products'
#     id = Column(UUID(as_uuid=True), primary_key=True)
#     parent_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_groups.id'))
#     groups = relationship('Groups', back_populates='tools')
#     name = Column(String)
#     num = Column(String, nullable=True)
#     code = Column(String, nullable=True)
#     product_type = Column(String, nullable=True)
#     cooking_place_type = Column(String, nullable=True)
#     main_unit = Column(String, nullable=True)
#     category_id = Column(UUID(as_uuid=True), ForeignKey('user_categories.id'), nullable=True)
#     user_category = relationship('Categories', back_populates='user_tool')
#     last_update = Column(DateTime(timezone=True), default=func.now())
#     product_expense = relationship('ProductExpense', back_populates='products')


class Nomenclatures(Base):
    __tablename__ = 'nomenclatures'
    id = Column(UUID(as_uuid=True), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_groups.id'), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_categories.id'), nullable=True)
    accounting_category = Column(UUID(as_uuid=True))
    name = Column(String)
    num = Column(String, nullable=True)
    code = Column(BIGINT, nullable=True)
    main_unit = Column(UUID, nullable=True)
    price = Column(Float, nullable=True)
    place_type = Column(UUID(as_uuid=True), nullable=True)
    included_in_menu = Column(Boolean, nullable=True)
    type = Column(String, nullable=True)
    unit_weight = Column(Float, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    category = relationship('Categories', back_populates='nomenclatures')
    groups = relationship('Groups', back_populates='nomenclatures')
    department_revenue = relationship('DepartmentRevenue', back_populates='nomenclatures')
    product_expense = relationship('ProductExpense', back_populates='nomenclatures')


class Departments(Base):
    __tablename__ = 'departments'
    id = Column(UUID(as_uuid=True), primary_key=True)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    tax_payer_id = Column(String, nullable=True)
    is_added = Column(Integer, default=0)
    last_update = Column(DateTime(timezone=True), default=func.now())
    employee = relationship('Employees', back_populates='department')
    shifts = relationship('ShiftList', back_populates='department')
    payments = relationship('ShiftPayments', back_populates='department')
    department_revenue = relationship('DepartmentRevenue', back_populates='department')
    product_expense = relationship('ProductExpense', back_populates='department')


# class Stores(Base):
#     __tablename__ = 'stores'
#     id = Column(UUID(as_uuid=True), primary_key=True)
#     parent_id = Column(UUID(as_uuid=True), nullable=True)
#     code = Column(String, nullable=True)
#     name = Column(String, nullable=True)
#     type = Column(String, nullable=True)
#     is_added = Column(Integer, default=0)
#     last_update = Column(DateTime(timezone=True), default=func.now())
#     employee = relationship('Employees', back_populates='department')
#     shifts = relationship('ShiftList', back_populates='department')
#     payments = relationship('ShiftPayments', back_populates='department')
#     department_revenue = relationship('DepartmentRevenue', back_populates='department')
#     product_expense = relationship('ProductExpense', back_populates='department')


class DepartmentRevenue(Base):
    __tablename__ = 'department_revenue'
    id = Column(BIGINT, primary_key=True, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    date = Column(Date, nullable=True)
    sum = Column(DOUBLE_PRECISION, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    department = relationship('Departments', back_populates='department_revenue')
    nomenclatures = relationship('Nomenclatures', back_populates='department_revenue')


class EmployeeRoles(Base):
    __tablename__ = 'employee_roles'
    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(String, nullable=True)
    name = Column(String)
    deleted = Column(Boolean)
    last_update = Column(DateTime(timezone=True), default=func.now())
    employee = relationship('Employees', back_populates='employee_role')


class Employees(Base):
    __tablename__ = 'employees'
    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(String, nullable=True)
    name = Column(String)
    role_id = Column(UUID(as_uuid=True), ForeignKey('employee_roles.id'), nullable=True)
    roles = Column(ARRAY(UUID(as_uuid=True)))
    role_codes = Column(ARRAY(String), nullable=True)
    role_code = Column(String, nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'))
    deleted = Column(Boolean, nullable=True)
    supplier = Column(Boolean, nullable=True)
    employee = Column(Boolean, nullable=True)
    client = Column(Boolean, nullable=True)
    representStore = Column(Boolean, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    shifts = relationship('ShiftList', back_populates='employee')
    employee_role = relationship('EmployeeRoles', back_populates='employee')
    department = relationship('Departments', back_populates='employee')
    payments = relationship('ShiftPayments', back_populates='employee')


class ShiftList(Base):
    __tablename__ = 'shift_list'
    id = Column(UUID(as_uuid=True), primary_key=True)
    session_number = Column(Integer, nullable=True)
    fiscal_number = Column(Integer, nullable=True)
    cash_reg_number = Column(Integer, nullable=True)
    cash_reg_serial = Column(String, nullable=True)
    open_date = Column(DateTime)
    close_date = Column(DateTime)
    accepted_date = Column(DateTime)
    manager_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=True)
    responsible_user_id = Column(UUID(as_uuid=True), nullable=True)
    session_start_cash = Column(Float, nullable=True)
    pay_orders = Column(BIGINT, nullable=True)
    sum_write_off_orders = Column(BIGINT, nullable=True)
    sales_cash = Column(Float, nullable=True)
    sales_credit = Column(Float, nullable=True)
    sales_card = Column(Float, nullable=True)
    pay_in = Column(Float, nullable=True)
    pay_out = Column(Float, nullable=True)
    pay_income = Column(Float, nullable=True)
    cash_remain = Column(Float, nullable=True)
    cash_diff = Column(Float, nullable=True)
    session_status = Column(String, nullable=True)
    conception_id = Column(UUID(as_uuid=True), nullable=True)
    point_of_sale_id = Column(UUID(as_uuid=True), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    is_added = Column(Integer, default=0)
    department = relationship('Departments', back_populates='shifts')
    employee = relationship('Employees', back_populates='shifts')
    payments = relationship('ShiftPayments', back_populates='shifts')


class ShiftPayments(Base):
    __tablename__ = 'shift_payments'
    id = Column(UUID(as_uuid=True), primary_key=True)
    shift_id = Column(UUID(as_uuid=True), ForeignKey('shift_list.id'), nullable=True)
    date = Column(DateTime, nullable=True)
    group = Column(String, nullable=True)
    account_id = Column(UUID(as_uuid=True), nullable=True)
    counteragent_id = Column(UUID(as_uuid=True), nullable=True)
    payment_type_id = Column(UUID(as_uuid=True), nullable=True)
    type = Column(String, nullable=True)
    sum = Column(Float, nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    cause_event_id = Column(UUID(as_uuid=True), nullable=True)
    cashier_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    actual_sum = Column(Float, nullable=True)
    original_sum = Column(Float, nullable=True)
    edited_payaccount_id = Column(UUID(as_uuid=True), nullable=True)
    original_payaccount_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    shifts = relationship('ShiftList', back_populates='payments')
    employee = relationship('Employees', back_populates='payments')
    department = relationship('Departments', back_populates='payments')


class ProductExpense(Base):
    __tablename__ = 'product_expense'
    id = Column(BIGINT, autoincrement=True, primary_key=True)
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_categories.id'), nullable=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey('nomenclature_groups.id'), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    date = Column(DateTime(timezone=True))
    name = Column(String)
    quantity = Column(Float, nullable=True)
    main_unit = Column(String, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    category = relationship('Categories', back_populates='product_expense')
    groups = relationship('Groups', back_populates='product_expense')
    nomenclatures = relationship('Nomenclatures', back_populates='product_expense')
    department = relationship('Departments', back_populates='product_expense')
