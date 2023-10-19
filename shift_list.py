import payments
from helpers.database import session
from helpers import crud, micro


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
