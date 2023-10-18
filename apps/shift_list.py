from apps import departments, payments
from database import session
import micro
import crud


def app():
    key = micro.authiiko()
    try:
        shifts = micro.shift_list(key=key)
    except:
        key = micro.authiiko()
        shifts = micro.shift_list(key=key)

    dict_department = payments.dict_department
    crud.add_shifts(db=session, shift_list=shifts, dict_department=dict_department)


if __name__ == '__main__':
    app()
