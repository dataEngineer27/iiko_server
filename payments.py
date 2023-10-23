from helpers.database import session
from helpers import crud, micro


def app():
    # department_dict = {}
    print("Authenticated")
    key = micro.login()
    shift_list = crud.get_all_shifts(db=session)
    for shift in shift_list:
        if shift.is_added == 0:
            try:
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            except:
                print("Key was expired")
                key = micro.login()
                print("Authenticated again")
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            # department_dict = crud.add_shift_payments(db=session, shift_payments=shift_payments)
            crud.add_shift_payments(db=session, shift_payments=shift_payments)
            crud.update_shift(db=session, id=shift.id)

    micro.logout(key=key)
    # return department_dict


if __name__ == '__main__':
    # dict_department = app()
    app()
