from sqlalchemy import Column, Integer, String, ForeignKey, Float, DECIMAL, DateTime, Date, Boolean, BIGINT, DOUBLE_PRECISION
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
    payments = relationship('ShiftPayments', back_populates='nomenclatures')
    remains = relationship('StoreRemains', back_populates='nomenclatures')
    incomings = relationship('StoreIncomings', back_populates='nomenclatures')
    units = relationship('ReferenceUnits', back_populates='nomenclatures')


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
    store = relationship('Stores', back_populates='department')


class Stores(Base):
    __tablename__ = 'stores'
    id = Column(UUID(as_uuid=True), primary_key=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    is_added = Column(Integer, default=0)
    department = relationship('Departments', back_populates='store')
    remains = relationship('StoreRemains', back_populates='store')
    incomings = relationship('StoreIncomings', back_populates='store')


class StoreRemains(Base):
    __tablename__ = 'store_remains'
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey('stores.id'), nullable=True)
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    datetime = Column(DateTime(timezone=True))
    amount = Column(DECIMAL, nullable=True)
    sum = Column(DECIMAL, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    store = relationship('Stores', back_populates='remains')
    nomenclatures = relationship('Nomenclatures', back_populates='remains')


class StoreIncomings(Base):
    __tablename__ = 'store_incomings'
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    incoming_invoice_id = Column(UUID(as_uuid=True), nullable=True)
    doc_number = Column(String, nullable=True)
    incoming_date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    supplier_id = Column(UUID(as_uuid=True), nullable=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey('stores.id'), nullable=True)
    actual_amount = Column(DECIMAL, nullable=True)
    price = Column(DECIMAL, nullable=True)
    price_withoutVat = Column(DECIMAL, nullable=True)
    sum = Column(DECIMAL, nullable=True)
    measureunit_id = Column(UUID(as_uuid=True), ForeignKey('reference_units.id'), nullable=True)
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    amount = Column(DECIMAL, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    store = relationship('Stores', back_populates='incomings')
    nomenclatures = relationship('Nomenclatures', back_populates='incomings')
    units = relationship('ReferenceUnits', back_populates='incomings')
    sendings = relationship('StoreSendings', back_populates='incomings')


class StoreSendings(Base):
    __tablename__ = 'store_sendings'
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    outgoing_invoice_id = Column(UUID(as_uuid=True), nullable=True)
    doc_number = Column(String, nullable=True)
    incoming_date = Column(DateTime(timezone=True))
    store_id = Column(UUID(as_uuid=True), ForeignKey('stores.id'), nullable=True)
    supplier_id = Column(UUID(as_uuid=True), nullable=True)
    incominginvoice_id = Column(UUID(as_uuid=True), nullable=True)
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    price = Column(DECIMAL, nullable=True)
    price_withoutVat = Column(DECIMAL, nullable=True)
    amount = Column(DECIMAL, nullable=True)
    sum = Column(DECIMAL, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    store = relationship('Stores', back_populates='sendings')
    incomings = relationship('StoreIncomings', back_populates='sendings')
    nomenclatures = relationship('Nomenclatures', back_populates='sendings')


class ReferenceUnits(Base):
    __tablename__ = 'reference_units'
    id = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(String, nullable=True)
    deleted = Column(Boolean, nullable=True)
    code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    incomings = relationship('StoreIncomings', back_populates='units')
    nomenclatures = relationship('Nomenclatures', back_populates='units')
    payments = relationship('ShiftPayments', back_populates='units')


class DepartmentRevenue(Base):
    __tablename__ = 'department_revenue'
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
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
    pay_orders = Column(DECIMAL, nullable=True)
    sum_write_off_orders = Column(DECIMAL, nullable=True)
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
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    order_id = Column(UUID(as_uuid=True), nullable=True)
    order_num = Column(BIGINT, nullable=True)
    payment_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True))
    nomenclature_id = Column(UUID(as_uuid=True), ForeignKey('nomenclatures.id'), nullable=True)
    nomenclature_name = Column(String, nullable=True)
    shift_id = Column(UUID(as_uuid=True), ForeignKey('shift_list.id'), nullable=True)
    shift_num = Column(Integer, nullable=True)
    cashier_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=True)
    soldwithdish_id = Column(UUID(as_uuid=True), nullable=True)
    soldwithitem_id = Column(UUID(as_uuid=True), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    ordertype_id = Column(UUID(as_uuid=True), ForeignKey('reference_units.id'), nullable=True)
    ordertype = Column(String, nullable=True)
    paymenttype_id = Column(UUID(as_uuid=True), ForeignKey('reference_units.id'), nullable=True)
    paymenttype = Column(String, nullable=True)
    paymenttype_group = Column(String, nullable=True)
    measure_unit = Column(String, nullable=True)
    nomenclature_amount = Column(DECIMAL, nullable=True)
    nomenclature_sum = Column(DECIMAL, nullable=True)
    is_delivery = Column(String, nullable=True)
    guest_num = Column(Integer, nullable=True)
    guestcard_num = Column(String, nullable=True)
    guestcard_owner = Column(String, nullable=True)
    paymentcard_num = Column(String, nullable=True)
    bonuscard_num = Column(String, nullable=True)
    orderdiscount_type = Column(String, nullable=True)
    orderdiscount_type_id = Column(UUID(as_uuid=True), ForeignKey('reference_units.id'), nullable=True)
    orderincrease_type = Column(String, nullable=True)
    orderincrease_type_id = Column(UUID(as_uuid=True), ForeignKey('reference_units.id'), nullable=True)
    itemsalediscount_name = Column(String, nullable=True)
    fiscalcheque_num = Column(Integer, nullable=True)
    discountdish_num = Column(DECIMAL, nullable=True)
    discount_percent = Column(DECIMAL, nullable=True)
    discount_sum = Column(DECIMAL, nullable=True)
    increase_percent = Column(DECIMAL, nullable=True)
    increase_sum = Column(DECIMAL, nullable=True)
    full_sum = Column(DECIMAL, nullable=True)
    last_update = Column(DateTime(timezone=True), default=func.now())
    shifts = relationship('ShiftList', back_populates='payments')
    employee = relationship('Employees', back_populates='payments')
    department = relationship('Departments', back_populates='payments')
    nomenclatures = relationship('Nomenclatures', back_populates='payments')
    units = relationship('ReferenceUnits', back_populates='payments')


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
