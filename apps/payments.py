from database import session
import crud
import micro


def app():
    department_dict = {}
    key = micro.authiiko()
    shift_list = crud.get_all_shifts(db=session)
    for shift in shift_list:
        if shift.is_added == 0:
            try:
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            except:
                key = micro.authiiko()
                shift_payments = micro.shift_payments(key=key, session_id=shift.id)
            department_dict = crud.add_shift_payments(db=session, shift_payments=shift_payments)
            crud.update_shift(db=session, id=shift.id)

    return department_dict


if __name__ == '__main__':
    dict_department = app()
