import requests
import os 
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
PASSWORD = os.environ.get('PASSWORD')
LOGIN = os.environ.get('LOGIN')
BASE_URL = os.environ.get('BASE_URL')


def login():
    data = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN}&pass={PASSWORD}")
    key = data.text
    return key


def logout(key):
    data = requests.get(f"{BASE_URL}/resto/api/logout?key={key}")
    print(data.text)


def department_list(key):
    departments = requests.get(f"{BASE_URL}/resto/api/corporation/departments?key={key}")
    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')
    return corporate_item_dtos


def category_list(key):
    categories = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/category/list?key={key}")
    return categories.json()


def nomenclature_groups(key):
    groups = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}")
    return groups.json()


# def nomenclature_list(key):
#     tools = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?includeDeleted=true&key={key}")
#     root = ET.fromstring(tools.content)
#     product_item_dtos = root.findall('productDto')
#     return product_item_dtos

def nomenclature_list(key):
    nomenclatures = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?includeDeleted=true&key={key}")
    return nomenclatures.json()


def employee_roles(key):
    roles = requests.get(f"{BASE_URL}/resto/api/employees/roles?key={key}")
    root = ET.fromstring(roles.content)
    corporate_item_dtos = root.findall('role')
    return corporate_item_dtos


def employee_list(key):
    employees = requests.get(f"{BASE_URL}/resto/api/employees?&key={key}")
    root = ET.fromstring(employees.content)
    corporate_item_dtos = root.findall('employee')
    return corporate_item_dtos


def shift_list(key, department_id):
    employee_shift = requests.get(f"{BASE_URL}/resto/api/v2/cashshifts/list?openDateFrom=2023-01-01&openDateTo=2023-09-30&departmentId={department_id}&status=ANY&key={key}")
    return employee_shift.json()


def shift_payments(key, session_id):
    withdraw_shift = requests.get(f"{BASE_URL}/resto/api/v2/cashshifts/payments/list/{session_id}?hideAccepted=false&key={key}")
    return withdraw_shift.json()


def department_revenue(key, department):
    department_data = requests.get(f"{BASE_URL}/resto/api/reports/sales?key={key}&department={department}&dateFrom=01.01.2023&dateTo=30.09.2023&dishDetails=true&allRevenue=true")
    root = ET.fromstring(department_data.content)
    corporate_item_dtos = root.findall('dayDishValue')
    return corporate_item_dtos


def product_expenses(key, department):
    response = requests.get(f"{BASE_URL}/resto/api/reports/productExpense?key={key}&department={department}&dateFrom=01.01.2023&dateTo=01.02.2023")
    root = ET.fromstring(response.content)
    expense_data = root.findall("dayDishValue")
    return expense_data
