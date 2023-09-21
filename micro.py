
import requests
import os 
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
load_dotenv()
PASSWORD_IIKO=os.environ.get('PASSWORD_IIKO')
LOGIN_IIKO=os.environ.get('LOGIN_IIKO')
BASE_URL = os.environ.get('BASE_URL')


def authiiko():
    data  = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}")

    key = data.text
    return key



def list_departments(key):

    departments = requests.get(f"{BASE_URL}/resto/api/corporation/departments?key={key}")


    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')

    return corporate_item_dtos


def list_categories(key):
    categories = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/category/list?key={key}")
    return categories.json()


def get_nomenclature_gr(key):
    groups = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}")
    return groups.json()


def get_tools(key):
    tools = requests.get(f"{BASE_URL}/resto/api/products?key={key}")
    root = ET.fromstring(tools.content)
    product_item_dtos = root.findall('productDto')

    return product_item_dtos



def get_employee_roles(key):
    roles = requests.get(f"{BASE_URL}/resto/api/employees/roles?key={key}")
    root = ET.fromstring(roles.content)
    corporate_item_dtos = root.findall('role')
    return corporate_item_dtos




def get_employees(key):
    employees = requests.get(f"{BASE_URL}/resto/api/employees?key={key}")
    root = ET.fromstring(employees.content)
    corporate_item_dtos = root.findall('employee')
    return corporate_item_dtos



def get_employee_shifts(key):
    employee_shift = requests.get(f"{BASE_URL}/resto/api/v2/cashshifts/list?openDateFrom=2023-01-01&openDateTo=2023-09-20&status=ANY&key={key}")
    return employee_shift.json()


def get_shift_withdraw(key,session_id):
    withdraw_shift = requests.get(f"{BASE_URL}/resto/api/v2/cashshifts/payments/list/{session_id}?hideAccepted=false&key={key}")
    return withdraw_shift.json()



def get_department_ravenue(key,department):
    department_data = requests.get(f"{BASE_URL}/resto/api/reports/sales?key={key}&department={department}&dateFrom=01.01.2023&dateTo=21.09.2023&dishDetails=true&allRevenue=true")
    root = ET.fromstring(department_data.content)
    corporate_item_dtos = root.findall('dayDishValue')
    return corporate_item_dtos



