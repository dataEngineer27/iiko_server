from database import engine, session
import requests

import crud
import micro

key = micro.authiiko()

# departments = micro.list_departments(key=key)
#dict_department = crud.add_departments(db=session,lst=departments)
#
#categories = micro.list_categories(key=key)
#new_dict_cat =crud.add_categories(db=session,lst=categories)
##
#nomenclature_groups = micro.get_nomenclature_gr(key=key)
#add_nomenclature = crud.add_groups(db=session,lst=nomenclature_groups)
##
##
#get_tools = micro.get_tools(key=key)
#
#add_tools = crud.add_tools(db=session,lst=get_tools,new_dict=new_dict_cat)
##
##
#get_roles = micro.get_employee_roles(key=key)
#add_roles = crud.add_roles(db=session,lst=get_roles)
#
#
#get_employees = micro.get_employees(key=key)
#add_employees = crud.add_employees(db=session,lst=get_employees,dict_department=dict_department)
#
#
#
#get_shifts = micro.get_employee_shifts(key=key)
#add_shifts = crud.add_employee_shifts(db=session,lst=get_shifts)
#
#
#
##big childs so comment before
#

# departments = crud.get_all_department(db=session)
# for i in departments:
#    if i.is_added ==0:
#        try:
#            get_department_ravenue = micro.get_department_ravenue(key=key,department=i.id)
#            add_department_ravenue = crud.add_department_ravenue(db=session,lst=get_department_ravenue,department=i.id)
#        except:
#            key = micro.authiiko()
#            get_department_ravenue = micro.get_department_ravenue(key=key, department=i.id)
#            add_department_ravenue = crud.add_department_ravenue(db=session, lst=get_department_ravenue, department=i.id)
#        crud.update_department_renenue(db=session, id=i.id)

